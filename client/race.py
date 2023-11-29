import logging
import uuid

date_format = "%Y-%m-%d"
logger = logging.getLogger(name=__name__)


class RaceClient:
    def __init__(self, con, cur, **kwargs):
        super().__init__(**kwargs)
        self.con = con
        self.cur = cur

    def create_table(self):
        """
        create_table() creates the race table, only needs to run once

        :return: none
        """
        self.cur.execute(
            "CREATE TABLE races "
            "(race_id VARCHAR(36), "
            "day_id VARCHAR(36), "
            "miles FLOAT, "
            "name VARCHAR(64), "
            "url VARCHAR(1024), "
            "training_block_id VARCHAR(1024), "
            "PRIMARY KEY (race_id), "
            "FOREIGN KEY (day_id) REFERENCES day(day_id), "
            "FOREIGN KEY (training_block_id) REFERENCES training_block(training_block_id));"
        )
        self.con.commit()
        # end create_table()

    def add_race(
            self,
            day_id: str = None,
            miles: int = 0,
            name: str = None,
            training_block_id: str = None,
            url: str = None
    ) -> str:
        """
        add_race() adds a new race

        :param day_id: day_id
        :param name: name for the new race
        :param miles: # of miles
        :param training_block_id: training_block_id
        :param url: race URL
        :return:
        """
        race_id = str(uuid.uuid4())
        self.cur.execute(
            "INSERT INTO race (race_id, day_id, miles, name, training_block_id, url) "
            "VALUES(?, ?, ?, ?, ?, ?)",
            (race_id, day_id, miles, name, training_block_id, url)
        )
        self.con.commit()
        return race_id
        # end add_race()

    def delete_race_by_id(self, race_id: str = None):
        """
        delete_race_by_id() removes a race associated with the provided race ID

        :param race_id: race ID to remove
        :return:
        """
        self.cur.execute("DELETE FROM race WHERE race_id = ?", (race_id,))
        self.con.commit()
        # end delete_race_by_id()

    def delete_race_by_name(self, name: str = None):
        """
        delete_race_by_name() removes a race associated with the provided name

        :param name: race name to remove
        :return:
        """
        self.cur.execute("DELETE FROM race WHERE name = ?", (name,))
        self.con.commit()
        # end delete_race_by_name()

    def get_race_by_name(self, name: str = None):
        """
        get_race_by_name() retrieves a race give the race's name

        :return: race
        """
        res = self.cur.execute("SELECT * FROM race WHERE name = ?", (name,))
        self.con.commit()
        return res.fetchone()
        # end get_race_by_name()

    def get_day_id_by_name(self, name: str = None):
        """
        get_day_id_by_name() retrieves the day_id of a race given the race's
        name

        :return: day_id
        """
        res = self.cur.execute("SELECT day_id FROM race WHERE name = ?", (name,))
        self.con.commit()
        return res.fetchone()[0]
        # end get_day_id_by_name()

    def get_miles_by_name(self, name: str = None):
        """
        get_miles_by_name() retrieves the # of miles given a race's name

        :return: miles
        """
        res = self.cur.execute("SELECT miles FROM race WHERE name = ?", (name,))
        self.con.commit()
        return res.fetchone()[0]
        # end get_miles_by_name()

    def get_url_by_name(self, name: str = None):
        """
        get_url_by_name() retrieves the URL given a race's name

        :return: url
        """
        res = self.cur.execute("SELECT url FROM race WHERE name = ?", (name,))
        self.con.commit()
        return res.fetchone()[0]
        # end get_url_by_name()

    def get_races(self):
        """
        get_races() retrieves all the races in the race table

        :return:
        """
        res = self.cur.execute("SELECT * FROM race")
        self.con.commit()
        return res.fetchall()
        # end get_races()

    def get_races_by_training_block_id(self, training_block_id: str = None):
        """
        get_races_by_training_block_id() retrieves all the races given a
        training_block_id

        :param training_block_id: training_block_id
        :return: an [] of races
        """
        res = self.cur.execute(
            "SELECT * FROM race WHERE training_block_id = ?",
            (training_block_id,)
        )
        self.con.commit()
        return res.fetchall()
        # end get_races_by_training_block_id()

    def update_day_id_by_id(self, race_id: str = None, day_id: str = None):
        """
        update_day_id_by_id() updates the day_id of a given race ID

        :param race_id: race_id
        :param day_id: day_id
        :return: none
        """
        self.cur.execute(
            "UPDATE race SET day_id = ? WHERE race_id = ?",
            (day_id, race_id)
        )
        self.con.commit()
        # end update_day_id_by_id()

    def update_name_by_id(self, race_id: str = None, name: str = None):
        """
        update_name_by_id() updates the name of a given race ID

        :param race_id: race_id
        :param name: name
        :return: none
        """
        self.cur.execute("UPDATE race SET name = ? WHERE race_id = ?",
                               (name, race_id))
        self.con.commit()
        # end update_name_by_id()

    def update_miles_by_id(self, race_id: str = None, miles: int = 0):
        """
        update_miles_by_id() updates the miles of a given race ID

        :param race_id: race_id
        :param miles: miles
        :return: none
        """
        self.cur.execute("UPDATE race SET miles = ? WHERE race_id = ?",
                               (miles, race_id))
        self.con.commit()
        # end update_miles_by_id()

    def update_url_by_id(self, race_id: str = None, url: str = None):
        """
        update_url_by_id() updates the url of a given race ID

        :param race_id: race_id
        :param url: url
        :return: none
        """
        self.cur.execute("UPDATE race SET url = ? WHERE race_id = ?",
                               (url, race_id))
        self.con.commit()
        # end update_url_by_id()

    def validate_name(self, name: str = None) -> bool:
        """
        validate_name() checks if the provided name matches one of the
        races already in the system

        :param name: race_name
        :return: bool
        """
        if name is None:
            return False
        names = []
        rows = self.cur.execute("SELECT name FROM race").fetchall()
        self.con.commit()
        for row in rows:
            names.append(row[0])
        # end for
        return name in names
        # end validate_name()

    # end Race

# end of file
