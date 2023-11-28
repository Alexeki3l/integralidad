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
            rol = 'Profesores Guías'
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