from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, generics
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
#from rest_framework_gis.filters import InBBoxFilter
from .filters import InBBoxFilter

from .models import Site, SiteAgency, SiteOperation, SiteIdentifiers
from .serialisers import SitesSerializer

class SitesViewSetApiTest(viewsets.ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, ]
    template_name = 'sites/api_custom.html'
    queryset = Site.objects.all()
    serializer_class = SitesSerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, )


class SitesViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SitesSerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, )


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
