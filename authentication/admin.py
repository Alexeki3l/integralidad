from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('user', 'rol_fac', 'rol_universitario', 'solapin' , 'grupo', 'academy_year')

# Registra el modelo en el panel de administración con la configuración personalizada
admin.site.register(Profile, ProfileAdmin)
