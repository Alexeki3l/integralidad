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
    if request.user.profile.rol_fac == 1:
        
        in_valida = False
        cadena=""
        
        activities = Activity.objects.all()
        
        act_and_student_filter = ActivityAndStudent.objects.filter(profile = request.user.profile, is_valid = False)
        
        if act_and_student_filter.count() > 0:
            for act_and_student in act_and_student_filter:
                cadena += f' {act_and_student.activity.name},'
                act_and_student.delete()
            in_valida = True
        cadena = cadena[:-1]
        
        context = {
            'activities':activities,
            'cadena': cadena,
            'in_valida': in_valida
        }
        return render(request, 'activity/activities.html', context=context)
    else:
        return redirect('list_roles', 1)

# -------------- CRUD de Actividad ------------------------------------------
# Crear Actividades
class AddActivityView(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = AddActivityView
    template_name = 'activity/add_activity.html'


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