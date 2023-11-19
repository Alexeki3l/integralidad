from typing import Any
from django.shortcuts import render, redirect
from .models import Activity, Aspecto, ActivityAndStudent, Asignatura
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import AddActivityView, EditActivityView, AddProfileView, EditProfileView, EditActivityAndStudentView, AddActivityAndStudentView

from django.urls import reverse, reverse_lazy

from django.contrib import messages

from authentication.models import Profile

from app.metodos_personalizados.message import *

import math

def list_activities(request):
    activities = Activity.objects.all()
    context = {
        'activities':activities
    }
    return render(request, 'activity/activities.html', context=context)

# Create your views here.
# def list_activities(request):
#     if request.user.is_authenticated:
#         print('HEADERS GET', request.headers)
        
#         response = HttpResponse()
        
#         var = 10
#         number_page = 0
#         response.set_cookie(key='number_page', value=0)
#         response.set_cookie(key='cant_element', value=var)
            
#         begin = var*number_page
#         end = (number_page + 1)*var + number_page
        
#         # --------Hacemos un paginado------------
#         all_activities = Activity.objects.all().order_by('-id')
#         activities = all_activities[begin:end]
#         count_total_objects = all_activities.count()
#         cant_page = math.ceil(count_total_objects/var)
#         cant_page = list(range(0, cant_page))
#         is_pagination = False
        
#         if end > count_total_objects:
#             end = count_total_objects

#         begin += 1
        
#         # -----------Hojear paginas--------------
#         anterior = 0
#         siguiente = 0
        
#         try:
#             if cant_page[number_page - 1]:
#                 anterior = number_page - 1
#         except IndexError:
#             anterior = 0
        
#         try:
#             if cant_page[number_page + 1]:
#                 siguiente = number_page + 1
#         except IndexError:
#             siguiente = 0
            
#         # ----------------------------------------
#         # Cuando halla una peticion HTMX
#         context = {
#             'actividades': activities,
#             'begin':begin,
#             'end':end,
#             'count_total_objects':count_total_objects,
#             'pages':cant_page,
#             # 'disabled':disabled,
#             'anterior':anterior,
#             'siguiente':siguiente,
#             'flag': True,
#             'is_pagination':is_pagination
#         }
        
#         html =  render(request, 'activity/activities.html', context=context)
#         response.set_cookie(key='siguiente', value=siguiente)
#         response.set_cookie(key='anterior', value=anterior)
        
#         response.content = html.content
#         return response
#     else:
#         return redirect('login')
    
    
# def list_activities_htmx(request):
#     if request.user.is_authenticated:
#         print('-----------------------------')
#         print('HEADERS HTMX', request.headers)
#         print('-----------------------------')
#         response = HttpResponse()
#         try:  
#             if request.headers['Hx-Trigger-Name'] == 'siguiente':
#                 print('pasa por aqui')
#                 cant_element = int(request.COOKIES.get('cant_element'))
#                 number_page = int(request.COOKIES.get('number_page'))
#                 # number_page += 1
                
#             elif request.headers['Hx-Trigger-Name'] == 'select_cant':
#                 cant_element = int(request.COOKIES.get('cant_element'))
#                 number_page = int(request.COOKIES.get('number_page'))
                
#             else:
#                 cant_element = int(request.COOKIES.get('cant_element'))
#                 number_page = int(request.COOKIES.get('number_page'))
                
#         except:
#             pass
        
#         begin = cant_element*number_page
#         end = (number_page + 1)*cant_element + number_page
        
#         # --------Hacemos un paginado------------
#         all_activities = Activity.objects.all().order_by('-id')
#         if end > all_activities.count():
#             activities = all_activities[begin:all_activities.count()]
#         else:
#             activities = all_activities[begin:end]
            
#         count_total_objects = all_activities.count()
#         cant_page = math.ceil(count_total_objects/cant_element)
#         cant_page = list(range(0, cant_page))
#         print('cant_page',cant_page)
#         is_pagination = False
#         if end > count_total_objects:
#             end = count_total_objects
            
#         begin += 1
        
#         # -----------Hojear paginas--------------
#         # if not request.headers['Hx-Trigger-Name'] == 'siguiente':
#         anterior = int(request.COOKIES.get('anterior'))
#         siguiente = int(request.COOKIES.get('siguiente'))
        
#         try:
#             if cant_page[number_page - 1]:
#                 anterior = number_page - 1
#         except IndexError:
#             anterior = 0
        
#         try:
#             if cant_page[number_page + 1]:
#                 number_page += 1
#                 siguiente = number_page
                
#             if cant_page[siguiente]:
#                 pass
#         except IndexError:
#             siguiente = 0
#             number_page = 0
        
