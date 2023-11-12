# from matplotlib import widgets
# from blog.models import Post
from .models import Activity
from authentication.models import Profile

from . import forms
from django import forms

class AddActivityView(forms.ModelForm):
    class Meta:
        model  = Activity  
        fields = ('description','month','weight','is_open','aspecto',)
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
        fields = ('description','month','weight','is_open','aspecto',)
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