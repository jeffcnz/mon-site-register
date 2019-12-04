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
        # Extract the bounding box strung
        bbox_string = request.query_params.get(self.bbox_param, None)
        if not bbox_string:
            return None
        # Extract the coordinates from the bbox string, raise error if issue
        try:
            p1x, p1y, p2x, p2y = (float(n) for n in bbox_string.split(','))
        except ValueError:
            raise ParseError('Invalid bbox string supplied for parameter {0}'.format(self.bbox_param))
        # Check bounding box coordinate validity
        # Check valid longitudes
        if p1x > 180 or p1x < -180 or p2x > 180 or p2x < -180:
            raise ParseError('Invalid longitude provided')
        # Check valid latitudes
        elif p1y > 90 or p1y < -90 or p2y > 90 or p2y < -90:
            raise ParseError('Invalid latitude provided')
        # Check valid bounding box
        elif p1x > p2x or p1y > p2y:
            raise ParseError('Invalid Bounding Box')
        # If valid then process to a polygon and return
        else:
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
        # Identify where sites have no locations
        nolocation = queryset.filter(location__isnull=True)
        # Identify sites in the bounding box
        queryset = queryset.filter(Q(**{'%s__%s' % (filter_field, geoDjango_filter): bbox}))
        # Join the results from the bbox filter with the sites with no locations
        queryset = queryset.union(nolocation)
        # return the queryset
        return queryset
# backward compatibility
InBBOXFilter = InBBoxFilter


class SiteFilter(filters.FilterSet):
    #agency = filters.CharFilter(field_name='site__agency', lookup_expr='iexact')
    # Filter to allow site names containing a string
    name = filters.CharFilter(field_name='site_name', lookup_expr='icontains')
    # Filter to search for sites that have an agency name
    agency = filters.CharFilter(field_name='siteagency__agency__agency_name', lookup_expr='exact')
    #operating = filters.DateTimeFilter(field_name='siteagency__from_date', lookup_expr='gte') & filters.DateTimeFilter(field_name='siteagency__to_date', lookup_expr='lte')


class InDateRangeFilter(BaseFilterBackend):
    """
    Filter results by a date range given based on the agency date ranges in the
    database.  Returns sites that were in use by an agency at some point in the
    period specified, and sites with no agencies.
    """
    daterange_param = 'datetime'  # The URL query parameter which contains the bbox.

    def get_filter_datetime(self, request):
        # Helper function to process the datetime interval provided and
        #make it useful for filtering.
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
        # Return the values if they were valid and
        # the second datetime was after the first
        # Otherwise raise an error
        if datetime1 and datetime2 and datetime2 >= datetime1:
            return [datetime1, datetime2]
        else:
            raise ParseError('Invalid datetime string supplied for parameter {0}'.format(self.daterange_param))

        #return x

    def filter_queryset(self, request, queryset, view):
        # Function to filter the dataset on the timerange
        # Process the given interval
        daterange = self.get_filter_datetime(request)
        # If there isn't a datetime parameter given then return the unaltered data
        if not daterange:
            return queryset
        # Identify where sites have no agencies
        noagency = queryset.filter(agencies__isnull=True)
        # Filter for the time interval.
        # the to_date must be after the start date provided (or null)
        queryset = queryset.filter(siteagency__to_date__gte=daterange[0]) | queryset.filter(siteagency__to_date__isnull=True)
        # remove duplicates
        queryset = queryset.distinct()
        # AND the from_date date must be before the end date provided
        queryset = queryset.filter(siteagency__from_date__lte=daterange[1])
        # Join the results from the daterange filter with the sites with no agencies
        queryset = queryset.union(noagency)
        # return the queryset
        return queryset

class ValidParameterFilter(BaseFilterBackend):
    """
    Filter checks whether the requested parameters are defined.
    If any aren't then it returns an error.
    """


    def filter_queryset(self,request, queryset, view):
        valid_params = ['bbox', 'name', 'agency', 'datetime', 'limit', 'offset', 'format']
        requested_parameters = request.query_params
        #print(requested_parameters)
        if all(param in valid_params for param in requested_parameters):
            return queryset
        else:
            raise ParseError('Invalid parameters provided.')
