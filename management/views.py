from rest_framework import viewsets

from management.models import Team, Member
from management.serializers import (
    TeamSerializer,
    MemberSerializer,
    MemberListSerializer,
    TeamListSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TeamListSerializer
        return TeamSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return MemberListSerializer
        return MemberSerializer
