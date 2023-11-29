import logging
import sqlite3 as sl

from app import App

logger = logging.getLogger(name=__name__)


if __name__ == "__main__":
    with sl.connect(f"/Users/ryanperkins/Desktop/miles/db/miles_database") as con:
        cur = con.cursor()
        app = App(con=con, cur=cur)
        app.__exec__()
    # end with
    # end __main__()

# end of file
