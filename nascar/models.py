from datetime import timezone
from os import name
from tkinter import CASCADE

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Base(models.Model):
    createdAt = models.DateTimeField("date created", auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    updatedAt = models.DateTimeField("date last updated", auto_now=True, null=True)

    class Meta:
        abstract = True


class RacingSeries(Base):
    def __str__(self) -> str:
        return f"{self.name}"

    name = models.CharField(max_length=32, null=False)
    # team = models.ForeignKey(Team, blank=True, on_delete=models.CASCADE)
    class META:
        verbose_name_plural = "Racing Series"
        # verbose_name = "Racing Series"
        label = "Racing Series"
class Team(Base):
    def __str__(self) -> str:
        return f"{self.name} - {self.series.name}"

    name = models.CharField(max_length=32)
    owner = models.CharField(max_length=32, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    series = models.ForeignKey(RacingSeries, on_delete=models.CASCADE, blank=True)


class Role(Base):
    name = models.CharField(max_length=32, null=False, blank=False)

    def __str__(self) -> str:
        return self.name

    class META:
        unique = ["name"]


class Person(Base):
    PERSON_ROLE_CHOICES = {
        "Owner": "OWNER",
        "Crew Chief": "CREW_CHIEF",
        "Driver": "DRIVER",
        "Crew Member": "CREW_MEMBER",
    }
    role = models.ManyToManyField(Role, blank=True)
    name = models.CharField(max_length=32, default="", null=False)
    website = models.URLField(null=True, blank=True)
    team = models.ManyToManyField(Team, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        # unique_together = ["name", "team"]
        ordering = ["name"]


class Track(Base):
    name = models.CharField(max_length=32)
    website = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Race(Base):
    name = models.CharField(max_length=64)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, null=True)
    race_date = models.DateTimeField(null=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


# class Role(Base):
#     name = models.CharField(max_length=32, null=False)


class AutoManufacturer(Base):
    name = models.CharField(max_length=32, null=False)

    def __str__(self) -> str:
        return self.name


class RaceResult(Base):
    """One Race One Driver"""

    def __str__(self) -> str:
        return f"{self.driver} {self.finish_pos}"

    MANUFACTURER_CHOICES = {
        "Chevrolet": "CHEVROLET",
        "Ford": "FORD",
        "Toyota": "TOYOTA",
    }
    team = models.ForeignKey(Team, on_delete=models.CASCADE,null=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Person, on_delete=models.CASCADE)
    # manufacturer = models.CharField(
    #     max_length=32, default="N/A", choices=MANUFACTURER_CHOICES
    # )
    manufacturer = models.ForeignKey(
        AutoManufacturer, on_delete=models.CASCADE, null=True
    )
    start_pos = models.IntegerField(default=-1)
    finish_pos = models.IntegerField(default=-1)
    car_no = models.IntegerField(default=-1)
    laps = models.IntegerField(default=11)
    start = models.IntegerField(default=-1)
    led = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    penality = models.IntegerField(default=0)

    # TODO: Fix a solution for verbose_name

    class META:
        verbose_name_plural = "Race Results"
        verbose_name = "Race Results"
