from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Member(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    teams = models.ManyToManyField(Team, related_name="members", blank=True)

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
