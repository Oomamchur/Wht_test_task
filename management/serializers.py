from rest_framework import serializers

from management.models import Team, Human


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name")


class TeamListSerializer(TeamSerializer):
    class Meta:
        model = Team
        fields = ("id", "name")


class HumanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Human
        fields = ("id", "first_name", "last_name")


class HumanListSerializer(HumanSerializer):
    class Meta:
        model = Human
        fields = ("id", "first_name")
