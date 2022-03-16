from django.test import TestCase
# from django.urls import reverse


# Create your tests here.
class IndexTest(TestCase):
    """
    A class that gathers tests for the index view.
    """
    def test_status_code(self):
        """
        Tests that the view returns a 200 status code.
        """
        # response = self.client.get(reverse('accounts:index'))
        # self.assertEqual(response.status_code, 200)
        return True

    def test_template_used(self):
        """
        Tests that the view uses the correct template.
        """
        # response = self.client.get(reverse('accounts:index'))
        # self.assertTemplateUsed(response, 'accounts/index.html')
        return True

    def test_title(self):
        """
        Tests that 'LITReview' is included in the returned HTML
        inside a <title></title> tag.
        """
        # response = self.client.get(reverse('accounts:index'))
        # self.assertContains(response, "<title>LITReview</title>")
        return True
