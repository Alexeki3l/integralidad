# Generated by Django 4.1.4 on 2023-12-04 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_alter_integralidad_cultura_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='integralidad',
            name='was_generate',
            field=models.BooleanField(default=False),
        ),
    ]