"""tigerlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from api.views import RankViewSet
from django.conf.urls import handler404, handler500, handler403

router = routers.SimpleRouter()
router.register("ranks", RankViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('coreapp/', include('coreapp.urls')),
    path(r'ranks', include('rest_framework.urls'))

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404="accounts.views.handle_404"
handler403="accounts.views.csrf_failure"
handler500="accounts.views.handle_500"