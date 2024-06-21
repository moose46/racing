import string
from datetime import timezone
from email import message
from os import name
from tkinter import CASCADE
from xml.dom import ValidationErr

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify


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


class Role(Base):
    name = models.CharField(max_length=32, null=False, blank=False, unique=True)

    def __str__(self) -> str:
        return self.name

    class META:
        unique = ["name"]


class Team(Base):
    def __str__(self) -> str:
        return f"{self.name} - {self.series.name}"

    name = models.CharField(max_length=32)
    owner = models.CharField(max_length=32, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    series = models.ForeignKey(RacingSeries, on_delete=models.CASCADE, blank=True)

    # def validate_unique(self, *args, **kwargs):
    #     super().validate_unique(*args, **kwargs)
    #     if self.__class__.objects.filter(series=self.series, name=self.name).exists():
    #         raise ValidationError(
    #             message=f"{self.name} and Racing Series {self.series} Already Exist"
    #         )

    # drivers = models.ManyToManyField(Person, blank=True)
    class META:
        unique_together = ["name", "series.name"]


class Person(Base):
    PERSON_ROLE_CHOICES = {
        "Owner": "OWNER",
        "Crew Chief": "CREW_CHIEF",
        "Driver": "DRIVER",
        "Crew Member": "CREW_MEMBER",
    }
    role = models.ManyToManyField(Role, blank=True)
    name = models.CharField(max_length=32, default="", null=False, unique=True)
    website = models.URLField(null=True, blank=True)
    team = models.ManyToManyField(Team, blank=True)
    slug = models.TextField(blank=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(f"{self.name}")
        print(self.slug)
        if update_fields is not None and name in update_fields:
            update_fields = {"slug"}.union(update_fields)
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def __str__(self) -> str:
        return self.name

    class Meta:
        # unique_together = ["name", "team"]
        ordering = ["name"]


class State(Base):
    name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return string.capwords(self.name)

    @property
    def state_name(self):
        return string.capwords(self.name)

    class META:
        unique = "name"
        ordering = "name"


class Track(Base):
    name = models.CharField(max_length=32, unique=True)
    website = models.URLField(null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    length = models.DecimalField(
        decimal_places=2, default=0.00, max_digits=2, blank=True
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True
    )  # Validators should be a list

    def __str__(self) -> str:
        return string.capwords(self.name)

    @property
    def track_name(self):
        return string.capwords(self.name)


class Race(Base):
    name = models.CharField(max_length=64)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, null=True)
    race_date = models.DateField(null=True)
    website = models.URLField(null=True, blank=True)
    laps = models.IntegerField(default=-1)

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
    team = models.CharField(max_length=64, null=True)
    # team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
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
        ordering = ["driver__name"]
