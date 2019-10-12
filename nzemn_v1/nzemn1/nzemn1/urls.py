"""nzemn1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.views.generic.base import RedirectView
from rest_framework import routers, serializers, viewsets
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.filters import InBBoxFilter
from sites.models import Site

class SitesSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = Site
        geo_field = 'location'
        fields = '__all__'


# /sites/?in_bbox=-90,29,-89,35
class SitesViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SitesSerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, )


router = routers.DefaultRouter()
router.register(r'sites', SitesViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='/sites/')),
    path('sites/', include('sites.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
