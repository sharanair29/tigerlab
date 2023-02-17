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
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        self.client.login(username='testuser', password='password')

    def test_csv_upload_success(self):
        url = '/ranks/uploadfile/'
        myfile = open('test.csv','rb')
        data = SimpleUploadedFile(
        content=myfile.read(), name=myfile.name, content_type="multipart/form-data"
            )
        response = self.client.post(url, {'test':myfile}, format="multipart")
        logging.info(f"Test API CSV UPLOAD : RESPONSE STATUS CODE : {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
