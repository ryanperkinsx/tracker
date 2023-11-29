import logging
import sys

from functools import cached_property

from printer import Printer
from menu.race import Menu as RaceMenu
from menu.training_block import Menu as TrainingBlockMenu

date_format = "%Y-%m-%d"
logger = logging.getLogger(name="app")


class App:
    def __init__(self, con, cur):
        self.con = con
        self.cur = cur
        # end __init__()

    @cached_property
    def printer(self) -> Printer:
        """
        printer() caches a Printer client for use the duration of the process

        :return: Printer client
        """
        return Printer(con=self.con, cur=self.cur)
        # end printer()

    @cached_property
    def race_menu(self) -> RaceMenu:
        """
        race_menu() caches a RaceMenu client for use the duration of the process

        :return: RaceMenu client
        """
        return RaceMenu(con=self.con, cur=self.cur)
        # end race_menu()

    @cached_property
    def tb_menu(self) -> TrainingBlockMenu:
        """
        tb_menu() caches a TrainingBlockMenu client for use the duration of
        the process

        :return: TrainingBlockMenu client
        """
        return TrainingBlockMenu(con=self.con, cur=self.cur)
        # end tb_menu()

    def __exec__(self):
        """
        __exec__() is the main execution function of the App

        :return: none
        """
        self.printer.print_main_menu()
        while True:
            params = input("~ ").lower().strip().split(' ')
            cmd = params[0]

            if cmd == "tb" or cmd == "training-blocks":
                self.tb_menu.main()
            # end if "tb"

            elif cmd == 'r' or cmd == "race":
                self.race_menu.main()
            # end elif 'r'

            elif cmd == 'h' or cmd == "help":
                self.printer.print_main_menu()
            # end elif 'h'

            elif cmd == "x" or cmd == "exit":
                sys.exit("bye :)")
            # end elif "x"

            else:
                print("invalid command!")
            # end else
        # end while
        # end _exec()

    # end App

# end of file
