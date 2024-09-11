import string
from atexit import register

from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from nascar.models import (
    AutoManufacturer,
    Person,
    Race,
    RaceResult,
    RacingSeries,
    Role,
    State,
    Team,
    Track,
)

# Register your models here.


@admin.register(AutoManufacturer)
class AutoManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "series", "show_website"]
    list_filter = ["series"]
    ordering = ["name"]

    def show_website(self, instance):
        return format_html("<a href='{url}'>{url}</a>", url=instance.website)


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ["uname", "track", "race_date"]
    ordering = ["-race_date"]

    def uname(self, instance):
        return string.capwords(instance.name)


@admin.register(RacingSeries)
class RacingSeriesAdmin(admin.ModelAdmin):
    display_name = "Racing Series"


class PersonInLine(admin.TabularInline):
    model = Person.team.through


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["name", "show_website"]
    list_filter = ["role"]
    inlines = [PersonInLine]
    exclude = ["slug"]
    ordering = ["name"]

    def show_website(self, instance):
        return format_html("<a href='{url}'>{url}</a>", url=instance.website)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ["track_name", "state", "show_website"]
    ordering = ["name"]

    def show_website(self, instance):
        return format_html("<a href='{url}'>{url}</a>", url=instance.website)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ["state_name"]
    list_filter = ("name",)


@admin.register(RaceResult)
class RaceResultsAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = [
        "race",
        "driver_name",
        "finish_pos",
        "track_name",
        "race_date",
        "driver",
    ]
    list_filter = ("race__track__name", "race", "driver")
    ordering = ["driver"]

    def driver_name(self, instance):
        return instance.driver.name  # "Ralf Hale"

    def track_name(self, instance):
        return instance.race.track  # "Peoria Motor Speedway"

    def race_date(self, instance):
        return instance.race.race_date

    def team_name(self, instance):
        return instance.driver.team.name


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass
