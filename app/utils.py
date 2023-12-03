from multimedia.models import Multimedia
from .forms import MultimediaForm
from .metodos_personalizados.message import *
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import ActivityAndStudent, Aspecto

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Table, TableStyle, Image as ImageRL
from reportlab.lib.units import cm, inch
from reportlab.lib import colors

from django.contrib.staticfiles.storage import staticfiles_storage

import os
from django.conf import settings
from django.urls import reverse

import textwrap


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
    cadena_investigativa = ""
    cadena_pol_ideo = ""
    cadena_extension =""
    cadena_academica =""
    cadena_distincion_otorgada =""
    cadena_mision =""
    cadena_sanciones =""
    cadena_senalamiento =""
    
    dict_aux = {}
    list_actividades = ActivityAndStudent.objects.filter(profile_id = perfil, year = year, is_valid=True)
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
                cadena_investigativa+= f"""He participado vario(s) en evento(s) y competencia(s). Tales como, {cadena_sub} obteniendo resultados de {obj.TYPE_RESULT[int(result_evento)][1]} a nivel {
                    obj.TYPE_NIVEL[int(nivel)][1]}."""
                
            if obj.es_colateral:
                result_colateral =  result[1]
                nombre_evento_colateral = obj.nombre_evento_colateral
                cadena_investigativa += f""" Tambien, participe en eventos colateral(es) {nombre_evento_colateral} obteniendo resultado de {
                    obj.TYPE_RESULT[int(result_colateral)][1]}."""
                
        if obj.activity.id == 4:
            if obj.has_roles:
                nivel_alcanzado = obj.TYPE_NIVEL_ALCANZADO[int(obj.nivel_alcanzado)][1]
                roles = obj.roles.split(",")
                cadena_sub =""
                for id_rol in roles:
                    id_rol = int(id_rol)
                    cadena_sub += f'{obj.TYPE_ROLES[int(id_rol)][1]}, '
                cadena_sub = cadena_sub[:-2]
                cadena_investigativa+=f"""Tengo certificacion en roles de {cadena_sub} obteniendo un nivel de {nivel_alcanzado} en algunos de ellos."""
                
        if obj.activity.id == 5:
            if obj.has_investigacion:
                cadena_investigativa+=f"""Perteneciendo/pertenici a una linea de investigacion, participando en {
                    obj.TYPE_PARTICIPACION[obj.participacion][1]} en eventos {obj.TYPE_NIVEL_EVENTO[obj.nivel_evento][1]}."""
                
        if obj.activity.id == 6:
            if obj.has_publicacion:
                cadena_investigativa+=f"""Tengo publicacion logradas como {
                    obj.TYPE_AUTOR[obj.nivel_autor][1]}, tales como {obj.nombre_publicacion} teniendo un alcance de {obj.TYPE_NIVEL_PUBLICACION[obj.nivel_publicacion][1]} en dicha publicacion"""
        
        # Politico Ideologica
        if obj.activity.id == 7:
            evaluacion = obj.evaluacion.split(',')
            if obj.is_feu:
                evaluacion_feu = int((evaluacion[0])) - 1
                cadena_pol_ideo += f"""Perteneci a la Federacion Estudiantil Universitaria(FEU). Ocupando el cargo de {
                    obj.TYPE_NIVEL_CARGO_FEU[obj.cargo_feu][1]} a nivel {obj.TYPE_NIVEL[int(obj.nivel)][1]
                    } con evaluacion de {obj.TYPE_EVALUACION[evaluacion_feu][1]} durante ese periodo."""
            if obj.is_ujc:
                evaluacion_ujc = int((evaluacion[1])) - 1
                cadena_pol_ideo += f"""Perteneci a la Union de Jovenes Comunistas(UJC). Ocupando el cargo de {obj.TYPE_NIVEL_CARGO_UJC[obj.cargo_ujc][1]
                    } en el comite de base {obj.comite_base} con evaluacion de {obj.TYPE_EVALUACION[evaluacion_ujc][1]} durante ese periodo."""
        
        if obj.activity.id == 8:
            if obj.descripcion != "" or obj.descripcion.replace("[']","").replace("']","") !="":
                descripcion = obj.descripcion.split('.')
                if len(descripcion) > 1:
                    cadena_pol_ideo += "He participados en varios actos y matutinos, tales como: "
                if len(descripcion) == 1:
                    cadena_pol_ideo += "He participado en un acto o matutino, llamado: "
                cadena =""
                for descrip in descripcion:
                    cadena += f' {descrip},'
                cadena = cadena[:-1]
                cadena_pol_ideo += f'{cadena}. '
                
        if obj.activity.id == 9:
            cadena_pol_ideo += " Tengo reconocimientos "
            if obj.distincion_marzo:
                cadena_pol_ideo += ' Distinción 13 de Marzo,'
            if obj.distincion_fututo_maestro:
                cadena_pol_ideo += ' Distinción Futuro Maestro,'
            if obj.distincion_joven:
                cadena_pol_ideo += ' Distinción Joven Maestro,'
            if obj.is_ayudante:
                cadena_pol_ideo += ' Reconocimiento por ser Alumno Ayudante,'
            
            cadena_pol_ideo = cadena_pol_ideo[:-1]
            evaluacion = obj.TYPE_EVALUACION[int(obj.evaluacion)][1]
            cadena_pol_ideo += f'.Teniendo una evaluación relativa en todos estos logros de {evaluacion}. '
            
        
        #Extension
        if obj.activity.id == 19:
            cadena_extension += 'Por el aspecto de Extensión Universitaria. '
            if obj.actividades_participacion_actos_matutinos != "" or obj.actividades_participacion_actos_matutinos.replace("[']","").replace("']","") !="":
                descripcion = str(obj.actividades_participacion_actos_matutinos).split('.')
                if len(descripcion) > 1:
                    cadena_extension += "He participados en varios actos y matutinos, tales como: "
                if len(descripcion) == 1:
                    cadena_extension += "He participado en un acto o matutino, llamado: "
                cadena =""
                for descrip in descripcion:
                    cadena += f' {descrip},'
                cadena = cadena[:-1]
                cadena_extension += f'{cadena}. '
                
            if obj.if_participacion_festivales:
                cadena_extension += f"Tambien participe en el Festival de Artistas Aficinados. En la Manifestación de {obj.manifestacion_festivales} a nivel {obj.get_nivel_artista_aficionado_display()} alcanzando el premio de {obj.get_premio_artista_aficionado_display()}."
            
            if obj.nombre_actividad_facultad !="" and obj.manifestacion_actividad_facultad !="":
                cadena_extension += f" Además, participe como artista en la actividad {obj.nombre_actividad_facultad} de la facultad en la manifestacion de {obj.manifestacion_actividad_facultad}."
        
        if obj.activity.id == 20:
            evaluacion = obj.TYPE_EVALUACION[int(obj.evaluacion)][1]
            cadena_extension += f"Realice mi TSU(Trabajo Socialmente Util) en {obj.lugar_dnd_realizo} obteniendo una evaluación de {evaluacion}."
        
        if obj.activity.id == 21:
            if obj.if_jjmm:
                cadena_extension += f" Participe en los Juegos Deportivos Julio Antonio Mella en: "
                deportes = str(obj.deporte).replace("['","").replace("']","").split(",")
                cadena =""
                for deporte in deportes:
                    deporte = deporte.replace("'","")
                    cadena+=f" {obj.TYPE_DEPORTE[int(deporte)][1]},"
                cadena =cadena[:-1]
                cadena_extension += cadena
                
                cadena_extension +=". Obteniendo los resultados de: "
                
                result_deportes = str(obj.resultado_deporte).replace("['","").replace("']","").split(",")
                cadena =""
                for result in result_deportes:
                    result = result.replace("'","")
                    cadena+=f" {obj.TYPE_RESULTADO_DEPORTE[int(result)][1]},"
                cadena =cadena[:-1]
                cadena_extension += f'{cadena} respectivamente. Evento que tuvo lugar en el/la {obj.get_lugar_display()}.'
            result_deportes = str(obj.resultado_deporte).replace("['","").replace("']","").split(",")
            if obj.if_copas_mundialess:
                # result_deportes = str(obj.resultado_deporte).replace("['","").replace("']","").split(",")
                result_copas = result_deportes[0].replace("'","")
                result = obj.TYPE_RESULTADO_DEPORTE[int(result_copas)][1]
                cadena_extension += f"También, he participado en copas y mundialitos llamado {obj.nombre_evento_copas_mundiales} que se realizo en el/la {obj.get_lugar_display()}, obteniendo {result}. "
            
            if obj.if_marabana:
                result_marabana = result_deportes[1].replace("'","")
                result = obj.TYPE_RESULTADO_DEPORTE[int(result_marabana)][1]
                
                cadena_extension += f"Ese mismo año participe en el Proyecto Marabana en el evento {obj.get_nombre_evento_marabana_display()} obteniendo participación de {result}. "
        
        
        #Academico
        if obj.activity.id == 10:
            pid = obj.where_pid.replace("['","").replace("']","")
            rol = obj.rol.replace("['","").replace("']","")
            evaluacion = obj.evaluacion.split(',')
            
            cadena_academica += f"Tuve mi participación en la PID en {pid} con el rol de {rol} obteniendo evaluación de {obj.TYPE_EVALUACION[int(evaluacion[0])][1]} en esta esfera y participando en {obj.get_actividades_pid_display()} como actividades relacionadas con las mismas. "
        
        if obj.activity.id == 11: 
            evaluacion = obj.evaluacion.split(',')
            cadena =""
            for asig in obj.asignaturas_ayudante.all():
                cadena += f" {asig.name }, "
            cadena = cadena[:-1]
            cadena_academica += f"He sido Alumno Ayudante de las asignaturas de {cadena} obteniendo evalución de {obj.TYPE_EVALUACION[int(evaluacion[0])][1]}. "
            
            if obj.grupo_edu_amor:
                cadena_academica += "Pertenezco al Grupo Educando Por Amor."
            
        
        # Sanciones
        if obj.activity.id == 26:
            cadena_sanciones += f"En este año recibi una sanción o medida disciplinaria {obj.sanciones_o_medida} por motivos de {obj.motivo_sancion}. "
        
        # Señalamiento durante la carrera
        if obj.activity.id ==27:
            senalamientos = obj.senalamiento_curso.split(',')
            cadena =""
            for senal in senalamientos:
                cadena += f' {senal},'
            cadena = cadena[:-1]
            cadena_senalamiento += f"Durante mi carrera tuve los siguiente señalamientos: {cadena}. "
        
        #Distinciones Otorgadas
        if obj.activity.id == 28:
            cadena_distincion_otorgada += f"Recibi la distionción {obj.nombre_distincion} que se me fue otorgado/a por {obj.organismo_otorga_distincion} por mi buen desempeño. "
        
        #Misiones que haya participado
        if obj.activity.id == 29:
            cadena_mision += f"Participe en la misión {obj.nombre_mision} donde desempeñe la función de {obj.funsion_desempenada} dicha misión esta en proceso de {obj.get_proceso_display()}. "
        
        
        # Datos a Retornar
        dict_aux['Señalamiento durante la carrera'] = cadena_senalamiento
        dict_aux['Sanciones y Medidas Disciplinarias'] = cadena_sanciones
        dict_aux['Misiones cumplidas o en cumplimiento'] = cadena_mision
        dict_aux['Distinciones Otorgadas'] = cadena_distincion_otorgada
        dict_aux['Academico'] = cadena_academica
        dict_aux['Investigativa'] = cadena_investigativa
        dict_aux['Politico Ideologico'] = cadena_pol_ideo
        dict_aux['Extension Universitaria'] = cadena_extension
    return dict_aux

