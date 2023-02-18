from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from .views import *
import logging
logging.basicConfig(filename="./testing.log", level=logging.DEBUG)
from django.utils import timezone


"""

The following class TestUrlsAccounts is focused on testing URL paths

"""

class TestUrlsAccounts(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse("index")
        logging.info(f"{resolve(url)}, TIME : {timezone.now()}")
        self.assertEquals(resolve(url).func, index)

    def test_register_url_resolves(self):
        url = reverse("register")
        logging.info(f"{resolve(url)}, TIME : {timezone.now()}")
        self.assertEquals(resolve(url).func, register)

    def test_login_url_resolves(self):
        url = reverse("login")
        logging.info(f"{resolve(url)}, TIME : {timezone.now()}")
        self.assertEquals(resolve(url).func, login)

    def test_logout_url_resolves(self):
        url = reverse("logout")
        logging.info(f"{resolve(url)}, TIME : {timezone.now()}")
        self.assertEquals(resolve(url).func, logout)


""""

The following class TestRegister is focused on testing the accounts.views.register view
which is the user's ability to register an account in different scenarios.

The class TestLogin is focused on testing the accounts.views.login view
which is the user's ability to login.

"""

class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.user={
            'first_name' : 'John',
            'last_name' : 'Doe',
            'email':'testemail@gmail.com',
            'username':'username',
            'password':'password',
            'password2' : 'password'
       
        }
        self.user_short_password={
            'first_name' : 'John',
            'last_name' : 'Doe',
            'email':'testemail@gmail.com',
            'username':'username',
            'password':'tes',
            'password2':'tes',

        }
        self.user_unmatching_password={
            'first_name' : 'John',
            'last_name' : 'Doe',
            'email':'testemail@gmail.com',
            'username':'username',
            'password':'teslatt',
            'password2':'teslatto',
   
        }

        self.user_invalid_email={
            'first_name' : 'John',
            'last_name' : 'Doe',
            'email':'test.com',
            'username':'username',
            'password':'teslatt',
            'password2':'teslatto',
        }
        return super().setUp()


class TestRegister(BaseTest):
    def test_can_view_page_correctly(self):
       response=self.client.get(self.register_url)
       self.assertEqual(response.status_code,200)
       self.assertTemplateUsed(response,'accounts/index.html')

    def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'coreapp/dashboard.html')

    def test_cannot_register_user_with_unmatching_passwords(self):
            response=self.client.post(self.register_url,self.user_unmatching_password,format='text/html')
            self.assertNotEquals(response.status_code,200)
            self.assertTemplateNotUsed(response)

    def test_cannot_register_user_with_invalid_email(self):
            response=self.client.post(self.register_url,self.user_invalid_email,format='text/html')
            self.assertNotEquals(response.status_code,200)
            self.assertTemplateNotUsed(response)

    def test_cannot_register_user_with_taken_email(self):
            self.client.post(self.register_url,self.user,format='text/html')
            response=self.client.post(self.register_url,self.user,format='text/html')
            self.assertNotEquals(response.status_code,200)
            self.assertTemplateNotUsed(response)



# No non default models to test within accounts app

# No forms to test within accounts app