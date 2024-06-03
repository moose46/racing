from atexit import register

from django.contrib import admin
from django.utils.html import format_html

from nascar.models import (
    AutoManufacturer,
    Person,
    Race,
    RaceResults,
    RacingSeries,
    Role,
    Team,
    Track,
)

# Register your models here.


@admin.register(AutoManufacturer)
class AutoManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "show_website"]
    list_filter = ["series"]
    ordering = ["name"]

    def show_website(self, instance):
        return format_html("<a href='{url}'>{url}</a>", url=instance.website)


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ["name", "track"]


@admin.register(RacingSeries)
class RacingSeriesAdmin(admin.ModelAdmin):
    pass


class PersonInLine(admin.TabularInline):
    model = Person.team.through


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = [PersonInLine]
    exclude = ["team"]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ["name", "show_website"]

    def show_website(self, instance):
        return format_html("<a href='{url}'>{url}</a>", url=instance.website)


@admin.register(RaceResults)
class RaceResultsAdmin(admin.ModelAdmin):
    list_display = ["race", "driver", "track_name", "race_date"]
    list_filter = ["race_id", "driver"]

    def track_name(self, instance):
        return instance.race.track  # "Peoria Motor Speedway"

    def race_date(self, instance):
        return instance.race.race_date


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass
