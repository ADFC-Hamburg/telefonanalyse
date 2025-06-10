"""This module provides a sub window where users can
export the phone call list to a file."""

from common import database, entries, strings, templates
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile as tk_asksaveasfile

class Window(templates.InputWindow):
    """A handler for a sub window.

    This window lets the user export the list of phone calls."""

    TITLE = strings.WINDOW.EXPORT
    BUTTON_LABEL = strings.BUTTON.EXPORT
    MENU_PRIORITY = 50
    DEFAULT_HEIGHT = 180
    DEFAULT_WIDTH = 300
    MIN_HEIGHT = 160
    MIN_WIDTH = 280


    def _populate(self, frame) -> None:
        """
        Creates the content of the sub window
        and places it in the designated frame.
        """

        # Create radio buttons
        RADIO_TEXT = (
            strings.LABEL.EXPORT_ENTIRE_LIST,
            strings.LABEL.EXPORT_DAYS_LN1+' \n'+strings.LABEL.EXPORT_DAYS_LN2
            )

        self._limit_days = tk.BooleanVar(master=frame,value=False)
        radio_limit_days = []
        for i in range(len(RADIO_TEXT)):
            radio_limit_days.append(ttk.Radiobutton(frame,text=RADIO_TEXT[i],
                                                variable=self._limit_days,
                                                value=bool(i)))
            radio_limit_days[i].grid(row=i,column=0,sticky='nw',
                                     columnspan=1 if i==1 else 2)

        # Create checkbox
        self._include_title_row = tk.BooleanVar(master=frame,value=True)
        checkbox_title = ttk.Checkbutton(frame,
                                        text=strings.LABEL.TABLE_WITH_HEADER,
                                        variable=self._include_title_row)
        checkbox_title.grid(row=2,column=0,columnspan=2,
                            sticky='nw',pady=self.PADDING)
        
        # Create day number field
        def enable_day_limit():
            self._limit_days.set(True)

        self._day_number = tk.IntVar(frame,value=30)
        days_field = ttk.Spinbox(frame, from_=0, to_=9999,
                                 width=4, justify=tk.RIGHT,
                                 textvariable=self._day_number,
                                 command=enable_day_limit)
        days_field.grid(row=1,column=1,sticky='nw')

    def execute(self) -> None:

        # Get max number of days
        try:
            days = int(self._day_number.get())\
                   if self._limit_days.get() else None
        except (ValueError,tk.TclError):
            self.alert(strings.ALERT.TITLE.ENTRYERROR,
                       strings.ALERT.FORMAT_DAYS,
                       error=True)
            return
        
        # Fetch table
        try:
            with database.Connection() as con:
                table = con.fetch(days=days)
        except database.sqlite3.Error as e:
            self.alert(
                strings.ALERT.TITLE.SQLERROR,
                strings.ALERT.ERROR_DB_ACCESS,
                detail=str(e),error=True
            )
            return
        
        # Abort if table empty
        if not table:
            self.alert(
                strings.ALERT.TITLE.NOENTRIESFOUND,
                strings.ALERT.ZERO_ENTRIES,
                warning=True
            )
            return
        
        # Open 'Save As' dialogue
        try:
            with tk_asksaveasfile(filetypes=strings.EXPORT_TYPES,
                               initialfile=strings.EXPORT_DEFAULT_PATH,
                               parent=self.window) as f:

                try:
                    # Write to file
                    if self._include_title_row.get():
                        f.write(entries.COMMA_SEPERATED_ORDER+'\n')
                    f.write('\n'.join(tuple(entries.comma_seperated(entry)
                                            for entry in table)))

                except (IOError,OSError):
                    self.window.alert(
                        strings.ALERT.TITLE.FILEERROR,
                        strings.ALERT.ERROR_FILE_SAVE,
                        error=True
                    )
                    return
        except TypeError:
            return
        except (FileNotFoundError,PermissionError,OSError):
            self.alert(
                strings.ALERT.TITLE.FILEERROR,
                strings.ALERT.ERROR_FILE_OPEN,
                error=True
            )
            return
        
        # Confirm success and close window
        self.alert(strings.ALERT.TITLE.SUCCESS,
                   strings.ALERT.SUCCESS_SAVE)
        self.window.destroy()
