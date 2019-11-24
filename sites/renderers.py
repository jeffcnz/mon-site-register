from rest_framework.renderers import JSONRenderer

class GeoJSONRenderer(JSONRenderer):
    """
    Renderer which serializes to GeoJSON.
    """
    media_type = 'application/geo+json'
