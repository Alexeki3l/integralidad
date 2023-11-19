# Generated by Django 4.1.4 on 2023-11-17 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_activityandstudent_distincion_fututo_maestro_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asignatura',
            name='actividades',
        ),
        migrations.AddField(
            model_name='asignatura',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.activityandstudent'),
        ),
    ]