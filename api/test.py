import logging
logging.basicConfig(filename="./testlogs/apitests.log", level=logging.DEBUG)

import csv, os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import RequestFactory

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from datetime import timezone

class API_DRF_Test(APITestCase):
    """

    Set up a dummmy user and login since view has IsAuthenticated decorator restriction
    
    """
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        self.client.login(username='testuser', password='password')

    """

    Test ability to post csv file to the API endpoint and generate Team Score Objects.
    Within out RankViewSet class in api.views.py we have stated that on success
    return a Response with a status code of 201, hence the assertion is set equal to 
    status code 201.
    
    """
    def test_csv_upload_success(self):
        url = '/ranks/uploadfile/'
        myfile = open('test.csv','rb')
        data = SimpleUploadedFile(
        content=myfile.read(), name=myfile.name, content_type="multipart/form-data"
            )
        response = self.client.post(url, {'test':myfile}, format="multipart")
        logging.info(f"Test API CSV UPLOAD : RESPONSE STATUS CODE : {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

# No models to test
# No forms to test

"""
We don't have any models or forms listed within the api application.
"""

