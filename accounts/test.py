from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .views import *
import logging
logging.basicConfig(filename="./testing.log", level=logging.DEBUG)


class TestUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse("index")
        logging.info(resolve(url))
        self.assertEquals(resolve(url).func, index)
    def test_login_url_resolves(self):
        url = reverse("login")
        logging.info(resolve(url))
        self.assertEquals(resolve(url).func, login)
    def test_logout_url_resolves(self):
        url = reverse("logout")
        logging.info(resolve(url))
        self.assertEquals(resolve(url).func, logout)
