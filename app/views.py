from django.shortcuts import render, redirect
from .models import Activity, Aspecto
from django.http import HttpResponse
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import AddActivityView, EditActivityView

from django.urls import reverse, reverse_lazy

# Create your views here.

def activities(request):
    if request.user.is_authenticated:
        activities = Activity.objects.all()
        if request.htmx:
            if request.htmx.target == 'search-results':
                search_input = request.GET.get('search_activities', None)
                if search_input:
                    # print(request.path)
                    
                    patterns =Q(description__icontains=search_input) | Q(aspecto_id__in=Aspecto.objects.filter(name__icontains = search_input).values_list('id', flat=True))
                    activities = activities.filter(patterns)
                    
                    return HttpResponse(
                            [f"""<tr>
                                                        <td>{activity.description}</td>
                                                        <td>{activity.aspecto}</td>
                                                        <td>{activity.is_open}</td>
                                                        <td class="table-action">
                                                            <a href="javascript: void(0);" class="action-icon text-success"> <i class="mdi mdi-eye"></i></a>
                                                            <a href="javascript: void(0);" class="action-icon text-primary"> <i class="mdi mdi-pencil"></i></a>
                                                            <a href="javascript: void(0);" class="action-icon text-danger"> <i class="mdi mdi-delete"></i></a>
                                                        </td>
                                                    </tr>""" for activity in activities]
                        )
                    # else:
                    #     return HttpResponse(
                    #         '<p class="text-center">Center aligned text on all viewport sizes.</p>'
                    #         )
                else:
                    # activities = Activity.objects.all()
                    return HttpResponse(
                        [f"""<tr>
                                                    <td>{activity.description}</td>
                                                    <td>{activity.aspecto}</td>
                                                    <td>{activity.is_open}</td>
                                                    <td class="table-action">
                                                        <a href="javascript: void(0);" class="action-icon text-success"> <i class="mdi mdi-eye"></i></a>
                                                        <a href="javascript: void(0);" class="action-icon text-primary"> <i class="mdi mdi-pencil"></i></a>
                                                        <a href="javascript: void(0);" class="action-icon text-danger"> <i class="mdi mdi-delete"></i></a>
                                                    </td>
                                                </tr>""" for activity in activities])
            
        context = {
            'actividades': activities,
            'flag': True
        }
        return render(request, 'actividad.html', context=context)
    else:
        return redirect('login')
    
    
def search_activities(request):
    search_input = request.GET.get('search_activities', None)
    if search_input:
        # print(request.path)
        
        patterns =Q(description__icontains=search_input) | Q(aspecto_id__in=Aspecto.objects.filter(name__icontains = search_input).values_list('id', flat=True))
        activities = Activity.objects.filter(patterns).all()
        
        return HttpResponse(
                [f"""<tr>
                                            <td>{activity.description}</td>
                                            <td>{activity.aspecto}</td>
                                            <td>{activity.is_open}</td>
                                            <td class="table-action">
                                                <a href="javascript: void(0);" class="action-icon text-success"> <i class="mdi mdi-eye"></i></a>
                                                <a href="javascript: void(0);" class="action-icon text-primary"> <i class="mdi mdi-pencil"></i></a>
                                                <a href="javascript: void(0);" class="action-icon text-danger"> <i class="mdi mdi-delete"></i></a>
                                            </td>
                                        </tr>""" for activity in activities]
            )
        # else:
        #     return HttpResponse(
        #         '<p class="text-center">Center aligned text on all viewport sizes.</p>'
        #         )
    else:
        activities = Activity.objects.all()
        return HttpResponse(
            [f"""<tr>
                                        <td>{activity.description}</td>
                                        <td>{activity.aspecto}</td>
                                        <td>{activity.is_open}</td>
                                        <td class="table-action">
                                            <a href="javascript: void(0);" class="action-icon text-success"> <i class="mdi mdi-eye"></i></a>
                                            <a href="javascript: void(0);" class="action-icon text-primary"> <i class="mdi mdi-pencil"></i></a>
                                            <a href="javascript: void(0);" class="action-icon text-danger"> <i class="mdi mdi-delete"></i></a>
                                        </td>
                                    </tr>""" for activity in activities])
        
# -------------- CRUD de Actividad ------------------------------------------
# Añadir Actividades
class AddActivityView(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = AddActivityView
    template_name = 'add_activity.html'

    # def form_valid(self, form):
    #     form.instance.created = timezone.now()
    #     form.instance.encargado = self.request.user
    #     return super().form_valid(form)
    
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
    
    
class EditActivityView(UpdateView):
    model = Activity
    form_class = EditActivityView
    template_name='edit_activity.html'
    
    # def form_valid(self, form):
    #     form.instance.updated = timezone.now()
    #     form.instance.autor = self.request.user
    #     return super().form_valid(form)
    
    
class DeleteActivityView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = "delete_activity.html"
    success_url = reverse_lazy('activities')
    
    
# -------------- (FIN) CRUD de Actividad ------------------------------------------
