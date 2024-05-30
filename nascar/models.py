from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Base(models.Model):
    createdAt = models.DateTimeField("date created", auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updatedAt = models.DateTimeField("date last updated", auto_now=True, null=True)

    class Meta:
        abstract = True

class Team(Base):
    name = models.CharField(max_length=32)
    def __str__(self) -> str:
        return self.name
    
class Driver(Base):
    name = models.CharField(max_length=32, default="", null=False)
    # car_no = models.IntegerField(default=99)
    # sponsor = models.CharField(max_length=64, default="N/A")
    # make = models.CharField(max_length=32, default="N/A")
    # team = models.CharField(max_length=64, default="N/A")
    # salary = models.IntegerField(default=3000)
    # starting_position = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name

    class Meta:
        unique_together = ["name", "team"]
        ordering = ["name"]

class Track(Base):
    name = models.CharField(max_length=32)
    def __str__(self) -> str:
        return self.name

class Race(Base):
    name = models.CharField(max_length=64)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, null=True)
    race_date = models.DateTimeField(null=True)
    drivers = models.ManyToManyField(Driver)
    def __str__(self) -> str:
        return self.name
    