# Generated by Django 4.1.4 on 2023-11-17 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_asignatura_actividades'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityandstudent',
            name='distincion_fututo_maestro',
            field=models.BooleanField(default=False, help_text='Este se refiere a la distincion del Futuro Maestro'),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='distincion_joven',
            field=models.BooleanField(default=False, help_text='Este campo se refiere a la distinsion Joven 20 Aniversario de la FEU'),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='distincion_marzo',
            field=models.BooleanField(default=False, help_text='Este se refiere a la distincion 13 de Marzo'),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='es_feu',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='es_ujc',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='grupo_edu_amor',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='has_investigacion',
            field=models.BooleanField(default=False, help_text='Si pertence o no a una linea de investigacion'),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='has_publicacion',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='has_roles',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='is_ayudante',
            field=models.BooleanField(default=False, help_text="Este campo se refiere a que si el alumno fue 'alumno ayudante'"),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='is_valid',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='with_arrastres',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='with_mundiales',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activityandstudent',
            name='with_repitencias',
            field=models.BooleanField(default=False),
        ),
    ]