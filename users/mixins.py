from rest_framework import mixins, viewsets


class CreateUpdateListRetrieveViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    pass
