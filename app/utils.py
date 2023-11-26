from multimedia.models import Multimedia
from .forms import MultimediaForm
from .metodos_personalizados.message import *
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import ActivityAndStudent


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
    """Metodo auxiliar que devuelve True en caso que la cadena no sea vacia"""
    if len(cadena) == 0:
        return False
    
    else:
        return True
    
def generar_parrafo(list_actividades):
    cadena_investigativa = ""
    for obj in list_actividades:
        cadena = ""
        if obj.activity.id == 3:
            if obj.is_evento:
                obj.TYPE_NOMBRE_EVENTO
                # nombre_evento = get_nombre_evento_display()
                cadena += f'He participado vario(s) en evento(s) y competencia(s). Tales como, {nombre_evento} a nivel de {nivel_evento}'
                