from django.test import TestCase

from management.models import Team, Member


class ModelsTests(TestCase):
    def test_team_str(self) -> None:
        team = Team.objects.create(name="test")

        self.assertEquals(str(team), team.name)

    def test_member_str(self) -> None:
        member = Member.objects.create(
            first_name="test_first_name", last_name="test_last_name"
        )

        self.assertEquals(
            str(member), f"{member.first_name} {member.last_name}"
        )
