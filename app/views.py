from django.shortcuts import render, redirect
from .models import Activity, Aspecto
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import AddActivityView, EditActivityView

from django.urls import reverse, reverse_lazy
from .utils import return_list_activities_html, return_content_full_table_html

import math

# Create your views here.

def activities(request, number_page=0):
    if request.user.is_authenticated:
        if request.method == 'GET':
            var = 10
            number_page = 0
            
        try:
            if request.headers['Hx-Trigger-Name'] == 'siguiente':
                number_page += 1
        except KeyError:
            pass
        begin = var*number_page
        end = (number_page + 1)*var + number_page
        
        # --------Hacemos un paginado------------
        all_activities = Activity.objects.all().order_by('-id')
        activities = all_activities[begin:end]
        count_total_objects = all_activities.count()
        cant_page = math.ceil(count_total_objects/var)
        cant_page = list(range(0, cant_page))
        is_pagination = False
        if end > count_total_objects:
            end = count_total_objects
            
        begin += 1
        
        # -----------Hojear paginas--------------
        anterior = 0
        siguiente = 0
        response = HttpResponse()
        
        if request.htmx:
            number_page = int(request.path[-1])
        
        try:
            if cant_page[number_page - 1]:
                anterior = number_page - 1
        except IndexError:
            anterior = 0
        
        try:
            if cant_page[number_page + 1]:
                siguiente = number_page + 1
        except IndexError:
            siguiente = 0
            
        # try:
        #     if request.headers['Hx-Trigger-Name'] == 'siguiente':
        #         response.set_cookie(key='siguiente', value=siguiente)
        # except:
        #     pass
        
        print('COOKIES 1',request.COOKIES)
        print('COOKIES',request.COOKIES.get('siguiente'))
        # response.set_cookie('siguiente', siguiente)
        print(request.headers)
        print('siguiente',siguiente)
        # ----------------------------------------
        # Cuando halla una peticion HTMX
        if request.htmx:
            # ----------------- PAGINACION -----------------
            # Boton Siguiente
            if request.htmx.target == 'basic-datatable-preview' and request.htmx.trigger_name == 'siguiente':
                    response = HttpResponse(
                        return_content_full_table_html(activities)
                        )
                    response.set_cookie(key='siguiente', value=siguiente)
                    return response
                    
                    
            # -------------- END PAGINATION ----------------------
            
            # ------------ BUSCAR ACTIVIDADES --------------------
            
            if request.htmx.target == 'basic-datatable-preview' and request.htmx.trigger_name == 'search_activities':
                search_input = request.GET.get('search_activities', None)
                print(search_input)
                if search_input:
                    # print(request.path)
                    patterns =Q(description__icontains=search_input) | Q(aspecto_id__in=Aspecto.objects.filter(name__icontains = search_input).values_list('id', flat=True))
                    activities = all_activities.filter(patterns)
                    # print(return_list_activities_html(activities))
                    return HttpResponse(
                            return_content_full_table_html(activities)
                        )
                    # else:
                    #     return HttpResponse(
                    #         '<p class="text-center">Center aligned text on all viewport sizes.</p>'
                    #         )
                
                else:
                    # activities = Activity.objects.all()
                    return HttpResponse(
                        return_content_full_table_html(activities)
                        )
                    
            # -------------END BUSCAR ACTIVIDADES -------------
        
        context = {
            'actividades': activities,
            'begin':begin,
            'end':end,
            'count_total_objects':count_total_objects,
            'pages':cant_page,
            # 'disabled':disabled,
            'anterior':anterior,
            'siguiente':siguiente,
            'flag': True,
            'is_pagination':is_pagination
        }
        return render(request, 'activity/activities.html', context=context)
    else:
        return redirect('login')
        
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
    success_url = reverse_lazy('activities', args=[0])
    
    
# ----------------------- (FIN) CRUD de Actividad ----------------------------

# ----------------------- TRATAMIENTO DE ERRORES -----------------------------

# Error 404
def custom_404(request, exception):
    return render(request, 'error/404.html', status=404)
