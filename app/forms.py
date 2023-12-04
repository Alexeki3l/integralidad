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
            'file':forms.FileInput(attrs={'class': 'form-control'}),
            
            'is_feu':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'is_ujc':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nivel':forms.Select(attrs={'class':'form-control'}),
            'cargo_feu':forms.Select(attrs={'class':'form-control'}),
            'cargo_ujc':forms.Select(attrs={'class':'form-control'}),
            
            'evaluacion':forms.Select(attrs={'class':'form-control'}),
            
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$", 'title':"Debe empezar con letra inicial mayuscula."}),
            'distincion_marzo':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'distincion_fututo_maestro':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'distincion_joven':forms.CheckboxInput(attrs={'class':'form-check-input'}),

            'is_ayudante':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'is_evento':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_evento':forms.SelectMultiple(attrs={'class':'form-control'}),
            'nombre_sub_evento':forms.Select(attrs={'class':'form-control'}),
            'es_colateral':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_evento_colateral':forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'nivel':forms.SelectMultiple(attrs={'class':'form-control'}),
            'result':forms.SelectMultiple(attrs={'class':'form-control'}),
            
            'has_roles':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'roles':forms.SelectMultiple(attrs={'class':'form-control'}),
            'nivel_alcanzado':forms.Select(attrs={'class':'form-control'}),
            
            'has_investigacion':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'participacion':forms.Select(attrs={'class':'form-control'}),
            'nivel_evento':forms.Select(attrs={'class':'form-control'}),
            
            'has_publicacion':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_publicacion': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'nivel_autor':forms.Select(attrs={'class':'form-control'}),
            'nivel_publicacion':forms.Select(attrs={'class':'form-control'}),
            
            'where_pid': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'rol': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'actividades_pid':forms.Select(attrs={'class':'form-control'}),
            
            'grupo_edu_amor':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            
            'with_arrastres':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'with_mundiales':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'with_repitencias':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'cantidad_repitencias':forms.NumberInput(attrs={'class':'form-control'}),
            
            'other_reconocimiento':forms.Textarea(attrs={'class':'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'is_miembro':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_catedra': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'actividad_participado': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'actividades_participacion_actos_matutinos':forms.Textarea(attrs={'class':'form-control', 
                                                                            'placeholder':"Escribe actos y matutinos que hallas participado.", 'pattern':"^[A-Z][a-z]*$"}),
            
            'if_participacion_festivales':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'manifestacion_festivales': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),            
            'nivel_artista_aficionado':forms.Select(attrs={'class':'form-control'}),
            'premio_artista_aficionado':forms.Select(attrs={'class':'form-control'}),

            'nombre_actividad_facultad': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'manifestacion_actividad_facultad': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'lugar_dnd_realizo': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'if_jjmm':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'deporte':forms.Select(attrs={'class':'form-control'}),
            'resultado_deporte':forms.SelectMultiple(attrs={'class':'form-control'}),
            'lugar':forms.Select(attrs={'class':'form-control'}),
            
            'if_copas_mundialess':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_evento_copas_mundiales': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'resultado_copas_mundiales':forms.Select(attrs={'class':'form-control'}),
            'lugar_copas_mundiales': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'if_marabana':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_evento_marabana':forms.Select(attrs={'class':'form-control'}),
            'resultado_evento_marabana':forms.Select(attrs={'class':'form-control'}),

            'evaluacion_cuarteleria':forms.Select(attrs={'class':'form-control'}),

            'responsabilidad':forms.Select(attrs={'class':'form-control'}),
            
            'if_senalamiento_residencia':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            
            'total_ausencias':forms.NumberInput(attrs={'class':'form-control'}),
            'total_ausencias_justificadas':forms.NumberInput(attrs={'class':'form-control'}),
            'total_ausencias_injustificadas':forms.NumberInput(attrs={'class':'form-control'}),
            'total_recuperadas':forms.NumberInput(attrs={'class':'form-control'}),
            
            'if_senalamiento_guardia_estudiantil':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'cantidad_senalamiento_guardia_estudiantil':forms.NumberInput(attrs={'class':'form-control'}),
            
            'if_actividades_limpieza_areas_comunes':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_actividades_limpieza_areas_comunes': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'mes': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'resultado_actividades_limpieza_areas_comunes': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'if_bk_mas_bonita':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            
            'reconocimiento_otorgado_por': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'sanciones_o_medida': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'motivo_sancion': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'senalamiento_curso': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'nombre_distincion': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'organismo_otorga_distincion': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'nombre_mision': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'funsion_desempenada': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'proceso':forms.Select(attrs={'class':'form-control'}),
            
            'asignaturas_ayudante':forms.SelectMultiple(attrs={'class':'form-control'}),
            
            'comite_base': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            
        }


class AddActivityView(forms.ModelForm):
    class Meta:
        model  = Activity  
        fields = ('name','is_open','aspecto',)
        
        
        
class EditActivityView(forms.ModelForm):
    class Meta:
        model  = Activity  
        fields = ('name','is_open','aspecto',)
        
        
