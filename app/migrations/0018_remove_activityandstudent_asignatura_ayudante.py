# Generated by Django 4.1.4 on 2023-11-17 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_activityandstudent_asignaturas_ayudante'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityandstudent',
            name='asignatura_ayudante',
        ),
    ]
