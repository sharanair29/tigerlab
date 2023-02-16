from django.urls import path

from . import views

urlpatterns = [
    path('', views.coreapp, name='coreapp'),
    path('analytics', views.analytics, name='analytics'),
    path('deleteobj/<str:pk>', views.deleteobj, name='deleteobj'),
    path('edit_data/<str:pk>', views.edit_data, name='edit_data'),
    path('addobj', views.addobj, name='addobj'),
    path('listteamscores', views.listteamscores, name='listteamscores'),
    path('deletefile/<str:pk>', views.deletefile, name='deletefile'),

]