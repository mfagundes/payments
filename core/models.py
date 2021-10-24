from django.db import models
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

    def __str__(self):
        return "perfil do usuário {}".format(self.user)

