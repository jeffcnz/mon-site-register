from rest_framework import viewsets
from rest_framework import mixins

class NoDeleteViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset that provides all actions other than delete.
    It provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, and `list()` actions, but not destroy().

    To use, override the class and set the .queryset and
    .serializer_class attributes.
    """
    pass
