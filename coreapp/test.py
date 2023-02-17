from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .views import *

import logging
logging.basicConfig(filename="./testing.log", level=logging.DEBUG)

class TestUrls(SimpleTestCase):
    """urls with no arguments within coreapp"""
    def test_coreapp_url_resolves(self):
        url = reverse("coreapp")
        logging.info(resolve(url))
        self.assertEquals(resolve(url).func, coreapp)
    def test_analytics_url_resolves(self):
        url = reverse("analytics")
        logging.info(resolve(url))
        self.assertEquals(resolve(url).func, analytics)
    def test_addobj_url_resolves(self):
        url = reverse("addobj")
        logging.info(resolve(url))
        self.assertEquals(resolve(url).func, addobj)
    def test_listteamscores_url_resolves(self):
        url = reverse("listteamscores")
        logging.info(resolve(url))
        self.assertEquals(resolve(url).func, listteamscores)
    """urls with arguments within coreapp"""
    def test_deleteobj_url_resolves(self):
        url = reverse("deleteobj", args=['some-pk'])
        logging.info(resolve(url))
        self.assertEquals(resolve(url).func, deleteobj)
    def test_edit_data_url_resolves(self):
        url = reverse("edit_data", args=['some-pk'])
        logging.info(resolve(url))
        self.assertEquals(resolve(url).func, edit_data)
    def test_deletefile_url_resolves(self):
        url = reverse("deletefile", args=['some-pk'])
        logging.info(resolve(url))
        self.assertEquals(resolve(url).func, deletefile)