class EditActivityAndStudentView(forms.ModelForm):
    class Meta:
        model  = ActivityAndStudent
        # fields = ('is_ayudante','year','evaluacion','asignaturas_ayudante','grupo_edu_amor','file',)
        fields = ('__all__')
        widgets={
            'file':forms.FileInput(attrs={'class': 'form-control'}),
            
            'is_feu':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'is_ujc':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nivel':forms.Select(attrs={'class':'form-control'}),
            'cargo_feu':forms.Select(attrs={'class':'form-control'}),
            'cargo_ujc':forms.Select(attrs={'class':'form-control'}),
            
            'evaluacion':forms.Select(attrs={'class':'form-control'}),
            
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'distincion_marzo':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'distincion_fututo_maestro':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'distincion_joven':forms.CheckboxInput(attrs={'class':'form-check-input'}),

            'is_ayudante':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'is_evento':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_evento':forms.SelectMultiple(attrs={'class':'form-control'}),
            'nombre_sub_evento':forms.Select(attrs={'class':'form-control'}),
            'es_colateral':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_evento_colateral':forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'nivel':forms.SelectMultiple(attrs={'class':'form-control'}),
            'result':forms.SelectMultiple(attrs={'class':'form-control'}),
            
            'has_roles':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'roles':forms.SelectMultiple(attrs={'class':'form-control'}),
            'nivel_alcanzado':forms.Select(attrs={'class':'form-control'}),
            
            'has_investigacion':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'participacion':forms.Select(attrs={'class':'form-control'}),
            'nivel_evento':forms.Select(attrs={'class':'form-control'}),
            
            'has_publicacion':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_publicacion': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'nivel_autor':forms.Select(attrs={'class':'form-control'}),
            'nivel_publicacion':forms.Select(attrs={'class':'form-control'}),
            
            'where_pid': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'rol': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'actividades_pid':forms.Select(attrs={'class':'form-control'}),
            
            'grupo_edu_amor':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            
            'with_arrastres':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'with_mundiales':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'with_repitencias':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'cantidad_repitencias':forms.NumberInput(attrs={'class':'form-control'}),
            
            'other_reconocimiento':forms.Textarea(attrs={'class':'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'is_miembro':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_catedra': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'actividad_participado': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'actividades_participacion_actos_matutinos':forms.Textarea(attrs={'class':'form-control', 
                                                                            'placeholder':"Escribe actos y matutinos que hallas participado.", 'pattern':"^[A-Z][a-z]*$"}),
            
            'if_participacion_festivales':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'manifestacion_festivales': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),            
            'nivel_artista_aficionado':forms.Select(attrs={'class':'form-control'}),
            'premio_artista_aficionado':forms.Select(attrs={'class':'form-control'}),

            'nombre_actividad_facultad': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'manifestacion_actividad_facultad': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'lugar_dnd_realizo': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'if_jjmm':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'deporte':forms.Select(attrs={'class':'form-control'}),
            'resultado_deporte':forms.SelectMultiple(attrs={'class':'form-control'}),
            'lugar':forms.Select(attrs={'class':'form-control'}),
            
            'if_copas_mundialess':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_evento_copas_mundiales': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'resultado_copas_mundiales':forms.Select(attrs={'class':'form-control'}),
            'lugar_copas_mundiales': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'if_marabana':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_evento_marabana':forms.Select(attrs={'class':'form-control'}),
            'resultado_evento_marabana':forms.Select(attrs={'class':'form-control'}),

            'evaluacion_cuarteleria':forms.Select(attrs={'class':'form-control'}),

            'responsabilidad':forms.Select(attrs={'class':'form-control'}),
            
            'if_senalamiento_residencia':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            
            'total_ausencias':forms.NumberInput(attrs={'class':'form-control'}),
            'total_ausencias_justificadas':forms.NumberInput(attrs={'class':'form-control'}),
            'total_ausencias_injustificadas':forms.NumberInput(attrs={'class':'form-control'}),
            'total_recuperadas':forms.NumberInput(attrs={'class':'form-control'}),
            
            'if_senalamiento_guardia_estudiantil':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'cantidad_senalamiento_guardia_estudiantil':forms.NumberInput(attrs={'class':'form-control'}),
            
            'if_actividades_limpieza_areas_comunes':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'nombre_actividades_limpieza_areas_comunes': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'mes': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'resultado_actividades_limpieza_areas_comunes': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'if_bk_mas_bonita':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            
            'reconocimiento_otorgado_por': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'sanciones_o_medida': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'motivo_sancion': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'senalamiento_curso': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'nombre_distincion': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'organismo_otorga_distincion': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'nombre_mision': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            'funsion_desempenada': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$"}),
            
            'proceso':forms.Select(attrs={'class':'form-control'}),
            
            'asignaturas_ayudante':forms.SelectMultiple(attrs={'class':'form-control'}),
            
            'comite_base': forms.TextInput(attrs={'class': 'form-control', 'pattern':"^[A-Z][a-z]*$" }),
            
            
        }



class AddProfileView(forms.ModelForm):
    class Meta:
        model  = Profile  
        # fields = ('description','month','weight','is_open','aspecto',)
        fields = ('__all__')
        
        
        
class EditProfileView(forms.ModelForm):
    class Meta:
        model  = Profile  
        # fields = ('description','month','weight','is_open','aspecto',)
        fields = ('__all__')
        