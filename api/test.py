import logging
logging.basicConfig(filename="./testlogs/apitests.log", level=logging.DEBUG)

import csv, os
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APITestCase, APIClient


# ../ranks/uploadfile/
#/ranks/