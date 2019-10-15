# Modified standard gis api filter so call fo bbox is bbox not inbbox.
# Makes filter conform to OGC WFS3 requirements.

from math import cos, pi

from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured
from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon, Point
from django.contrib.gis import forms

from rest_framework.filters import BaseFilterBackend
from rest_framework.exceptions import ParseError

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
