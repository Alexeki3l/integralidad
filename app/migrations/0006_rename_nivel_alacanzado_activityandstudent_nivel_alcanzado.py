# Generated by Django 4.1.4 on 2023-11-15 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_activityandstudent_cargo_feu_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activityandstudent',
            old_name='nivel_alacanzado',
            new_name='nivel_alcanzado',
        ),
    ]
