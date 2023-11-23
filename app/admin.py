from django.contrib import admin
from .models import Activity, Aspecto, ActivityAndStudent, Asignatura

class ActivityAdmin(admin.ModelAdmin):
    
    list_display = ('name','aspecto',)

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Aspecto)
admin.site.register(ActivityAndStudent)
admin.site.register(Asignatura)


# Register your models here.
