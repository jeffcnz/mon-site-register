from collections import OrderedDict

from django.core.exceptions import ImproperlyConfigured
from django.contrib.gis.geos import Polygon

from rest_framework.serializers import ModelSerializer, ListSerializer, LIST_SERIALIZER_KWARGS
from rest_framework.utils.urls import replace_query_param
from rest_framework_gis.fields import GeometryField, GeometrySerializerMethodField  # noqa


class GeoModelSerializer(ModelSerializer):
    """
    Deprecated, will be removed in django-rest-framework-gis 1.0
    """


class OGCGeoFeatureModelListSerializer(ListSerializer):
    @property
    def data(self):
        return super(ListSerializer, self).data

    def to_representation(self, data):
        """
        Add OGC GeoJSON compatible formatting to a serialized queryset list.
        Including the links field
        """
        request = self.context.get("request")
        url = request.build_absolute_uri()
        output_links = [
            {
            'href': url,
            'rel': 'self',
            'type': request.accepted_media_type.split(';')[0],
            'title': 'this page'
            },
            {
            "href": replace_query_param(url, 'format', 'json'),
            "rel": "alternate",
            "type": "application/geo+json",
            "title": "this document as json"
            },
            {
            "href": replace_query_param(url, 'format', 'html'),
            "rel": "alternate",
            "type": "text/html",
            "title": "this document as html"
            }
            ]
        return OrderedDict((
            ("type", "FeatureCollection"),
            ("links", output_links),
            ("features", super(OGCGeoFeatureModelListSerializer, self).to_representation(data))
        ))


