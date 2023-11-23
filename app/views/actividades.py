from typing import Any
from django.shortcuts import render, redirect
from ..models import Activity, Aspecto, ActivityAndStudent, Asignatura
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..forms import AddActivityView, EditActivityView, AddProfileView, EditProfileView, EditActivityAndStudentView, AddActivityAndStudentView, MultimediaForm

from django.urls import reverse, reverse_lazy

from django.contrib import messages

from authentication.models import Profile
from multimedia.models import Multimedia

from app.metodos_personalizados.message import *

import math

def list_activities(request):
    activities = Activity.objects.all().order_by('-id')
    context = {
        'activities':activities
    }
    return render(request, 'activity/activities.html', context=context)

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


# Editar Actividades
class EditActivityView(CreateView):
    model = Activity
    form_class = EditActivityAndStudentView
    template_name='activity/edit_activity.html'
    
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


# ----------------------- TRATAMIENTO DE ERRORES -----------------------------

# Error 404
def custom_404(request, exception):
    return render(request, 'error/404.html', status=404)