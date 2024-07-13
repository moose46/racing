import os
import re
from datetime import datetime
from pathlib import Path
from venv import logger

from django.contrib.auth.models import User

from nascar.models import Race, Role, Track

date_format = "%m-%d-%Y"
source_txt_race_file = (
    Path(__file__).resolve().parent.parent.parent / "beerme2" / "data"
)
target_csv_race_file = Path(__file__).resolve().parent.parent / "scripts" / "csv"


class RaceData:
    """_summary_
    When passed a file name, parse the track and race date from the file name
    """

    def __init__(self, pfile_name) -> None:

        self.file_name = pfile_name
        self._race_track = pfile_name.split("_")[1]
        self.race_date = re.findall(r"\d+-\d+-\d+", pfile_name)[0]
        self.race_date = datetime.strptime(self.race_date, "%m-%d-%Y").strftime(
            "%Y-%m-%d"
        )

    @property
    def race_track(self):
        return self._race_track

    @race_track.setter
    def race_track(self, value):
        self._race_track = value

    def __str__(self):
        return f"{self.race_date} - {self.race_track}"


def check_env(dir_name):
    if Path.exists(dir_name):
        race_list = []
        for f in os.listdir(dir_name):
            if f.__contains__("results_"):
                race_date = RaceData(f)
                race_list.append(race_date)
        return race_list
    print(f"{dir_name} does not Exist, exiting...!")
    exit()


def load_tracks(race_list):
    user = User.objects.get(pk=1)
    for race in race_list:
        if not Track.objects.filter(name=race.race_track).exists():
            track = Track()
            track.name = race.race_track
            track.user = user
            track.save()


def load_races(race_list):
    user = User.objects.get(pk=1)
    for race in race_list:
        if not Race.objects.filter(race_date=race.race_date).exists():
            the_track = Track.objects.get(name=race.race_track)
            # print(f"{the_track}")
            the_race = Race()
            the_race.name = the_track.name
            the_race.race_date = race.race_date
            the_race.user = user
            the_race.track = the_track
            the_race.save()


def load_roles():
    roles = ["Driver", "Owner", "Crew Chief"]
    for role in roles:
        if not Role.objects.filter(name=role).exists():
            new_role = Role()
            new_role.name = role
            new_role.save()
            logger.info(f"Added New Role {role}")
            print(f"Added New Role {role}")


def run():
    print(f"Hello World!")
    race_list = check_env(source_txt_race_file)
    load_roles()
    load_tracks(race_list)
    load_races(race_list)
