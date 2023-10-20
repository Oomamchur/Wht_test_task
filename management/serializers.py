from rest_framework import serializers

from management.models import Team, Member


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name")


class TeamListSerializer(TeamSerializer):
    members = serializers.StringRelatedField(many=True)

    class Meta:
        model = Team
        fields = ("id", "name", "members")


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("id", "first_name", "last_name", "email", "teams")


class MemberListSerializer(MemberSerializer):
    teams = serializers.StringRelatedField(many=True)

    class Meta:
        model = Member
        fields = ("id", "first_name", "last_name", "teams")


class MemberDetailSerializer(MemberSerializer):
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = ("id", "first_name", "last_name", "email", "teams")
