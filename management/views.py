from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

from management.models import Team, Member
from management.pagination import MemberPagination
from management.permissions import IsAdminOrReadOnly
from management.serializers import (
    TeamSerializer,
    TeamListSerializer,
    MemberSerializer,
    MemberListSerializer,
    MemberDetailSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.prefetch_related("members")
    serializer_class = TeamSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TeamListSerializer
        return TeamSerializer

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type=OpenApiTypes.STR,
                description="Filter by name(ex. ?name=Lak)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.prefetch_related("teams")
    serializer_class = MemberSerializer
    pagination_class = MemberPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return MemberListSerializer
        if self.action == "retrieve":
            return MemberDetailSerializer
        return MemberSerializer

    def get_queryset(self):
        queryset = self.queryset
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        team = self.request.query_params.get("team")

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "first_name",
                type=OpenApiTypes.STR,
                description="Filter by first_name(ex. ?first_name=Will)",
            ),
            OpenApiParameter(
                "last_name",
                type=OpenApiTypes.STR,
                description="Filter by last_name(ex. ?last_name=Smith)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
