"""This module provides a sub window where users can
enter new phone calls into the database."""

import tkcalendar

from common import database, strings, templates
import datetime
import tkinter as tk
from tkinter import ttk

class Window(templates.InputWindow):
    """A handler for a sub window.
    
    This window lets the user enter a new phone call into the database."""

    TITLE = 'Ein Telefongespräch eintragen'
    BUTTON_LABEL = 'OK'
    MENU_PRIORITY = 250
    DEFAULT_HEIGHT = 185
    DEFAULT_WIDTH = 300
    MIN_HEIGHT = 170
    MIN_WIDTH = 210

    def _populate(self,frame:tk.Widget) -> None:
        """
        Creates the content of the sub window
        and places it in the designated frame.
        """

        # Layout
        frame.columnconfigure(1,weight=1)
        frame.rowconfigure(1,pad=self.PADDING)

        # Create index labels
        label_left:list[ttk.Label]=[]
        label_right:list[ttk.Label] = []

        for text in ('Zeitpunkt','Dauer','Thema'):
            label_left.append(ttk.Label(frame,text=text+':'))
        for i in range(len(label_left)):
            label_left[i].grid(row=i,column=0,sticky='nw')

        # Date & time fields
        subframe_date = ttk.Frame(frame)
        subframe_date.grid(row=0,column=1,columnspan=2,sticky='new')

        self._date_field=tkcalendar.DateEntry(subframe_date)
        self._date_field.config(
            mindate=database.DAYZERO,date_pattern='dd.mm.yyyy',
            justify='right',width=9
            )
        self._date_field.pack(side=tk.TOP,anchor='ne')

        self._hours = tk.StringVar(frame,
            value=str(datetime.datetime.now().hour)
            )
        self._minutes = tk.StringVar(
            frame,value=datetime.datetime.now().strftime('%M')
            )
        hours_field = ttk.Spinbox(
            subframe_date,from_=0,to=23,width=2,
            justify='right',textvariable=self._hours
            )
        minutes_field = ttk.Spinbox(
            subframe_date,from_=0,to=59,width=2,format='%02.0f',
            justify='right',textvariable=self._minutes
            )
        label_right.append(ttk.Label(subframe_date,text=':'))
        minutes_field.pack(side=tk.RIGHT)
        label_right[-1].pack(side=tk.RIGHT)
        hours_field.pack(side=tk.RIGHT)

        # Duration field
        self._duration = tk.IntVar(frame)
        dur_field = ttk.Spinbox(
            frame,from_=0,to=999,width=3,justify='right',
            textvariable=self._duration
            )
        dur_field.grid(row=1,column=1,sticky='e')
        label_right.append(ttk.Label(frame,text='Minuten'))
        label_right[-1].grid(row=1,column=2,sticky='w')

        # Topic field
        self._topic = tk.StringVar(frame)
        topicbox = ttk.Combobox(
            frame,textvariable=self._topic,
            values=sorted(strings.TOPICLIST),width=12
            )
        topicbox.grid(row=2,column=1,columnspan=2)

    def execute(self) -> None:
        """
        If user entered data is valid, writes it into the database.

        Closes this sub window on success.
        
        To be run when the button is pressed.
        """
        date:datetime.date = self._date_field.get_date()

        try:
            time = datetime.time(
                int(self._hours.get()),int(self._minutes.get())
                )
        except:
            self.alert(
                'Fehleingabe','Gib bitte eine korrekte Uhrzeit ein.',
                error=True
                )
            return
        try:
            duration = int(self._duration.get())
        except:
            self.alert(
                'Fehleingabe',
                'Gib die Dauer des Anrufes bitte in ganzen Minuten an.',
                error=True
                )
            return
        if not duration:
            self.alert(
                'Fehlende Eingabe',
                'Gib bitte die Dauer des Anrufes an.',error=True
                )
            return
        topic = self._topic.get()
        if not topic:
            self.alert(
                'Fehlende Eingabe',
                'Gib bitte den Grund des Anrufes an.',
                error=True
                )
            return
        with database.Connection() as con:
            try:
                con.write(duration,date,time,topic)
            except database.sqlite3.Error as e:
                self.alert(
                    'SQL-Fehler',
                    'Fehler beim Aktualisieren der Datenbank',
                    detail=str(e),error=True
                    )
                return
            except ValueError as e:
                self.alert(
                    'Eingabefehler',
                    'Fehler beim Aktualisieren der Datenbank',
                    detail=str(e),error=True
                    )
                return
        self.alert('Erfolg','Eintrag erstellt')
        self.window.destroy()
