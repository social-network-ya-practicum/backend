from rest_framework import mixins, viewsets


class UpdateListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    pass


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass
