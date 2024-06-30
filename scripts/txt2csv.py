"""_summary_
Prompt for race date
Open file 

"""

import os
from datetime import datetime
from pathlib import Path
from shutil import copyfile

date_format = "%m-%d-%Y"
from_race_data = Path.home() / "Documents" / "VisualCodeSource" / "beerme2" / "data"
target_race_data = Path.cwd() / "scripts" / "working"


def get_race_date():
    """_summary_

    Returns:
                                                                    _type_: _description_
                                                                                                                                    Returns a valid date
    """
    while True:
        race_date = input(f"Enter Race Date {date_format}:  ")
        try:
            race_date = "05-05-2019"
            datetime.strptime(race_date, date_format)
            return race_date
        except ValueError as e:
            print(e)


def check_env():
    if Path.exists(from_race_data):
        return os.listdir(from_race_data)
    print(f"{from_race_data} does not Exist, exiting...!")
    exit()


def run():
    dirs = []
    dirs = check_env()
    race_date = get_race_date()
    print(from_race_data)
    for f in dirs:
        if f.endswith(".txt") and f.__contains__("results_"):
            print(f)
            copyfile(from_race_data / f, target_race_data / f)
