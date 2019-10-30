from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from rest_framework import viewsets, generics
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import permissions
#from rest_framework_gis.filters import InBBoxFilter
from .filters import InBBoxFilter

from .models import Site, SiteAgency, SiteOperation, SiteIdentifiers, About, AboutBody, ApiInfo, ApiConformance
from .serialisers import SitesSerializer, AboutSerialiser, ApiInfoSerialiser, ApiConformanceSerialiser
from . import info

#class AboutViewSet(APIView):
class AboutViewSet(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, ]
    #template_name = 'api_custom.html'
    template_name = 'sites/about.html'
    #queryset = About.objects.all()
    #serializer_class = AboutSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        about = About.objects.all()
        serializer = AboutSerialiser(about[0], many=False)
        return Response(serializer.data)


class ApiInfoViewSet(APIView):
#class ApiInfoViewSet(viewsets.ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, ]
    template_name = 'sites/api_info.html'
    #queryset = ApiInfo.objects.all()
    #serializer_class = ApiInfoSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        info = ApiInfo.objects.all()
        serializer = ApiInfoSerialiser(info[0], many=False)
        return Response(serializer.data)


class ApiConformanceViewSet(APIView):
#class ApiConformanceViewSet(viewsets.ReadOnlyModelViewSet):
    #renderer_classes = [TemplateHTMLRenderer, JSONRenderer, ]
    #template_name = 'api_custom.html'
    #queryset = ApiConformance.objects.all()
    #serializer_class = ApiConformanceSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        conformance = ApiConformance.objects.all()
        serializer = ApiConformanceSerialiser(conformance, many=True)
        return Response(serializer.data)


class SitesViewSetApiTest(viewsets.ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, ]
    template_name = 'sites/api_sitelist.html'
    queryset = Site.objects.all()
    serializer_class = SitesSerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, )


class SitesViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SitesSerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, )


#def about(request):
#    return render(request, 'sites/about.html')

#class SiteDetailViewSet(viewsets.ModelViewSet):
#    queryset = Site.objects.all()
#    serializer_class = SitesSerializer


def siteList(request):
    site_list = Site.objects.order_by('site_name')
    context = {'site_list': site_list,}
    return render(request, 'sites/siteList.html', context)


def site(request, site_id):
    #return HttpResponse("You're looking at site %s." % site_id)
    site = get_object_or_404(Site, pk=site_id)
    print(site.identifiers)
    site_agency = SiteAgency.objects.filter(site=site.id)
    site_operation = SiteOperation.objects.filter(site=site.id)
    site_identifier = SiteIdentifiers.objects.filter(site=site.id)
    return render(request, 'sites/site.html', {'site': site,
                                               'site_agency':site_agency,
                                               'site_operation':site_operation,
                                               'site_identifier':site_identifier
                                               })
