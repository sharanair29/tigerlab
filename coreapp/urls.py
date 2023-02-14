from django.urls import path

from . import views

urlpatterns = [
    path('', views.coreapp, name='coreapp'),
    # path('login', views.login, name='login'),

]