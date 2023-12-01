import logging
import sys

from functools import cached_property

from client.day import DayClient
from printer import Printer
from menu.race import Menu as RaceMenu
from client.race import RaceClient
from client.training_block import TrainingBlockClient
from client.week import WeekClient

from datetime import datetime, timedelta

logger = logging.getLogger(name=__name__)
date_format = "%Y-%m-%d"


class Menu:
    def __init__(self, con, cur, **kwargs):
        super().__init__(**kwargs)
        self.con = con
        self.cur = cur
        # end __init__()

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
    def race_menu(self) -> RaceMenu:
        """
        race_menu() caches a RaceMenu client for use the duration of the process

        :return: a RaceMenu client
        """
        return RaceMenu(con=self.con, cur=self.cur)
        # end race_menu()

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
            print("invalid date!")
            return False
        # end except
        # end is_date()

    def main(self):
        """
        main() controls the main training block menu

        :return: none
        """
        self.printer.print_training_block_menu()

        while True:
            params = input("~ ").lower().strip().split(' ')
            cmd = params[0]
            params.remove(cmd)

            if cmd == "ls" or cmd == "list":
                self.printer.print_training_blocks()
                # end if "ls"

            elif cmd == 'o' or cmd == "open":
                training_block_name = input("name: ").strip()
                x = 0
                while x < 4 and not self.tb.validate_name(name=training_block_name):
                    training_block_name = input("invalid, try again: ").strip()
                    x += 1
                # end while

                if not self.tb.validate_name(name=training_block_name):
                    print("max tries exceeded!")
                    print()
                    continue
                # end if
                else:
                    self.edit_menu(name=training_block_name)
                    self.printer.print_training_block_menu()
                # end else
            # end if 'o'

            elif cmd == 'a' or cmd == "add":
                training_block_name = input("name (64 char. limit): ").strip()
                x = 0
                while x < 4 and self.tb.validate_name(name=training_block_name):
                    training_block_name = input("invalid, try again: ").strip()
                    x += 1
                # end while

                if self.tb.validate_name(name=training_block_name):
                    print("max tries exceeded!")
                    print()
                    continue

                input_date = input("start date (YYYY-MM-DD, hit ENTER for today): ").strip()

                if len(input_date) == 0:
                    start_date = datetime.now()
                # end if
                else:
                    x = 0
                    while x < 4 and not self.is_date(date=input_date):
                        input_date = input("invalid date! try again: ").strip()
                        x += 1
                    # end while
                    if not self.is_date(date=input_date):
                        continue
                    # end if
                    start_date = datetime.strptime(input_date, date_format)
                # end else

                training_block_id = self.tb.add_training_block(
                    name=training_block_name,
                    start_date=start_date
                )

                weeks = input("# of weeks (min: 1, max: 99): ").strip()
                x = 0
                while x < 4 and (not weeks.isdigit() or int(weeks) < 0):
                    weeks = input("invalid #, try again: ").strip()
                    x += 1
                # end while

                if not weeks.isdigit():
                    print("max tries exceeded! please provide a #!")
                    print()
                    self.tb.delete_training_block_by_id(training_block_id=training_block_id)
                    continue
                # end if
                weeks = int(weeks)
                if weeks < 0 or weeks > 99:
                    print("max tries exceeded! training blocks have a minimum (0) and a maximum (99)!")
                    print()
                    self.tb.delete_training_block_by_id(training_block_id=training_block_id)
                    continue
                # end if

                for x in range(weeks):
                    week_id = self.week.add_week(
                        training_block_id=training_block_id,
                        week_number=(x + 1)
                    )

                    for y in range(7):
                        self.day.add_day(
                            date=start_date,
                            day_number=(y + 1),
                            week_id=week_id,
                            training_block_id=training_block_id
                        )
                        start_date += timedelta(days=1)
                    # end for
                # end for
                print(f"{training_block_name} added!")
                print()
            # end elif 'a'

            elif cmd == "rm" or cmd == "remove":
                training_block_name = input("name: ").strip()
                if not self.tb.validate_name(name=training_block_name):
                    print("please select an existing training block name!")
                    print()
                    continue
                    # end if
                else:
                    confirmation = input("are you sure you want to remove "
                                         f"{training_block_name}? (y/n): ").strip().lower()
                    x = 0
                    while x < 4 and confirmation != 'y':
                        if confirmation == 'n':
                            break
                        confirmation = input("(y/n): ").strip().lower()
                        x += 1
                    # end while

                    if confirmation == 'y':
                        training_block = self.tb.get_training_block_by_name(name=training_block_name)
                        training_block_id = training_block[0]
                        self.tb.delete_training_block_by_id(training_block_id=training_block_id)

                        weeks = self.week.get_weeks_by_training_block_id(training_block_id=training_block_id)
                        for week in weeks:
                            week_id = week[0]
                            self.week.delete_week_by_id(week_id=week_id)
                            self.day.delete_days_by_week_id(week_id=week_id)
                        # end for
                        print(f"{training_block_name} was deleted!")
                        print()
                    # end if
                    else:
                        print("cancelled!")
                        print()
                        continue
                    # end else
                # end else
            # end elif "rm"

            elif cmd == 'h' or cmd == "help":
                self.printer.print_training_block_menu()
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

    def edit_menu(self, name: str = None):
        """
        edit_menu() controls the edit training block menu

        :param name: name
        :return: none
        """
        self.printer.print_training_block_open_menu()
        training_block = self.tb.get_training_block_by_name(name=name)
        training_block_id = training_block[0]
        weeks = self.week.get_weeks_by_training_block_id(training_block_id=training_block_id)

        while True:
            params = input("~ ").lower().strip().split(' ')
            cmd = params[0]
            params.remove(cmd)

            if cmd == 'p' or cmd == "print":
                self.printer.pretty_print_training_block(name=name)
            # end if 'p'

            elif cmd == 'd' or cmd == "date":
                if len(params) == 2:
                    if not params[0].strip().isdigit():
                        print(f"please provide a valid week #! (max: {len(weeks)})")
                        print()
                        continue

                    if not params[1].strip().isdigit():
                        print("please provide a valid day #! (1-7)")
                        print()
                        continue

                    week_number = int(params[0].strip())
                    day_number = int(params[1].strip())

                    if week_number < 1 or week_number > len(weeks):
                        print(f"week # is too big! (max: {len(weeks)})")
                        print()
                        continue

                    if day_number < 1 or day_number > 7:
                        print("day # is too big! (1-7)")
                        print()
                        continue

                    self.printer.print_date(
                        training_block_id=training_block_id,
                        week_number=week_number,
                        day_number=day_number
                    )
                # end if
                elif len(params) == 0:
                    self.printer.print_today(training_block_id=training_block_id)
                # end elif
                else:
                    print("invalid syntax!")
                    print()
                # end else
            # end elif 'd'

            elif cmd == 'u' or cmd == "update":
                if len(params) == 3:
                    week_number = params[0].strip()
                    if not week_number.isdigit() or int(week_number) > len(weeks):
                        print(f"please provide a valid week number! (max: {len(weeks)})")
                        print()
                        continue
                    # end if

                    day_number = params[1].strip()
                    if not day_number == 'g' and not (day_number.isdigit() and (0 < int(day_number) < 8)):
                        print("please provide a valid day number! (1-7 or 'g' for goal)")
                        print()
                        continue
                    # end if

                    miles = params[2].strip()
                    if not (miles.isdigit() and (0 <= int(miles) < 999)):
                        print("please provide a valid # of miles!")
                        print()
                        continue
                    # end if

                    week_number = int(week_number)
                    day_number = 'g' if day_number == 'g' else int(day_number)
                    miles = int(miles)

                    week = self.week.get_week_by_training_block_id_and_week_number(
                        training_block_id=training_block_id,
                        week_number=week_number
                    )  # could ref. the 'weeks' variable above
                    week_id = week[0]
                    if day_number == 'g':
                        self.week.update_goal_by_week_id(
                            goal=miles,
                            week_id=week_id
                        )
                        print("goal updated!")
                    # end if
                    else:
                        self.day.update_day_by_week_id_and_day_number(
                            miles=miles,
                            week_id=week_id,
                            day_number=int(day_number)
                        )
                        print("week/day updated!")
                    # end else
                    print()
                # end if
                else:
                    print("invalid syntax!")
                    print()
                # end else
            # end elif 'u'

            elif cmd == 'a' or cmd == "add":
                if len(params) == 1:
                    if params[0].strip() == "week":
                        num_weeks = input("# of weeks (hit ENTER for 1)").strip()
                        if num_weeks.isdigit():
                            num_weeks = int(params[1].strip())
                        # end if
                        else:
                            num_weeks = 1

                        last_week = self.week.get_last_week_by_training_block_id(
                            training_block_id=training_block_id
                        )
                        week_id = last_week[0]
                        start_week_number = last_week[1] + 1
                        if start_week_number > 99:
                            print("can't add anymore weeks! (max: 99)")
                            continue
                        # end if
                        last_day = self.day.get_day_by_week_id_and_day_number(
                            week_id=week_id,
                            day_number=7
                        )
                        last_day_date = last_day[1]
                        last_day_date = datetime.strptime(last_day_date, date_format)
                        date = last_day_date + timedelta(days=1)

                        for x in range(num_weeks):
                            if (start_week_number + x) > 99:
                                print("can't add anymore weeks! (max: 99), added {x + 1} weeks")
                                break
                            # end if
                            week_id = self.week.add_week(
                                training_block_id=training_block_id,
                                week_number=(start_week_number + x)
                            )

                            for y in range(7):
                                self.day.add_day(
                                    date=date,
                                    day_number=(y + 1),
                                    week_id=week_id,
                                    training_block_id=training_block_id
                                )
                                date += timedelta(days=1)
                            # end for
                        # end for
                    # end if
                    elif params[0].strip() == "race":
                        self.race_menu.add_race_wizard(training_block_id=training_block_id)
                    # end elif
                # end if
                else:
                    print("please provide an option! (week, race)")
                    print()
                # end else
            # end elif 'a'

            elif cmd == "rm" or cmd == "remove":
                if len(params) == 1:
                    if params[0].strip() == "week":
                        num_weeks = input("# of weeks (hit ENTER for 1): ").strip()
                        if num_weeks.isdigit():
                            num_weeks = int(num_weeks)
                        # end if
                        else:
                            num_weeks = 1
                        # end else

                        for x in range(num_weeks):
                            last_week = self.week.get_last_week_by_training_block_id(training_block_id=training_block_id)
                            if last_week is None:
                                print("no more weeks!")
                                break
                            # end if
                            week_id = last_week[0]
                            self.week.delete_week_by_id(week_id=week_id)
                            self.day.delete_days_by_week_id(week_id=week_id)
                            print("done!")
                            print()
                        # end for
                    elif params[0].strip() == "race":
                        race_name = input("name: ").strip()
                        if not self.race.validate_name(name=race_name):
                            print("please select an existing race name!")
                            continue
                        self.race.delete_race_by_name(name=race_name)
                    # end elif
                # end if
                else:
                    print("please provide an option! (week, race)")
                    print()
                # end else
            # end elif "rm"

            elif cmd == 'r' or cmd == "race":
                self.printer.print_races(training_block_id=training_block_id)
                continue
            # end elif 'r'

            elif cmd == 'h' or cmd == "help":
                self.printer.print_training_block_open_menu()
            # end elif 'h'

            elif cmd == 'm' or cmd == "menu":
                return
            # end elif 'x'

            elif cmd == 'x' or cmd == "exit":
                sys.exit("bye :)")
            # end elif 'x'
        # end while
        # end edit_menu()

    # end Menu

# end of file
