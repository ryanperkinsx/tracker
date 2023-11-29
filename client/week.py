import logging
import uuid

from functools import cached_property

from client.day import DayClient

date_format = "%Y-%m-%d"
logger = logging.getLogger(name=__name__)


class WeekClient:
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

    def create_table(self):
        """
        create_table() creates the week table, only needs to run once

        :return: none
        """
        self.cur.execute(
            "CREATE TABLE week "
            "(week_id VARCHAR(36), "
            "goal INTEGER, "
            "training_block_id VARCHAR(36), "
            "week_number INTEGER, "
            "PRIMARY KEY (week_id), "
            "FOREIGN KEY (training_block_id) REFERENCES training_block(training_block_id));"
        )
        self.con.commit()
    # end create_table()

    def add_week(self, training_block_id: str = None, week_number: int = 1):
        """
        add_week()

        :param training_block_id: training_block_id
        :param week_number: week number in the training block
        :return: str week_id
        """
        week_id = str(uuid.uuid4())
        self.cur.execute(
            "INSERT INTO week (week_id, training_block_id, week_number, goal) "
            "VALUES(?, ?, ?, 0)",
            (week_id, training_block_id, week_number)
        )
        self.con.commit()
        return week_id
    # end add_week()

    def delete_week_by_id(self, week_id: str = None):
        """
        delete_week_by_id() removes a week given a week_id

        :param week_id: week_id
        :return: none
        """
        self.cur.execute(
            "DELETE FROM week WHERE week_id = ?",
            (week_id,)
        )
        self.con.commit()
    # end delete_week_by_id()

    def get_week_by_id(self, week_id: str = None):
        """
        get_week_by_id() retrieves a week given a week_id

        :param week_id: week_id
        :return: a week
        """
        res = self.cur.execute("SELECT * FROM week WHERE week_id = ?",
                               (week_id,))
        self.con.commit()
        return res.fetchone()
    # end get_week_by_id()

    def get_last_week_by_training_block_id(self, training_block_id: str = None):
        """
        get_last_week_by_training_block_id() retrieves the last week from a
        training block. "Last" is determined by the training block week with the
        greatest week_number

        :param training_block_id: training_block_id
        :return: the last week in a training block
        """
        res = self.cur.execute(
            "SELECT week_id, MAX(week_number) FROM week WHERE training_block_id = ?",
            (training_block_id,)
        )
        self.con.commit()
        return res.fetchone()
        # end get_last_week_by_training_block_id()

    def get_weeks_by_training_block_id(self, training_block_id: str = None):
        """
        get_weeks_by_training_block_id() retrieves all the weeks associated with a
        training block

        :param training_block_id: training_block_id
        :return: an [] of weeks
        """
        res = self.cur.execute(
            "SELECT * FROM week WHERE training_block_id = ? ",
            (training_block_id,)
        )
        self.con.commit()
        return res.fetchall()
    # end get_weeks_by_training_block_id()

    def get_week_by_training_block_id_and_week_number(
            self,
            training_block_id: str = None,
            week_number: int = None
    ) -> str:
        """
        get_week_by_training_block_id_and_week_number() retrieves a specific day (defined
        by week_number associated with a training_block_id

        :param training_block_id: training_block_id
        :param week_number: # of the desired week
        :return: a week
        """
        res = self.cur.execute(
            "SELECT week_id FROM week WHERE training_block_id = ? AND week_number = ?",
            (training_block_id, week_number)
        )
        self.con.commit()
        return res.fetchone()
    # end get_week_id_by_training_block_id_and_week_number()

    def delete_weeks_from_training_block(self, training_block_id: str = None, num_weeks: int = 1):
        """
        remove_week_from_training_block() removes 1+ week from the Week table given
        a training_block_id

        :param training_block_id: training_block_id
        :param num_weeks: # of weeks to delete, defaults to 1
        :return: none
        """
        count = 0
        while count < num_weeks:
            last_week = self.get_last_week_by_training_block_id(training_block_id=training_block_id)
            week_id = last_week[0]

            self.cur.execute("DELETE FROM week WHERE week_id = ?", (week_id,))
            self.con.commit()
            self.day.delete_days_by_week_id(week_id=week_id)

            count += 1
        # end while
    # end delete_weeks_from_training_block()

    def update_goal_by_week_id(self, goal: int = 0, week_id: str = None):
        """
        update_goal_by_week_id() updates the goal for a given week_id

        :param goal: mileage goal, defaults to 0
        :param week_id: week_id
        :return: nonw
        """
        self.cur.execute("UPDATE week SET goal = ? WHERE week_id = ?", (goal, week_id))
        self.con.commit()
    # end update_goal_by_week_id()

    # end Week

# end of file
