from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Site


def siteList(request):
    site_list = Site.objects.order_by('site_name')
    context = {'site_list': site_list,}
    return render(request, 'sites/siteList.html', context)


def site(request, site_id):
    #return HttpResponse("You're looking at site %s." % site_id)
    site = get_object_or_404(Site, pk=site_id)
    return render(request, 'sites/site.html', {'site': site})
