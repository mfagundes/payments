import datetime

from django.core.exceptions import ValidationError
from django.db import models

from core.errors import CNPJException
from core.validators import validate_cnpj
from utils import calculate_discount
from utils.models import Base
from django.contrib.auth.models import User


class Profile(Base):
    """
    Profile must be Staff (has access to admin) or Provider (access only the API endpoints
    Default user must have Provider profile
    """
    STAFF = 1
    PROVIDER = 2
    PROFILE_NAME_OPTIONS = (
        (STAFF, 'Staff'),
        (PROVIDER, 'Provider')
    )

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_type_id = models.IntegerField('Perfil', default=PROVIDER, choices=PROFILE_NAME_OPTIONS)  # default is Provider
    company_name = models.CharField('Razão Social', max_length=100, null=True)
    cnpj = models.CharField('CNPJ', max_length=14, unique=True, null=True, help_text='Apenas números')

    def __str__(self):
        return "perfil do usuário {}".format(self.user)

    def clean(self):
        if self.cnpj:
            validate_cnpj(self.cnpj)

    def save(self, *args, **kwargs):
        try:
            self.clean()
        except CNPJException:
            pass
        super(Profile, self).save()


class Payment(Base):
    provider = models.ForeignKey(User, verbose_name='fornecedor', on_delete=models.CASCADE)
    issue_date = models.DateTimeField('Data de emissão')
    due_date = models.DateField('Data de vencimento')
    description = models.CharField('Descrição', max_length=255, null=True, blank=True)
    value = models.DecimalField('Valor', max_digits=9, decimal_places=2)  # supports up to 9,999,999.99

    class Meta:
        verbose_name = 'pagamento'
        verbose_name_plural = 'pagamentos'
        ordering = ('-due_date',)

    def __str__(self):
        due_date = self.due_date.strftime("%d/%m/%Y")
        return f"Pagamento de {self.value} do {self.provider.profile.company_name}, vencimento em {due_date}"


class PaymentAdvance(Base):
    PENDING = 1
    APPROVED = 2
    DENIED = 3
    ADVANCE_STATUS_OPTIONS = (
        (PENDING, 'Pendente'),
        (APPROVED, 'Aprovado'),
        (DENIED, 'Negado')
    )
    payment = models.ForeignKey(Payment, verbose_name='Pagamento', on_delete=models.CASCADE)
    original_value = models.DecimalField('Valor original', max_digits=9, decimal_places=2, null=True, blank=True)
    original_due_date = models.DateField('Data original')
    new_date = models.DateField('Nova data', null=True, blank=True)
    new_value = models.DecimalField('Novo Valor', max_digits=9, decimal_places=2)
    status = models.IntegerField(default=PENDING, choices=ADVANCE_STATUS_OPTIONS)
    requested_by = models.ForeignKey(User, verbose_name='Solicitado por', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'antecipação de pagamento'
        verbose_name_plural = 'antecipações de pagamento'

    def __str__(self):
        return f"Antecipação do pagamento {self.payment.id}"

    def clean(self):
        if self.payment.due_date <= datetime.date.today():
            raise ValidationError({'new_date': "Pagamento já vencido"})

    def save(self, *args, **kwargs):
        try:
            self.clean()
            self.original_due_date = self.payment.due_date
            self.original_value = self.payment.value
            self.new_value = calculate_discount(self.payment.value, self.payment.due_date, self.new_date)
        except ValidationError:
            pass
        super(PaymentAdvance, self).save(*args, **kwargs)
