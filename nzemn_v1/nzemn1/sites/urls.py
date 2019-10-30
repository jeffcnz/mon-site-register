from django.urls import path, include
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view

from . import views
from . import custom_routers

#router = routers.DefaultRouter()
router = custom_routers.OGCRouter()
router.register(r'sites', views.SitesViewSetApiTest, basename='apisite')
#router.register(r'sites/items/<int:pk>', views.SitesViewSetApiTest)

#apirouter = routers.DefaultRouter()
#apirouter.register(r'about', views.AboutViewSet, basename='about')
#apirouter.register(r'conformance', views.ApiConformanceViewSet, basename='conformance')
#apirouter.register(r'', views.ApiInfoViewSet, basename='info')


urlpatterns = [
    path('', views.ApiInfoViewSet.as_view(), name='info'),
    #path('', RedirectView.as_view(url='web/')),
    #path('', include(apirouter.urls)),

    path('conformance/', views.ApiConformanceViewSet.as_view(), name='conformance'),
    #path('collections/', views.collections, name='collections'),

    # ex: /sites/
    #path('web/', views.siteList, name='siteList'),
    # ex: /sites/id/5/
    #path('web/id/<int:site_id>/', views.site, name='site'),
    #appi

    path('about/', views.AboutViewSet.as_view(), name='about')
    #path('api/collections/sites', views.SitesViewSet)
    #path('api/<int:pk>/', views.SiteDetailViewSet)
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('api/', get_schema_view(
    title="NZEMS",
    description="A prototype New Zealand Environmental Monitoring Site Register."
    ), name='openapi-schema'),
    path('api.html', TemplateView.as_view(
    template_name='sites/swagger-api.html'
    ), name='swagger-ui'),
    path('collections/', include(router.urls))
]
