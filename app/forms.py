# from matplotlib import widgets
# from blog.models import Post
from typing import Any
from .models import Activity, ActivityAndStudent, Asignatura
from authentication.models import Profile
from multimedia.models import Multimedia

from . import forms
from django import forms

class MultimediaForm(forms.ModelForm):
    class Meta:
        model = Multimedia
        fields = ['actividades','file'] 
        
# class EventoForm(forms.ModelForm):
#     class Meta:
#         model = Evento
#         fields = ('nombre_evento', 'nombre_sub_evento', 'es_colateral', 'nivel', 'result', 'actividades',)

class AddActivityAndStudentView(forms.ModelForm):
    file = forms.FileField(label='Selecciona un archivo')
    class Meta:
        model  = ActivityAndStudent
        # fields = ('is_ayudante','year','evaluacion','asignaturas_ayudante','grupo_edu_amor','file',)
        fields = ('__all__')
        widgets={
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'where_pid': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.TextInput(attrs={'class': 'form-control'}),
            'comite_base': forms.Textarea(attrs={'class': 'form-control'}),
            'roles':forms.SelectMultiple(attrs={'class':'form-control'}),
            'evaluacion':forms.Select(attrs={'class':'form-control'}),
            'nivel_alcanzado':forms.Select(attrs={'class':'form-control'}),
            'asignaturas_ayudante':forms.SelectMultiple(attrs={'class':'form-control'}),
            'actividades_pid':forms.Select(attrs={'class':'form-control'}),
            'nivel':forms.Select(attrs={'class':'form-control'}),
            'cargo_feu':forms.Select(attrs={'class':'form-control'}),
            'cargo_ujc':forms.Select(attrs={'class':'form-control'}),
            'is_ayudante':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'grupo_edu_amor':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'other_reconocimiento':forms.Textarea(attrs={'class':'form-control'}),
        #     'weight':forms.FloatField(attrs={'class':'form-control'}),
        #     'is_open':forms.BooleanField(attrs={'class':'form-control'}),
        #     'aspecto':forms.SelectMultiple(attrs={'class':'form-control'}),
        #     # 'precio':forms.FloatField(attrs={'class':'form-control'}),
        #     # 'image':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'image1':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'image2':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'description':forms.Textarea(attrs={'class':'form-control'}),
        #     # 'instock':forms.BooleanField(attrs={'class':'form-control'}),
        }
    # def save(self, commit=True):
    #     instance = super().save(commit)
    #     # set Car reverse foreign key from the Person model
    #     instance.asignaturas_set.add(self.cleaned_data['asignaturas'])
    #     return instance


class AddActivityView(forms.ModelForm):
    class Meta:
        model  = Activity  
        fields = ('name','is_open','aspecto',)
        # fields = ('__all__')
        # widgets={
        #     'description':forms.CharField(attrs={'class':'form-control'}),
        #     'month':forms.IntegerField(attrs={'class':'form-control'}),
        #     'weight':forms.FloatField(attrs={'class':'form-control'}),
        #     'is_open':forms.BooleanField(attrs={'class':'form-control'}),
        #     'aspecto':forms.SelectMultiple(attrs={'class':'form-control'}),
        #     # 'precio':forms.FloatField(attrs={'class':'form-control'}),
        #     # 'image':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'image1':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'image2':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'description':forms.Textarea(attrs={'class':'form-control'}),
        #     # 'instock':forms.BooleanField(attrs={'class':'form-control'}),
        # }
        
        
class EditActivityView(forms.ModelForm):
    class Meta:
        model  = Activity  
        fields = ('name','is_open','aspecto',)
        # fields = ('__all__')
        # widgets={
        #     'description':forms.CharField(attrs={'class':'form-control'}),
        #     'month':forms.IntegerField(attrs={'class':'form-control'}),
        #     'weight':forms.FloatField(attrs={'class':'form-control'}),
        #     'is_open':forms.BooleanField(attrs={'class':'form-control'}),
        #     'aspecto':forms.SelectMultiple(attrs={'class':'form-control'}),
        #     # 'precio':forms.FloatField(attrs={'class':'form-control'}),
        #     # 'image':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'image1':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'image2':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'description':forms.Textarea(attrs={'class':'form-control'}),
        #     # 'instock':forms.BooleanField(attrs={'class':'form-control'}),
        # }
        
