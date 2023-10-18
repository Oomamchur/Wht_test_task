from rest_framework import viewsets

from management.models import Team, Human
from management.serializers import (
    TeamSerializer,
    TeamListSerializer,
    HumanSerializer,
    HumanListSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TeamListSerializer
        return TeamSerializer


class HumanViewSet(viewsets.ModelViewSet):
    queryset = Human.objects.all()
    serializer_class = HumanSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return HumanListSerializer
        return HumanSerializer
