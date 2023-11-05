from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('activities_htmx')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # El usuario ha iniciado sesión correctamente.
            # Puedes redirigirlo a la página que desees.
            return redirect('activities_htmx')  # Reemplaza 'home' con la URL a la que deseas redirigir.
        else:
            # El inicio de sesión falló. Muestra un mensaje de error.
            messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')

    return render(request, 'login.html')