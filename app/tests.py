from django.test import TestCase
from .models import Activity, Aspecto, Integralidad, ActivityAndStudent
from authentication.models import Profile

from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


class InvalidarActividadViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.profile = Profile.objects.get(user=self.user)
        self.profile.rol_fac = 2
        self.profile.academy_year = 4
        self.profile.save()
        
        self.activity_and_student = ActivityAndStudent.objects.create(profile=self.profile, is_valid=True)

    def test_not_invalidar_actividad_view(self):
        """Cuando no desmarcamos el checkbox de validar"""
        url = reverse('invalidar_actividad', args=[self.activity_and_student.pk])  

        response = self.client.post(url, {'is_valid': 'on', 'csrfmiddlewaretoken': 'tu_token_csrf'})
        self.assertEqual(response.status_code, 302)
        
        self.activity_and_student.refresh_from_db()
        self.assertTrue(self.activity_and_student.is_valid)
        
    def test_invalidar_actividad_view(self):
        """Cuando no desmarcamos el checkbox de validar"""
        url = reverse('invalidar_actividad', args=[self.activity_and_student.pk])  

        response = self.client.post(url, {'is_valid': '', 'csrfmiddlewaretoken': 'tu_token_csrf'})
        self.assertEqual(response.status_code, 302)
        
        self.activity_and_student.refresh_from_db()
        self.assertFalse(self.activity_and_student.is_valid)
        
    def test_exportar_pdf_student_view(self):
        # Crea la URL de la vista
        url = reverse('exportar_pdf_student', args=[self.profile.pk])  # Ajusta según la URL de tu vista

        # Realiza una solicitud GET a la vista
        response = self.client.get(url)

        # Asegúrate de que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)

        # Verifica el tipo de contenido
        self.assertEqual(response['Content-Type'], 'application/pdf')

        # Verifica el encabezado de disposición de contenido
        expected_filename = f'evaluacion_integral_{self.user.first_name.lower()}.pdf'
        self.assertEqual(response['Content-Disposition'], f'attachment; filename="{expected_filename}"')
        
        
class AddActivityAndStudentViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.profile = Profile.objects.get(user=self.user)  
        self.profile.academy_year=4
        self.profile.save()
        self.aspecto = Aspecto.objects.create(name = 'Ejemplo')
        self.activity = Activity.objects.create(name='Actividad de ejemplo', id=15, aspecto = self.aspecto)

    def test_add_activity_and_student_view(self):
        
        self.client.force_login(self.user)

        url = reverse('add_activities_and_student', args=[self.activity.pk])  # Ajusta según la URL de tu vista

        response = self.client.post(url, {'other_reconocimiento': 'Ejemplo', 'csrfmiddlewaretoken': 'tu_token_csrf'})

        self.assertEqual(response.status_code, 200)

        self.assertIn('elemento_anadido', response.context)
        self.assertTrue(response.context['elemento_anadido'])
        self.assertIn('activities', response.context)
        self.assertIn('act_and_student_all', response.context)

        activity_and_student = ActivityAndStudent.objects.get(profile=self.profile, activity=self.activity)
        self.assertEqual(activity_and_student.other_reconocimiento, 'Ejemplo')



