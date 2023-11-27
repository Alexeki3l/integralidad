from multimedia.models import Multimedia
from .forms import MultimediaForm
from .metodos_personalizados.message import *
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import ActivityAndStudent

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Table, TableStyle, Image as ImageRL
from reportlab.lib.units import cm, inch
from reportlab.lib import colors

from django.contrib.staticfiles.storage import staticfiles_storage

import os
from django.conf import settings
from django.urls import reverse


def crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults):
    """Crea un objeto de tipo ActivityAndStudent y crea la imagen para este objeto"""
    is_create_image = False
    name_file = request.FILES['file']
    print(name_file)
    formato_file = str(name_file).split('.')[-1] 
    
    if formato_file not in ['jpg', 'jpeg', 'png', 'peng']:
        messages.error(request, ERROR_EVIDENCIAS)
        return redirect('add_activities_and_student', pk = pk_activity)
    
    objeto, creado = ActivityAndStudent.objects.update_or_create(
                                activity_id = pk_activity,
                                profile_id = pk_profile,
                                year = request.user.profile.academy_year,
                                defaults=defaults
                            )
                
    #Añadir la imagen
    dict_aux = request.POST.copy()
    dict_aux['actividades'] = objeto.id
                
    for element in objeto.multimedia_set.all():
        element.delete()
    print(request.FILES)
    form = MultimediaForm(dict_aux, request.FILES)
    if form.is_valid():
        # form.save()
        for archivo in request.FILES.getlist('file'):
            Multimedia.objects.create(file=archivo, actividades= objeto)
        is_create_image = True
    else:
        pass
    
    return objeto, creado, is_create_image  


def if_cadena_empty(cadena):
    """Metodo auxiliar que devuelve True en caso que la cadena_investigativano sea vacia"""
    if len(cadena) == 0:
        return False
    
    else:
        return True
    
def generar_parrafo(perfil, year):
    cadena_investigativa= ""
    cadena_pol_ideo= ""
    dict_aux = {}
    list_actividades = ActivityAndStudent.objects.filter(profile_id = perfil, year = year)
    for obj in list_actividades:
        # Investigativa
        if obj.activity.id == 3:
            if obj.is_evento:
                nombre_evento = obj.nombre_evento[1:-1].replace("'","")
                nombre_evento_split = str(nombre_evento).split(',')
                result = obj.result.replace("'","").replace("]","").replace("[","").split(',')
                result_evento = result[0]
                nivel = obj.nivel.replace("'","").replace("]","").replace("[","").split(',')[0]
                cadena_sub =""
                for id_evento in nombre_evento_split:
                    id_evento = int(id_evento)
                    cadena_sub += f'{obj.TYPE_NOMBRE_EVENTO[int(id_evento)][1]}, '
                cadena_investigativa+= f"""He participado vario(s) en evento(s) y competencia(s). 
                Tales como, {cadena_sub} obteniendo resultados de {obj.TYPE_RESULT[int(result_evento)][1]} a nivel 
                {obj.TYPE_NIVEL[int(nivel)][1]}."""
                
            if obj.es_colateral:
                result_colateral =  result[1]
                nombre_evento_colateral = obj.nombre_evento_colateral
                cadena_investigativa +=f""" Tambien, participe en eventos colateral(es) {nombre_evento_colateral} obteniendo resultado de 
                {obj.TYPE_RESULT[int(result_colateral)][1]}."""
                
        if obj.activity.id == 4:
            if obj.has_roles:
                nivel_alcanzado = obj.TYPE_NIVEL_ALCANZADO[int(obj.nivel_alcanzado)][1]
                roles = obj.roles.split(",")
                cadena_sub =""
                for id_rol in roles:
                    id_rol = int(id_rol)
                    cadena_sub += f'{obj.TYPE_ROLES[int(id_rol)][1]}, '
                cadena_sub = cadena_sub[:-2]
                cadena_investigativa+=f"""
                    Tengo certificacion en roles de {cadena_sub} obteniendo un nivel de {nivel_alcanzado} en algunos de ellos.
                """
                
        if obj.activity.id == 5:
            if obj.has_investigacion:
                cadena_investigativa+=f"""
                    Perteneciendo/pertenici a una linea de investigacion, participando en {obj.TYPE_PARTICIPACION[obj.participacion][1]} en eventos {obj.TYPE_NIVEL_EVENTO[obj.nivel_evento][1]}.
                """
                
        if obj.activity.id == 6:
            if obj.has_publicacion:
                cadena_investigativa+=f"""
                    Tengo publicacion logradas como {obj.TYPE_AUTOR[obj.nivel_autor][1]}, tales como {obj.nombre_publicacion} teniendo un alcance de 
                    {obj.TYPE_NIVEL_PUBLICACION[obj.nivel_publicacion][1]} en dicha publicacion.
                """
        
        # Politico Ideologica
        if obj.activity.id == 7:
            evaluacion = obj.evaluacion.split(',')
            if obj.is_feu:
                evaluacion_feu = int((evaluacion[0]))
                cadena_pol_ideo += f"""
                Perteneci a la Federacion Estudiantil Universitarria(FEU). Ocupando el cargo de {obj.TYPE_NIVEL_CARGO_FEU[obj.cargo_feu][1]} a nivel 
                {obj.TYPE_NIVEL[int(obj.nivel)][1]} con evaluacion de {obj.TYPE_EVALUACION[evaluacion_feu][1]} durante ese periodo.
                """
            if obj.is_ujc:
                evaluacion_ujc = int((evaluacion[1]))
                cadena_pol_ideo += f"""
                Perteneci a la Union de Jovenes Comunistas(UJC). Ocupando el cargo de {obj.TYPE_NIVEL_CARGO_UJC[obj.cargo_ujc][1]} en el comite de base 
                {obj.comite_base} con evaluacion de {obj.TYPE_EVALUACION[evaluacion_feu][1]} durante ese periodo.
                """
        dict_aux['Investigativa'] = cadena_investigativa
        dict_aux['Politico Ideologico'] = cadena_pol_ideo
    return dict_aux

