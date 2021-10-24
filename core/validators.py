from django.core.exceptions import ValidationError
from localflavor.br.validators import BRCNPJValidator

INVALID_CNPJS = [str(i) * 14 for i in range(10)]


def validate_cnpj(cnpj):
    if cnpj in INVALID_CNPJS:
        raise ValidationError({'cnpj': 'Número de CNPJ inválido'})
    validator = BRCNPJValidator()
    validator(cnpj)
