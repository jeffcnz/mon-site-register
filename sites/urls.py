from django.urls import path, include
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view

from . import views
#from . import custom_routers

#router = routers.DefaultRouter()
# Register sites api to use a custome router that complies with requirements of WFS3.
#router = custom_routers.OGCRouter()
router = routers.DefaultRouter()
router.register(r'items', views.SitesViewSetApi, basename='apisite')

#Assign paths for api info and conformance endpoints
urlpatterns = [
    path('', views.ApiInfoViewSet.as_view(), name='info'),
    path('conformance/', views.ApiConformanceViewSet.as_view(), name='conformance'),

]

# Setup type routing for html and json
urlpatterns = format_suffix_patterns(urlpatterns)

# Add the api info in swagger format for html or jason otherwise.
urlpatterns += [
    path('api/', get_schema_view(
    title="NZEMS",
    description="A prototype New Zealand Environmental Monitoring Site Register."
    ), name='openapi-schema'),
    path('api.html', TemplateView.as_view(
    template_name='sites/swagger-api.html'
    ), name='swagger-ui'),
    path('collections/', views.collection, name='collections'),
    path('collections/sites/', include(router.urls))
]