def exportar_pdf(dict_integral, perfil, response, request):
    pdf_canvas = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    ruta_actual = os.getcwd()
    # Esta es la ruta del logo de la uci
    nombre_archivo = f'{ruta_actual}/app/static/app/assets_2/images/tesis/logo_uci.png'
    
    x_inicio = 250
    y_inicio = 730
    altura = 90
    pdf_canvas.line(x_inicio, y_inicio, x_inicio, y_inicio + altura)

    pdf_canvas.drawImage(nombre_archivo, 120, 730, width=100, height=80, mask='auto')
    
    name_proyecto_1 = "SISTEMA DE GESTION" 
    name_proyecto_2 = "DEL PROCESO DE INTEGRALIDAD"
    
    pdf_canvas.drawString(270, 800, name_proyecto_1)
    pdf_canvas.drawString(270, 780, name_proyecto_2)
    
    # ------------DATOS INTRODUCTORIOS------------------
    
    data = [['Carrera', 'Curso', 'Facultad',
             'Grupo', 'Año Academico']]
    
    if perfil.academy_year == 4:
        year = "Cuarto Año"
    elif perfil.academy_year == 3:
        year = "Tercer Año"
    elif perfil.academy_year == 2:
        year = "Segundo Año"
    elif perfil.academy_year == 1:
        year = "Primer Año"
    
    list_split_carrera = str(perfil.carrera).split(' ')
    carrera = ' '.join(list_split_carrera[:-1])
    carrera += f'\n{list_split_carrera[-1]}'
    data.append([carrera, '2022-2023', 'Facultad 2', perfil.grupo, year])
    
    t = Table(data, colWidths=[1.63*inch, 0.93 *
            inch, 0.915*inch, 0.91*inch, 1.10*inch])
    
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -6), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -6), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    
    t.wrapOn(pdf_canvas, width, height)
    table1_height = t._height
    table1_width = t._width
    table1_pos = (40, 650)
    t.drawOn(pdf_canvas, *table1_pos)
    
    ruta_image_user = ruta_actual + perfil.image.url
    pdf_canvas.drawImage(ruta_image_user, table1_width + 50, 600, width=100, height=100, mask='auto')
    
    pdf_canvas.drawString(40, table1_pos[1] - 20, 'DATOS PERSONALES')
    
    data = [['Nombre y Apellido', 'C.I.', 'Provincia',
             'Municipio', 'Militante']]
    
    data.append([f'{perfil.user.first_name} {perfil.user.last_name}' , f'{perfil.ci}', \
        f'{perfil.provincia}', f'{perfil.municipio}', 'No'])
    
    t = Table(data, colWidths=[1.63*inch, 0.93 *
            inch, 1.315*inch, 1.01*inch, 0.70*inch])
    
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -6), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -6), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    
    t.wrapOn(pdf_canvas, width, height)
    table1_height = t._height
    table1_width = t._width
    table1_pos = (40, table1_pos[1] - 60)
    t.drawOn(pdf_canvas, *table1_pos)
    
    pdf_canvas.drawString(40, 570, 'SINTESIS DE LA TRAYECTORIA ESTUDIANTIL')
    pdf_canvas.line(40, 550, 560, 550)
    
    pdf_canvas.showPage()
    pdf_canvas.save()



