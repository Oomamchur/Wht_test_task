from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Human(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    team = models.ForeignKey(
        Team,
        related_name="humans",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
