# Generated by Django 4.1.4 on 2023-11-17 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_asignatura_actividades'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignatura',
            name='actividades',
            field=models.ManyToManyField(blank=True, to='app.activityandstudent'),
        ),
    ]