#         # ----------------------------------------
#         # Cuando halla una peticion HTMX
#         if request.htmx:
#             # ----------------- PAGINACION -----------------
#             # --------------- Boton Siguiente -------------
#             if request.htmx.target == 'basic-datatable-preview' and request.htmx.trigger_name == 'siguiente':
#                     print('SGUIENTE')
#                     response = HttpResponse(
#                         return_content_full_table_html(activities, begin, end, count_total_objects, anterior, siguiente)
#                         )
#                     # valor = int(request.COOKIES.get('cant_element'))
#                     # response.set_cookie(key='cant_element', value=valor)
#                     # siguiente = int(request.COOKIES.get('siguiente'))
                        
#                     response.set_cookie(key='siguiente', value=siguiente)
#                     response.set_cookie(key='number_page', value=number_page)
#                     return response
                    
                    
#             # -------------- END PAGINATION ----------------------
#             #----------- Selector de Cantidad de Elementos--------
#             if request.htmx.target == 'basic-datatable-preview' and request.htmx.trigger_name == 'select_cant':
#                 print('SELECT')
#                 list_aux = [0, 10, 20, 50, 100]
#                 valor_seleccionado = request.GET.get('select_cant')
#                 valor = list_aux[int(valor_seleccionado)]
#                 if valor > all_activities.count():
#                     valor = all_activities.count()
#                     siguiente = -1
#                     end = valor
#                 activities = all_activities[:valor]
                
#                 response = HttpResponse(
#                             return_content_full_table_html(activities, begin, end, count_total_objects, anterior, siguiente)
#                         )
#                 response.set_cookie(key='cant_element', value=valor)
#                 response.set_cookie(key='siguiente', value=siguiente)
#                 response.set_cookie(key='number_page', value=number_page)
#                 return response
            
#             # ------- END Selector de Cantidad de Elementos ------------
#             # ------------ BUSCAR ACTIVIDADES --------------------
            
#             if request.htmx.target == 'basic-datatable-preview' and request.htmx.trigger_name == 'search_activities':
#                 print('BUSCAR')
#                 search_input = request.GET.get('search_activities', None)
#                 if search_input:
#                     patterns =Q(description__icontains=search_input) | Q(aspecto_id__in=Aspecto.objects.filter(name__icontains = search_input).values_list('id', flat=True))
#                     activities = all_activities.filter(patterns)
#                     response =  HttpResponse(
#                             return_content_full_table_html(activities, begin, end, count_total_objects, anterior, siguiente)
#                         )
                    
#                     # valor = int(request.COOKIES.get('cant_element'))
#                     # response.set_cookie(key='cant_element', value=valor)
#                     # response.set_cookie(key='siguiente', value=siguiente)
#                     # response.set_cookie(key='number_page', value=number_page)
#                     return response
#                 else:
#                     response =  HttpResponse(
#                             return_content_full_table_html(activities, begin, end, count_total_objects, anterior, siguiente)
#                         )
#                     # valor = int(request.COOKIES.get('cant_element'))
#                     # response.set_cookie(key='cant_element', value=valor)
#                     # response.set_cookie(key='siguiente', value=siguiente)
#                     # response.set_cookie(key='number_page', value=number_page)
#                     return response
                    
#             # -------------END BUSCAR ACTIVIDADES -------------
        
#         context = {
#             'actividades': activities,
#             'begin':begin,
#             'end':end,
#             'count_total_objects':count_total_objects,
#             'pages':cant_page,
#             # 'disabled':disabled,
#             # 'anterior':anterior,
#             # 'siguiente':siguiente,
#             'flag': True,
#             'is_pagination':is_pagination
#         }
#         html =  render(request, 'activity/activities.html', context=context)
#         response.set_cookie(key='siguiente', value=siguiente)
#         response['encabezado'] = 'TESTING'
#         print(request.headers.keys())
#         response.content = html.content
#         return response
#     else:
#         return redirect('login')
        
