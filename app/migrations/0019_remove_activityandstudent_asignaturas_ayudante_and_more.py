# Generated by Django 4.1.4 on 2023-11-17 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_remove_activityandstudent_asignatura_ayudante'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityandstudent',
            name='asignaturas_ayudante',
        ),
        migrations.AddField(
            model_name='activityandstudent',
            name='asignaturas_ayudante',
            field=models.ManyToManyField(to='app.asignatura'),
        ),
    ]