def exportar_pdf(dict_integral_pdf, perfil, response, request):
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
    pdf_canvas.line(40, 560, 560, 560)
    
    position = 540
    
    for key_father in dict_integral_pdf.keys():
        flag = False
        
        if position - 20 <= 0:
            pdf_canvas.showPage()
            position = 750

        pdf_canvas.drawString(40, position, key_father)
        position = position - 20

        for key_children, value_children in dict_integral_pdf[key_father].items():
            if not flag:
                
                pdf_canvas.drawString(40, position, key_children)
                position = position - 15
                
                # position = line_break(value_children, pdf_canvas, position)
                lines = textwrap.wrap(value_children, width=95)  # Ajusta el ancho según tus necesidades
    
                # Dibuja cada línea en el PDF
                for line in lines:
                    # pdf_canvas.drawString(40, position, line)
                    if position - 40 <= 0:
                        pdf_canvas.showPage()
                        position = 750
                    else:
                        position -= 15
                    pdf_canvas.drawString(40, position, line)
                    
                # pdf_canvas.drawString(40, position, text)
                position = position - 40
                flag = True
                print('IF la position', position)
            else:
                position = position - 55
                pdf_canvas.drawString(40, position, key_children)
                position = position - 15
                pdf_canvas.drawString(40, position, value_children)
                print('ELSE la position', position)
    
    pdf_canvas.showPage()
    pdf_canvas.save()


