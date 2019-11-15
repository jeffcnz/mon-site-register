# Modified standard gis api filter so call fo bbox is bbox not inbbox.
# Makes filter conform to OGC WFS3 requirements.

from math import cos, pi

from django.utils import dateparse
from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured
from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon, Point
from django.contrib.gis import forms

from rest_framework.filters import BaseFilterBackend
#from rest_framework import filters
from django_filters import rest_framework as filters
from rest_framework.exceptions import ParseError

from .models import Site

#from .tilenames import tile_edges

try:
    import django_filters
except ImportError:  # pragma: no cover
    raise ImproperlyConfigured(
        'restframework-gis filters depend on package "django-filter" '
        'which is missing. Install with "pip install django-filter".'
    )
try:
    # Django >= 2.0
    from django.contrib.gis.db.models.fields import BaseSpatialField
except ImportError:
    try:  # pragma: no cover
        # django >= 1.8,<2.0
        from django.contrib.gis.db.models.lookups import gis_lookups
    except ImportError:  # pragma: no cover
        # django <= 1.7
        gis_lookups = models.sql.query.ALL_TERMS
else:
    gis_lookups = BaseSpatialField.get_lookups()


__all__ = [
    'InBBoxFilter'
]


class InBBoxFilter(BaseFilterBackend):
    bbox_param = 'bbox'  # The URL query parameter which contains the bbox.

    def get_filter_bbox(self, request):
        bbox_string = request.query_params.get(self.bbox_param, None)
        if not bbox_string:
            return None

        try:
            p1x, p1y, p2x, p2y = (float(n) for n in bbox_string.split(','))
        except ValueError:
            raise ParseError('Invalid bbox string supplied for parameter {0}'.format(self.bbox_param))

        x = Polygon.from_bbox((p1x, p1y, p2x, p2y))
        return x

    def filter_queryset(self, request, queryset, view):
        filter_field = getattr(view, 'bbox_filter_field', None)
        include_overlapping = getattr(view, 'bbox_filter_include_overlapping', False)
        if include_overlapping:
            geoDjango_filter = 'bboverlaps'
        else:
            geoDjango_filter = 'contained'

        if not filter_field:
            return queryset

        bbox = self.get_filter_bbox(request)
        if not bbox:
            return queryset
        return queryset.filter(Q(**{'%s__%s' % (filter_field, geoDjango_filter): bbox}))
# backward compatibility
InBBOXFilter = InBBoxFilter


class SiteFilter(filters.FilterSet):
    #agency = filters.CharFilter(field_name='site__agency', lookup_expr='iexact')
    # Filter to allow site names containing a string
    name = filters.CharFilter(field_name='site_name', lookup_expr='icontains')
    # Filter to search for sites that have an agency name
    agency = filters.CharFilter(field_name='siteagency__agency__agency_name', lookup_expr='exact')
    #operating = filters.DateTimeFilter(field_name='siteagency__from_date', lookup_expr='gte') & filters.DateTimeFilter(field_name='siteagency__to_date', lookup_expr='lte')



class DateFilter(filters.FilterSet):
#    datetime = filters.CharFilter(method='daterange_filter')
    opbefore = filters.DateTimeFilter(field_name='siteagency__from_date', lookup_expr='lte')

#    class Meta:
#        model = SiteAgency
#        fields = ['from_date', 'to_date']


class InDateRangeFilter(BaseFilterBackend):
    daterange_param = 'datetime'  # The URL query parameter which contains the bbox.

    def get_filter_datetime(self, request):
        daterange_string = request.query_params.get(self.daterange_param, None)
        if not daterange_string:
            return None

        try:
            # Split the string on the /
            datetime1, datetime2 = (n for n in daterange_string.split('/'))
            # Handle empty values
            if datetime1 == "" or datetime1 == "..":
                #Blank start date provided so use end datetime
                datetime1 = dateparse.parse_datetime(datetime2)
            else:
                datetime1 = dateparse.parse_datetime(datetime1)

            if datetime2 == "" or datetime1 == "..":
                #Blank end date provided so use start datetime
                datetime2 = dateparse.parse_datetime(datetime1)
            else:
                datetime2 = dateparse.parse_datetime(datetime2)
        except:
            # A valid single timedate could have been provided
            try:
                datetime1 = dateparse.parse_datetime(daterange_string)
                datetime2 = datetime1
            except:
                datetime1, datetime2 = None
        if datetime1 and datetime2:
            x = [datetime1, datetime2]
        else:
            raise ParseError('Invalid datetime string supplied for parameter {0}'.format(self.daterange_param))

        return x

    def filter_queryset(self, request, queryset, view):

        daterange = self.get_filter_datetime(request)
        if not daterange:
            return queryset
        queryset = queryset.filter(siteagency__to_date__gte=daterange[0]) | queryset.filter(siteagency__to_date__isnull=True)
        queryset = queryset.distinct()
        print(daterange[1])
        queryset = queryset.filter(siteagency__from_date__lte=daterange[1])
        return queryset.filter(**{})
