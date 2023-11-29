import logging
import re
import sys

from datetime import datetime
from functools import cached_property

from client.day import DayClient
from client.race import RaceClient
from client.training_block import TrainingBlockClient
from printer import Printer

date_format = "%Y-%m-%d"
logger = logging.getLogger(name=__name__)


class Menu:
    def __init__(self, con, cur):
        self.con = con
        self.cur = cur

    @cached_property
    def day(self) -> DayClient:
        """
        day() caches a DayClient for use the duration of the process

        :return: a DayClient
        """
        return DayClient(con=self.con, cur=self.cur)
        # end day()

    @cached_property
    def printer(self) -> Printer:
        """
        printer() caches a Printer client for use the duration of the process

        :return: a Printer client
        """
        return Printer(con=self.con, cur=self.cur)
        # end printer()

    @cached_property
    def race(self) -> RaceClient:
        """
        race() caches a RaceClient for use the duration of the process

        :return: a RaceClient
        """
        return RaceClient(con=self.con, cur=self.cur)
        # end race()

    @cached_property
    def tb(self) -> TrainingBlockClient:
        """
        tb() caches a TrainingBlockClient for use the duration of the process

        :return: a TrainingBlockClient
        """
        return TrainingBlockClient(con=self.con, cur=self.cur)
        # end tb()

    @staticmethod
    def is_date(date: str = None) -> bool:
        """
        is_date() checks if the provided str is datetime convertable

        :param date: date str
        :return: bool
        """
        try:
            datetime.strptime(date, date_format)
            return True
        # end try
        except ValueError:
            return False
        # end except
        # end is_date()

    @staticmethod
    def is_url(url: str = None) -> bool:
        """
        is_url() checks if the provided str matches a URL REGEX
        for REGEX ref. https://www.geeksforgeeks.org/python-check-url-string/

        :param url: URL str
        :return: bool
        """
        if len(url) == 0:
            return True
        # end if
        if url is None:
            return False
        # end if
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|"\
                r"(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, url)
        if len(url) == 0:
            print("invalid url!")
            return False
        # end if
        return True
        # end is_url()

    def main(self):
        self.printer.print_race_menu()

        while True:
            params = input("~ ").lower().strip().split(' ')
            cmd = params[0]
            params.remove(cmd)

            if cmd == "ls" or cmd == "list":
                self.printer.print_races()
            # end if "ls"

            elif cmd == 'e' or cmd == "edit":
                race_name = input("name: ").strip()
                if not self.race.validate_name(name=race_name):
                    print("please select an existing name!")
                    print()
                    continue
                # end if
                else:
                    self.edit_menu(name=race_name)
                    self.printer.print_race_menu()
                # end else
            # end if 'e'

            elif cmd == 'a' or cmd == "add":
                self.add_race_wizard()
            # end elif 'a'

            elif cmd == "rm" or cmd == "remove":
                race_name = input("name: ").strip()
                if not self.race.validate_name(race_name):
                    print("please select an existing name!")
                    print()
                    continue
                # end if
                confirmation = input(f"are you sure you want to remove {race_name}? (y/n): ").strip().lower()
                x = 0
                while x < 4 and not confirmation == 'y':
                    if confirmation == 'n':
                        break
                    confirmation = input(f"remove {race_name}? (y/n):  ").strip().lower()
                    x += 1
                # end while

                if confirmation == 'y':
                    self.race.delete_race_by_name(name=race_name)
                    print(f"{race_name} was deleted!")
                    print()
                # end if
                else:
                    print("cancelled!")
                    print()
                    continue
                # end else
            # end elif "rm"

            elif cmd == 'h' or cmd == "help":
                self.printer.print_race_menu()
            # end elif 'h'

            elif cmd == 'm' or cmd == "menu":
                self.printer.print_main_menu()
                return
            # end elif 'm'

            elif cmd == 'x' or cmd == "exit":
                sys.exit("bye :)")
            # end elif 'x'
        # end while
        # end main()

    def add_race_wizard(self, training_block_id: str = None):
        input_name = input("name (64 char. limit): ").strip()
        x = 0
        while x < 4 and self.race.validate_name(name=input_name):
            input_name = input("name taken! try again: ").strip()
            x += 1
        # end while
        if self.race.validate_name(name=input_name):
            print("max tries exceeded!")
            print()
            return
        # end if
        race_name = input_name

        input_date = input("race date (YYYY-MM-DD): ").strip()
        x = 0
        while x < 4 and not self.is_date(date=input_date):
            input_date = input("invalid date! try again: ").strip()
            x += 1
        # end while
        if not self.is_date(date=input_date):
            print("max tries exceeded!")
            print()
            return
        # end if
        race_date = datetime.strptime(input_date, date_format)

        if training_block_id is not None:
            day = self.day.get_day_by_training_block_id_and_date(
                date=race_date,
                training_block_id=training_block_id
            )
            if day is None:
                print("day not found in training block!")
                print()
                return
            # end if
            day_id = day[0]
        # end if
        else:
            attach = input("attach to training block (y/n): ").strip().lower()
            if attach == 'y':
                training_block_name = input("training block name: ").strip()
                x = 0
                while x < 4 and not self.tb.validate_name(name=training_block_name):
                    training_block_name = input("invalid training block! try again: ").strip()
                    x += 1
                # end while

                if not self.tb.validate_name(name=training_block_name):
                    print("max tries exceeded!")
                    print()
                    return
                # end if

                training_block = self.tb.get_training_block_by_name(name=training_block_name)
                training_block_id = training_block[0]
                day = self.day.get_day_by_training_block_id_and_date(
                    training_block_id=training_block_id,
                    date=race_date
                )
                if day is not None:
                    day_id = day[0]
                else:
                    day_id = self.day.add_day(date=race_date, miles=0)
            # end if
            else:
                day_id = self.day.add_day(date=race_date, miles=0)
                # end if
            # end else
        # end else

        miles = input("miles: ").strip()
        x = 0
        while x < 4 and (not miles.isdigit() or int(miles) < 0):
            print("try again!")
            miles = input("~ ").strip()
            x += 1
        # end while

        if not miles.isdigit():
            print("max tries exceeded! please provide a #!")
            print()
            return
        # end if
        miles = int(miles)
        if miles < 0:
            print("max tries exceeded! # of miles has to be > 0!")
            print()
            return
        # end if

        url = input("url (hit ENTER for none): ").strip()
        x = 0
        while x < 4 and not self.is_url(url=url):
            url = input("invalid URL! try again: ").strip()
            x += 1
        # end while

        if not self.is_url(url=url):
            print("max tries exceeded!")
            print()
            return
        # end if

        self.race.add_race(
            day_id=day_id,
            miles=miles,
            name=race_name,
            training_block_id=training_block_id,
            url=url
        )

        print(f"{race_name} added!")
        print()
        # end add_race_wizard()

    def edit_menu(self, name: str = None):
        """
        edit_race_menu() is responsible for interactions with a specific race

        :param name: name of the race to interact with
        :return: none
        """
        self.printer.print_race_edit_menu()
        race = self.race.get_race_by_name(name=name)
        race_id = race[0]

        while True:
            params = input("~ ").lower().strip().split(' ')
            cmd = params[0]
            params.remove(cmd)

            if cmd == 'p' or cmd == "print":
                self.printer.print_race(race=race)
            # end if 'p'

            elif cmd == 'e' or cmd == "edit":
                if len(params) == 1:
                    if params[0] == "date":
                        day_id = self.race.get_day_id_by_name(name=name)
                        day = self.day.get_day_by_id(day_id=day_id)
                        date = day[1]
                        training_block_id = day[4]  # for later...
                        print(f"current: {date}")
                        input_date = input("new date (YYYY-MM-DD):").strip()
                        x = 0
                        while x < 4 and not self.is_date(date=input_date):
                            print("invalid date!")
                            input_date = input("new date (YYYY-MM-DD):").strip()
                            x += 1
                        # end while

                        if not self.is_date(date=input_date):
                            print("invalid date!")
                            continue
                        # end if
                        date = datetime.strptime(input_date, date_format)

                        if training_block_id is None:  # later
                            day_id = self.day.add_day(date=date)
                            if day_id is None:
                                print("day could not be created!")
                                continue
                            # end if
                        # end if
                        else:
                            day_id = self.day.get_day_by_training_block_id_and_date(
                                date=date,
                                training_block_id=training_block_id
                            )
                        # end else

                        if day_id is None:
                            print("day not found in the training block!")
                            continue
                        # end if

                        self.race.update_day_id_by_id(
                            race_id=race_id,
                            day_id=day_id
                        )
                        print(f"{name} date updated to {date}!")
                        print()
                    # end if "date"

                    elif params[0] == "name":
                        print(f"current name: {name}")
                        input_name = input("new name (64 char. limit): ").strip()
                        x = 0
                        while x < 4 and self.race.validate_name(name=input_name):
                            input_name = input("name taken! try again: ").strip()
                            x += 1
                        # end while

                        if self.race.validate_name(name=input_name):
                            print("a valid name was not provided!")
                            continue
                        # end if
                        self.race.update_name_by_id(race_id=race_id, name=input_name)
                        print(f"\"{name}\" was updated to \"{input_name}\"!")
                        print()
                    # end elif "name"

                    elif params[0] == "miles":
                        miles = self.race.get_miles_by_name(name=name)
                        print(f"current: {miles}")
                        input_miles = input("new miles: ").strip()
                        x = 0
                        while x < 4 and not input_miles.isdigit():
                            print("invalid character!")
                            input_miles = input("new miles: ").strip()
                            x += 1
                        # end while

                        if not input_miles.isdigit():
                            print("please provide a #!")
                            print()
                            continue
                        # end if

                        miles = int(input_miles)
                        if miles < 0:
                            print("miles must be > 0!")
                            print()
                            continue
                        # end if

                        self.race.update_miles_by_id(race_id=race_id, miles=miles)
                        print(f"{name} miles were updated to {miles}!")
                        print()
                    # end elif "miles"

                    elif params[0] == "url":
                        url = self.race.get_url_by_name(name=name)
                        print(f"current: {url}")
                        input_url = input("new: ").strip()
                        x = 0
                        while x < 4 and not self.is_url(url=input_url):
                            print("invalid URL!")
                            input_url = input("new: ").strip()
                            x += 1
                        # end while

                        if not self.is_url(url=input_url):
                            print("invalid URL!")
                            print()
                            continue
                        # end if

                        self.race.update_url_by_id(race_id=race_id, url=input_url)
                        print(f"{name} URL was updated to {input_url}!")
                        print()
                    # end elif "url"
                # end if
                else:
                    print("please provide a field to update! (date, name, miles, url)")
                    print()
                # end else
            # end elif 'e'

            elif cmd == 'd' or cmd == "delete":
                confirmation = input("are you sure? (y/n): ").strip().lower()
                x = 0
                while x < 4 and not confirmation == 'y':
                    if confirmation == 'n':
                        break
                    confirmation = input("(y/n): ").strip().lower()
                    x += 1
                # end while

                if confirmation == 'y':
                    self.race.delete_race_by_id(race_id=race_id)
                    print(f"{name} was deleted!")
                    print()
                    return
                # end if
                else:
                    print("cancelled!")
                    print()
                    continue
                # end else
            # end elif 'd'

            elif cmd == 'h' or cmd == "help":
                self.printer.print_race_edit_menu()
            # end elif 'h'

            elif cmd == 'm' or cmd == "menu":
                return
            # end elif 'x'

            elif cmd == 'x' or cmd == "exit":
                sys.exit("bye :)")
            # end elif 'x'
        # end while
        # end edit_race_menu()

    # end Menu

# end of file
