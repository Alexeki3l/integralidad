from django.db import models
from authentication.models import Profile
from django.contrib.auth.models import User
# Create your models here.

class Aspecto(models.Model):
    name = models.CharField(max_length=1500)
    
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Activity(models.Model):
    MONTHS = (
        (0, '--'),
        (1, 'enero'),
        (2, 'febrero'),
        (3, 'marzo'),
        (4, 'abril'),
        (5, 'mayo'),
        (6, 'junio'),
        (7, 'julio'),
        (8, 'agosto'),
        (9, 'septiembre'),
        (10, 'octubre'),
        (11, 'noviembre'),
        (12, 'diciembre'),
    )
    
    
    description = models.CharField(max_length=2500, null=True, blank=True)
    month =  models.IntegerField(choices=MONTHS, default=0, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    is_open = models.BooleanField(default=True, null=True, blank=True)
    aspecto = models.ForeignKey(Aspecto, on_delete=models.CASCADE, null=True, blank=True)
    
    profiles = models.ManyToManyField(Profile, through="ActivityAndStudent")
    
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
    
class ActivityAndStudent(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=True, null=True, blank=True)
    
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.description} {self.profile.user.first_name}'

class Caracterizacion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    fac = models.CharField(max_length=4)
    in_production = models.CharField(max_length=1)
    is_investigation = models.CharField(max_length=1)
    
    deporte = models.CharField(max_length=1)
    guardia = models.CharField(max_length=1)
    cultura = models.CharField(max_length=1)
    residencia = models.CharField(max_length=1)
    tsu = models.CharField(max_length=1)
    
    feu_ujc = models.CharField(max_length=1)
    premio_mella = models.BooleanField(default=False)
    titulo_oro = models.BooleanField(default=False)
    #medidas disciplinarias
    menos_graves = models.IntegerField(default=0)
    graves = models.IntegerField(default=0)
    muy_graves = models.IntegerField(default=0)
    
    is_repitente = models.BooleanField(default=False)
    arrastre = models.IntegerField(default=0)
    mundial = models.IntegerField(default=0)
    
    index_academico = models.FloatField(default=0)
    other_indicator = models.FloatField(default=0)
    valor_final = models.FloatField(default=0)


class Group(models.Model):
    name = models.CharField(max_length=4)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)