from django.contrib import admin
from .models import Profile

from django.utils.html import format_html

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('user', 'rol_fac', 'rol_universitario', 'solapin' , 'grupo', 'academy_year')
    
    # def imagen(self, obj):
    #     return format_html('<img src={} width="130" height="100" />', obj.image.url)

# Registra el modelo en el panel de administración con la configuración personalizada
admin.site.register(Profile, ProfileAdmin)
