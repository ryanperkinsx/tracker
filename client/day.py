import logging
import uuid

from datetime import datetime

date_format = "%Y-%m-%d"
logger = logging.getLogger(name=__name__)


class DayClient:
    def __init__(self, con, cur, **kwargs):
        super().__init__(**kwargs)
        self.con = con
        self.cur = cur
        # end __init__()

    def create_table(self):
        """
        create_table() creates the day table, only needs to run once

        :return: none
        """
        self.cur.execute(
            "CREATE TABLE day "
            "(day_id VARCHAR(36), "
            "date VARCHAR(12), " 
            "day_number INTEGER, "
            "miles INTEGER, "
            "training_block_id VARCHAR(36), "
            "week_id VARCHAR(36), "
            "PRIMARY KEY (day_id), "
            "FOREIGN KEY (training_block_id) REFERENCES training_block(training_block_id), "
            "FOREIGN KEY (week_id) REFERENCES week(week_id));"
        )
        self.con.commit()
        # end create_table()

    def add_day(
            self,
            date: datetime = None,
            day_number: int = None,
            miles: int = 0,
            training_block_id: str = None,
            week_id: str = None
    ) -> str:
        """
        add_day() adds a row to the day table given the provided inputs, mileage
        defaults to 0

        :param day_number: day_number
        :param date: %Y-%m-%d of the day added
        :param miles: # of miles run
        :param training_block_id: training_block_id
        :param week_id: week_id
        :return: a str day_id
        """
        day_id = str(uuid.uuid4())
        self.cur.execute(
            "INSERT INTO day (day_id, date, day_number, miles, training_block_id, week_id) "
            "VALUES(?, ?, ?, ?, ?, ?)",
            (day_id, date.strftime(date_format), day_number, miles, training_block_id, week_id)
        )
        self.con.commit()
        return day_id
        # end add_day()

    def delete_day_by_id(self, day_id: str = None):
        """
        delete_day_by_id() removes a day given a day_id

        :param day_id: day_id
        :return: none
        """
        self.cur.execute("DELETE FROM day WHERE day_id = ?", (day_id,))
        self.con.commit()
        # end delete_day_by_id()

    def delete_days_by_week_id(self, week_id: str = None):
        """
        delete_days_by_week_id() removes all the days associated with a week_id

        :param week_id: week_id
        :return: none
        """
        self.cur.execute("DELETE FROM day WHERE week_id = ?", (week_id,))
        self.con.commit()
        # end delete_days_by_week_id()

    def get_day_by_id(self, day_id: str = None):
        """
        get_day_by_id() retrieves a day by a given the day_id

        :param day_id: day_id
        :return:
        """
        res = self.cur.execute("SELECT * FROM day WHERE day_id = ?", (day_id,))
        self.con.commit()
        return res.fetchone()
    # end get_day_by_id()

    def get_days_by_week_id(self, week_id: str = None):
        """
        get_days_by_week_id() retrieves all the days associated with a week_id

        :param week_id: week_id
        :return: an [] of days
        """
        res = self.cur.execute("SELECT * FROM day WHERE week_id = ?", (week_id,))
        self.con.commit()
        return res.fetchall()
        # get_days_by_week_id()

    def get_day_by_week_id_and_day_number(self, week_id: str = None, day_number: int = 0):
        """
        get_day_by_week_id_and_day_number() retrieves a specific day (defined by day_number)
        associated with a week_id

        :param week_id: week_id
        :param day_number: day_number
        :return: a day
        """
        res = self.cur.execute(
                "SELECT * FROM day WHERE week_id = ? AND day_number = ?",
                (week_id, day_number)
            )
        self.con.commit()
        return res.fetchone()
        # end get_day_by_week_id_and_day_number()

    def get_day_by_training_block_id_and_date(
            self,
            date: datetime = None,
            training_block_id: str = None
    ):
        """
        get_day_by_training_block_id_and_date() retrieves a day given the date

        :param training_block_id: training_block_id
        :param date: date
        :return: day
        """
        res = self.cur.execute(
            "SELECT * FROM day "
            "WHERE date = ? "
            "AND training_block_id = ?",
            (date.strftime(date_format), training_block_id)
        )
        self.con.commit()
        return res.fetchone()
        # end get_day_by_date()

    def update_day_by_week_id_and_day_number(
            self,
            miles: int = 0,
            week_id: str = None,
            day_number: int = None
    ):
        """
        update_day_by_week_id_and_day_number() updates a specific day (defined by day_number)
        associated with a week_id

        :param miles: # of miles run
        :param week_id: week_id
        :param day_number: day_number
        :return: none
        """
        self.cur.execute(
            "UPDATE day SET miles = ? WHERE week_id = ? AND day_number = ? ",
            (miles, week_id, day_number)
        )
        self.con.commit()
        # end update_day_by_week_id_and_day_number()

    # end DayClient

# end of file
