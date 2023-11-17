from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib import messages

from django.http import HttpResponse
# Create your views here.

from .utils import populate_bd_with_excel_file

def login_view(request):
    if request.user.is_authenticated:
        return redirect('list_activities')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # El usuario ha iniciado sesión correctamente.
            # Puedes redirigirlo a la página que desees.
            return redirect('list_activities')  # Reemplaza 'home' con la URL a la que deseas redirigir.
        else:
            # El inicio de sesión falló. Muestra un mensaje de error.
            messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    # Redirige a la página que desees después del logout
    return redirect('login')  # Reemplaza 'nombre_de_la_ruta' con la ruta a la que deseas redirigir



def update_data(request):
    # response = HttpResponse('<h4>CARGAR LOS DATOS CON HTMX</h4><p>Actualizaremos los datos de usuarios</p>')
    populate_bd_with_excel_file()
    # return response
    return redirect('login')