from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet


class APIRootViewSet(GenericViewSet):
    """
    API root view.
    """
    def list(self, request):
        return Response({
            'users': reverse('user_detail', request=request),
            'time': reverse('time', request=request),
            'docs': reverse('docs', request=request),
        })
