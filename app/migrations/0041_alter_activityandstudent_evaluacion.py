# Generated by Django 4.1.4 on 2023-11-26 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_alter_activityandstudent_nombre_evento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityandstudent',
            name='evaluacion',
            field=models.CharField(blank=True, choices=[(1, 'Bien'), (2, 'Regular'), (3, 'Mal')], max_length=255, null=True),
        ),
    ]
