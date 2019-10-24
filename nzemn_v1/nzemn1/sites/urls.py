from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.DefaultRouter()
router.register(r'collections/sites/items', views.SitesViewSetApiTest, basename='apisite')
#router.register(r'collections/sites/items/<int:pk>', views.SitesViewSetApiTest)


urlpatterns = [
    path('', RedirectView.as_view(url='web/')),
    # ex: /sites/
    path('web/', views.siteList, name='siteList'),
    # ex: /sites/id/5/
    path('web/id/<int:site_id>/', views.site, name='site'),
    #appi
    path('api/', include(router.urls)),
    #path('api/collections/sites', views.SitesViewSet)
    #path('api/<int:pk>/', views.SiteDetailViewSet)
]