class OGCGeoFeatureModelSerializer(ModelSerializer):
    """
    A subclass of ModelSerializer
    that outputs geojson-ready data as
    features and feature collections in OGC format.
    Extends Django Rest GIS GeoFeatureModel Serializer
    by adding links.
    """
    @classmethod
    def many_init(cls, *args, **kwargs):
        child_serializer = cls(*args, **kwargs)
        list_kwargs = {'child': child_serializer}
        list_kwargs.update(dict([
            (key, value) for key, value in kwargs.items()
            if key in LIST_SERIALIZER_KWARGS
        ]))
        meta = getattr(cls, 'Meta', None)
        list_serializer_class = getattr(meta, 'list_serializer_class', OGCGeoFeatureModelListSerializer)
        return list_serializer_class(*args, **list_kwargs)

    def __init__(self, *args, **kwargs):
        super(OGCGeoFeatureModelSerializer, self).__init__(*args, **kwargs)
        meta = getattr(self, 'Meta')
        default_id_field = None
        primary_key = self.Meta.model._meta.pk.name
        # use primary key as id_field when possible
        if not hasattr(meta, 'fields') or meta.fields == '__all__' or primary_key in meta.fields:
            default_id_field = primary_key
        meta.id_field = getattr(meta, 'id_field', default_id_field)

        if not hasattr(meta, 'geo_field') or not meta.geo_field:
            raise ImproperlyConfigured("You must define a 'geo_field'.")

        def check_excludes(field_name, field_role):
            """make sure the field is not excluded"""
            if hasattr(meta, 'exclude') and field_name in meta.exclude:
                raise ImproperlyConfigured("You cannot exclude your '{0}'.".format(field_role))

        def add_to_fields(field_name):
            """Make sure the field is included in the fields"""
            if hasattr(meta, 'fields') and meta.fields != '__all__':
                if field_name not in meta.fields:
                    if type(meta.fields) is tuple:
                        additional_fields = (field_name,)
                    else:
                        additional_fields = [field_name]
                    meta.fields += additional_fields

        check_excludes(meta.geo_field, 'geo_field')
        add_to_fields(meta.geo_field)

        meta.bbox_geo_field = getattr(meta, 'bbox_geo_field', None)
        if meta.bbox_geo_field:
            check_excludes(meta.bbox_geo_field, 'bbox_geo_field')
            add_to_fields(meta.bbox_geo_field)

        meta.auto_bbox = getattr(meta, 'auto_bbox', False)
        if meta.bbox_geo_field and meta.auto_bbox:
            raise ImproperlyConfigured("You must eiher define a 'bbox_geo_field' or "
                                       "'auto_bbox', but you can not set both")

    def to_representation(self, instance):
        """
        Serialize objects -> primitives.
        """
        # prepare OrderedDict geojson structure
        feature = OrderedDict()
        # the list of fields that will be processed by get_properties
        # we will remove fields that have been already processed
        # to increase performance on large numbers
        fields = list(self.fields.values())

        # optional id attribute
        if self.Meta.id_field:
            field = self.fields[self.Meta.id_field]
            value = field.get_attribute(instance)
            feature["id"] = field.to_representation(value)
            fields.remove(field)

        # required type attribute
        # must be "Feature" according to GeoJSON spec
        feature["type"] = "Feature"

        # required geometry attribute
        # MUST be present in output according to GeoJSON spec
        field = self.fields[self.Meta.geo_field]
        geo_value = field.get_attribute(instance)
        feature["geometry"] = field.to_representation(geo_value)
        fields.remove(field)
        # Bounding Box
        # if auto_bbox feature is enabled
        # bbox will be determined automatically automatically
        if self.Meta.auto_bbox and geo_value:
            feature["bbox"] = geo_value.extent
        # otherwise it can be determined via another field
        elif self.Meta.bbox_geo_field:
            field = self.fields[self.Meta.bbox_geo_field]
            value = field.get_attribute(instance)
            feature["bbox"] = value.extent if hasattr(value, 'extent') else None
            fields.remove(field)

        # Add links as per OGC, spec.
        # Links only added if the request is not for a feature collection.
        # OGC requires feature collection from .../items
        # so clean up url and look for .../items as the last component..
        request = self.context.get("request")
        url = request.build_absolute_uri()
        base_component_list = url.split("?")[0].split("/")
        if base_component_list[-1] == '':
            base_component_list = base_component_list[:-1]
        if base_component_list[-1] != 'items':

            feature["links"] = [
                {
                'href': url,
                'rel': 'self',
                'type': request.accepted_media_type.split(';')[0],
                'title': 'this page'
                },
                {
                "href": replace_query_param(url, 'format', 'json'),
                "rel": "alternate",
                "type": "application/geo+json",
                "title": "this document as json"
                },
                {
                "href": replace_query_param(url, 'format', 'html'),
                "rel": "alternate",
                "type": "text/html",
                "title": "this document as html"
                }
                ]

        # GeoJSON properties
        feature["properties"] = self.get_properties(instance, fields)

        return feature

    def get_properties(self, instance, fields):
        """
        Get the feature metadata which will be used for the GeoJSON
        "properties" key.

        By default it returns all serializer fields excluding those used for
        the ID, the geometry and the bounding box.

        :param instance: The current Django model instance
        :param fields: The list of fields to process (fields already processed have been removed)
        :return: OrderedDict containing the properties of the current feature
        :rtype: OrderedDict
        """
        properties = OrderedDict()

        for field in fields:
            if field.write_only:
                continue
            value = field.get_attribute(instance)
            representation = None
            if value is not None:
                representation = field.to_representation(value)
            properties[field.field_name] = representation

        return properties

    def to_internal_value(self, data):
        """
        Override the parent method to first remove the GeoJSON formatting
        """
        if 'properties' in data:
            data = self.unformat_geojson(data)
        return super(OGCGeoFeatureModelSerializer, self).to_internal_value(data)

    def unformat_geojson(self, feature):
        """
        This function should return a dictionary containing keys which maps
        to serializer fields.

        Remember that GeoJSON contains a key "properties" which contains the
        feature metadata. This should be flattened to make sure this
        metadata is stored in the right serializer fields.

        :param feature: The dictionary containing the feature data directly
                        from the GeoJSON data.
        :return: A new dictionary which maps the GeoJSON values to
                 serializer fields
        """
        attrs = feature["properties"]

        if 'geometry' in feature:
            attrs[self.Meta.geo_field] = feature['geometry']

        if self.Meta.bbox_geo_field and 'bbox' in feature:
            attrs[self.Meta.bbox_geo_field] = Polygon.from_bbox(feature['bbox'])

        return attrs
