# Generated by Django 4.1.4 on 2023-11-21 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_remove_activityandstudent_organizacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityandstudent',
            name='actividad_participado',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='activityandstudent',
            name='is_miembro',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='activityandstudent',
            name='nombre_catedra',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
