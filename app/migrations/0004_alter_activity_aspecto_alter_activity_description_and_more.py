# Generated by Django 4.1.4 on 2023-11-03 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_activity_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='aspecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.aspecto'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.CharField(max_length=2500),
        ),
        migrations.AlterField(
            model_name='activity',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='month',
            field=models.IntegerField(choices=[(0, '--'), (1, 'enero'), (2, 'febrero'), (3, 'marzo'), (4, 'abril'), (5, 'mayo'), (6, 'junio'), (7, 'julio'), (8, 'agosto'), (9, 'septiembre'), (10, 'octubre'), (11, 'noviembre'), (12, 'diciembre')], default=0),
        ),
        migrations.AlterField(
            model_name='activity',
            name='weight',
            field=models.FloatField(),
        ),
    ]
