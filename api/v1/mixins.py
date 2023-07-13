from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


class UpdateListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    def update(self, request, *args, **kwargs):
        if self.request.method == 'PUT':
            error_data = {
                "type": "client_error",
                "errors": [
                    {
                        "code": "method_not_allowed",
                        "detail": "Метод 'PUT' не разрешен.",
                        "attr": None
                    }
                ]
            }
            return Response(error_data, status=HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass
