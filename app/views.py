from typing import Any
from django.shortcuts import render, redirect
from .models import Activity, Aspecto
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import AddActivityView, EditActivityView, AddProfileView, EditProfileView

from django.urls import reverse, reverse_lazy
from .custom_html_response import return_list_activities_html, return_content_full_table_html,\
delete_key_values_in_cookies

from .custom_method import order_list_by_group

from authentication.models import Profile

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
class EditActivityView(UpdateView):
    model = Activity
    form_class = EditActivityView
    template_name='activity/edit_activity.html'
    
    # def form_valid(self, form):
    #     form.instance.updated = timezone.now()
    #     form.instance.autor = self.request.user
    #     return super().form_valid(form)


# Eliminar Actividades
class DeleteActivityView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = "activity/delete_activity.html"
    success_url = reverse_lazy('list_activities')
    
    
# ----------------------- (FIN) CRUD de Actividad ----------------------------

# ----------------------------- ROLES -------------------------------
def list_roles(request, id_rol):
    profiles = Profile.objects.all()
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
    
    obj = profiles[0]
    print(obj.get_rol_fac_display())

    if str(obj.grupo) == 'nan':
        flag = True
    else:
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
