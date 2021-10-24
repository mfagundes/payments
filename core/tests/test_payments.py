import datetime

import pytz
from django.core.exceptions import ValidationError
from django.test import TestCase
from model_mommy import mommy

from core.models import Profile, Payment

from django.contrib.auth import get_user_model


class TestPayment(TestCase):
    """
    Test payment class
    """
    def setUp(self):
        self.user_model = get_user_model()
        self.provider = self.user_model(
            email='user@user.com',
            username='user',
            first_name="Fulano",
            last_name='de Tal'
        )
        self.provider.save()

        user_profile = Profile.objects.get(user=self.provider)
        user_profile.company_name = 'Empresa Ltda'
        user_profile.cnpj = '34135215000131'
        user_profile.save()

        self.payment = Payment(
            provider=self.provider,
            issue_date=datetime.datetime(2021, 6, 1, 15, 0, 0, tzinfo=pytz.timezone('America/Sao_Paulo')),
            due_date=datetime.date(2021, 11, 30),
            description="Descrição sucinta do objeto do pagamento",
            value=100.00
        )

    def test_payment_model(self):
        self.payment.save()
        payment = Payment.objects.get(pk=1)
        assert payment is not None
        assert payment.value == 100
