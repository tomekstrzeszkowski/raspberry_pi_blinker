from contextlib import closing
import sqlite3


def get_mode():
    current_state = None
    with closing(sqlite3.connect("blinker.db")) as connection:
        with closing(connection.cursor()) as cursor:
            current_state = cursor.execute(
                "SELECT is_night FROM mode"
            ).fetchall()[0][0] == 1
            connection.commit()
    return current_state

def set_mode(value):
    with closing(sqlite3.connect("blinker.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                "UPDATE mode SET is_night = ?",
                (value,)
            )
            connection.commit()