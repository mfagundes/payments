from django.test import TestCase
from django.shortcuts import resolve_url as r


class TestCoreViews(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('home'))

    def test_get(self):
        """Get / must return status_code 200"""
        self.assertEqual(200, self.resp.status_code)

    # def test_template(self):
    #     """
    #     This test is failing when running all tests, despite the fact that it passes when running alone
    #     AssertionError: No templates used to render the response
    #
    #     Must use index.html
    #     """
    #     self.assertTemplateUsed(self.resp, 'index.html')
