from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from .. import views
from django.contrib.auth.models import User
from ..forms import SignUpForm

class SignUpTest(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.get(url)
        self.view = resolve('/accounts/signup/')

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_signup_url_resolve_signup_view(self):
        self.assertEquals(self.view.func,views.signup)

    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')

    def test_contain_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form,SignUpForm)

    def test_form_inputs(self):
        self.assertContains(self.response,'<input',5)
        self.assertContains(self.response,'type="text"',1)
        self.assertContains(self.response,'type="email"',1)
        self.assertContains(self.response,'type="password"',2)



class SuccessfulSignUpTest(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        data = {
            'username':'john',
            'email':'john@doe.com',
            'password1':'abc123456',
            'password2':'abc123456'
        }
        self.response = self.client.post(url,data)
        self.home_url = reverse('home')

    def test_redirection(self):
        self.assertRedirects(self.response,self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTest(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.post(url,{})

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
