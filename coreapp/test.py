from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .views import *

class TestUrls(SimpleTestCase):
    def test_coreapp_url_resolves(self):
        url = reverse("coreapp")
        print(resolve(url))
        self.assertEquals(resolve(url).func, coreapp)
    def test_analytics_url_resolves(self):
        url = reverse("analytics")
        print(resolve(url))
        self.assertEquals(resolve(url).func, analytics)
    def test_addobj_url_resolves(self):
        url = reverse("addobj")
        print(resolve(url))
        self.assertEquals(resolve(url).func, addobj)
    def test_listteamscores_url_resolves(self):
        url = reverse("listteamscores")
        print(resolve(url))
        self.assertEquals(resolve(url).func, listteamscores)
    def test_deleteobj_url_resolves(self):
        url = reverse("deleteobj", args=['some-pk'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, deleteobj)
    def test_edit_data_url_resolves(self):
        url = reverse("edit_data", args=['some-pk'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, edit_data)
    def test_deletefile_url_resolves(self):
        url = reverse("deletefile", args=['some-pk'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, deletefile)

