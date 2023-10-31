# Generated by Django 4.1.4 on 2023-10-31 02:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol_fac', models.IntegerField(choices=[(1, 'estudiante'), (2, 'profesor guia'), (3, 'profesor de año'), (4, 'vicedecana/o')], default=1, null=True)),
                ('rol_universitario', models.IntegerField(choices=[(1, 'estudiante'), (2, 'profesor'), (3, 'vicedecana/o')], default=1, null=True)),
                ('solapin', models.CharField(max_length=7, null=True)),
                ('grupo', models.CharField(max_length=7, null=True)),
                ('carrera', models.CharField(max_length=100, null=True)),
                ('provincia', models.CharField(max_length=50, null=True)),
                ('municipio', models.CharField(max_length=50, null=True)),
                ('ci', models.CharField(max_length=11, null=True)),
                ('id_exp', models.CharField(max_length=7, null=True)),
                ('academy_year', models.IntegerField(default=None, null=True)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
