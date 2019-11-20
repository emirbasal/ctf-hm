from .models import Challenge, ChallengeType
from rest_framework import viewsets, permissions, mixins
from .serializers import (
    ChallengeListSerializer,
    ChallengeTypeListSerializer,
    ChallengeDetailSerializer,
    ChallengeCreateSerializer,
    ChallengeTypeCreateSerializer
)


#(Controller in Springboot)
class ChallengeListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeListSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class ChallengeCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeCreateSerializer
    permission_classes = [
        permissions.IsAdminUser
    ]


# class ChallengeDetailViewSet(viewsets.ModelViewSet):
#     queryset = Challenge.objects.all()
#     serializer_class = ChallengeDetailSerializer
#     permission_classes = [
#         permissions.AllowAny
#     ]
#
#     def get_object(self):
#         pk = self.kwargs.get('pk')
#         return self.request.challenge
#
#     def get(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = ChallengeDetailSerializer
#         return Response(serializer.data)


class ChallengeTypeListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ChallengeType.objects.all()
    serializer_class = ChallengeTypeListSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class ChallengeTypeCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ChallengeType.objects.all()
    serializer_class = ChallengeTypeCreateSerializer
    permission_classes = [
        permissions.IsAdminUser
    ]


