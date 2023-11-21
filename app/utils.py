from multimedia.models import Multimedia
from .forms import MultimediaForm

from .models import ActivityAndStudent


def crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults):
    """Crea un objeto de tipo ActivityAndStudent y crea la imagen para este objeto"""
    is_create_image = False
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
                
    form = MultimediaForm(dict_aux, request.FILES)
    if form.is_valid():
        form.save()
        is_create_image = True
    else:
        pass
    
    return objeto, creado, is_create_image  