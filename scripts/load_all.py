"""
python manage.py runscript load_all

"""

import csv
import logging
import os
import re
import select
from collections import namedtuple

# from curses import raw
from datetime import datetime
from importlib.resources import contents
from pathlib import Path
from time import strptime
from venv import logger
from xmlrpc.client import Boolean

from django.contrib.auth.models import User
from genericpath import isfile

from nascar.models import (
    AutoManufacturer,
    Person,
    Race,
    RaceResult,
    RaceSettings,
    RacingSeries,
    Role,
    Team,
    Track,
)

date_format = "%m-%d-%Y"
# the race results data source , .txt files
source_txt_race_file = (
    Path(__file__).resolve().parent.parent.parent / "beerme2" / "data"
)
source_txt_race_file = RaceSettings.objects.get(contents="race_results")
source_csv_files = Path(__file__).resolve().parent.parent / "scripts" / "csv"

# logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=Path(__file__).resolve().parent.parent
    / "scripts"
    / "logs"
    / "load_all.txt",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)

from datetime import datetime


def is_valid_date(date_str):
    # Checks if a date string is valid ISO 8601 format
    # Returns True if valid, False otherwise
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False


class RaceData:
    """_summary_
    When passed a file name, parse the track and race date from the file name
    """

    def __init__(self, race: Race) -> None:

        self._race_date = race.race_date
        # print(f"RaceData() -> {self.race_date}")
        race = Race.objects.get(race_date=self._race_date)
        self._race_track = race.track
        # print(f"RaceData() -> {self._race_track}")
        # print(f"{r.race_date} {race_date}")
        file_race_date = str(self._race_date).split("-")
        try:
            file_race_date = datetime.strptime(
                str(self._race_date), "%Y-%m-%d"
            ).strftime("%m-%d-%Y")
        except Exception as e:
            print(f"{self.race_date} {e}")
            exit()
        # print(f"RaceData() -> {file_race_date}")
        # self._raw_race_date = raw_race_date
        self._reload = False
        self._src_path = RaceSettings.objects.get(contents="race_results")
        # print(f"RaceData() -> {self._src_path}")
        # exit()
        # self._file_name = pfile_name
        # self._race_track = pfile_name.split("_")[1]
        # self.race_date = re.findall(r"\d+-\d+-\d+", pfile_name)[0]
        # self.race_date = datetime.strptime(self.race_date, "%m-%d-%Y").strftime(
        #     "%Y-%m-%d"
        # )
        # if not is_valid_date(self.race_date):
        #     logger.debug(f"Bad date exiting {self.race_date} {self.file_name}")
        #     exit()
        self._src_file_name =  f"{self._src_path}results_{self._race_track}_{file_race_date}_.txt"

    def is_valid(self) -> Boolean:
        valid = False
        if (
            self._race_track and self._race_date and self._src_path and self._file_name
        ) is not None:
            valid = True
        else:
            valid = False

        return valid

    # @property
    # def raw_race_date(self):
    #     return self._raw_race_date

    @property
    def reload(self):
        return self._reload

    @reload.setter
    def reload(self, value):
        self._reload = value

    @property
    def race_date(self):
        return self._race_date

    @race_date.setter
    def race_date(self, value):
        self._race_date = value

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
        return f"race_date={self.race_date}"


def check_env(dir_name):
    """
    when passed a directory name, it
    returns a list of race results file names
    """
    if Path.exists(dir_name):
        race_list = []
        for f in os.listdir(dir_name):
            if f.__contains__("results_"):
                race_date = RaceData(f, dir_name)
                race_list.append(race_date)
                logger.info(f)
        logging.info(f"Found {len(race_list)} Race results in {dir_name}")
        return race_list
    logging.debug(f"{dir_name} does not exist! Fatal exiting...")
    print(f"{dir_name} does not Exist, exiting...!")
    exit()


def load_tracks(race_list: list):
    """
    Passed a list of races and checks to see if the track exists
    If the track does not exist, the track is inserted intp the database and logged
    """
    user = User.objects.get(pk=1)
    for race in race_list:
        # print(f"load_tracks() -> {race.race_track}")
        if not Track.objects.filter(name=race.race_track).exists():
            track = Track()
            track.name = race.race_track
            track.user = user
            track.save()
            logging.info(f"+ Track {track}")


def load_races(race_list):
    print(f"Calling load_races() -> {len(race_list)}")
    user = User.objects.get(pk=1)
    for race in race_list:
        # if the race does not exist, create the race entry in the Race table
        print(f"load_races() -> race = {race}")
        if not Race.objects.filter(race_date=race.race_date).exists():
            print(f"Create race {race.race_date} {race.raw_race_date}")
            the_track = Track.objects.get(name=race.race_track)
            # print(f"{the_track}")
            the_race = Race()
            the_race.name = the_track.name
            print(f"load_races() -> the_date = {race.race_date}")
            exit()
            if is_valid_date(race.race_date):
                the_race.race_date = race.race_date
            else:
                print(
                    f"load_races() -> Bad Race Date Information {the_track.name} {the_race.race_date}"
                )
                exit()
            the_race.user = user
            the_race.track = the_track
            the_race.save()
            logger.debug(f"Created race {the_race}")


