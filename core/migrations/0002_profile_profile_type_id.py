# Generated by Django 3.2.8 on 2021-10-24 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_type_id',
            field=models.IntegerField(choices=[(1, 'Staff'), (2, 'Provider')], default=2, verbose_name='Perfil'),
        ),
    ]
