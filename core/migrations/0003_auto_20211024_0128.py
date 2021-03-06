# Generated by Django 3.2.8 on 2021-10-24 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_profile_profile_type_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cnpj',
            field=models.CharField(help_text='Apenas números', max_length=14, null=True, unique=True, verbose_name='CNPJ'),
        ),
        migrations.AddField(
            model_name='profile',
            name='company_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Razão Social'),
        ),
    ]
