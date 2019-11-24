from collections import OrderedDict

from rest_framework import pagination
from rest_framework.response import Response


class OGCFeaturesPagination(pagination.LimitOffsetPagination):
    """
    A geoJSON implementation of a pagination serializer.
    Modified from the Django Rest GIS GeoJsonPagination
    to conform with OGC Features specification.
    """
    #page_size_query_param = 'page_size'



    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('type', 'FeatureCollection'),
            ('numberMatched', self.count),
            ('numberReturned', len(data['features'])),
            ('links', [
                {
                'href': self.request.build_absolute_uri(),
                'rel': 'self',
                'type': self.request.accepted_media_type.split(';')[0],
                'title': 'this page'
                },
                #{
                #'href': self.json_url(),
                #'rel': 'alternate',
                #'type': 'application/geo+json',
                #'title': 'this page as geoJSON'
                #},
                #{
                #'href': self.html_url(),
                #'rel': 'alternate',
                #'type': 'text/html',
                #'title': 'this page as html'
                #},
                {
                'href':self.get_next_link(),
                'rel': 'next',
                'type': 'application/geo+json',
                'title': 'next page'
                },
                {
                'href':self.get_previous_link(),
                'rel': 'prev',
                'type': 'application/geo+json',
                'title': 'previous page'
                }
            ]),
            #('next', ),
            #('previous', self.get_previous_link()),
            ('features', data['features'])
        ]))
