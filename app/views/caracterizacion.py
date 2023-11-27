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

from app.utils import crear_objeto_activity_and_student, if_cadena_empty, generar_parrafo, exportar_pdf

from django.contrib import messages

from authentication.models import Profile
from multimedia.models import Multimedia

from app.metodos_personalizados.message import *

import math


def caracterizacion(request):
    perfil = request.user.profile
    
    parrafo_primer_anno = generar_parrafo(perfil, 1)
    parrafo_segundo_anno = generar_parrafo(perfil, 2)
    parrafo_tercer_anno = generar_parrafo(perfil, 3)
    parrafo_cuarto_anno = generar_parrafo(perfil, 4)
    
    if request.user.profile.academy_year == 4:
        dict_integral = {}
        for aspecto in Aspecto.objects.all():
            cadena_inv = ""
            try:
                cadena_inv += f"""<h5>Periodo de Primer Año</h5><p>{parrafo_primer_anno[f'{aspecto.name}']}</p>"""
            except:
                cadena_inv += ""
            try:
                cadena_inv += f"""<h5 class='text-mute'>Periodo de Segundo Año</h5><p>{parrafo_segundo_anno[f'{aspecto.name}']}</p>"""
            except:
                cadena_inv += ""
            try:
                cadena_inv += f"""<h5>Periodo de Tercer Año</h5><p>{parrafo_tercer_anno[f'{aspecto.name}']}</p>"""
            except:
                cadena_inv += ""
            try:
                cadena_inv += f"""<strong class='text-mute'>Periodo de Cuarto Año</strong><p>{parrafo_cuarto_anno[f'{aspecto.name}']}</p>"""
            except:
                cadena_inv += ""
            if cadena_inv != "":
                dict_integral[f'{aspecto.name}'] = cadena_inv
            else:
                continue
    
    print(request.path)
    if request.path == "/caracterizacion":
        context={
            'parrafo_primer_anno':parrafo_primer_anno,
            'parrafo_segundo_anno':parrafo_segundo_anno,
            'parrafo_tercer_anno':parrafo_tercer_anno,
            'parrafo_cuarto_anno':parrafo_cuarto_anno,
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
        
        exportar_pdf(dict_integral, perfil, response, request)
        
        return response
    else:
        context={
            'parrafo_integral':dict_integral,
            'profile':perfil,
        }
        return render(request, 'caracterizacion/evaluacion_integral.html', context)
    