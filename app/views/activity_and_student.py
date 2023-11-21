from typing import Any
from django.shortcuts import render, redirect
from ..models import Activity, Aspecto, ActivityAndStudent, Asignatura
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..forms import AddActivityView, EditActivityView, AddProfileView, EditProfileView, EditActivityAndStudentView,\
AddActivityAndStudentView, MultimediaForm

from django.urls import reverse, reverse_lazy

from app.utils import crear_objeto_activity_and_student

from django.contrib import messages

from authentication.models import Profile
from multimedia.models import Multimedia

from app.metodos_personalizados.message import *

import math

# ----------------------CRUD de ActividadAndStudent ----------------------------
class AddActivityAndStudentView(LoginRequiredMixin, CreateView):
    model = ActivityAndStudent
    form_class = AddActivityAndStudentView
    template_name = 'activity_and_student/add_activity_and_student.html'
    
    def dispatch(self, request, *args, **kwargs):
        
        if request.method == 'POST':
            pk_activity = int(self.request.path.split('/')[-1])
            pk_profile = int(self.request.user.profile.id)
            print('POST',request.POST)
            # Eliminamos el token de seguridad y creamos una copia del diccionario que se envia en el request.
            defaults = dict(request.POST).copy()
            del defaults['csrfmiddlewaretoken']
            
            # # # # # # ACADEMICO # # # # # #
            
            # Area donde ha realizado la PID
            if 10 == pk_activity:
                print(type(defaults['where_pid']))
                defaults['evaluacion'] = int(defaults['evaluacion'][0])
                defaults['actividades_pid'] = int(defaults['actividades_pid'][0])
                
                year_student = int(self.request.user.profile.academy_year)
                defaults['year'] = year_student
                
                try:
                    if defaults['where_pid'][0] and defaults['rol'][0] and defaults['evaluacion'] and defaults['actividades_pid']:
                        objeto, creado = ActivityAndStudent.objects.update_or_create(
                                activity_id = pk_activity,
                                profile_id = pk_profile,
                                defaults=defaults
                            )
                        if creado:
                            pass
                        print(objeto, objeto.id)
                        dict_aux = request.POST.copy()
                        dict_aux['actividades'] = objeto.id
                            
                        for element in objeto.multimedia_set.all():
                            element.delete()
                        try:
                            form = MultimediaForm(dict_aux, request.FILES)
                            if form.is_valid():
                                form.save()
                            
                            return redirect('list_activities')
                        except Exception as e:
                            print(e)
                            
                except Exception as e:
                    print(e)
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
            
            # Alumno Ayudante
            elif 11 == pk_activity:
                year_student = int(self.request.user.profile.academy_year)
                
                defaults['year'] = year_student
                try:
                    defaults['evaluacion'] = int(defaults['evaluacion'][0])
                except:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                    
                
                try:
                    if 'on' in defaults['is_ayudante']:
                        defaults['is_ayudante'] = True
                    else:
                        defaults['is_ayudante'] = False
                except:
                    pass
                
                try:
                    if 'on' in defaults['grupo_edu_amor']:
                        defaults['grupo_edu_amor'] = True
                    else:
                        defaults['grupo_edu_amor'] = False
                except:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                try:
                    ids_asignaturas = defaults['asignaturas_ayudante']
                except:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                #Si detectamos mas de 2 asignaturas enviamos un mensaje de error al template
                try:
                    pos_2 = ids_asignaturas[2]
                    if pos_2:
                        messages.error(request, ERROR_GENERAL)
                        return redirect('add_activities_and_student', pk = pk_activity)
                except IndexError:
                    pass
                
                try:
                    defaults['is_ayudante']
                except:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                del defaults['asignaturas_ayudante']
                
                objeto, creado = ActivityAndStudent.objects.update_or_create(
                                activity_id = pk_activity,
                                profile_id = pk_profile,
                                defaults=defaults
                            )
                if creado:
                    
                    objeto.asignaturas_ayudante.clear()
                    
                    for id_asignatura in ids_asignaturas:
                        asignatura = Asignatura.objects.get(id=id_asignatura)
                        objeto.asignaturas_ayudante.add(asignatura)
                        
                dict_aux = request.POST.copy()
                dict_aux['actividades'] = objeto.id
                
                for element in objeto.multimedia_set.all():
                    element.delete()
                
                form = MultimediaForm(dict_aux, request.FILES)
                if form.is_valid():
                    form.save()
                else:
                    print('error')

                return redirect('list_activities')
            
            #Arrastres
            elif 12 == pk_activity:
                try:
                    if 'on' in defaults['with_arrastres']:
                        defaults['with_arrastres'] = True
                    else:
                        defaults['with_arrastres'] = False
                except:
                    pass
                
                try:
                    ids_asignaturas = defaults['asignaturas_ayudante']
                except:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                #Si detectamos mas de 2 asignaturas enviamos un mensaje de error al template
                try:
                    pos_2 = ids_asignaturas[2]
                    if pos_2:
                        messages.error(request, ERROR_GENERAL)
                        return redirect('add_activities_and_student', pk = pk_activity)
                except IndexError:
                    pass
                
                del defaults['asignaturas_ayudante']
                
                objeto, creado = ActivityAndStudent.objects.update_or_create(
                                activity_id = pk_activity,
                                profile_id = pk_profile,
                                defaults=defaults
                            )
                objeto.asignaturas_ayudante.clear()
                    
                for id_asignatura in ids_asignaturas:
                    asignatura = Asignatura.objects.get(id=id_asignatura)
                    objeto.asignaturas_ayudante.add(asignatura)
                
                #Añadir la imagen
                dict_aux = request.POST.copy()
                dict_aux['actividades'] = objeto.id
                
                for element in objeto.multimedia_set.all():
                    element.delete()
                
                form = MultimediaForm(dict_aux, request.FILES)
                if form.is_valid():
                    form.save()
                else:
                    print('error')

                return redirect('list_activities')
                
            # Mundiales
            elif 13 == pk_activity:
                try:
                    if 'on' in defaults['with_mundiales']:
                        defaults['with_mundiales'] = True
                    else:
                        defaults['with_mundiales'] = False
                except:
                    pass
                
                try:
                    ids_asignaturas = defaults['asignaturas_ayudante']
                except:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                #Si detectamos mas de 2 asignaturas enviamos un mensaje de error al template
                try:
                    pos_2 = ids_asignaturas[2]
                    if pos_2:
                        messages.error(request, ERROR_GENERAL)
                        return redirect('add_activities_and_student', pk = pk_activity)
                except IndexError:
                    pass
                
                del defaults['asignaturas_ayudante']
                
                objeto, creado = ActivityAndStudent.objects.update_or_create(
                                activity_id = pk_activity,
                                profile_id = pk_profile,
                                defaults=defaults
                            )
                objeto.asignaturas_ayudante.clear()
                    
                for id_asignatura in ids_asignaturas:
                    asignatura = Asignatura.objects.get(id=id_asignatura)
                    objeto.asignaturas_ayudante.add(asignatura)
                
                #Añadir la imagen
                dict_aux = request.POST.copy()
                dict_aux['actividades'] = objeto.id
                
                for element in objeto.multimedia_set.all():
                    element.delete()
                
                form = MultimediaForm(dict_aux, request.FILES)
                if form.is_valid():
                    form.save()
                else:
                    print('error')

                return redirect('list_activities')
                # other_reconocimiento
            
            # Repitencias
            elif 14 == pk_activity:
                try:
                    if 'on' in defaults['with_repitencias']:
                        defaults['with_repitencias'] = True
                    else:
                        defaults['with_repitencias'] = False
                except:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                try:
                    defaults['cantidad_repitencias'] = int(defaults['cantidad_repitencias'][0])
                    if defaults['with_repitencias'] and not defaults['cantidad_repitencias']:
                        messages.error(request, ERROR_REPITENCIAS)
                        return redirect('add_activities_and_student', pk = pk_activity)
                except:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                objeto, creado = ActivityAndStudent.objects.update_or_create(
                                activity_id = pk_activity,
                                profile_id = pk_profile,
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
                else:
                    print('error')

                return redirect('list_activities')
        
            #Reconocimiento en otras esferas
            elif 15 == pk_activity:
                # other_reconocimiento
                defaults['other_reconocimiento'] = defaults['other_reconocimiento'][0]
                if defaults['other_reconocimiento'] == '':
                    messages.error(request, ERROR_OTHER_RECONOCIMIENTO)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                objeto, creado = ActivityAndStudent.objects.update_or_create(
                                activity_id = pk_activity,
                                profile_id = pk_profile,
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
                else:
                    print('error')

                return redirect('list_activities')
                
        
            # # # # # # INVESTIGATIVA # # # # # #
            
            # Certificacion de Roles
            elif 4 == pk_activity:
                try:
                    if 'on' in defaults['has_roles']:
                        defaults['has_roles'] = True
                except:
                    defaults['has_roles'] = False
                    
                try:        
                    cadena = ','.join(defaults['roles'])
                    defaults['roles'] = cadena
                    
                    defaults['nivel_alcanzado'] = defaults['nivel_alcanzado'][0]
                    
                    if defaults['nivel_alcanzado'] == '':
                        messages.error(request, ERROR_GENERAL)
                        return redirect('add_activities_and_student', pk = pk_activity)
                except:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                
                objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)

                return redirect('list_activities')
                
            # Eventos y Competenias
            elif 3 == pk_activity:
                try:
                    if 'on' in defaults['is_evento']:
                        defaults['is_evento'] = True
                    else:
                        defaults['is_evento'] = False
                except:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                try:
                    defaults['nombre_evento'] =int(defaults['nombre_evento'][0])
                    if defaults['is_evento'] and defaults['nombre_evento']== 4:
                        if defaults['nombre_sub_evento'][0] == '':
                            messages.error(request, ERROR_NOMBRE_SUB_EVENTO)
                            return redirect('add_activities_and_student', pk = pk_activity)
                        else:
                            defaults['nombre_sub_evento'] = int(defaults['nombre_sub_evento'][0])
                    else:
                        if defaults['nombre_sub_evento'][0] == '':
                            defaults['nombre_sub_evento'] = 0  
                except:
                    messages.error(request, ERROR_NOMBRE_EVENTO)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                try:
                    if 'on' in defaults['es_colateral']:
                        defaults['es_colateral'] = True
                except:
                    defaults['es_colateral'] = False
                
                if defaults['es_colateral']:
                    if defaults['nombre_evento_colateral'] == '':
                        messages.error(request, ERROR_NOMBRE_EVENTO_COLATERAL)
                        return redirect('add_activities_and_student', pk = pk_activity)
                    
                    elif defaults['nivel'] == '':
                        messages.error(request, ERROR_NIVEL_EVENTO_COLATERAL)
                        return redirect('add_activities_and_student', pk = pk_activity)
                    
                    elif defaults['result'] == '':
                        messages.error(request, ERROR_RESULTADO_EVENTO_COLATERAL)
                        return redirect('add_activities_and_student', pk = pk_activity)
                    
                    defaults['nivel'] = int(defaults['nivel'][0])
                    defaults['result'] = int(defaults['result'][0])
                    
                else:
                    defaults['nivel'] = 0
                    defaults['result'] = 0
                
                objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                
                return redirect('list_activities')
                
            # Pertenece a alguna linea de investigacion
            elif 5 == pk_activity:
                try:
                    if 'on' in defaults['has_investigacion']:
                        defaults['has_investigacion'] = True
                except:
                    defaults['has_investigacion'] = False
                
                if defaults['has_investigacion'] and (defaults['participacion'][0] !='' ) and (defaults['nivel_evento'][0] !='' ):
                    
                    defaults['participacion'] = int(defaults['participacion'][0])
                    defaults['nivel_evento'] = int(defaults['nivel_evento'][0])
                    
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)

                    return redirect('list_activities')
                
                elif not defaults['has_investigacion'] and (defaults['participacion'][0] !='' ) and (defaults['nivel_evento'][0] !='' ):
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
            # Publicaciones logradas como autor o coautor    
            elif 6 == pk_activity:
                try:
                    if 'on' in defaults['has_publicacion']:
                        defaults['has_publicacion'] = True
                except:
                    defaults['has_publicacion'] = False
                
                if defaults['has_publicacion'] and (defaults['nombre_publicacion'][0] !='' ) and (defaults['nivel_autor'][0] !='' ) and (defaults['nivel_publicacion'][0] !='' ):
                    
                    defaults['nivel_autor'] = int(defaults['nivel_autor'][0])
                    defaults['nivel_publicacion'] = int(defaults['nivel_publicacion'][0])
                    defaults['nombre_publicacion'] = defaults['nombre_publicacion'][0]
                    
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)

                    return redirect('list_activities')
                
                else:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                    
                    
            # # # # # # POLITICO IDEOLOGICA # # # # # #
            
            # Direccion de Organizaciones
            elif pk_activity == 7:
                try:
                    if 'on' in defaults['is_feu']:
                        defaults['is_feu'] = True
                except:
                    defaults['is_feu'] = False
                    
                try:
                    if 'on' in defaults['is_ujc']:
                        defaults['is_ujc'] = True
                except:
                    defaults['is_ujc'] = False
                    
                if defaults['is_feu']:
                    defaults['evaluacion'] = defaults['evaluacion'][0]
                
                if not defaults['is_feu'] and defaults['is_ujc']:
                    defaults['evaluacion'] = defaults['evaluacion'][1]
                
                if defaults['is_feu'] and defaults['is_ujc']:
                    messages.error(request, ERROR_ORGANIZACIONES)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                if not defaults['is_feu'] and not defaults['is_ujc']:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                print('------------------------')
                print(defaults)
                if (defaults['is_feu'] and (defaults['nivel'][0] !='' ) and (defaults['cargo_feu'][0] !='' ) and (defaults['evaluacion'] !='' )) and \
                    (not defaults['is_ujc'] and (defaults['comite_base'][0] =='' ) and (defaults['cargo_ujc'][0] =='' ) ):
                    
                    defaults['nivel'] = int(defaults['nivel'][0])
                    defaults['cargo_feu'] = int(defaults['cargo_feu'][0])
                    defaults['evaluacion'] = int(defaults['evaluacion'])
                    
                    defaults['cargo_ujc'] = 0
                    
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)

                    return redirect('list_activities')
                
                elif (defaults['is_ujc'] and (defaults['comite_base'][0] !='' ) and (defaults['cargo_ujc'][0] !='' ) and (defaults['evaluacion'] !='' )) and \
                    (not defaults['is_feu'] and (defaults['nivel'][0] =='' ) and (defaults['cargo_feu'][0] =='' ) ):
                    
                    defaults['comite_base'] = defaults['comite_base'][0]
                    defaults['cargo_ujc'] = int(defaults['cargo_ujc'][0])
                    defaults['evaluacion'] = int(defaults['evaluacion'])
                    
                    defaults['nivel'] = 0
                    defaults['cargo_feu'] = 0
                    
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)

                    return redirect('list_activities')
                
                else:
                    messages.error(request, ERROR_ORGANIZACIONES)
                    return redirect('add_activities_and_student', pk = pk_activity)
                    
            # Otras Actividades Politico - ideologicas
            elif pk_activity == 8:
                if defaults['descripcion'][0] =='':
                    messages.error(request, ERROR_DESCRIPCION)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                defaults['descripcion'] = defaults['descripcion'][0]
                
                objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)

                return redirect('list_activities')
                
            # Reconocimientos logrados en este ambito
            elif pk_activity == 9:
                
                list_aux = []
                
                try:
                    if 'on' in defaults['distincion_marzo']:
                        defaults['distincion_marzo'] = True
                except:
                    defaults['distincion_marzo'] = False
                
                list_aux.append(defaults['distincion_marzo'])
                
                try:
                    if 'on' in defaults['distincion_fututo_maestro']:
                        defaults['distincion_fututo_maestro'] = True
                except:
                    defaults['distincion_fututo_maestro'] = False
                    
                list_aux.append(defaults['distincion_fututo_maestro'])
                    
                try:
                    if 'on' in defaults['distincion_joven']:
                        defaults['distincion_joven'] = True
                except:
                    defaults['distincion_joven'] = False
                    
                list_aux.append(defaults['distincion_joven'])
                    
                try:
                    if 'on' in defaults['is_ayudante']:
                        defaults['is_ayudante'] = True
                except:
                    defaults['is_ayudante'] = False
                    
                list_aux.append(defaults['is_ayudante'])
                
                is_true = any(valor for valor in list_aux)
                
                if not is_true and defaults['evaluacion'][0] != '':
                    messages.error(request, ERROR_RECONOCIMIENTO_LOGRADO)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                if is_true and defaults['evaluacion'][0] != '':
                    defaults['evaluacion'] =int(defaults['evaluacion'][0])

                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)

                    return redirect('list_activities')
                
                if is_true and defaults['evaluacion'][0] == '':
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        pk = int(self.request.path.split('/')[-1])
        
        context['pk_activity'] = str(self.request.path).split('/')[-1]
        context['object_name'] = Activity.objects.get(id = pk).name
        context['asignaturas'] = Asignatura.objects.all()
        context['evaluaciones'] = ActivityAndStudent.TYPE_EVALUACION
        return context
    
# class EventoView(LoginRequiredMixin, CreateView):
#     model = Evento
#     form_class = EventoForm
#     template_name = 'activity_and_student/testing.html'