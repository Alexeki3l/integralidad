# Generated by Django 4.1.4 on 2023-11-21 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_activityandstudent_roles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityandstudent',
            name='organizacion',
        ),
        migrations.AddField(
            model_name='activityandstudent',
            name='is_feu',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='activityandstudent',
            name='is_ujc',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='nombre_evento',
            field=models.IntegerField(blank=True, choices=[(1, 'Forum de Historia'), (2, 'Seminario Juvenil MArtiano'), (3, 'Olimpiada de Idiomas'), (4, 'Jornada de Ingeniero en Ciencias Informaticas'), (5, 'Jornada Cientifica Estudiantil'), (6, 'Peña Tecnologica')], null=True),
        ),
    ]
