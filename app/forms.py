# from matplotlib import widgets
# from blog.models import Post
from .models import Activity, ActivityAndStudent
from authentication.models import Profile

from . import forms
from django import forms


class AddActivityAndStudentView(forms.ModelForm):
    class Meta:
        model  = ActivityAndStudent
        # fields = ('name','is_open','aspecto',)
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