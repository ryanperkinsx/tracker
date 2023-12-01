import logging

from datetime import datetime
from functools import cached_property

from client.day import DayClient
from client.race import RaceClient
from client.training_block import TrainingBlockClient
from client.week import WeekClient

date_format = "%Y-%m-%d"
logger = logging.getLogger(name=__name__)


class Printer:
    """
    Printer is a class to house the various print methods
    """

    def __init__(self, con, cur, **kwargs):
        super().__init__(**kwargs)
        self.con = con
        self.cur = cur
        # end __init__()

    @cached_property
    def tb(self) -> TrainingBlockClient:
        """
        tb() caches a TrainingBlockClient for use the duration of the process

        :return: a TrainingBlockClient
        """
        return TrainingBlockClient(con=self.con, cur=self.cur)
        # end tb()

    @cached_property
    def week(self) -> WeekClient:
        """
        week() caches a WeekClient for use the duration of the process

        :return: a WeekClient
        """
        return WeekClient(con=self.con, cur=self.cur)
        # end week()

    @cached_property
    def day(self) -> DayClient:
        """
        day() caches a DayClient for use the duration of the process

        :return: a DayClient
        """
        return DayClient(con=self.con, cur=self.cur)
        # end day()

    @cached_property
    def race(self) -> RaceClient:
        """
        race() caches a RaceClient for use the duration of the process

        :return: a RaceClient
        """
        return RaceClient(con=self.con, cur=self.cur)
        # end race()

    @staticmethod
    def print_main_menu():
        """
        print_main_menu() prints the main menu options

        :return: none
        """
        print("----------------------")
        print("         cmds:")
        print("----------------------")
        print("(tb) training-blocks: opens the training block menu")
        print("(r)             race: opens the race menu")
        print("(h)             help: re-print the commands")
        print("(x)             exit: exit the process")
        print()
        # end print_main_menu()

    @staticmethod
    def print_training_block_menu():
        """
        print_training_block_menu() prints the menu options for the training block table

        :return: none
        """
        print("----------------------")
        print("         cmds:")
        print("----------------------")
        print("(ls)   list: list all the training blocks")
        print("(o)    open: open a training block")
        print("(a)     add: add a new training block")
        print("(rm) remove: remove an existing training block")
        print("(h)    help: print the menu")
        print("(m)    menu: returns to the main menu")
        print("(x)    exit: exits the process")
        print()
        # end print_training_block_menu()

    @staticmethod
    def print_training_block_open_menu():
        """
        print_training_block_open_menu() prints the menu options for the training block table

        :return: none
        """
        print("----------------------")
        print("         cmds:")
        print("----------------------")
        print("(p)   print: print the block")
        print("(d)    date: print the date ex. d <week> <day>")
        print("(u)  update: add data ex. u <week> <day> <miles>")
        print("(a)     add: add week(s) or a new race")
        print("(rm) remove: remove week(s) or an existing race")
        print("(r)    race: print the races within this training block")
        print("(h)    help: print the menu")
        print("(m)    menu: returns to the main menu")
        print("(x)    exit: exits the process")
        print()
        # end print_training_block_open_menu()

    @staticmethod
    def print_race_menu():
        """
        print_race_menu() prints the menu options for the race table

        :return: none
        """
        print("----------------------")
        print("         cmds:")
        print("----------------------")
        print("(ls)   list: list all the races")
        print("(o)    open: open a race")
        print("(a)     add: add a new race")
        print("(rm) remove: remove an existing race")
        print("(h)    help: print the menu")
        print("(m)    menu: returns to the main menu")
        print("(x)    exit: exits the process")
        print()
        # end print_race_menu()

    @staticmethod
    def print_race_edit_menu():
        """
        print_race_edit_menu() prints the menu options for the race table

        :return: none
        """
        print("----------------------")
        print("         cmds:")
        print("----------------------")
        print("(p)   print: re-print the race details")
        print("(e)    edit: edit the race")
        print("(d)  delete: delete the race")
        print("(h)    help: print the menu")
        print("(m)    menu: returns to the race menu")
        print("(x)    exit: exits the process")
        print()
        # end print_race_edit_menu()

    @staticmethod
    def format_week_day_miles(miles: int = None) -> str:
        """
        format_week_day_miles() provides formatting that supports mileage up to 99 miles
        for the pretty_print_training_block() function

        :param miles: # of miles
        :return: formatted str
        """
        if miles is not None:
            return f"{'.  ' if miles == 0 else f'{miles} ' if miles > 9 else f'{miles}  '}   "
        else:
            logger.warning("please provide an int!")
            return ""
        # end format_week_day_miles()

    def print_race(self, name: str = None, race: [] = None):
        """
        print_race() prints a specific race

        :return: none
        """
        if race is None:
            race = self.race.get_race_by_name(name=name)
        # end if

        if race is None:
            print(f"{name} not found!")
            print()
            return
        # end if

        print("--------------------------------------------")
        day_id = race[1]
        day = self.day.get_day_by_id(day_id=day_id)
        date = day[1]
        name = race[3]
        miles = race[2]
        url = race[5] if len(race[5]) > 0 else "none"
        print(f" {date} |  {name},  {miles},  {url}")
        print("--------------------------------------------")
        print()
        # end print_race()

    def print_races(self, training_block_id: str = None):
        """
        print_races() prints a list of the available races

        :return: none
        """
        if training_block_id is None:
            races = self.race.get_races()
        # end if
        else:
            races = self.race.get_races_by_training_block_id(training_block_id=training_block_id)
        # end else

        if races is None or len(races) == 0:
            print("no races found!")
            print()
            return

        print("--------------------------------------------")
        print("    date    |  name,  miles,  url")
        print("--------------------------------------------")
        for race in races:
            day_id = race[1]
            miles = int(race[2])
            name = race[3]
            url = race[5] if len(race[5]) > 0 else "none"
            day = self.day.get_day_by_id(day_id=day_id)
            date = day[1]
            print(f" {date} |  {name},  {miles},  {url}")
        print("--------------------------------------------")
        print()
        # end print_races()

    def print_training_blocks(self):
        """
        print_training_blocks() prints a list of the available training blocks

        :return: none
        """
        print("----------------------")
        print("   training blocks:")
        print("----------------------")
        names = self.tb.get_all_training_block_names()
        for name in names:
            print(name)
        print()
        # end print_training_blocks()

    def pretty_print_training_block(self, name: str = None):
        """
        pretty_print_training_block() prints a nicely formatted view of a training
        block

        :param name: name of the training block to print
        :return: none
        """
        print("----------------------------------------------------------------")
        print("| week |  1  |  2  |  3  |  4  |  5  |  6  |  7  | total(goal) |")
        print("----------------------------------------------------------------")

        training_block_id = self.tb.get_training_block_by_name(name)[0]
        weeks = self.week.get_weeks_by_training_block_id(training_block_id=training_block_id)

        for week in weeks:
            week_id = week[0]
            week_number = week[3]
            goal = week[1]

            week_day_miles = [0, 0, 0, 0, 0, 0, 0]
            days = self.day.get_days_by_week_id(week_id=week_id)
            for day in days:
                day_number = int(day[2])
                miles = int(day[3])
                week_day_miles[day_number - 1] = miles
            # end for

            tot = sum(week_day_miles)

            print("  "
                  f"{week_number if week_number > 9 else f' {week_number}'}   |  "
                  f"{self.format_week_day_miles(miles=week_day_miles[0])}"
                  f"{self.format_week_day_miles(miles=week_day_miles[1])}"
                  f"{self.format_week_day_miles(miles=week_day_miles[2])}"
                  f"{self.format_week_day_miles(miles=week_day_miles[3])}"
                  f"{self.format_week_day_miles(miles=week_day_miles[4])}"
                  f"{self.format_week_day_miles(miles=week_day_miles[5])}"
                  f"{self.format_week_day_miles(miles=week_day_miles[6])}"
                  f"{f'  {tot} ({goal})' if tot < 10 else f'{tot} ({goal})' if tot > 99 else f' {tot} ({goal})'}")
        # end for
        print("|--------------------------------------------------------------|")
        print()
        # end pretty_print_training_block()

    def print_date(
            self,
            training_block_id: str = None,
            week_number: int = 1,
            day_number: int = 1
    ):
        """
        print_date() finds the date in the provided training block given a week
        and day #

        :param training_block_id: training_block_id
        :param week_number: week # of the desired date
        :param day_number: day # of the desired date
        :return: none
        """
        if training_block_id is not None:
            week = self.week.get_week_by_training_block_id_and_week_number(
                training_block_id=training_block_id,
                week_number=week_number
            )
            week_id = week[0]
            day = self.day.get_day_by_week_id_and_day_number(
                week_id=week_id,
                day_number=day_number
            )
            date = day[1]
            week_day = datetime.strptime(date, date_format).strftime('%A').lower()
            print(f"week {week_number}, day {day_number}: {week_day} {date}")
            print()
        # end if
        else:
            print("please provide a valid training block!")
            print()
        # end else
        # end print_date()

    def print_today(self, training_block_id: str = None):
        """
        print_today() finds today's date in the training block and prints the
        week #, day #, weekday and %Y-%m-%d formatted date

        :return: none
        """
        today = datetime.now()
        day = self.day.get_day_by_training_block_id_and_date(
            date=today,
            training_block_id=training_block_id,
        )
        if day is not None:
            day_number = day[2]
            date = day[1]
            week_day = datetime.strptime(date, date_format).strftime('%A').lower()
            week_id = day[5]
        # end if
        else:
            print(f"{today.strftime(date_format)} is not in the training block!")
            print()
            return
        # end else

        week = self.week.get_week_by_id(week_id=week_id)
        if week is not None:
            week_number = week[3]
        else:
            print("week_id was not found!")
            print()
            return

        print(f"week {week_number}, day {day_number}: {week_day} {date}")
        print()
        # end print_today()

    # end Printer

# end of file
