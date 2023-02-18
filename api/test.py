import logging
logging.basicConfig(filename="./testlogs/apitests.log", level=logging.DEBUG)
from django.urls import reverse, resolve
import csv, os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import RequestFactory

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from datetime import timezone

"""

Test ability to post csv file to the API endpoint and generate Team Score Objects.
Within out RankViewSet class in api.views.py we have stated that on success
return a Response with a status code of 201, hence the assertion is set equal to 
status code 201.

"""

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

    Test csv upload success for files with headers

    """

    def test_csv_upload_success_with_headers(self):
        url = '/ranks/uploadfile/'
        file_name = "testwithheaders.csv"
        # Open file in write mode (Arrange)
        with open(file_name, "w") as file:
            writer = csv.writer(file)
            # Add some rows in csv file
            writer.writerow(["team_1 name", "team_1 score", "team_2 name", "team_2 score"])
            writer.writerow(["Crazy Ones", 3, "Rebels", 3])
            writer.writerow(
                ["Fantastics", 28748, "Rebels", 1],
            )
            writer.writerow(
                ["Crazy Ones", 2381741, "Rebels", 78],
            )
            writer.writerow(
                ["Andorra", 468, "AD", 90],
            )
        # open file in read mode
        data = open(file_name, "rb")
        # Create a simple uploaded file
        data = SimpleUploadedFile(
            content=data.read(), name=data.name, content_type="multipart/form-data"
        )
       
        response = self.client.post(url, {'test':data}, format="multipart")
        logging.info(f"Test API CSV UPLOAD : RESPONSE STATUS CODE : {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        os.remove(file_name)
        

    """

    Test csv upload success for files without headers as sample input 
    in assignment pdf suggests

    """  

    def test_csv_upload_success_without_headers(self):
        url = '/ranks/uploadfile/'
        file_name = "testwithoutheaders.csv"
        # Open file in write mode (Arrange)
        with open(file_name, "w") as file:
            writer = csv.writer(file)
            # Add some rows in csv file
            writer.writerow(["Crazy Ones", 3, "Rebels", 3])
            writer.writerow(
                ["Fantastics", 28748, "Rebels", 1],
            )
            writer.writerow(
                ["Crazy Ones", 2381741, "Rebels", 78],
            )
            writer.writerow(
                ["Andorra", 468, "AD", 90],
            )
        # open file in read mode
        data = open(file_name, "rb")
        # Create a simple uploaded file
        data = SimpleUploadedFile(
            content=data.read(), name=data.name, content_type="multipart/form-data"
        )
       
        response = self.client.post(url, {'test':data}, format="multipart")
        logging.info(f"Test API CSV UPLOAD : RESPONSE STATUS CODE : {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        os.remove(file_name)



"""
We don't have any models or forms listed within the api application.
"""

