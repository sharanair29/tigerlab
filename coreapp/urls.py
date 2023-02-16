from django.urls import path

from . import views

urlpatterns = [
    path('', views.coreapp, name='coreapp'),
    path('analytics', views.analytics, name='analytics'),
    path('deleteobj/<str:pk>', views.deleteobj, name='deleteobj'),
    path('addobj', views.addobj, name='addobj'),
    path('deletefile/<str:pk>', views.deletefile, name='deletefile'),

]