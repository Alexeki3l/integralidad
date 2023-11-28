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

from app.utils import crear_objeto_activity_and_student, if_cadena_empty, generar_parrafo, exportar_pdf, return_dict_integrality

from django.contrib import messages

from authentication.models import Profile
from multimedia.models import Multimedia

from app.metodos_personalizados.message import *

import math


def caracterizacion(request):
    perfil = request.user.profile
    
    dict_integral, dict_integral_pdf, list_parrafo = return_dict_integrality(request, perfil)
    
    print(request.path)
    if request.path == "/caracterizacion":
        context={
            'parrafo_primer_anno':list_parrafo[0],
            'parrafo_segundo_anno':list_parrafo[1],
            'parrafo_tercer_anno':list_parrafo[2],
            'parrafo_cuarto_anno':list_parrafo[3],
        }
        return render(request, 'caracterizacion/caracterizacion.html', context)
    
    elif request.path == "/caracterizacion/exportar_pdf":
        context={
            'parrafo_integral':dict_integral,
            'profile':perfil,
        }
        name_pdf = f'evaluacion_integral_{perfil.user.first_name.lower()}'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{name_pdf}.pdf"'
        
        exportar_pdf(dict_integral_pdf, perfil, response, request)
        
        return response
    else:
        context={
            'parrafo_integral':dict_integral,
            'profile':perfil,
        }
        return render(request, 'caracterizacion/evaluacion_integral.html', context)
    

def evaluacion_integral_student(request, pk_student):
    
    perfil = Profile.objects.get(id = pk_student)
    
    dict_integral, _, _ = return_dict_integrality(request, perfil)
    
    context={
            'parrafo_integral':dict_integral,
            'profile':perfil,
        }
    return render(request, 'caracterizacion/evaluacion_integral_para_profesores.html', context)

def exportar_pdf_student(request, pk_student):
    
    perfil = Profile.objects.get(id = pk_student)
    
    dict_integral, dict_integral_pdf, _ = return_dict_integrality(request, perfil)
    
    context={
            'parrafo_integral':dict_integral,
            'profile':perfil,
        }
    name_pdf = f'evaluacion_integral_{perfil.user.first_name.lower()}'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{name_pdf}.pdf"'
        
    exportar_pdf(dict_integral_pdf, perfil, response, request)
        
    return response