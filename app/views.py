from django.shortcuts import render, redirect
from .models import Activity, Aspecto
from django.http import HttpResponse
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import AddActivityView, EditActivityView

from django.urls import reverse, reverse_lazy
from .utils import return_list_activities_html

import math

# Create your views here.

def activities(request, number_page=0):
    if request.user.is_authenticated:
        print(number_page)
        var = 20
        begin = var*number_page
        end = (number_page + 1)*var + number_page
        
        # Hacemos un paginado
        all_activities = Activity.objects.all()
        activities = all_activities[begin:end]
        count = all_activities.count()
        cant_page = math.ceil(count/20)
        cant_page = list(range(0, cant_page))
        print(cant_page)
        
        disabled = False
        print(request.path)
        if str(number_page) in request.path:
            disabled = True
        
        # Cuando halla una peticion HTMX
        if request.htmx:
            if request.htmx.target == 'search-results':
                search_input = request.GET.get('search_activities', None)
                if search_input:
                    # print(request.path)
                    patterns =Q(description__icontains=search_input) | Q(aspecto_id__in=Aspecto.objects.filter(name__icontains = search_input).values_list('id', flat=True))
                    activities = all_activities.filter(patterns)
                    print(return_list_activities_html(activities))
                    return HttpResponse(
                            return_list_activities_html(activities)
                        )
                    # else:
                    #     return HttpResponse(
                    #         '<p class="text-center">Center aligned text on all viewport sizes.</p>'
                    #         )
                else:
                    # activities = Activity.objects.all()
                    return HttpResponse(
                        return_list_activities_html(activities)
                        )
        # Si es un GET
        context = {
            'actividades': activities,
            'total':count,
            'pages':cant_page,
            'disabled':disabled,
            'flag': True
        }
        return render(request, 'actividad.html', context=context)
    else:
        return redirect('login')
        
# -------------- CRUD de Actividad ------------------------------------------
# Crear Actividades
class AddActivityView(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = AddActivityView
    template_name = 'add_activity.html'

    # def form_valid(self, form):
    #     form.instance.created = timezone.now()
    #     form.instance.encargado = self.request.user
    #     return super().form_valid(form)


# Detalle Actividades
class DetailsActivityView(DetailView):
    model = Activity
    template_name = 'details_activity.html'
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
    template_name='edit_activity.html'
    
    # def form_valid(self, form):
    #     form.instance.updated = timezone.now()
    #     form.instance.autor = self.request.user
    #     return super().form_valid(form)


# Eliminar Actividades
class DeleteActivityView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = "delete_activity.html"
    success_url = reverse_lazy('activities')
    
    
# -------------- (FIN) CRUD de Actividad ------------------------------------------
