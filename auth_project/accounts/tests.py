from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
User = get_user_model()


class AuthTests(TestCase):
    def test_login_required_home_page(self):
        """Защищенная страница недоступна без входа — редирект на логин."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_signup_page_shows_form(self):
        """Страница регистрации содержит поля логина и пароля."""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password1"')
        self.assertContains(response, 'name="password2"')

    def test_user_can_register(self):
        """Пользователь может зарегистрироваться."""
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'password1': 'StrongPass!234',
            'password2': 'StrongPass!234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_all_flow(self):
        """Полный цикл: регистрация -> вход -> защищенная страница -> выход."""
        User.objects.create_user(
            username='test_user_1', password='StrongR@ssw0rd')
        # login
        responce = self.client.post(
            reverse('login'),
            {'username': 'test_user_1',
             'password': 'StrongR@ssw0rd'
             },
        )

        self.assertEqual(responce.status_code, 302)
        # Защищенная страница доступна
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Выход
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        # После выхода страница недоступна
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
