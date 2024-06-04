"""
    Reads drivers.csv file and imports drivers into the drivers table.
    If there are duplicates, it will stop, and throw up
    must have django-extensions installed and in entered into the INSTALLED_APPS settings file.
    
        INSTALLED_APPS = [
            "nascar.apps.NascarConfig",
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "django_extensions",
        ]

    to run:
        python manage.py runscript load_results_from_csv
"""

import csv
import logging
import os
import sys
from collections import namedtuple
from pathlib import Path

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from nascar.models import AutoManufacturer, Person, Race, RaceResult, Track,Role

# https://k0nze.dev/posts/python-relative-imports-vscode/
file_path = Path.cwd() / "scripts" / "results"
logging.basicConfig(
    filename=Path.cwd() / "scripts" / "logs" / "log_results_races.txt",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)


def check_if_race_is_already_loaded(race_date):
    try:
        race = Race.objects.get(race_date=race_date)
        logging.info(f"race_id={race.id}")
        results_data = RaceResult.objects.filter(race_id=race.id)
        # results_data = Results.objects.extra(
        #     select={
        #         "race_count": f"select count(*) from nascar_results where race_id={race.id}",
        #     }
        # )
        logging.critical(f"count={results_data.count()}")
        if results_data.count() > 0:
            results_data.delete()
    except Race.DoesNotExist as e:
        return False
    
def check_role_driver_exists():
    """ see if the role driver exists, if not create driver and return role else return role driver"""
    try:
        role = Role.objects.get(name='Driver')
        return role
    except Role.DoesNotExist as e:
        role = Role()
        role.name = 'Driver'
        role.save()
        return role
    return role
def check_auto_manufacturer_exists(auto_manufacturer):
    """ see if the manufacturer exists, if not create it and return manufacturer else return manufacturer"""
    try:
        manufacturer = AutoManufacturer.objects.get(name=auto_manufacturer)
        return manufacturer
    except AutoManufacturer.DoesNotExist as e:
        manufacturer = AutoManufacturer()
        manufacturer.name = auto_manufacturer
        manufacturer.save()
        return manufacturer
    return manufacturer

def run():
    logging.info(file_path)
    print(f"{file_path}")

    user = User.objects.get(pk=1)
    logging.info(f"user={user}")
    for race_results in file_path.glob("*.csv"):
        # results = f.stem.split("_")[1]
        logging.info(f"\nProcessing File={race_results.name}")
        # Get the race details from the first header in the race results file
        # TRACK,RACE_DATE
        # Mid Ohio, 07/10/1946
        # logging.critical(f"{race_results}")
        with open(race_results) as f:
            reader = csv.reader(f, delimiter="\t")
            RaceInfo = namedtuple("RaceInfo", next(reader), rename=True)
            for header in reader:
                data = RaceInfo(*header)
                # logging.info(f"\nRaceInfo={data}")
                try:
                    race = Race.objects.get(race_date=data.RACE_DATE)
                    check_if_race_is_already_loaded(race_date=data.RACE_DATE)
                    # logging.info(f"race={race}")
                except Race.DoesNotExist as e:
                    logging.critical(
                        f"The Race Date {data.RACE_DATE} is not in the Database, exiting ....  = {e}"
                    )
                    exit()
                ResultsInfo = namedtuple("ResultsInfo", next(reader), rename=True)
                for row in reader:
                    resultsInfo = ResultsInfo(*row)
                    # logging.critical(f"results={resultsInfo}")
                    role = check_role_driver_exists()
                    auto_manufacturer = check_auto_manufacturer_exists(resultsInfo.MANUFACTURER)
                    logging.info(f'role={role}')
                    try:
                        # logging.info(f"results={resultsInfo.DRIVER}")
                        driver = Person.objects.get(name=resultsInfo.DRIVER)
                        # logging.info(f"driver={driver}")
                    except Person.DoesNotExist as e:
                        # logging.debug(f"\n{resultsInfo.DRIVER} Not Found")
                        driver = Person()
                        driver.user = user
                        driver.name = resultsInfo.DRIVER
                        driver.save()
                        driver.role.set([role])
                        driver.save()
                        # results.driver = Driver.objects.get(name=Results.driver)
                    results = RaceResult()
                    results.user = user
                    results.driver = driver
                    results.race = race
                    results.car_no = resultsInfo.CAR
                    results.start_pos = resultsInfo.START
                    results.finish_pos = resultsInfo.POS
                    results.manufacturer = auto_manufacturer
                    results.save()

            # break
            #     race = Race()
            #     race.race_date = race_info.DATE
            #     race.track = track_info
            #     race.save()
            #     break
            # # Now get the race results data
            # RaceResults = namedtuple("RaceResults", next(reader), rename=True)
            # for row in reader:
            #     race_results = RaceResults(*row)

            #     logging.info(f"{race_results}")
            #     # print(race_results)

            #     r = Results()
            #     r.user = user
            #     r.car = race_results.CAR
            #     logging.critical(f"{race_results.DRIVER}")
            #     r.driver = Driver.objects.get(name=race_results.DRIVER)
            #     r.start_pos = race_results.START
            #     r.finish_pos = race_results.POS
            #     r.manufacturer = race_results.MANUFACTURER
            #     r.race = Race.objects.get(name=race_info.DATE)
            #     r.save()
    #     for row in f_csv:
    #         print(row)
    #         row = Row(*row)
    #         print(row.TRACK)
    #         d = Track()
    #         d.name = row.TRACK
    #         d.owner = row.OWNER
    #         d.track_length = row.MILES
    #         d.configuration = row.CONFIG
    #         d.city = row.CITY
    #         d.state = row.STATE
    #         d.user = user
    #         d.save()
