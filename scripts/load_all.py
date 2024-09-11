"""
python manage.py runscript load_all

"""

import csv
import os
import re
from collections import namedtuple
from datetime import datetime
from pathlib import Path
from venv import logger

from django.contrib.auth.models import User

from nascar.models import AutoManufacturer, Person, Race, RaceResult, Role, Track

date_format = "%m-%d-%Y"
source_txt_race_file = (
    Path(__file__).resolve().parent.parent.parent / "beerme2" / "data"
)
target_csv_race_file = Path(__file__).resolve().parent.parent / "scripts" / "csv"


class RaceData:
    """_summary_
    When passed a file name, parse the track and race date from the file name
    """

    def __init__(self, pfile_name, src_path=source_txt_race_file) -> None:

        self.file_name = pfile_name
        self._race_track = pfile_name.split("_")[1]
        self.race_date = re.findall(r"\d+-\d+-\d+", pfile_name)[0]
        self.race_date = datetime.strptime(self.race_date, "%m-%d-%Y").strftime(
            "%Y-%m-%d"
        )
        self._src_file_name = src_path / self.file_name

    @property
    def src_file_name(self):
        return self._src_file_name

    @property
    def race_track(self):
        return self._race_track

    @race_track.setter
    def race_track(self, value):
        self._race_track = value

    def __str__(self):
        return f"{self.race_date} - {self.race_track}"


def check_env(dir_name):
    """when passed a directory name, it
    returns a list of race results file names
    """
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
            print(f"{the_track}")
            driver_results = Race()
            driver_results.name = the_track.name
            driver_results.race_date = race.race_date
            driver_results.user = user
            driver_results.track = the_track
            driver_results.save()


def load_roles():
    roles = ["Driver", "Owner", "Crew Chief"]
    for role in roles:
        if not Role.objects.filter(name=role).exists():
            new_role = Role()
            new_role.name = role
            new_role.save()
            logger.info(f"Added New Role {role}")
            print(f"Added New Role {role}")


def load_results(race_list):
    """Passed a list of races"""
    user = User.objects.get(pk=1)
    for race in race_list:
        # print(f"{race.file_name}")
        if Race.objects.filter(race_date=race.race_date).exists():
            load_results_file(race)


def look_up_driver(driver_name):
    try:
        return Person.objects.get(
            name=driver_name, role=Role.objects.get(name="Driver")
        )

    except Person.DoesNotExist as e:
        driver = Person()
        # TODO: many to many insert
        role = Role.objects.get(name="Driver")
        driver.name = driver_name
        driver.save()
        driver.role.add(role)
        driver.save()
        return driver


def look_up_manufacturer(manufacturer_name):
    try:
        return AutoManufacturer.objects.get(name=manufacturer_name)
    except AutoManufacturer.DoesNotExist as e:
        auto_manufacturer = AutoManufacturer()
        auto_manufacturer.name = manufacturer_name
        auto_manufacturer.save()
        return auto_manufacturer


def load_results_file(race):
    print(f"loading... {race}")
    with open(race.src_file_name) as f:
        reader = csv.reader(f, delimiter="\t")
        RaceInfo = namedtuple("RaceInfo", next(reader), rename=True)
        the_race = Race.objects.get(race_date=race.race_date)
        if RaceResult.objects.filter(race=the_race).exists():
            print(f"{the_race} is already loaded!")
            return
        for header in reader:
            driver_results = RaceResult()
            data = RaceInfo(*header)
            try:
                driver_results.race = the_race
                # check to make sure the driver is in the database
                # print(data.START)
                driver_results.start_pos = data.START
                driver_results.driver = look_up_driver(data.DRIVER)
                driver_results.car_no = data.CAR
                driver_results.manufacturer = look_up_manufacturer(data.MANUFACTURER)
                driver_results.laps = data.LAPS
                driver_results.start = data.START
                driver_results.led = data.LED
                driver_results.points = data.PTS
                driver_results.bonus = data.BONUS
                driver_results.penality = data.PENALTY
                driver_results.finish_pos = data.POS
                driver_results.save()
            except Exception as e:
                print(f"Exiting {race} {e} {driver_results.driver}")
                exit()


def run():
    print(f"Hello World!")
    # the data files come from beer me
    race_list = check_env(source_txt_race_file)
    load_roles()
    load_tracks(race_list)
    load_races(race_list)
    load_results(race_list)
