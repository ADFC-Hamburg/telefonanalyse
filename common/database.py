"""This module contains functionality to connect to and interact with the
database and also defines relevant constants and default values."""

from datetime import date, time, timedelta

from os import chmod
import sqlite3

from common import strings
from common.entries import PhoneCall

DAYZERO = date(year=2000,month=1,day=1)

class Connection():
    """A handler for connections to the database with methods for common
    interactions.
    
    Recommended use is as part of a with statement."""

    class NotConnectedError(Exception):
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.disconnect()

    def _cursor(self) -> sqlite3.Cursor:
        """
        Returns the database curser.
        If not connected, raise NotConnectedError.
        """
        try:
            return self._c
        except AttributeError:
            raise self.NotConnectedError

    # Functions to manage database connection

    def connect(self) -> None:
        """Connects to the database and prepares a cursor."""
        self._db = sqlite3.connect(strings.DB_PATH)
        try:
            chmod(strings.DB_PATH,0o666) # Permits all users to read/write to db
        except:
            pass
        self._c = self._db.cursor()

    def disconnect(self) -> None:
        """Closes connection to the database."""
        self._db.close()
        del self._c
        del self._db
    
    # Functions to handle values

    @staticmethod
    def _datetoint(day:date) -> int:
        """Calculates number of days since DAYZERO from a date."""
        return (day-DAYZERO).days

    @staticmethod
    def _inttodate(day:int) -> date:
        """Calculates a date from number of days since DAYZERO."""
        return DAYZERO + timedelta(days=day)

    @staticmethod
    def _timetoint(time:time) -> int:
        """Converts a time object to number of minutes."""
        return time.hour*60 + time.minute

    @staticmethod
    def _inttotime(minutes:int) -> time:
        """Converts number of minutes to a time object."""
        return time(hour=minutes//60,minute=minutes%60)

    # Functions to perform SQL calls

    def write(self,duration:int,day:date,hm:time,topic:str) -> None:
        """Writes a new entry to the list of phone calls
        (first creating said list if it does not yet exist).
        
        Args:
            duration: Duration of the call in minutes.
            date: The day of the call.
            hm: The time of the call.
            topic: The topic of the call.
        """

        c = self._cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {strings.DB_NAME_CALLS} (\
                    ID INTEGER PRIMARY KEY, Duration INTEGER,\
                    Day INTEGER, Time INTEGER, Topic TEXT)")
        c.execute(f'INSERT INTO {strings.DB_NAME_CALLS}\
                  (Duration, Day, Time, Topic) VALUES\
                  ("{str(duration)}", "{self._datetoint(day)}",\
                   "{self._timetoint(hm)}", "{topic}")')
        self._db.commit()

    def fetch(self,days:int|None=None) -> tuple[PhoneCall]:
        """Fetch database entries from the list of phone calls.

        Args:
            days: If set, only fetches entries dating back
                no more than that number of days.
        
        Returns:
            A tuple containing each entry as a PhoneCall object.
        """
        c = self._cursor()
        command = f"SELECT * FROM {strings.DB_NAME_CALLS}"
        if not days is None:
            startday = self._datetoint(date.today()) - days
            command += f" WHERE Day >= {str(startday)}"
        command += ";"
        c.execute(command)
        return tuple(PhoneCall(entry[0],
                               entry[1],
                               self._inttodate(entry[2]),
                               self._inttotime(entry[3]),
                               entry[4])
                     for entry in c.fetchall())
