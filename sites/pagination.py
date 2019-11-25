from collections import OrderedDict

from rest_framework import pagination
from rest_framework.response import Response


class OGCFeaturesPagination(pagination.LimitOffsetPagination):
    """
    A geoJSON implementation of a pagination serializer.
    Modified from the Django Rest GIS GeoJsonPagination
    to conform with OGC Features specification.
    """

    def get_paginated_response(self, data):
        # define additional pagination links
        pagination_links = [{
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
                }]
        # create final links list by adding pagination links to existing
        final_links = data['links'] + pagination_links
        return Response(OrderedDict([
            ('type', 'FeatureCollection'),
            ('numberMatched', self.count),
            ('numberReturned', len(data['features'])),
            ('links', final_links),
            ('features', data['features'])
        ]))
