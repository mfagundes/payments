# Generated by Django 3.2.8 on 2021-10-25 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentAdvance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Criado em')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('original_value', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Valor original')),
                ('original_due_date', models.DateField(verbose_name='Data original')),
                ('new_date', models.DateField(blank=True, null=True, verbose_name='Nova data')),
                ('new_value', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Novo Valor')),
                ('status', models.IntegerField(choices=[(1, 'Pendente'), (2, 'Aprovado'), (3, 'Negado')], default=1)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.payment', verbose_name='Pagamento')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Solicitado por')),
            ],
            options={
                'verbose_name': 'antecipação de pagamento',
                'verbose_name_plural': 'antecipações de pagamento',
            },
        ),
    ]
