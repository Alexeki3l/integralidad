from django.shortcuts import render, redirect
from .models import Activity

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        actividades = Activity.objects.all()
        context = {
            'actividades': actividades
        }
        
        return render(request, 'actividad.html', context=context)
    else:
        return redirect('login')
