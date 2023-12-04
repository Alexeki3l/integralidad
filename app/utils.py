from multimedia.models import Multimedia
from .forms import MultimediaForm
from .metodos_personalizados.message import *
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import ActivityAndStudent, Aspecto, Integralidad

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Table, TableStyle, Image as ImageRL
from reportlab.lib.units import cm, inch
from reportlab.lib import colors

from django.db.models import Q

from django.contrib.staticfiles.storage import staticfiles_storage

import os
from django.conf import settings
from django.urls import reverse

import textwrap


def crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults):
    """Crea un objeto de tipo ActivityAndStudent y crea la imagen para este objeto"""
    is_create_image = False
    try:
        name_file = request.FILES['file']
        formato_file = str(name_file).split('.')[-1] 
    except:
        pass
    try:
        if formato_file not in ['jpg', 'jpeg', 'png', 'peng']:
            messages.error(request, ERROR_EVIDENCIAS)
            return redirect('add_activities_and_student', pk = pk_activity)
    except UnboundLocalError:
        pass
    except Exception as e:
        print(e)
    
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
    
    try:
        form = MultimediaForm(dict_aux, request.FILES)
        if form.is_valid():
            # form.save()
            for archivo in request.FILES.getlist('file'):
                Multimedia.objects.create(file=archivo, actividades= objeto)
            is_create_image = True
        else:
            pass
    except:
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
        if obj.activity.aspecto.name == 'Investigativa':
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
            
            dict_aux['Investigativa'] = cadena_investigativa
        
        # Politico Ideologica
        if obj.activity.aspecto.name == 'Politico Ideologico':
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
                
            dict_aux['Politico Ideologico'] = cadena_pol_ideo
            
        #Extension
        if obj.activity.aspecto.name == 'Extension Universitaria':
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
            
            dict_aux['Extension Universitaria'] = cadena_extension
            
        #Academico
        if obj.activity.aspecto.name == 'Academico':
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
                
            if obj.activity.id == 12:
                cadena =''
                for asig in obj.asignaturas_ayudante.all():
                    cadena += f' {asig.name},'
                cadena = cadena[:-1]
                cadena_academica += f"He tenido arrastre en las siguientes asignaturas: {cadena}. "
                
            dict_aux['Academico'] = cadena_academica
            
        # Sanciones
        if obj.activity.aspecto.name == 'Sanciones y Medidas Disciplinarias':
            if obj.activity.id == 26:
                cadena_sanciones += f"En este año recibi una sanción o medida disciplinaria {obj.sanciones_o_medida} por motivos de {obj.motivo_sancion}. "
        
            dict_aux['Sanciones y Medidas Disciplinarias'] = cadena_sanciones
            
        # Señalamiento durante la carrera
        if obj.activity.aspecto.name == 'Señalamiento durante la carrera':
            if obj.activity.id ==27:
                senalamientos = obj.senalamiento_curso.split(',')
            cadena =""
            for senal in senalamientos:
                cadena += f' {senal},'
            cadena = cadena[:-1]
            cadena_senalamiento += f"Durante mi carrera tuve los siguiente señalamientos: {cadena}. "
        
            dict_aux['Señalamiento durante la carrera'] = cadena_senalamiento
        
        #Distinciones Otorgadas
        if obj.activity.aspecto.name == 'Distinciones Otorgadas':
            if obj.activity.id == 28:
                cadena_distincion_otorgada += f"Recibi la distionción {obj.nombre_distincion} que se me fue otorgado/a por {obj.organismo_otorga_distincion} por mi buen desempeño. "
                dict_aux['Distinciones Otorgadas'] = cadena_distincion_otorgada
                
        #Misiones que haya participado
        if obj.activity.aspecto.name == 'Misiones cumplidas o en cumplimiento':
            if obj.activity.id == 29:
                cadena_mision += f"Participe en la misión {obj.nombre_mision} donde desempeñe la función de {obj.funsion_desempenada} dicha misión esta en proceso de {obj.get_proceso_display()}. "
                dict_aux['Misiones cumplidas o en cumplimiento'] = cadena_mision
        
    
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
    
    try:
        ruta_image_user = ruta_actual + perfil.image.url
        pdf_canvas.drawImage(ruta_image_user, table1_width + 50, 630, width=100, height=100, mask='auto')
    except:
        pass
    
    pdf_canvas.drawString(40, table1_pos[1] - 20, 'DATOS PERSONALES')
    
    data = [['Nombre y Apellido', 'C.I.', 'Provincia',
             'Municipio', 'Militante', 'Indice']]
    try:
        integralidad_valor_total = perfil.user.integralidad.valor_final
    except:
        integralidad_valor_total = 0.00
    
    data.append([f'{perfil.user.first_name} {perfil.user.last_name}' , f'{perfil.ci}', \
        f'{perfil.provincia}', f'{perfil.municipio}', 'No', f'{integralidad_valor_total}'])
    
    t = Table(data, colWidths=[1.63*inch, 0.93 *
            inch, 1.315*inch, 1.01*inch, 0.70*inch , 0.70*inch, 0.40*inch])
    
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
                
            else:
                position = position - 55
                pdf_canvas.drawString(40, position, key_children)
                position = position - 15
                pdf_canvas.drawString(40, position, value_children)
    
    pdf_canvas.showPage()
    pdf_canvas.save()


