import datetime

import pytz
from django.core.exceptions import ValidationError
from django.test import TestCase
from model_mommy import mommy

from core.models import Profile, Payment, PaymentAdvance

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
            issue_date=datetime.datetime(2022, 6, 1, 15, 0, 0, tzinfo=pytz.timezone('America/Sao_Paulo')),
            due_date=datetime.date(2022, 10, 1),
            description="Descrição sucinta do objeto do pagamento",
            value=1000.00
        )

        self.admin_user = self.user_model(
            email='admin@user.com',
            username='admin@user.com',
            first_name="Admin",
            last_name='Cliente',
            is_staff=True
        )
        self.admin_user.is_staff = True
        self.admin_user.set_password('pass')
        self.admin_user.save()
        user_profile = Profile.objects.get(user=self.admin_user)
        user_profile.profile_type_id = 1
        user_profile.save()

    def test_payment_model(self):
        self.payment.save()
        # as it is intended to allow multiple payments, changed to get the payment pk
        # from database based on the id from the saved payment
        payment = Payment.objects.get(pk=self.payment.pk)
        assert payment is not None
        assert payment.value == 1000

    def test_payment_advance_by_operator(self):
        self.payment.save()
        payment = Payment.objects.get(pk=self.payment.id)

        credentials = {'username': self.admin_user.email, 'password': 'pass'}
        response = self.client.login(**credentials)

        payment_advance = PaymentAdvance(
            payment=payment,
            original_value=payment.value,
            original_due_date=payment.due_date,
            new_date=datetime.date(2022, 9, 15),
            status=PaymentAdvance.PENDING,
            requested_by=self.admin_user
        )
        payment_advance.save()

        requested_advance = PaymentAdvance.objects.get(pk=payment_advance.id)
        assert payment_advance.__str__() == f"Antecipação do pagamento {requested_advance.payment.id}"
        assert payment_advance.new_value == 984.00

    def test_payment_advance_by_operator_overdue(self):
        overdue_payment = Payment(
            provider=self.provider,
            issue_date=datetime.datetime(2021, 6, 1, 15, 0, 0, tzinfo=pytz.timezone('America/Sao_Paulo')),
            due_date=datetime.date(2021, 10, 1),
            description="Descrição sucinta do objeto do pagamento",
            value=1000.00
        )
        overdue_payment.save()
        payment = Payment.objects.get(pk=overdue_payment.id)

        credentials = {'username': self.admin_user.email, 'password': 'pass'}
        response = self.client.login(**credentials)

        payment_advance = PaymentAdvance(
            payment=payment,
            original_value=payment.value,
            original_due_date=payment.due_date,
            new_date=datetime.date(2021, 10, 31),
            status=PaymentAdvance.PENDING,
            requested_by=self.admin_user
        )
        with self.assertRaises(ValidationError):
            payment_advance.clean()