def line_break(character_string, pdf_canvas, pos):
    """It is in charge of making a line break in case the string is too long."""
    width_txt = pdf_canvas.stringWidth(character_string)
    print('canvas',width_txt)
    if width_txt > 330:
        split_character_string = str(character_string).split(" ")
        # print(split_character_string)
        aux_string=""
        init = 0
        end = len(split_character_string)
        flag = False
        for element in split_character_string[init:end]:
            print(init, end)
            if flag:
                aux_string = ""
            aux_string+=f"{element} "
            width_sub_text = pdf_canvas.stringWidth(aux_string)
            if width_sub_text < 550:
                continue
            else:
                pdf_canvas.drawString(40, pos, aux_string)
                flag = True
                print(aux_string)
                pos -= 15
                init = split_character_string.index(element)
        return pos
        # aux_string+="\n"
        # for element in split_character_string[position+1:]:
        #     aux_string+=f"{element} "
        # print('return', aux_string)
        # return aux_string

    else:
        pass
        # print('return', character_string)
        # return character_string
        
        
def return_dict_integrality(request, perfil):
    
    parrafo_primer_anno = generar_parrafo(perfil, 1)
    parrafo_segundo_anno = generar_parrafo(perfil, 2)
    parrafo_tercer_anno = generar_parrafo(perfil, 3)
    parrafo_cuarto_anno = generar_parrafo(perfil, 4)
    
    dict_integral = {}
    dict_integral_pdf = {}
    
    if perfil.academy_year == 4:
        
        for aspecto in Aspecto.objects.all():
            cadena_inv = ""
            aux_dict = {}
            try:
                if parrafo_cuarto_anno[f'{aspecto.name}'] != '':
                    cadena_inv += f"""<h5>Periodo de Primer Año</h5><p>{parrafo_primer_anno[f'{aspecto.name}']}</p>"""
                    aux_dict['Primer Año'] = parrafo_primer_anno[f'{aspecto.name}']
            except:
                cadena_inv += ""
                # aux_dict['Primer Año'] = {}
            
            try:
                if parrafo_cuarto_anno[f'{aspecto.name}'] != '':
                    cadena_inv += f"""<h5 class='text-mute'>Periodo de Segundo Año</h5><p>{parrafo_segundo_anno[f'{aspecto.name}']}</p>"""
                    aux_dict['Segundo Año'] = parrafo_segundo_anno[f'{aspecto.name}']
            except:
                cadena_inv += ""
                # aux_dict['Segundo Año'] = {}
                
            try:
                if parrafo_cuarto_anno[f'{aspecto.name}'] != '':
                    cadena_inv += f"""<h5>Periodo de Tercer Año</h5><p>{parrafo_tercer_anno[f'{aspecto.name}']}</p>"""
                    aux_dict['Tercer Año'] = parrafo_tercer_anno[f'{aspecto.name}']
            except:
                cadena_inv += ""
                # aux_dict['Tercer Año'] = {}
            
            try:
                if parrafo_cuarto_anno[f'{aspecto.name}'] != '':
                    cadena_inv += f"""<strong class='text-mute'>Periodo de Cuarto Año</strong><p>{parrafo_cuarto_anno[f'{aspecto.name}']}</p>"""
                    aux_dict['Cuarto Año'] = parrafo_cuarto_anno[f'{aspecto.name}']
            except:
                cadena_inv += ""
                # aux_dict['Cuarto Año'] = {}
            
            if cadena_inv != "":
                dict_integral[f'{aspecto.name}'] = cadena_inv
                dict_integral_pdf[f'{aspecto.name}'] = aux_dict
            else:
                continue
    
    return dict_integral, dict_integral_pdf, [parrafo_primer_anno, parrafo_segundo_anno, parrafo_tercer_anno, parrafo_cuarto_anno]
