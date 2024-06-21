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
file_path = Path.cwd() / "scripts" / "results"
logging.basicConfig(
    filename=Path.cwd() / "scripts" / "logs" / "log_load_races.txt",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)


def get_track(track_name: str):
    try:
        logging.info(f"Finding {track_name}")
        track = Track.objects.get(name=track_name)  # configuration=data.CONFIGURATION
        print(f"Found track {track_name} ok!")
        logging.info(f"Found {track_name} ok!")
        return track
    except Track.DoesNotExist as e:
        print(f"Creating Track {track_name}")
        try:
            track = Track()
            track.name = track_name
            track.save()
            return track
        except Track.DoesNotExist as e:
            logging.info(f"Create {track.name} failed, exiting at get_track()!")
            exit(-1)


def run():
    user = User.objects.get(pk=1)
    # find all the csv files and get the race header information for the track and date
    for race in file_path.glob("*.csv"):
        logging.info(f"race={race}")
        with open(race) as f:
            reader = csv.reader(f, delimiter="\t")
            RaceInfo = namedtuple("RaceInfo", next(reader), rename=True)
            for row in reader:
                data = RaceInfo(*row)
                # logging.info(f"{data}")
                # for row in reader:
                logging.info(f"data.DATE={data.RACE_DATE}")
                track = get_track(data.TRACK)
                try:
                    race = Race.objects.get(race_date=data.RACE_DATE, track=track)
                    print(f"Found race {track} {race} ok!")
                    break
                except Race.DoesNotExist as e:
                    print(f"Race: {e} race_date='{data.RACE_DATE}'")
                    exit(-1)
                    # logging.info(f"\nSkipping - race={data}")
                logging.info(f"\nInserting - {data}")
                race = Race()
                race.user = user
                # logging.info(f"{data.RACE_DATE}")
                race.race_date = data.RACE_DATE
                race.save()
                # logging.info(f"{race}")
