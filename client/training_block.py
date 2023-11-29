import logging
import uuid

from datetime import datetime

date_format = "%Y-%m-%d"
logger = logging.getLogger(name=__name__)


class TrainingBlockClient:
    def __init__(self, con, cur, **kwargs):
        super().__init__(**kwargs)
        self.con = con
        self.cur = cur
        # end __init__()

    def create_table(self):
        """
        create_table() creates the training_block table, only needs to run once

        :return: none
        """
        self.cur.execute(
            "CREATE TABLE training_block"
            "(training_block_id VARCHAR(36),"
            " name VARCHAR(64),"
            " start_date VARCHAR(10),"
            " PRIMARY KEY (training_block_id));")
        self.con.commit()
        # end create_table()

    def add_training_block(
            self,
            name: str = "new_block",
            start_date: datetime = None
    ) -> str:
        """
        add_training_block() adds a new training block

        :param name: name of the new training block
        :param start_date: starting date of the new training block, defaults
                            to the current dats (system dependent)
        :return: training_block_id
        """
        __id = str(uuid.uuid4())
        self.cur.execute(
            "INSERT INTO training_block (training_block_id, name, start_date) "
            "VALUES(?, ?, ?)", (__id, name, start_date.strftime(date_format))
        )
        self.con.commit()
        return __id
        # end add_training_block()

    def delete_training_block_by_id(self, training_block_id: str = None):
        """
        delete_training_block_by_id() removes a training block given
        the training_block_id

        :param training_block_id: training_block_id
        :return: none
        """
        self.cur.execute("DELETE FROM training_block WHERE training_block_id = ?",
                         (training_block_id,))
        self.con.commit()
        # end delete_training_block_by_id()

    def get_all_training_block_names(self) -> [str]:
        """
        get_all_training_block_names() retrieves a list of the training block
        names in the DB

        :return: an [] of training block names
        """
        res = self.cur.execute("SELECT name FROM training_block")
        self.con.commit()
        names = []
        for row in res.fetchall():
            names.append(row[0])
        return names
        # end get_all_training_block_names()

    def get_training_block_by_name(self, name: str = None):
        """
        get_training_block_by_name() retrieves a training block given the
        provided name

        :param name: name of the desired training block
        :return: a training block
        """
        res = self.cur.execute("SELECT * FROM training_block WHERE name = ?",
                               (name,))
        self.con.commit()
        return res.fetchone()
        # end get_training_block_id()

    def validate_name(self, name: str = None) -> bool:
        """
        validate_name() checks if the provided name matches one of the
        training blocks already in the system

        :param name: training_block_name
        :return: bool
        """
        if name is None:
            return False
        names = []
        rows = self.cur.execute("SELECT name FROM training_block").fetchall()
        self.con.commit()
        for row in rows:
            names.append(row[0])
        # end for
        return name in names
        # end validate_name()

    # end TrainingBlockClient

# end of file
