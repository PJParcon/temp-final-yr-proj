from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class RegistrationTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:register')
        self.data = {
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'Test-Password-123!',
            'password2': 'Test-Password-123!',
        }

    def test_registration_page_displays_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="password1"')
        self.assertContains(response, 'name="password2"')

    def test_valid_submission_creates_user_with_hashed_password(self):
        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, reverse('accounts:registration_complete'))
        user = get_user_model().objects.get(username='newuser')
        self.assertTrue(user.check_password(self.data['password1']))
        self.assertNotEqual(user.password, self.data['password1'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_first_and_last_name_are_saved_and_displayed_on_profile(self):
        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, reverse('accounts:registration_complete'))
        user = get_user_model().objects.get(username='newuser')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.client.force_login(user)
        response = self.client.get(reverse('accounts:profile'))
        self.assertContains(response, 'John')
        self.assertContains(response, 'Doe')

    def test_invalid_submissions_do_not_create_users(self):
        for changes, field in [
            ({'username': ''}, 'username'),
            ({'first_name': ''}, 'first_name'),
            ({'last_name': ''}, 'last_name'),
            ({'password2': 'different-password'}, 'password2'),
            ({'password1': '123', 'password2': '123'}, 'password2'),
        ]:
            with self.subTest(changes=changes):
                response = self.client.post(self.url, self.data | changes)
                self.assertEqual(response.status_code, 200)
                self.assertIn(field, response.context['form'].errors)
                self.assertEqual(get_user_model().objects.count(), 0)

    def test_duplicate_username_is_rejected(self):
        get_user_model().objects.create_user(username='newuser')
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.context['form'].errors)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_post_requires_csrf_token(self):
        response = Client(enforce_csrf_checks=True).post(self.url, self.data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(get_user_model().objects.exists())
