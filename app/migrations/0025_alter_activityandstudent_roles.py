# Generated by Django 4.1.4 on 2023-11-20 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_rename_es_feu_activityandstudent_es_colateral_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityandstudent',
            name='roles',
            field=models.CharField(blank=True, choices=[(1, 'Administrador'), (2, 'Analista'), (3, 'Programador'), (4, 'Jefe de Proyecto')], max_length=255, null=True),
        ),
    ]
