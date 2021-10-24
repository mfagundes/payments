from django.test import TestCase
from model_mommy import mommy

from core.models import Profile

from django.contrib.auth import get_user_model


class ModelTestCase(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.default_user = self.user_model(
            email='user@user.com',
            username='user',
            first_name="Fulano",
            last_name='de Tal'
        )

    def test_model_profile(self):
        user = mommy.make('User')
        assert user.profile is not None
        # default user is Provider
        assert user.profile.profile_type_id == Profile.PROVIDER

    def test_email_login_default_profile(self):
        """
        User must login using email/password.
        """
        user = self.default_user
        user.set_password('pass')
        user.save()
        credentials = {'username': user.email, 'password': 'pass'}
        # user can login
        response = self.client.login(**credentials)
        self.assertTrue(response)

        # user can't access admin
        admin_resp = self.client.post('/admin', **credentials)
        self.assertEqual(301, admin_resp.status_code)

    def test_email_login_staff_profile(self):
        """
        User must login using email/password.
        """
        admin_user = self.user_model(
            email='user@user.com',
            username='user@user.com',
            first_name="Fulano",
            last_name='de Tal',
            is_staff=True
        )
        admin_user.is_staff = True
        admin_user.set_password('pass')
        admin_user.save()
        user_profile = Profile.objects.get(user=admin_user)
        user_profile.profile_type_id = 1
        user_profile.save()
        credentials = {'username': admin_user.email, 'password': 'pass'}

        # user can login
        response = self.client.login(**credentials)
        self.assertTrue(response)

        # user profile is staff
        saved_user = self.user_model.objects.get(email='user@user.com')
        self.assertEqual(1, saved_user.profile.profile_type_id)

        # user can access admin
        admin_resp = self.client.post('/admin/', **credentials)
        self.assertEqual(200, admin_resp.status_code)
