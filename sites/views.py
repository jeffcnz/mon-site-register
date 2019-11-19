#from django.http import HttpResponse
#from django.shortcuts import get_object_or_404, render
#from django.views.generic import TemplateView
from django.utils import dateparse

from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes#, renderer_classes
from rest_framework import permissions
#from rest_framework_gis.filters import InBBoxFilter
from .filters import InBBoxFilter, SiteFilter, InDateRangeFilter

from django_filters import rest_framework as filters

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
        serializer = ApiInfoSerialiser(info[0], context={'request':request}, many=False)
        return Response(serializer.data)


class ApiConformanceViewSet(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, ]
    template_name = 'sites/api_conformance.html'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        conformance = ApiConformance.objects.all()
        serializer = ApiConformanceSerialiser(conformance, many=False)
        return Response(serializer.data)


class SitesViewSetApi(custom_viewsets.NoDeleteViewset):
#class SitesViewSetApi(viewsets.ModelViewSet):
    def get_queryset(self):
        """ Initial custom filtering of the queryset """
        queryset = Site.objects.all()
        operating = self.request.query_params.get('operating', None)
        if operating is not None:
            print(queryset)
            opdate = dateparse.parse_datetime(operating)
            queryset = queryset.filter(siteagency__to_date__gte = opdate) | queryset.filter(siteagency__to_date__isnull=True)
            queryset = queryset.distinct()
        return queryset

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, ]
    template_name = 'sites/api_sitelist.html'
    #queryset = Site.objects.all()
    queryset = get_queryset
    serializer_class = SitesSerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, filters.DjangoFilterBackend, InDateRangeFilter)
    filterset_class = SiteFilter




@api_view()
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def collection(request):
    output = {"id": "sites", "title": "Environmental Monitoring Sites", "description": "Environmental monitoring sites"}
    return Response(output)


#class SitesViewSet(viewsets.ModelViewSet):
#    queryset = Site.objects.all()
#    serializer_class = SitesSerializer
#    bbox_filter_field = 'location'
#    filter_backends = (InBBoxFilter, )