def load_roles():
    roles = ["Driver", "Owner", "Crew Chief"]
    for role in roles:
        if not Role.objects.filter(name=role).exists():
            new_role = Role()
            new_role.name = role
            new_role.save()
            logger.info(f"Added New Role {role}")
            # print(f"Added New Role {role}")


def load_results(race_list):
    """Passed a list of races"""
    print(f"Calling load_results() -> {len(race_list)}")
    user = User.objects.get(pk=1)
    for race in race_list:
        print(f"load_results -> {race} {race.reload}")
        if race.reload == True:
            load_results_file(race)


def look_up_person(person_name, role="Driver", update=False):
    try:
        if update == False:
            return Person.objects.get(name=person_name)
        person = Person.objects.get(name=person_name)
        role = Role.objects.get(name=role)
        return _extracted_from_look_up_person_7(person, role)
    except Person.DoesNotExist as e:
        # person = Person()
        # TODO: many to many insert
        role = Role.objects.get(name=role)
        person.name = person_name
        person.save()
        logger.debug(f"Created person {person} {__name__}")
        return _extracted_from_look_up_person_7(person, role)


# TODO Rename this here and in `look_up_person`
def _extracted_from_look_up_person_7(person: Person, role):
    if person.role == role:
        return person
    person.role.add(role)
    person.save()
    return person


def look_up_driver(driver_name, role="Driver"):
    try:
        return Person.objects.get(name=driver_name, role=Role.objects.get(name=role))

    except Person.DoesNotExist as e:
        driver = Person()
        # TODO: many to many insert
        role = Role.objects.get(name=role)
        driver.name = driver_name
        driver.save()
        driver.role.add(role)
        driver.save()
        logger.debug(f"Created {role} {driver}")
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
    """__Passed a anchored file name__

    Args:
        race (_type_): _an anchored file name with the results data in the file_
    """
    print(f"load_results_file() -> loading... {race.src_file_name}")
    if not os.path.isfile(race.src_file_name):
        print(f"Race Results do not exist exiting... {race.src_file_name}")
        exit()
    with open(race.src_file_name) as f:
        reader = csv.reader(f, delimiter="\t")
        RaceInfo = namedtuple("RaceInfo", next(reader), rename=True)
        the_race = Race.objects.get(race_date=race.race_date)
        if RaceResult.objects.filter(race=the_race, reload=False):
            # print(f"{the_race} is already loaded!")
            return
        # remove the old race results
        results_to_be_deleted = RaceResult.objects.get(race_id=the_race.id)
        print(f"results_to_be_deleted = {the_race.id} {results_to_be_deleted}")
        # results_list.objects.all().delete()

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
                logger.debug(f"Not found {race} {e} {driver_results.driver}")
                exit()


def look_up_team(name, owner=""):
    try:
        return Team.objects.get(name=name)
    except Team.DoesNotExist as e:
        team = Team()
        team.name = name
        team.owner = owner
        # TODO: look up racing series and insert if not there
        team.series = RacingSeries.objects.get(name="NASCAR")
        team.save()
        logger.debug(f"Created team {team.name}")
        return team


def load_person_teams():

    # print(source_csv_files)
    logger.debug(f"Source of the data is {source_csv_files}")
    with open(f"{source_csv_files}/persons.csv") as f:
        reader = csv.reader(f, delimiter=",")
        PersonInfo = namedtuple("PersonInfo", next(reader), rename=True)
        for header in reader:
            person_info = Person()
            data = PersonInfo(*header)
            # print(f"{data.name}")
            person = look_up_person(data.name, data.role, update=True)
            person.website = data.website
            person.slug = data.slug
            person.save()
            team = look_up_team(data.team, data.owner)
            team.website = data.teamwebsite
            team.save()
            person.team.add(team)
            person.save()


def check_db():
    """
    Looks at the datbase Race table and checks the reload field. If checked the race is added to the list

    """
    race_list = []
    load_race_results = Race.objects.all()
    for race in load_race_results:
        race_data = RaceData(race)
        # print(f"check_db() -> {race_data.src_file_name}")
        # print(
        #     f"Check_db -> {race_data.reload} {race_data.src_file_name}"
        # )
        race_list.append(race_data)
        CreateResultsFile(race_data.src_file_name)
    # for x in race_list:
    #     print(f"Check_db() -> {x.file_name}")
    return race_list


def CreateResultsFile(results_file_name):
    """
    If filename exists just exit, else create a empty file with the race track and date

    Args:
        results_file_name (_type_): _description_
    """
    results_file = Path(results_file_name)
    if not results_file.is_file():
        print(f"CreateResultsFile -> {results_file_name}")
        try:
            # Create an empty file
            with open(results_file_name, "w"):
                pass
        except Exception as e:
            print(f"{e}")
            exit()


def run():
    logging.info("Hello World")
    # the data files come from beer me
    # race_list = check_env(source_txt_race_file)
    race_list = check_db()
    # for r in race_list:
    #     print(f"{r}")
    load_roles()
    load_tracks(race_list)
    load_races(race_list)
    load_results(race_list)
    load_person_teams()
