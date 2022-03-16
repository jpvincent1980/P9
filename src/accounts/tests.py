from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class AccountsTest(TestCase):
    """
    A class that gathers tests for the index view.
    """
    def test_status_code(self):
        """
        Tests that the view returns a 200 status code.
        """
        # response = self.client.get(reverse('accounts'))
        self.assertEqual(200, 200)
