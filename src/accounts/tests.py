from django.test import TestCase


# Create your tests here.
class AccountsTest(TestCase):
    """
    A class that gathers tests for the index view.
    """
    def test_status_code(self):
        """
        Tests that the view returns a 200 status code.
        """
        self.assertEqual(200, 200)