class EditActivityAndStudentView(forms.ModelForm):
    class Meta:
        model  = ActivityAndStudent
        fields = ('comite_base','descripcion',)
        # fields = ('__all__')
        # widgets={
        #     'description':forms.CharField(attrs={'class':'form-control'}),
        #     'month':forms.IntegerField(attrs={'class':'form-control'}),
        #     'weight':forms.FloatField(attrs={'class':'form-control'}),
        #     'is_open':forms.BooleanField(attrs={'class':'form-control'}),
        #     'aspecto':forms.SelectMultiple(attrs={'class':'form-control'}),
        #     # 'precio':forms.FloatField(attrs={'class':'form-control'}),
        #     # 'image':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'image1':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'image2':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'description':forms.Textarea(attrs={'class':'form-control'}),
        #     # 'instock':forms.BooleanField(attrs={'class':'form-control'}),
        # }
        

# class EditActivityView(forms.ModelForm):
#     # Campos de ActivityAndStudent
#     campo_adicional_1 = forms.CharField(max_length=100, required=False)
#     campo_adicional_2 = forms.CharField(max_length=100, required=False)

#     class Meta:
#         model = Activity
#         fields = ('name', 'is_open', 'aspecto',)

#     def __init__(self, *args, **kwargs):
#         super(EditActivityView, self).__init__(*args, **kwargs)

#         # Si ya tienes una instancia de Activity, puedes establecer los valores iniciales
#         if self.instance:
#             # Obtener la instancia de ActivityAndStudent asociada (puede haber múltiples)
#             activity_and_student_instances = ActivityAndStudent.objects.filter(activity=self.instance)

#             # Puedes decidir qué hacer si hay múltiples instancias, aquí estoy tomando la primera
#             if activity_and_student_instances.exists():
#                 activity_and_student_instance = activity_and_student_instances.first()
#                 self.fields['campo_adicional_1'].initial = activity_and_student_instance.comite_base
#                 self.fields['campo_adicional_2'].initial = activity_and_student_instance.descripcion

#     def save(self, commit=True):
#         activity_instance = super(EditActivityView, self).save(commit)

#         # Guardar o actualizar instancias de ActivityAndStudent
#         activity_and_student_instances = ActivityAndStudent.objects.filter(activity=activity_instance)

#         if activity_and_student_instances.exists():
#             activity_and_student_instance = activity_and_student_instances.first()
#         else:
#             activity_and_student_instance = ActivityAndStudent(activity=activity_instance)

#         activity_and_student_instance.comite_base = self.cleaned_data['campo_adicional_1']
#         activity_and_student_instance.descripcion = self.cleaned_data['campo_adicional_2']
        
#         if commit:
#             activity_and_student_instance.save()

#         return activity_instance

        
# ---------------- ROLES --------------------

class AddProfileView(forms.ModelForm):
    class Meta:
        model  = Profile  
        # fields = ('description','month','weight','is_open','aspecto',)
        fields = ('__all__')
        # widgets={
        #     'description':forms.CharField(attrs={'class':'form-control'}),
        #     'month':forms.IntegerField(attrs={'class':'form-control'}),
        #     'weight':forms.FloatField(attrs={'class':'form-control'}),
        #     'is_open':forms.BooleanField(attrs={'class':'form-control'}),
        #     'aspecto':forms.SelectMultiple(attrs={'class':'form-control'}),
        #     # 'precio':forms.FloatField(attrs={'class':'form-control'}),
        #     # 'image':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'image1':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'image2':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'description':forms.Textarea(attrs={'class':'form-control'}),
        #     # 'instock':forms.BooleanField(attrs={'class':'form-control'}),
        # }
        
        
class EditProfileView(forms.ModelForm):
    class Meta:
        model  = Profile  
        # fields = ('description','month','weight','is_open','aspecto',)
        fields = ('__all__')
        # widgets={
        #     'description':forms.CharField(attrs={'class':'form-control'}),
        #     'month':forms.IntegerField(attrs={'class':'form-control'}),
        #     'weight':forms.FloatField(attrs={'class':'form-control'}),
        #     'is_open':forms.BooleanField(attrs={'class':'form-control'}),
        #     'aspecto':forms.SelectMultiple(attrs={'class':'form-control'}),
        #     # 'precio':forms.FloatField(attrs={'class':'form-control'}),
        #     # 'image':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'image1':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'image2':forms.ImageField(attrs={'class':'form-control'}),
        #     # 'description':forms.Textarea(attrs={'class':'form-control'}),
        #     # 'instock':forms.BooleanField(attrs={'class':'form-control'}),
        # }