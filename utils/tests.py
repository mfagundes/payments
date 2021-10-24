import datetime

import pytest
import pytz
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from model_mommy import mommy

from core.models import Profile, Payment
from . import create_logentry, calculate_discount


@pytest.mark.django_db
def test_create_logentry():
    user1 = mommy.make('User')
    user2 = mommy.make('User')

    assert not LogEntry.objects.all()

    create_logentry(creator=user1, object=user2)

    assert LogEntry.objects.all()
    logentry = LogEntry.objects.get(
        user=user1, object_id=user2.id, object_repr=str(user2), action_flag=ADDITION)
    assert logentry.change_message == 'Adicionado.'

    create_logentry(creator=user1, object=user2, is_change=True, message='Teste')
    logentry = LogEntry.objects.get(
        user=user1, object_id=user2.id, object_repr=str(user2), action_flag=CHANGE)
    assert logentry.change_message == 'Teste'


@pytest.fixture
def provider():
    user = mommy.make('User')
    user_profile = Profile.objects.get(user=user)
    user_profile.company_name = 'Empresa Ltda'
    user_profile.cnpj = '34135215000131'
    user_profile.save()
    return user


@pytest.mark.django_db
def test_calculate_discount(provider):
    payment = Payment(
        provider=provider,
        issue_date=datetime.datetime(2019, 10, 1, 15, 0, 0, tzinfo=pytz.timezone('America/Sao_Paulo')),
        due_date=datetime.date(2019, 10, 1),
        description="Descrição sucinta do objeto do pagamento",
        value=1000.00
    )

    new_date = datetime.date(2019, 9, 15)  # 16 days of difference to use example provided
    new_value = calculate_discount(payment.value, payment.due_date, new_date)
    assert new_value == 984.00


@pytest.mark.django_db
def test_calculate_discount_2(provider):
    payment = Payment(
        provider=provider,
        issue_date=datetime.datetime(2021, 6, 1, 15, 0, 0, tzinfo=pytz.timezone('America/Sao_Paulo')),
        due_date=datetime.date(2021, 11, 30),
        description="Descrição sucinta do objeto do pagamento",
        value=1450.32
    )

    new_date = datetime.date(2021, 10, 31)  # 30 days of difference
    new_value = calculate_discount(payment.value, payment.due_date, new_date)
    assert new_value == 1406.81