def line_break(character_string, pdf_canvas, pos):
    """It is in charge of making a line break in case the string is too long."""
    width_txt = pdf_canvas.stringWidth(character_string)
    if width_txt > 330:
        split_character_string = str(character_string).split(" ")
        aux_string=""
        init = 0
        end = len(split_character_string)
        flag = False
        for element in split_character_string[init:end]:
            if flag:
                aux_string = ""
            aux_string+=f"{element} "
            width_sub_text = pdf_canvas.stringWidth(aux_string)
            if width_sub_text < 550:
                continue
            else:
                pdf_canvas.drawString(40, pos, aux_string)
                flag = True
                pos -= 15
                init = split_character_string.index(element)
        return pos
        # aux_string+="\n"
        # for element in split_character_string[position+1:]:
        #     aux_string+=f"{element} "
        # return aux_string

    else:
        pass
        
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
                if parrafo_primer_anno[f'{aspecto.name}'] != '':
                    cadena_inv += f"""<h5>Periodo de Primer Año</h5><p>{parrafo_primer_anno[f'{aspecto.name}']}</p>"""
                    aux_dict['Primer Año'] = parrafo_primer_anno[f'{aspecto.name}']
            except:
                cadena_inv += ""
                # aux_dict['Primer Año'] = {}
            
            try:
                if parrafo_segundo_anno[f'{aspecto.name}'] != '':
                    cadena_inv += f"""<h5 class='text-mute'>Periodo de Segundo Año</h5><p>{parrafo_segundo_anno[f'{aspecto.name}']}</p>"""
                    aux_dict['Segundo Año'] = parrafo_segundo_anno[f'{aspecto.name}']
            except:
                cadena_inv += ""
                # aux_dict['Segundo Año'] = {}
                
            try:
                if parrafo_tercer_anno[f'{aspecto.name}']:
                    cadena_inv += f"""<h5>Periodo de Tercer Año</h5><p>{parrafo_tercer_anno[f'{aspecto.name}']}</p>"""
                    aux_dict['Tercer Año'] = parrafo_tercer_anno[f'{aspecto.name}']
            except:
                cadena_inv += ""
                # aux_dict['Tercer Año'] = {}
            
            try:
                if parrafo_cuarto_anno[f'{aspecto.name}']:
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


