from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.DefaultRouter()
router.register(r'sites', views.SitesViewSet)
router.register(r'sites/<int:pk>/', views.SitesViewSet)


urlpatterns = [
    path('', RedirectView.as_view(url='web/')),
    # ex: /sites/
    path('web/', views.siteList, name='siteList'),
    # ex: /sites/id/5/
    path('web/id/<int:site_id>/', views.site, name='site'),
    #appi
    path('api/', include(router.urls)),
    #path('api/<int:pk>/', views.SiteDetailViewSet)
]
