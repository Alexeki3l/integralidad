from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
    TIPE_VALUES_FAC = (
        (1, 'estudiante'),
        (2, 'profesor guia'),
        (3, 'profesor de año'),
        (4, 'vicedecana/o'),
    )
    TIPE_VALUES_UNIV = (
        (1, 'estudiante'),
        (2, 'profesor'),
        (3, 'vicedecana/o'),
    )
    
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    rol_fac  = models.IntegerField(choices=TIPE_VALUES_FAC, default=1, null=True, blank=True)
    rol_universitario  = models.IntegerField(choices=TIPE_VALUES_UNIV, default=1, null=True, blank=True)
    solapin  = models.CharField(max_length=7, null=True, blank=True)
    grupo  = models.CharField(max_length=7, null=True, blank=True)
    carrera = models.CharField(max_length=100, null=True, blank=True)
    provincia  = models.CharField(max_length=50, null=True, blank=True)
    municipio  = models.CharField(max_length=50, null=True, blank=True)
    ci = models.CharField(max_length=11, null=True, blank=True)
    id_exp = models.CharField(max_length=7, null=True, blank=True)
    academy_year = models.IntegerField(default=None, null=True, blank=True)
    
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user} -- {self.user.first_name} {self.user.last_name}'
    
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
    
# Creamos un Perfil cada vez que se cree un nuevo usuario
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user = instance)
        

post_save.connect(create_profile, sender = User)