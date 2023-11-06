from django.urls import path
from django.contrib.auth import login, views as auth_views
from . import views

urlpatterns = [
    # ...
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="login.html"), name="cerrar_seccion"),
    
    path('update_data/', views.update_data, name='update_data'),
    # ...
]