from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from management.models import Team, Member
from management.serializers import (
    MemberListSerializer,
    MemberDetailSerializer,
    TeamSerializer,
)

MEMBER_URL = reverse("management:member-list")


def detail_url(member_id: int):
    return reverse_lazy("management:member-detail", args=[member_id])


def new_member(**params) -> Member:
    defaults = {
        "first_name": "Test first_name",
        "last_name": "Test last_name",
        "email": "test@email.com",
    }
    defaults.update(**params)
    return Member.objects.create(**defaults)


def new_team(**params) -> Team:
    defaults = {"name": "Test name"}
    defaults.update(**params)
    return Team.objects.create(**defaults)


class UnauthenticatedMemberApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_team_list(self) -> None:
        new_member()
        new_member(first_name="Alex", email="test@example.com")

        members = Member.objects.all()
        serializer = MemberListSerializer(members, many=True)

        response = self.client.get(MEMBER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_member_retrieve(self) -> None:
        member = new_member()
        url = detail_url(member.id)
        serializer = MemberDetailSerializer(member)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_first_name(self) -> None:
        member1 = new_member()
        member2 = new_member(first_name="Alex", email="test@example.com")

        serializer1 = MemberListSerializer(member1)
        serializer2 = MemberListSerializer(member2)

        response = self.client.get(MEMBER_URL, {"first_name": "al"})

        self.assertNotIn(serializer1.data, response.data["results"])
        self.assertIn(serializer2.data, response.data["results"])

    def test_filter_by_last_name(self) -> None:
        member1 = new_member()
        member2 = new_member(last_name="James", email="test@example.com")

        serializer1 = MemberListSerializer(member1)
        serializer2 = MemberListSerializer(member2)

        response = self.client.get(MEMBER_URL, {"last_name": "jam"})

        self.assertNotIn(serializer1.data, response.data["results"])
        self.assertIn(serializer2.data, response.data["results"])

    def test_member_delete_forbidden(self) -> None:
        member = new_member()
        url = detail_url(member.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedMemberApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test123@test.com",
            "Test1234",
        )
        self.client.force_authenticate(self.user)

    def test_member_create_forbidden(self) -> None:
        payload = {
            "first_name": "Alex",
            "last_name": "Black",
            "email": "test@example.com",
        }

        response = self.client.post(MEMBER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminMemberApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin123@admin.com", "test1234", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_member_create(self) -> None:
        payload = {
            "first_name": "Alex",
            "last_name": "Black",
            "email": "test@example.com",
        }

        response = self.client.post(MEMBER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], payload["first_name"])
        self.assertEqual(response.data["email"], payload["email"])

    def test_member_update(self) -> None:
        new_team()
        new_team(name="Dynamo")
        teams = Team.objects.all()
        payload = {
            "first_name": "Updated",
            "teams": [team.id for team in teams],
        }

        member = new_member()
        url = detail_url(member.id)

        response1 = self.client.patch(url, payload)
        response2 = self.client.get(url)

        serializer = TeamSerializer(teams, many=True)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["first_name"], payload["first_name"])
        self.assertEqual(response2.data["teams"], serializer.data)

    def test_member_delete(self) -> None:
        member = new_member()
        url = detail_url(member.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
