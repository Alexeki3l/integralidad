from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
    TIPE_VALUES = (
        (1, 'estudiante'),
        (2, 'profesor guia'),
        (3, 'profesor de año'),
        (4, 'vicedecana/o'),
    )
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    rol  = models.IntegerField(choices=TIPE_VALUES, default=1)
    academy_year = models.IntegerField(max_length=1)
    

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user = instance)
        

post_save.connect(create_profile, sender = User)