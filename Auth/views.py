import requests
from rest_framework import permissions, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from Auth.models import Person
from Auth.serializers import PersonWriteSerializer, PersonReadSerializer


class AuthViewSet(GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PersonReadSerializer
    queryset = Person.objects.all()

    @list_route(methods=['post'])
    def register(self, request, **kwargs):
        serializer = PersonWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Token.objects.get_or_create(user=user)
        return Response(self.serializer_class(user).data)


class TodoViewSet(GenericViewSet, mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        data = requests.get('https://jsonplaceholder.typicode.com/todos')
        if data.status_code != 200:
            return Response({'error': 'Unable to get data'}, status=data.status_code)
        filtered_data = list(filter(lambda d: d['id'] % 2 == user_id % 2, data.json()))
        return Response(filtered_data)

