from django.test import TestCase
from .models import Activity

class PostModelTest(TestCase):
    def test_create_post(self):
        # Crear un objeto Post
        post = Activity.objects.create(description="1ro de Mayo")

        # Obtener el objeto Post de la base de datos
        saved_post = Activity.objects.get(id=post.id)

        # Comprobar que los campos del objeto son correctos
        self.assertEqual(saved_post.description, "1ro de Mayo")
        # self.assertEqual(saved_post.content, "Contenido de prueba")

