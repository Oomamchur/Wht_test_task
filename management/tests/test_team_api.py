from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from management.models import Team
from management.serializers import TeamListSerializer

TEAM_URL = reverse("management:team-list")


def detail_url(team_id: int):
    return reverse_lazy("management:team-detail", args=[team_id])


def new_team(**params) -> Team:
    defaults = {"name": "Test name"}
    defaults.update(**params)
    return Team.objects.create(**defaults)


class UnauthenticatedTeamApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_team_list(self) -> None:
        new_team()
        new_team(name="Dynamo")

        teams = Team.objects.all()
        serializer = TeamListSerializer(teams, many=True)

        response = self.client.get(TEAM_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_team_retrieve(self) -> None:
        team = new_team()
        url = detail_url(team.id)
        serializer = TeamListSerializer(team)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_name(self) -> None:
        team1 = new_team()
        team2 = new_team(name="Dynamo")

        serializer1 = TeamListSerializer(team1)
        serializer2 = TeamListSerializer(team2)

        response = self.client.get(TEAM_URL, {"name": "dyn"})

        self.assertNotIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)

    def test_team_delete_forbidden(self) -> None:
        team = new_team()
        url = detail_url(team.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedTeamApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test123@test.com",
            "Test1234",
        )
        self.client.force_authenticate(self.user)

    def test_team_create_forbidden(self) -> None:
        payload = {"name": "Created"}

        response = self.client.post(TEAM_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminTeamApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin123@admin.com", "test1234", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_team_create(self) -> None:
        payload = {"name": "Created"}

        response = self.client.post(TEAM_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], payload["name"])

    def test_team_update(self) -> None:
        team = new_team()
        url = detail_url(team.id)
        payload = {"name": "Updated"}

        response1 = self.client.patch(url, payload)
        response2 = self.client.get(url)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["name"], payload["name"])

    def test_team_delete(self) -> None:
        team = new_team()
        url = detail_url(team.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
