"""_summary_
Prompt for race date
Open file 

"""

import os
import re
from datetime import datetime
from pathlib import Path
from shutil import copyfile

from genericpath import isfile

date_format = "%m-%d-%Y"
source_txt_race_file = (
    Path.home() / "Documents" / "VisualCodeSource" / "beerme2" / "data"
)
target_txt_race_file = Path.cwd() / "scripts" / "txt"
target_csv_race_file = Path.cwd() / "scripts" / "csv"


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
    if Path.exists(source_txt_race_file):
        return os.listdir(source_txt_race_file)
    print(f"{source_txt_race_file} does not Exist, exiting...!")
    exit()


def add_headers(results_file_name):
    pass


def run():
    dirs = []
    dirs = check_env()
    race_date = get_race_date()
    print(source_txt_race_file)
    # clean directory first
    for file_name in os.listdir(target_txt_race_file):
        file = target_txt_race_file / file_name
        if os.path.isfile(file):
            os.remove(file)
    for file_name in os.listdir(target_csv_race_file):
        file = target_csv_race_file / file_name
        if os.path.isfile(file):
            os.remove(file)

    # copy race results files, from source directory to the target
    for f in dirs:
        if f.endswith(".txt") and f.__contains__("results_"):
            # print(f)

            copyfile(source_txt_race_file / f, target_txt_race_file / f)

    for f in target_txt_race_file.glob("results*_.txt"):
        race_track = f.stem.split("_")[1]
        race_date = re.findall(r"\d+-\d+-\d+", f.name)[
            0
        ]  # get the date from the file name
        print(f"Processing {race_track.capitalize()} - {race_date}")

        csv_filename = os.path.splitext(os.path.basename(f))[0]
        csv_filename = f"{csv_filename}.csv"
        print(f"{target_csv_race_file / csv_filename}.csv")
        with open(target_csv_race_file / csv_filename, "wt") as fo:
            fo.write("TRACK	RACE_DATE	CONFIGURATION\n")
            fo.writelines(f"{race_track.title()}	{race_date}	N/A\n")
            with open(source_txt_race_file / f, "rt") as txt_file:
                fo.write(txt_file.read())
