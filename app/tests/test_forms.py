from django.test import TestCase
from app.forms import RegisterForm
from django.contrib.auth.models import User


class RegisterFormTest(TestCase):

    def test_valid_form_data(self):
        """Корректные данные проходят валидацию"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123',
            'password2': 'securepassword123'
        }

        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        saved_user = User.objects.get(username='testuser')
        self.assertEqual(saved_user.email, 'test@example.com')

    def test_password_mismatch(self):
        """Разные пароли вызывают ошибку"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'differentpassword'
        }

        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

        error_messages = [str(error) for error in form.non_field_errors()]
        self.assertIn("Пароли не совпадают", error_messages)

    def test_required_fields(self):
        """Проверка обязательных полей"""
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password', form.errors)
        self.assertIn('password2', form.errors)
