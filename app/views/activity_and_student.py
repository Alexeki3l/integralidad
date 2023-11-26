from typing import Any
from django.db import models
from django.shortcuts import render, redirect
from ..models import Activity, Aspecto, ActivityAndStudent, Asignatura
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..forms import AddActivityView, EditActivityView, AddProfileView, EditProfileView, EditActivityAndStudentView,\
AddActivityAndStudentView, MultimediaForm

from django.urls import reverse, reverse_lazy

from app.utils import crear_objeto_activity_and_student, if_cadena_empty, generar_parrafo

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
                
                # objeto, creado = ActivityAndStudent.objects.update_or_create(
                #                 activity_id = pk_activity,
                #                 profile_id = pk_profile,
                #                 defaults=defaults
                #             )
                # if creado:
                    
                #     objeto.asignaturas_ayudante.clear()
                    
                #     for id_asignatura in ids_asignaturas:
                #         asignatura = Asignatura.objects.get(id=id_asignatura)
                #         objeto.asignaturas_ayudante.add(asignatura)
                        
                # dict_aux = request.POST.copy()
                # dict_aux['actividades'] = objeto.id
                
                # for element in objeto.multimedia_set.all():
                #     element.delete()
                # print(request.FILES['file'])
                # form = MultimediaForm(dict_aux, request.FILES)
                # if form.is_valid():
                #     form.save()
                # else:
                #     print('error')
                objeto, creado, is_create_image  = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                
                objeto.asignaturas_ayudante.clear()
                    
                for id_asignatura in ids_asignaturas:
                    asignatura = Asignatura.objects.get(id=id_asignatura)
                    objeto.asignaturas_ayudante.add(asignatura)

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
    
                objeto, creado, is_create_image = crear_objeto_activity_and_student(
                    request, pk_activity, pk_profile, defaults)
                
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
                
            # # # # # # EXTENSION ACADEMICA # # # # # #
            
            # Miembro o participacion en actividades de los proyectos extensionistas
            elif pk_activity == 17:
                if defaults['descripcion'][0] == '':
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                else:
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)

                    return redirect('list_activities')
            
            # Miembro o participacion en actividades de las Catedras de la Universidad
            elif pk_activity == 18: 
                try:
                    if 'on' in defaults['is_miembro']:
                        defaults['is_miembro'] = True
                except:
                    defaults['is_miembro'] = False
                    
                defaults['nombre_catedra'] = defaults['nombre_catedra'][0]
                defaults['actividad_participado'] = defaults['actividad_participado'][0]
                
                print(defaults)
                if defaults['is_miembro'] and (defaults['nombre_catedra'] !='')  and (defaults['actividad_participado'] != ''):
                    
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                    return redirect('list_activities')
                
                else:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
            
            # Actividades Culturales
            elif pk_activity == 19: 
                try:
                    if 'on' in defaults['if_participacion_actos_matutinos']:
                        defaults['if_participacion_actos_matutinos'] = True
                except:
                    defaults['if_participacion_actos_matutinos'] = False
                    
                try:
                    if 'on' in defaults['if_participacion_festivales']:
                        defaults['if_participacion_festivales'] = True
                except:
                    defaults['if_participacion_festivales'] = False
                    
                defaults['manifestacion_festivales'] = defaults['manifestacion_festivales'][0]
                defaults['nivel_artista_aficionado'] = defaults['nivel_artista_aficionado'][0]
                defaults['premio_artista_aficionado'] = defaults['premio_artista_aficionado'][0]
                
                defaults['nombre_actividad_facultad'] = defaults['nombre_actividad_facultad'][0]
                defaults['manifestacion_actividad_facultad'] = defaults['manifestacion_actividad_facultad'][0]
                    
                if defaults['if_participacion_festivales'] and (defaults['manifestacion_festivales']!='') and (defaults['nivel_artista_aficionado']!='') and (defaults['premio_artista_aficionado']!='')\
                    or defaults['nombre_actividad_facultad']!='' and defaults['manifestacion_actividad_facultad']!='' and not defaults['if_participacion_festivales'] and (defaults['manifestacion_festivales']=='') and (defaults['nivel_artista_aficionado']=='') and (defaults['premio_artista_aficionado']==''):
                    try:
                        defaults['nivel_artista_aficionado'] = int(defaults['nivel_artista_aficionado'])
                        defaults['premio_artista_aficionado'] = int(defaults['premio_artista_aficionado'])
                    except:
                        defaults['nivel_artista_aficionado'] = 0
                        defaults['premio_artista_aficionado'] = 0
                    
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                    return redirect('list_activities')

                else:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
            elif pk_activity == 20:
                
                defaults['lugar_dnd_realizo'] = defaults['lugar_dnd_realizo'][0]
                defaults['evaluacion'] = defaults['evaluacion'][0]
                
                if defaults['lugar_dnd_realizo']!=0 and defaults['evaluacion']!=0:
                    
                    defaults['evaluacion'] = int(defaults['evaluacion'])
                    
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                    return redirect('list_activities')
                
                else:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
            elif pk_activity == 21:
                try:
                    if 'on' in defaults['if_jjmm']:
                        defaults['if_jjmm'] = True
                except:
                    defaults['if_jjmm'] = False
                    
                try:
                    if 'on' in defaults['if_copas_mundialess']:
                        defaults['if_copas_mundialess'] = True
                except:
                    defaults['if_copas_mundialess'] = False
                    
                try:
                    if 'on' in defaults['if_marabana']:
                        defaults['if_marabana'] = True
                except:
                    defaults['if_marabana'] = False
                    
                list_deporte = defaults['deporte']
                list_resultado_deporte = defaults['resultado_deporte']
                # defaults['resultado_deporte'] = defaults['resultado_deporte'][0]
                
                if (len(list_deporte) != len(list_resultado_deporte)) or \
                    len(list_deporte) == 0 and len(list_resultado_deporte) == 0:
                    messages.error(request, ERROR_DEPORTE_RESULTADO)
                    return redirect('add_activities_and_student', pk = pk_activity)
                    
                
                defaults['deporte'] = str(defaults['deporte'])
                defaults['resultado_deporte'] = str(defaults['resultado_deporte'])
                
                defaults['lugar'] = defaults['lugar'][0]
                
                defaults['nombre_evento_marabana'] = defaults['nombre_evento_marabana'][0]
                
                defaults['nombre_evento_copas_mundiales'] = defaults['nombre_evento_copas_mundiales'][0]
                defaults['lugar_copas_mundiales'] = defaults['lugar_copas_mundiales'][0]
                
                
                
                condicion_1 = defaults['if_jjmm'] and (defaults['deporte']!='') and (defaults['resultado_deporte']!='') and (defaults['lugar']!='')
                condicion_2 = defaults['if_copas_mundialess'] and (defaults['nombre_evento_copas_mundiales']!='') and (defaults['resultado_copas_mundiales']!='') and (defaults['lugar_copas_mundiales']!='')
                condicion_3 = defaults['if_marabana'] and (defaults['nombre_evento_marabana']!='' and (defaults['resultado_copas_mundiales']!=''))
                
                if (condicion_1 and condicion_2 and condicion_3) or (not condicion_1 and not condicion_2 and condicion_3) or (condicion_1 and not condicion_2 and not condicion_3) or (not condicion_1 and condicion_2 and not condicion_3):
                    # print('pincha')
                    
                    try:
                        defaults['nombre_evento_marabana'] = int(defaults['nombre_evento_marabana'])
                    except:
                        defaults['nombre_evento_marabana'] = 0
                    
                    # defaults['deporte'] = int(defaults['deporte'])
                    # defaults['resultado_deporte'] = int(defaults['resultado_deporte'])
                    defaults['lugar'] = int(defaults['lugar'])
                    
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                    return redirect('list_activities')
                
                else:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
            elif pk_activity == 22:
                cuartelerias_dict = {}
                meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio",
                        "Septiembre","Octubre","Noviembre","Diciembre"]
                
                
                # La funcion map retorna un objeto de tipo map que contiene True o False segun el criterio de la funcion 'if_cadena_empty'.
                # Este objeto lo convertimos a lista con la funcion list y con la funcion all verificamos que si todos los elementos son True
                is_true = all(list(map(if_cadena_empty, defaults['evaluacion_cuarteleria'])))
                
                if not is_true:
                    messages.error(request, ERROR_FALTAN_EVALUACIONES)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                for position, evaluation in enumerate(defaults['evaluacion_cuarteleria']):
                    try:
                        evaluation = int(evaluation) - 1
                    except ValueError:
                        evaluation = 0
                        
                    if position < 11:
                        cuartelerias_dict[meses[position]] = ActivityAndStudent.TYPE_EVALUACION_CUARTELERIA[evaluation][1]
                    else:
                        defaults['responsabilidad'] = defaults['responsabilidad'][0]
                        if defaults['responsabilidad'] in ['1', '2']:
                            cuartelerias_dict['evaluacion_responsabilidad'] = ActivityAndStudent.TYPE_EVALUACION_CUARTELERIA[evaluation][1]
                        else:
                            messages.error(request, ERROR_RESPONSABILIDAD_EVALUACION)
                            return redirect('add_activities_and_student', pk = pk_activity)

                try:
                    if 'on' in defaults['if_senalamiento_residencia']:
                        defaults['if_senalamiento_residencia'] = True
                except:
                    defaults['if_senalamiento_residencia'] = False
                    
                defaults['descripcion'] = defaults['descripcion'][0]
                    
                condicion_1 = defaults['if_senalamiento_residencia'] and defaults['descripcion']!=''
                
                if not condicion_1:
                    messages.error(request, ERROR_SENALAMIENTO_RESIDENCIA)
                    return redirect('add_activities_and_student', pk = pk_activity)
                    
                defaults['cuartelerias'] = cuartelerias_dict
                
                objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                return redirect('list_activities')
                        
            elif pk_activity == 23:
                try:
                    defaults['total_ausencias'] = int(defaults['total_ausencias'][0])
                    defaults['total_ausencias_justificadas'] = int(defaults['total_ausencias_justificadas'][0])
                    defaults['total_ausencias_injustificadas'] = int(defaults['total_ausencias_injustificadas'][0])
                    defaults['total_recuperadas'] = int(defaults['total_recuperadas'][0])
                except:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                try:
                    if 'on' in defaults['if_senalamiento_guardia_estudiantil']:
                        defaults['if_senalamiento_guardia_estudiantil'] = True
                except:
                    defaults['if_senalamiento_guardia_estudiantil'] = False
                    
                defaults['cantidad_senalamiento_guardia_estudiantil'] = defaults['cantidad_senalamiento_guardia_estudiantil'][0]
                
                condicion_1 = defaults['if_senalamiento_guardia_estudiantil'] and defaults['cantidad_senalamiento_guardia_estudiantil']!=''
                
                if not condicion_1:
                    messages.error(request, ERROR_SENALAMIENTO_GUARDIA)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
                objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                return redirect('list_activities')
            
            elif pk_activity == 24:
                try:
                    if 'on' in defaults['if_actividades_limpieza_areas_comunes']:
                        defaults['if_actividades_limpieza_areas_comunes'] = True
                except:
                    defaults['if_actividades_limpieza_areas_comunes'] = False
                    
                    
                try:
                    if 'on' in defaults['if_bk_mas_bonita']:
                        defaults['if_bk_mas_bonita'] = True
                except:
                    defaults['if_bk_mas_bonita'] = False
                    
                
                defaults['nombre_actividades_limpieza_areas_comunes'] = defaults['nombre_actividades_limpieza_areas_comunes'][0]
                defaults['mes'] = defaults['mes'][0]
                defaults['resultado_actividades_limpieza_areas_comunes'] = defaults['resultado_actividades_limpieza_areas_comunes'][0]
                defaults['other_reconocimiento'] = defaults['other_reconocimiento'][0]
                
                condicion_1 = defaults['if_actividades_limpieza_areas_comunes'] and defaults['nombre_actividades_limpieza_areas_comunes']!='' and defaults['mes']!='' and defaults['resultado_actividades_limpieza_areas_comunes']!=''
                condicion_2 = defaults['if_bk_mas_bonita'] and defaults['other_reconocimiento']!=""
                
                if condicion_1:
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                    return redirect('list_activities')
                
                elif condicion_1 and condicion_2:
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                    return redirect('list_activities')
                
                else:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
            elif pk_activity == 25:
                defaults['other_reconocimiento'] = defaults['other_reconocimiento'][0]
                defaults['reconocimiento_otorgado_por'] = defaults['reconocimiento_otorgado_por'][0]
                
                condicion_1 = defaults['other_reconocimiento']!='' and defaults['reconocimiento_otorgado_por']!=''
                
                if condicion_1:
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                    return redirect('list_activities')
                
                else:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                    
            elif pk_activity == 26:
                defaults['sanciones_o_medida'] = defaults['sanciones_o_medida'][0]
                defaults['motivo_sancion'] = defaults['motivo_sancion'][0]
                
                condicion_1 = defaults['sanciones_o_medida']!="" and defaults['motivo_sancion']!=""
                
                if condicion_1:
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                    return redirect('list_activities')
                
                else:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
            elif pk_activity == 27:
                defaults['senalamiento_curso'] = defaults['senalamiento_curso'][0]
                
                if defaults['senalamiento_curso']!="":
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                    return redirect('list_activities')
                
                else:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                
            elif pk_activity ==28:
                defaults['nombre_distincion'] = defaults['nombre_distincion'][0]
                defaults['organismo_otorga_distincion'] = defaults['organismo_otorga_distincion'][0]
                
                condicion_1 = defaults['nombre_distincion']!="" and defaults['organismo_otorga_distincion']!=""
                
                if condicion_1:
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                    return redirect('list_activities')
                
                else:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
            
            elif pk_activity ==29:
                defaults['nombre_mision'] = defaults['nombre_mision'][0]
                defaults['funsion_desempenada'] = defaults['funsion_desempenada'][0]
                defaults['proceso'] = defaults['proceso'][0]
                
                condicion_1 = defaults['nombre_mision']!="" and defaults['funsion_desempenada']!="" and defaults['proceso']!=""
                
                if condicion_1:
                    try:
                        defaults['proceso'] = int(defaults['proceso'])
                    except:
                        defaults['proceso'] = 0
                        
                    objeto, creado, is_create_image = crear_objeto_activity_and_student(request, pk_activity, pk_profile, defaults)
                    return redirect('list_activities')
                
                else:
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
        context['meses'] = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio", "Septiembre","Octubre","Noviembre","Diciembre"]
        return context
    