# -------------- CRUD de Actividad ------------------------------------------
# Crear Actividades
class AddActivityView(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = AddActivityView
    template_name = 'activity/add_activity.html'

    # def form_valid(self, form):
    #     form.instance.created = timezone.now()
    #     form.instance.encargado = self.request.user
    #     return super().form_valid(form)


# Detalle Actividades
class DetailsActivityView(DetailView):
    model = Activity
    template_name = 'activity/details_activity.html'
    context_object_name = 'activity'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # kwargs={'pk': self.producto.pk}
    #     comentarios = ComentarioP.objects.filter(producto_id = kwargs['object'])
    #     # for comentario in comentarios:
    #     #     respuestas = RespuestaP.objects.filter(comentariosp_id = comentario.id)
    #     cantidad_comentarios = comentarios.count()
    #     # cantidad_respuestas = respuestas.count()
    #     total = cantidad_comentarios 
    #     ''' + cantidad_respuestas'''
    #     context["total"] = total
    #     context['productos'] = Product.objects.all()
        
    #     return context
    
    
# Editar Actividades
class EditActivityView(CreateView):
    model = Activity
    form_class = EditActivityAndStudentView
    template_name='activity/edit_activity.html'
    
    # def form_valid(self, form):
    #     form.instance.updated = timezone.now()
    #     form.instance.autor = self.request.user
    #     return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        print(context)
        pk = int(self.request.path.split('/')[-1])
        context['object_name'] = Activity.objects.get(id = pk)
        
        return context


# Eliminar Actividades
class DeleteActivityView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = "activity/delete_activity.html"
    success_url = reverse_lazy('list_activities')
    
    
# ----------------------- (FIN) CRUD de Actividad ----------------------------

# ----------------------CRUD de ActividadAndStudent ----------------------------
class AddActivityAndStudentView(LoginRequiredMixin, CreateView):
    model = ActivityAndStudent
    form_class = AddActivityAndStudentView
    template_name = 'activity_and_student/add_activity_and_student.html'
    
    def dispatch(self, request, *args, **kwargs):
        
        if request.method == 'POST':
            pk_activity = int(self.request.path.split('/')[-1])
            
            ### ACADEMICO ###
            # ALUMNO AYUDANTE
            if 11 == pk_activity:
                
                year_student = int(self.request.user.profile.academy_year)
                pk_profile = int(self.request.user.profile.id)
                
                defaults = dict(request.POST).copy()
                del defaults['csrfmiddlewaretoken']

                defaults['year'] = year_student
                try:
                    defaults['evaluacion'] = int(defaults['evaluacion'][0])
                except:
                    messages.error(request, ERROR_GENERAL)
                    return redirect('add_activities_and_student', pk = pk_activity)
                    
                
                try:
                    print(defaults)
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
                if creado or not creado:
                    for id_asignatura in ids_asignaturas:
                        asignatura = Asignatura.objects.get(id=id_asignatura)
                        objeto.asignaturas_ayudante.add(asignatura)
                
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        pk = int(self.request.path.split('/')[-1])
        
        context['pk_activity'] = str(self.request.path).split('/')[-1]
        context['object_name'] = Activity.objects.get(id = pk).name
        context['asignaturas'] = Asignatura.objects.all()
        context['evaluaciones'] = ActivityAndStudent.TYPE_EVALUACION
        return context


# ----------------------------- ROLES -------------------------------
def list_roles(request, id_rol):
    if request.user.profile.rol_fac == 4:
        profiles = Profile.objects.all().exclude(rol_fac = request.user.profile.rol_fac)
        rol = 'Todos'
        if id_rol == 1:
            profiles = profiles.filter(rol_fac = 1)
            rol = 'Estudiantes'
        if id_rol == 2:
            profiles = profiles.filter(rol_fac = 2)
            rol = 'Profesores Guias'
        if id_rol == 3:
            profiles = profiles.filter(rol_fac = 3)
            rol = 'Profesores de Año'
            
    elif request.user.profile.rol_fac == 3:
        profiles = Profile.objects.all().filter(academy_year = request.user.profile.academy_year).exclude(id = request.user.profile.id)
        rol = 'Todos'
        if id_rol == 1:
            profiles = profiles.filter(rol_fac = 1)
            rol = 'Estudiantes'
        if id_rol == 2:
            profiles = profiles.filter(rol_fac = 2)
            rol = 'Profesores Guias'
            
    elif request.user.profile.rol_fac == 2:
        profiles = Profile.objects.all().filter(academy_year = request.user.profile.academy_year, grupo =request.user.profile.grupo).exclude(id = request.user.profile.id)
        rol = 'Todos'
        if id_rol == 1:
            profiles = profiles.filter(rol_fac = 1)
            rol = 'Estudiantes'
        
    try:
        obj = profiles[0]
    except IndexError:
        obj = ""
        
    try:
        if str(obj.grupo) == 'nan':
            flag = True
        else:
            flag = False
    except AttributeError:
        flag = False
    
    context = {
        'profiles':profiles,
        'rol':rol,
        'flag':flag
    }
    return render(request, 'roles/all_roles.html', context=context)

# class AddProfileView(LoginRequiredMixin, CreateView):
#     model = Profile
#     form_class = AddProfileView
#     template_name = 'roles/add_profile.html'

# Detalle Profile
class DetailsProfileView(DetailView):
    model = Profile
    template_name = 'roles/details_profile.html'
    context_object_name = 'profile'
    
# Editar Profile
class EditProfileView(UpdateView):
    model = Profile
    form_class = EditProfileView
    template_name='roles/edit_profile.html'


# Eliminar Profile
# class DeleteProfileView(LoginRequiredMixin, DeleteView):
#     model = Profile
#     template_name = "roles/delete_profile.html"
#     success_url = reverse_lazy('list_roles')
            

# ----------------------- TRATAMIENTO DE ERRORES -----------------------------

# Error 404
def custom_404(request, exception):
    return render(request, 'error/404.html', status=404)
