#from django.http import HttpResponse
#from django.shortcuts import get_object_or_404, render
#from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework.decorators import api_view, renderer_classes
from rest_framework import permissions
#from rest_framework_gis.filters import InBBoxFilter
from .filters import InBBoxFilter

from .models import Site, SiteAgency, SiteOperation, SiteIdentifiers, ApiInfo, ApiConformance
from .serialisers import SitesSerializer, ApiInfoSerialiser, ApiConformanceSerialiser
#from . import info
from . import custom_viewsets


class ApiInfoViewSet(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, ]
    template_name = 'sites/api_info.html'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        info = ApiInfo.objects.all()
        serializer = ApiInfoSerialiser(info[0], many=False)
        return Response(serializer.data)


class ApiConformanceViewSet(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        conformance = ApiConformance.objects.all()
        serializer = ApiConformanceSerialiser(conformance, many=True)
        return Response(serializer.data)

class SitesViewSetApi(custom_viewsets.NoDeleteViewset):
#class SitesViewSetApi(viewsets.ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, ]
    template_name = 'sites/api_sitelist.html'
    queryset = Site.objects.all()
    serializer_class = SitesSerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, )


#class SitesViewSet(viewsets.ModelViewSet):
#    queryset = Site.objects.all()
#    serializer_class = SitesSerializer
#    bbox_filter_field = 'location'
#    filter_backends = (InBBoxFilter, )
