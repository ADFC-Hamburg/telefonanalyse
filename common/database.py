from datetime import date, time, timedelta

from os import chmod
import sqlite3

DAYZERO = date(year=2000,month=1,day=1)
TOPICLIST = (
    'Codierung','Verkehr','Mitgliedschaft','Touren','Versicherung','B2B',
    'Tourismus'
    )

class Connection():

    class NotConnectedError(Exception):
        pass

    PATH = 'telefonanalyse.db'
    TABLENAME = 'Anrufe'
    

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.disconnect()

    def _cursor(self) -> sqlite3.Cursor:
        try:
            return self._c
        except AttributeError:
            raise self.NotConnectedError

    # Functions to manage database connection

    def connect(self):
        self._db = sqlite3.connect(self.PATH)
        try:
            chmod(self.PATH,0o666)
        except:
            pass
        self._c = self._db.cursor()

    def disconnect(self):
        self._db.close()
        del self._c
        del self._db
    
    # Functions to handle values

    @staticmethod
    def _datetoint(day:date) -> int:
        return (day-DAYZERO).days

    @staticmethod
    def _inttodate(day:int) -> date:
        return DAYZERO + timedelta(days=day)

    @staticmethod
    def _timetoint(time:time) -> int:
        return time.hour*60 + time.minute

    @staticmethod
    def _inttotime(minutes:int) -> time:
        return time(hour=minutes//60,minute=minutes%60)

    # Functions to perform SQL calls

    def write(self,duration:int,day:date,hm:time,topic:str):
        c = self._cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {self.TABLENAME} (\
                    ID INTEGER PRIMARY KEY, Duration INTEGER,\
                    Day INTEGER, Time INTEGER, Topic TEXT)")
        c.execute(f'INSERT INTO {self.TABLENAME}\
                  (Duration, Day, Time, Topic) VALUES\
                  ("{str(duration)}", "{self._datetoint(day)}",\
                   "{self._timetoint(hm)}", "{topic}")')
        self._db.commit()