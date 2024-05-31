from atexit import register

from django.contrib import admin
from django.utils.html import format_html

from nascar.models import Driver, Race, RaceDriver, Team, Track

# Register your models here.


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "show_website"]

    def show_website(self, instance):
        return format_html("<a href='{url}'>{url}</a>", url=instance.website)


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ["name", "track"]


@admin.register(Driver)
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(RaceDriver)
class RaceDriversAdmin(admin.ModelAdmin):
    list_display = ["race", "driver", "track_name", "race_date"]
    list_filter = ["race_id"]

    def track_name(self, instance):
        return instance.race.track  # "Peoria Motor Speedway"

    def race_date(self, instance):
        return instance.race.race_date