def puntuaje_integralidad(perfil):
    """Este metodo se encarga de insertar y calcular las pautas de evaluacion de integralidad"""
    
    act_and_student_filter = ActivityAndStudent.objects.filter(profile = perfil)
    
    cont = 0
    cont_1 = 0
    try:
        integralidad_obj = Integralidad(
            user = perfil.user
        )
        integralidad_obj.save()
    except:
        integralidad_obj = Integralidad.objects.get(user = perfil.user)
        
    # Investigativa
    for act_and_student_obj in act_and_student_filter.filter(activity__aspecto__name = 'Investigativa'):
        # Puntuacion de 5.
        condicion_1 = act_and_student_obj.is_evento and act_and_student_obj.year in [1,2,3]
        condicion_2 = act_and_student_obj.is_evento or act_and_student_obj.es_colateral \
            or act_and_student_obj.has_roles or act_and_student_obj.has_investigacion or act_and_student_obj.has_publicacion
        
        condicion_3 = act_and_student_obj.is_evento and act_and_student_obj.nivel == '1'
        if condicion_3:
            cont += 1
        
        condicion_4 = act_and_student_obj.is_evento and act_and_student_obj.nivel == '2'
        if condicion_4:
            cont_1 += 1
        
        condicion_5 = act_and_student_obj.has_publicacion
        
        
        if condicion_1 and condicion_2 and cont==3 and cont_1==2 and condicion_5:
            integralidad_obj.is_investigation = '5'
            integralidad_obj.save()
            
        # ---------------------
        # Puntuacion de 4.
        condicion_1 = act_and_student_obj.is_evento
        condicion_2 = act_and_student_obj.is_evento and act_and_student_obj.nivel == '1'
        condicion_3 = act_and_student_obj.is_evento and act_and_student_obj.nivel == '2'
        cont = 0
        if condicion_1 and condicion_2:
            cont += 1
            if cont > 1 and condicion_3:
                integralidad_obj.is_investigation = '4'
                integralidad_obj.save()
                
        # Puntuacion de 3.
        condicion_1 = act_and_student_obj.is_evento
        condicion_2 = act_and_student_obj.es_colateral
        condicion_3 = act_and_student_obj.is_evento and act_and_student_obj.nivel == '1'
        cont = 0
        if condicion_1 or condicion_2:
            cont += 1
            if cont >= 3 and condicion_3:
                integralidad_obj.is_investigation = '3'
                integralidad_obj.save()
                
        # Puntuacion de 2.
        condicion_1 = act_and_student_obj.is_evento
        cont = 0
        if condicion_1:
            cont += 1
            if cont>1:
                integralidad_obj.is_investigation = '2'
                integralidad_obj.save()
                
        # Puntuacion de 1.
        condicion_1 = act_and_student_obj.es_colateral
        cont=0
        if condicion_1:
            cont += 1
            if cont > 1:
                integralidad_obj.is_investigation = '1'
                integralidad_obj.save()
                
        else:
            integralidad_obj.is_investigation = '0'
            integralidad_obj.save()
            
        condicion_1 = act_and_student_obj.has_roles
        count = 0
        cont = 0
        if act_and_student_obj.roles:
            roles = str(act_and_student_obj.roles).replace("['","").replace("']","").split(',')
            count = len(roles)
            
        condicion_2 = act_and_student_obj.has_roles and count >= 3
        
            
        integralidad_obj.save()
            
        
    # Extension Universitaria
    cont = 0
    cont_1 = 0
    for act_and_student_obj in act_and_student_filter.filter(activity__aspecto__name = 'Extension Universitaria'):   
        # Cultura
        # ----------------------------------------------
        condicion_1 = act_and_student_obj.if_participacion_festivales and act_and_student_obj.nivel_artista_aficionado == 1 and act_and_student_obj.premio_artista_aficionado in [1,2,3,4]
        condicion_2 = act_and_student_obj.if_participacion_festivales and act_and_student_obj.nivel_artista_aficionado == 1 or act_and_student_obj.nivel_artista_aficionado == 2 and act_and_student_obj.premio_artista_aficionado in [1,2,3]
        if condicion_1:
            cont += 1
        if condicion_2:
            cont_1 += 1
        # Puntuacion de 5
        if cont == 3 and cont_1 == 1:
            integralidad_obj.cultura = '5'
            
        condicion_1 = act_and_student_obj.if_participacion_festivales
        condicion_2 = act_and_student_obj.if_participacion_festivales and act_and_student_obj.nivel_artista_aficionado == 2 and act_and_student_obj.premio_artista_aficionado in [1,2,3,4]
        cont = 0
        cont_1 =0
        if condicion_1:
            cont +=1
        if condicion_2:
            cont_1 +=1
        # Puntuacion de 4
        condicion_3 = act_and_student_obj.premio_artista_aficionado in [1,2,3,4] and cont >=2
        condicion_4 = act_and_student_obj.actividades_participacion_actos_matutinos != "" and act_and_student_obj.nombre_actividad_facultad != ""
        if cont >2 and cont_1>=1 or condicion_3 or condicion_4:
            integralidad_obj.cultura = '4'
            
        # Puntuacion de 3
        condicion_5 = act_and_student_obj.premio_artista_aficionado in [1,2,3,4]
        if condicion_5:
            if cont >1:
                integralidad_obj.cultura = '3'
                
        if condicion_1 or condicion_4:
            integralidad_obj.cultura = '2'
            
        if condicion_4:
            integralidad_obj.cultura = '1'
        else:
            integralidad_obj.cultura = '0'
        
        integralidad_obj.save()
        
        
        # ------------------------------
        # Deporte
        # ------------------------------
        cont = 0
        condicion_1 = act_and_student_obj.if_jjmm
        if not act_and_student_obj.resultado_deporte is None:
            condicion_2 = len(list(element for element in act_and_student_obj.resultado_deporte.split(',') if '1' in element or '2' in element or '3' in element))>=2
        condicion_3 = act_and_student_obj.if_marabana
        condicion_4 = act_and_student_obj.lugar == 2
        condicion_5 = act_and_student_obj.lugar == 3
        
        if condicion_1:
            cont += 1
            
        if cont >=3 and condicion_2 or cont >=3 and condicion_3 or cont >=3 and condicion_4 or cont >=3 and condicion_5 or \
            condicion_2 and condicion_3 or condicion_2 and condicion_4 or condicion_2 and condicion_5 or \
                condicion_3 and condicion_4 or condicion_3 and condicion_5 or condicion_4 and condicion_5:
                    integralidad_obj.deporte = '5'
        cont_1 =0
        cont_2 =0
        condicion_6 = act_and_student_obj.if_copas_mundialess
        if condicion_6:
            cont_1 += 1
            
        if condicion_3:
            cont_2 += 1
        
        elif cont >=2 and cont_1 >=2 or cont >=2 and cont_2 >=2 or cont_1 >=2 and cont_2 >=2:
            integralidad_obj.deporte = '4'
            
        elif cont >=2 and condicion_3 and condicion_6:
            integralidad_obj.deporte = '3'
            
        elif condicion_1:
            integralidad_obj.deporte = '2'
        else:
            integralidad_obj.deporte = '0'
        
        # ------------------------------
        # Residencia
        # ------------------------------
        if act_and_student_obj.activity.id == 22:
            if not act_and_student_obj.if_senalamiento_residencia:
                aux = [True if evaluacion == 'Excelente' or evaluacion == 'Bien' else False for mes, evaluacion in act_and_student_obj.cuartelerias.items()]
                condicion_2 = act_and_student_obj.responsabilidad
                
                if all(aux) and condicion_2:
                    integralidad_obj.residencia = '5'
                    
                elif all(aux):
                    integralidad_obj.residencia = '4'
                
            elif all([True if evaluacion == 'Excelente' or evaluacion == 'Bien' or evaluacion == 'Regular' else False for mes, evaluacion in act_and_student_obj.cuartelerias.items()]):
                integralidad_obj.residencia = '3'
                
            elif all([True if evaluacion == 'Bien' or evaluacion == 'Regular' else False for mes, evaluacion in act_and_student_obj.cuartelerias.items()]):
                integralidad_obj.residencia = '2'
            
            elif all([True if evaluacion == 'Mal' or evaluacion == 'Regular' else False for mes, evaluacion in act_and_student_obj.cuartelerias.items()]):
                integralidad_obj.residencia = '1'
                
            else:
                integralidad_obj.residencia = '0'
                
            integralidad_obj.save()
        # ------------------------------
        # TSU
        # ------------------------------
        if act_and_student_obj.activity.id == 20:
            cont = 0
            cont_1 = 0
            cont_2 = 0
            if act_and_student_obj.evaluacion == 1: #Bien
                cont += 1
            if act_and_student_obj.evaluacion == 2: #Regular
                cont_1 += 1
            if act_and_student_obj.evaluacion == 3: #Mal
                cont_2 += 1
                
            if cont_2 == 0 and (cont_1 == 0 or cont_1 == 1) and cont_1 > 0 :
                integralidad_obj.tsu = '4'
                
            if cont_2 == 0 and (cont_1 == 0 or cont_1 == 0) and cont_1 > 0 :
                integralidad_obj.tsu = '5'
                
            if (cont_2 < 2 or (cont_1 <3)) and cont_1 > 0 :
                integralidad_obj.tsu = '3'
                
            if (cont_2 >= 2 or (cont_1 <3)) and cont_1 > 0 :
                integralidad_obj.tsu = '2'
                
            if (cont_2 >= 2 or (cont_1 >= 3)) and cont_1 > 0 :
                integralidad_obj.tsu = '1'
                
            else:
                integralidad_obj.tsu = '0'
                
        # ------------------------------
        # GUARDIA
        # ------------------------------
        if act_and_student_obj.activity.id == 23:
            condicion_1 = act_and_student_filter.filter(total_ausencias_justificadas__gte = 2).count()
            condicion_2 = act_and_student_filter.filter(total_ausencias_injustificadas__gte = 0).count()
            
            if condicion_1 <= 1 and condicion_2 == 0:
                integralidad_obj.guardia = '5'
                
            elif condicion_1 <=3 and condicion_2 == 0:
                integralidad_obj.guardia = '4'
                
            elif condicion_1 <=4 and condicion_2 <= 1:
                integralidad_obj.guardia = '3'
                
            elif condicion_1 <=5 and condicion_2 <= 2:
                integralidad_obj.guardia = '2'
                
            elif condicion_1 <=6 and condicion_2 <= 2:
                integralidad_obj.guardia = '1'
                
            else:
                integralidad_obj.guardia = '0'
        
        
    # Politico Ideologico
    for act_and_student_obj in act_and_student_filter.filter(activity__aspecto__name = 'Politico Ideologico'):
        
        # ------------------------------
        # FEU-UJC
        # ------------------------------
        condicion_1 = (act_and_student_obj.cargo_feu in [1,2] or act_and_student_obj.cargo_ujc in [1,2]) and act_and_student_obj.nivel == 1 and '3' not in act_and_student_obj.evaluacion
        condicion_2 = act_and_student_obj.distincion_marzo or act_and_student_obj.cargo_ujc
        condicion_3 = act_and_student_filter.filter(distincion_joven = True).count()
        condicion_4 = act_and_student_filter.filter(is_ayudante = True, evaluacion__icontains='1').count()
            
        condicion_5 = act_and_student_filter.filter(Q(is_ujc = True) | Q(is_feu=True) & Q(evaluacion__icontains='1') | Q(evaluacion__icontains='2')).count()    
        condicion_6 = act_and_student_filter.filter(distincion_marzo = True).count()
        
        if condicion_1 and condicion_2 and condicion_3 >=2 or condicion_1 and condicion_2 and condicion_4 >=3 \
            or condicion_4 and condicion_2 and condicion_3 or condicion_3 >=2:
                integralidad_obj.feu_ujc = '5'
                
        elif condicion_5 >= 2 and condicion_6 or condicion_5 >= 2 and condicion_3 >=2 or \
            condicion_4 >=2 and condicion_5 >= 2:
                integralidad_obj.feu_ujc = '4'
                
        elif condicion_5 >=3:
            integralidad_obj.feu_ujc = '3'
            
        elif act_and_student_filter.filter(Q(is_ujc = True) | Q(is_feu=True)).count() > 0 and condicion_4 == act_and_student_filter.filter(is_ayudante = True, evaluacion__icontains='1').count() >=1:
            integralidad_obj.feu_ujc = '2'
            
        elif act_and_student_filter.exclude(descripcion='').count() > 0:
            integralidad_obj.feu_ujc = '1'
            
        else:
            integralidad_obj.feu_ujc = '0'
    

    # Produccion
    for act_and_student_obj in act_and_student_filter.filter(Q(activity__aspecto__name = 'Academico') | Q(activity__aspecto__name = 'Investigativa')):
        act_and_student_filter_2 = act_and_student_filter.filter(Q(activity__aspecto__name = 'Academico') | Q(activity__aspecto__name = 'Investigativa'))
        if act_and_student_filter_2.filter(has_investigacion = True).count() > 0:
                integralidad_obj.in_production = '5'
            
        elif act_and_student_filter_2.filter(has_investigacion = True).count() > 0 and \
            act_and_student_filter_2.filter(has_roles = True).count() >0:
                integralidad_obj.in_production = '4'
                
        elif act_and_student_filter_2.filter(evaluacion_icontains = '1').count() >= 4:
            integralidad_obj.in_production = '3'
            
        elif act_and_student_filter_2.filter(Q(evaluacion_icontains = '1') & Q(evaluacion_icontains = '2')).count() >= 4:
            integralidad_obj.in_production = '2'
            
        elif act_and_student_filter_2.filter(Q(evaluacion_icontains = '3')).count() >0:
            integralidad_obj.in_production = '1'
            
        else:
            integralidad_obj.in_production = '0'
            
        integralidad_obj.save()
    
    return integralidad_obj