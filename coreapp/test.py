from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .views import *
from django.test.client import RequestFactory
from rest_framework import status
from django.utils import timezone
import logging
logging.basicConfig(filename="./testing.log", level=logging.DEBUG)

"""

The following class TestUrlsCoreapp is focused on testing URL paths

"""

class TestUrlsCoreapp(SimpleTestCase):
    """

    Test urls with no arguments within coreapp
    
    """
    def test_coreapp_url_resolves(self):
        url = reverse("coreapp")
        logging.info(f"{resolve(url)}, TIME : {timezone.now()}")
        self.assertEquals(resolve(url).func, coreapp)

    def test_analytics_url_resolves(self):
        url = reverse("analytics")
        logging.info(f"{resolve(url)}, TIME : {timezone.now()}")
        self.assertEquals(resolve(url).func, analytics)

    def test_addobj_url_resolves(self):
        url = reverse("addobj")
        logging.info(f"{resolve(url)}, TIME : {timezone.now()}")
        self.assertEquals(resolve(url).func, addobj)

    def test_listteamscores_url_resolves(self):
        url = reverse("listteamscores")
        logging.info(f"{resolve(url)}, TIME : {timezone.now()}")
        self.assertEquals(resolve(url).func, listteamscores)

    """
    
    Test urls with arguments within coreapp
    
    """
    def test_deleteobj_url_resolves(self):
        url = reverse("deleteobj", args=['some-pk'])
        logging.info(f"{resolve(url)}, TIME : {timezone.now()}")
        self.assertEquals(resolve(url).func, deleteobj)

    def test_edit_data_url_resolves(self):
        url = reverse("edit_data", args=['some-pk'])
        logging.info(f"{resolve(url)}, TIME : {timezone.now()}")
        self.assertEquals(resolve(url).func, edit_data)

    def test_deletefile_url_resolves(self):
        url = reverse("deletefile", args=['some-pk'])
        logging.info(f"{resolve(url)}, TIME : {timezone.now()}")
        self.assertEquals(resolve(url).func, deletefile)

""""

The following class TestViewsCoreapp is focused on testing views
within coreapp

"""

class TestViewsCoreapp(TestCase):
    """
    
    Set up a dummy user and login
    since views are restricted to authenticated users
    
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        self.client.login(username='testuser', password='password')
        self.listteamscores = reverse('listteamscores')
        self.addobj = reverse('addobj')
        self.deleteobj = reverse('deleteobj' , args=['some-pk'])

    """
    
    Test the ability to retrieve all Team Score Objects
    
    """
    def test_get_listtteamscores(self):
        response = self.client.get(self.listteamscores)
        self.assertEquals(response.status_code, 200)

    """
    
    Test the ability to add data as a Team Score Object
    
    """
    def test_add_team_score(self):
        TeamScore.objects.create(
            team_name_1 = "team name 1",
            team_score_1 = 55,
            team_name_2 = "team name 2",
            team_score_2 = 66,
        )

        response = self.client.post(self.addobj,{
            'team_name_1' : 'team name 1',
            'team_score_1' : 55,
            'team_name_2' : 'team name 2',
            'team_score_2' : 66,
        })

        self.assertEquals(response.status_code, 204)
