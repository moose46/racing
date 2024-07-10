"""
	Reads drivers.csv file and imports races into the races table.
	If there are duplicates, it will ignore duplicates
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
		python manage.py runscript load_races_from_csv
"""

import csv
import datetime
import logging
import os
import sys
from collections import namedtuple
from pathlib import Path

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from nascar.models import Race, Track

# https://k0nze.dev/posts/python-relative-imports-vscode/

# https://k0nze.dev/posts/python-relative-imports-vscode/
file_path = Path.cwd() / "scripts" / "csv"
logging.basicConfig(
    filename=Path.cwd() / "scripts" / "logs" / "log_load_races.txt",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)


def get_track(track_name: str):
    try:
        logging.info(f"Finding {track_name}")
        track = Track.objects.get(
            name__contains=track_name.strip(),
        )  # configuration=data.CONFIGURATION

        # print(f"Found track {track_name} ok!")
        logging.info(f"Found {track_name.strip()} ok!")
        return track
    except Track.MultipleObjectsReturned as e:
        logging.debug(f"{track_name.strip()} - {e}")
        exit(-1)
    except Track.DoesNotExist as e:
        logging.warning(f"Creating Track {track_name}!")
        try:
            track = Track()
            track.name = track_name.title().strip()
            track.save()
            track.refresh_from_db()
            return track
        except Track.DoesNotExist as e:
            logging.info(f"Create {track.name} failed, exiting at get_track()!")
            exit(-1)


def create_race(race_date_converted, track: Track):
    print(f"Creating Race: {track.name} {race_date_converted}")
    new_race = Race()
    new_race.name = "N/A"
    new_race.race_date = race_date_converted
    new_race.track = track
    new_race.save()
    return new_race


def run():
    user = User.objects.get(pk=1)
    # find all the csv files and get the race header information for the track and date
    # for file_name in os.listdir(file_path):
    #     file = file_path / file_name
    #     if os.path.isfile(file):
    #         os.remove(file)
    for race_results in file_path.glob("*.csv"):
        # logging.info(f"race_results={race_results}")
        with open(race_results) as f:
            reader = csv.reader(f, delimiter="\t")
            RaceInfo = namedtuple("RaceInfo", next(reader), rename=True)
            # print(f"{RaceInfo._fields}")
            for row in reader:
                data = RaceInfo(*row)
                # logging.info(f"{data}")
                # for row in reader:
                race_date_converted = datetime.datetime.strptime(
                    data.RACE_DATE, "%m-%d-%Y"
                ).strftime("%Y-%m-%d")
                # print(f"type={type(race_date_converted)}")
                track = get_track(data.TRACK)
                # logging.info(
                #     f"track={track.name} data.DATE={data.TRACK} - {data.RACE_DATE}"
                # )
                break
                try:
                    race = Race.objects.get(
                        race_date=race_date_converted,
                        track=track,
                    )
                    print(f"Found race {track} {race} ok!")
                    break
                except Race.DoesNotExist as e:
                    print(f"Race Does Not Exist: {e} race_date='{data.RACE_DATE}'")
                    create_race(race_date_converted=race_date_converted, track=track)
                    # exit(-1)
                    logging.info(
                        f"\nCreated - race= {track.name} - {race_date_converted}"
                    )
                # logging.info(f"\nInserting - {data}")
                # race = Race()
                # race.user = user
                # # logging.info(f"{data.RACE_DATE}")
                # race.race_date = race_date_converted
                # race.save()
                # # logging.info(f"{race}")
