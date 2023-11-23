# Generated by Django 4.1.4 on 2023-11-22 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_activityandstudent_evaluacion_cuarteleria_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityandstudent',
            name='evaluacion_cuarteleria',
            field=models.CharField(blank=True, choices=[(1, 'Excelente'), (2, 'Bien'), (3, 'Regular'), (4, 'Mal')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='nombre_evento_marabana',
            field=models.IntegerField(blank=True, choices=[(1, 'MaraCuba'), (2, 'MaraHabana'), (3, 'Cacahual'), (4, 'Maratón por el Día Olímpico'), (5, 'Maratón Terry Fox'), (6, 'Maratón 10 de Octubre')], null=True),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='resultado_copas_mundiales',
            field=models.CharField(blank=True, choices=[(1, 'Oro'), (2, 'Plata'), (3, 'Bronce'), (4, 'Participacion')], max_length=255, null=True),
        ),
    ]