def list_activity_and_student_for_profesor(request, pk_student):
    if request.user.profile.rol_fac != 1:
        data = {}
        list_annos = ["", 'Primer Año', 'Segundo Año', 'Tercer Año', 'Cuarto Año']
        
        for pos, anno in enumerate(list_annos):
            if pos != 0:
                try:
                    profile = Profile.objects.get(id = pk_student, academy_year = pos)
                except:
                    data[anno] ={}
                    continue
                dict_aux = {}
                for aspecto in Aspecto.objects.all():
                    list_activitys_relationed_with_student = profile.activity_set.filter(aspecto = aspecto)
                    name = '_'.join(aspecto.name.split())
                    dict_aux[f'{name}'] = list_activitys_relationed_with_student
                data[anno] = dict_aux
            else:
                pass
        # print('DATA RESPONSE: ', data)
        context = {
            'primer_anno':data['Primer Año'],
            'segundo_anno':data['Segundo Año'],
            'tercer_anno':data['Tercer Año'],
            'cuarto_anno':data['Cuarto Año'],
            'pk_student':pk_student,
        }
        print(data['Cuarto Año'])
        return render(request, 'activity_and_student/list_activity_and_student_for_profesor.html', context=context)
    else:
        return redirect('list_activities')
    
class DetailsActivityAndStudentForProfessorView(DetailView):
    model = ActivityAndStudent
    template_name = 'activity_and_student/details_activity_and_student_for_profesor.html'
    context_object_name = 'activity_and_student'
    
    def get_object(self, queryset=None):
        pk_activity = self.kwargs.get('pk_activity')
        pk_student = self.kwargs.get('pk_student')
        act_and_student = ActivityAndStudent.objects.get(activity_id=pk_activity, profile_id=pk_student)
        print(act_and_student.get_roles_display())
        return act_and_student
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        obj = kwargs['object']
        context["pk_activity"] = str(obj.activity.id)
        return context
    
    
def caracterizacion(request):
    
    list_actividades = ActivityAndStudent.objects.filter(profile_id = request.user.profile, year = 4)
    parrafo_cuarto_anno = generar_parrafo(list_actividades)
    context={
        'parrafo_cuarto_anno':parrafo_cuarto_anno,
    }
    return render(request, 'activity_and_student/caracterizacion.html')
    