# Generated by Django 4.1.4 on 2023-11-26 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_remove_activityandstudent_if_participacion_actos_matutinos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityandstudent',
            name='deporte',
            field=models.CharField(blank=True, choices=[(1, 'Ajedrez'), (2, 'Atletismo'), (3, 'Carrera de Orientacion'), (4, 'Baloncesto'), (5, 'Balonmano'), (6, 'Boxeo'), (7, 'Futbol Sala'), (8, 'Futbol 11'), (9, 'Natacion'), (10, 'Tenis'), (11, 'Pelota'), (12, 'Softball'), (13, 'Voleyball'), (14, 'Voleyball Playa'), (15, 'Yudo'), (16, 'Karate'), (17, 'Taewondo'), (18, 'Taewondo'), (19, 'Cubalon'), (20, 'Maraton'), (21, 'DOTA')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='roles',
            field=models.IntegerField(blank=True, choices=[(1, 'Administrador'), (2, 'Analista'), (3, 'Programador'), (4, 'Jefe de Proyecto')], null=True),
        ),
    ]
