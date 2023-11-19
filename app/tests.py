from django.test import TestCase
from .models import Activity, Aspecto

class PostModelTest(TestCase):
    def test_create_activity_better_case(self):
        # Crear un objeto Post para el mejor de los casos
        aspecto = Aspecto.objects.create(name = 'Investigativa')
        activity = Activity.objects.create(description="1ro de Mayo", 
                                           weight=2.0,
                                           aspecto = aspecto)

        # Comprobar que los campos del objeto son correctos
        self.assertEqual(activity.description, "1ro de Mayo")
        
        
        
    def test_create_activity_worst_case(self):
        # Crear un objeto Post para el mejor de los casos
        aspecto = Aspecto.objects.create(name = 'Investigativa')
        activity = Activity.objects.create(description="1ro de Mayo", 
                                           weight=2.0,
                                           aspecto = aspecto)

        # Comprobar que los campos del objeto no son correctos
        self.assertNotEqual(activity.description, "1ro de Junio")

