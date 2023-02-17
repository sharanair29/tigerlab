from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .views import *

class TestUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse("index")
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)
    def test_login_url_resolves(self):
        url = reverse("login")
        print(resolve(url))
        self.assertEquals(resolve(url).func, login)
    def test_logout_url_resolves(self):
        url = reverse("logout")
        print(resolve(url))
        self.assertEquals(resolve(url).func, logout)
