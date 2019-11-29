#from django.http import HttpResponse
#from django.shortcuts import get_object_or_404, render
#from django.views.generic import TemplateView
import datetime
from django.utils import dateparse, timezone
from django.db.models import Min, Max

from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import permissions
#from rest_framework.pagination import LimitOffsetPagination

from django.contrib.gis.db.models import Extent
#from rest_framework_gis.filters import InBBoxFilter
from .filters import InBBoxFilter, SiteFilter, InDateRangeFilter, ValidParameterFilter

from django_filters import rest_framework as filters

from .models import Site, SiteAgency, SiteOperation, SiteIdentifiers, ApiInfo, ApiConformance, ApiCollections
from .serialisers import SitesSerializer, ApiInfoSerialiser, ApiConformanceSerialiser, ApiCollectionsSerialiser, ApiRootSerialiser
#from . import info
from . import custom_viewsets
from .pagination import OGCFeaturesPagination
from .renderers import GeoJSONRenderer

class ApiInfoViewSet(APIView):
    """
    The landing page provides links to the API definition,
    the Conformance statements and the metadata about the feature data
    in this dataset.
    """
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
        conformance = ApiConformance.objects.filter(api_id=1)
        serializer = ApiConformanceSerialiser(conformance, many=False)
        return Response(serializer.data)


class SitesViewSetApi(custom_viewsets.NoDeleteViewset):
#class SitesViewSetApi(viewsets.ModelViewSet):
    def get_queryset(self):
        """ Initial custom filtering of the queryset """
        queryset = Site.objects.all()
        operating = self.request.query_params.get('operating', None)
        if operating is not None:
            #print(queryset)
            opdate = dateparse.parse_datetime(operating)
            queryset = queryset.filter(siteagency__to_date__gte = opdate) | queryset.filter(siteagency__to_date__isnull=True)
            queryset = queryset.distinct()
        return queryset

    renderer_classes = [TemplateHTMLRenderer, GeoJSONRenderer, ]
    template_name = 'sites/api_sitelist.html'
    #queryset = Site.objects.all()
    queryset = get_queryset
    serializer_class = SitesSerializer
    #pagination_class = LimitOffsetPagination
    pagination_class = OGCFeaturesPagination
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, filters.DjangoFilterBackend, InDateRangeFilter, ValidParameterFilter)
    filterset_class = SiteFilter


class Collection(object):
    def __init__(self, id, title, description, bbox, timerange):
        self.id = id
        self.title = title
        self.description = description
        self.bbox = bbox
        self.timerange = timerange


class ApiCollectionView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, ]
    template_name = 'sites/api_collections.html'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        #collection = Site.objects.all()
        bbox = Site.objects.aggregate(Extent('location'))
        earliest = Site.objects.aggregate(Min('siteagency__from_date'))
        latest_date = Site.objects.aggregate(Max('siteagency__to_date'))
        no_to_date = Site.objects.filter(siteagency__to_date__isnull=True)
        if len(no_to_date) > 0:
            latest = None
        else:
            latest = timezone.localtime(latest_date['siteagency__to_date__max']).isoformat()
        coll = ApiCollections.objects.filter(id='sites').first()
        #coll['bbox']="test"
        print(coll.id)
        collection = Collection(id=coll.id,
                        title=coll.title,
                        description=coll.description,
                        bbox = [list(bbox['location__extent'])],
                        timerange = [[timezone.localtime(earliest['siteagency__from_date__min']).isoformat(),
                            latest]])
        #output = {"id": "sites", "title": "Environmental Monitoring Sites", "description": "Environmental monitoring sites"}
        serializer = ApiCollectionsSerialiser(collection, context={'request':request})
        return Response(serializer.data)


class ApiRootView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, ]
    template_name = 'sites/api_root.html'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        #collection = Site.objects.all()
        bbox = Site.objects.aggregate(Extent('location'))
        earliest = Site.objects.aggregate(Min('siteagency__from_date'))
        latest_date = Site.objects.aggregate(Max('siteagency__to_date'))
        no_to_date = Site.objects.filter(siteagency__to_date__isnull=True)
        if len(no_to_date) > 0:
            latest = None
        else:
            latest = timezone.localtime(latest_date['siteagency__to_date__max']).isoformat()
        coll = ApiCollections.objects.filter(id='sites').first()
        #coll['bbox']="test"
        print(coll.id)
        collection = Collection(id=coll.id,
                        title=coll.title,
                        description=coll.description,
                        bbox = [list(bbox['location__extent'])],
                        timerange = [[timezone.localtime(earliest['siteagency__from_date__min']).isoformat(),
                            latest]])
        #output = {"id": "sites", "title": "Environmental Monitoring Sites", "description": "Environmental monitoring sites"}
        serializer = ApiRootSerialiser(collection, context={'request':request})
        return Response(serializer.data)


#@api_view()
#@permission_classes([permissions.IsAuthenticatedOrReadOnly])
#@renderer_classes([TemplateHTMLRenderer, JSONRenderer, ])
#def collection(request):

#    output = {"id": "sites", "title": "Environmental Monitoring Sites", "description": "Environmental monitoring sites"}
#    return Response(output, template_name = 'sites/api_collections.html')


#class SitesViewSet(viewsets.ModelViewSet):
#    queryset = Site.objects.all()
#    serializer_class = SitesSerializer
#    bbox_filter_field = 'location'
#    filter_backends = (InBBoxFilter, )
