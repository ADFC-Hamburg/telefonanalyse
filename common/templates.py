"""
This module contains templates for tkinter windows.
"""

from typing import Sequence, Type
import tkinter as tk
from tkinter import ttk,messagebox


class MainWindow():
    """A main menu with buttons to access any number of sub windows."""

    DEFAULT_BUTTON_WIDTH = 320
    DEFAULT_BUTTON_HEIGHT = 80
    MIN_BUTTON_WIDTH = 200
    MIN_BUTTON_HEIGHT = 40
    PADDING = 12


    class Button(ttk.Button):
        """A button to open a sub window."""

        COLUMN = 0
        STICKY_DIRECTIONS = 'news'

        def __init__(self,master:tk.Tk,target:Type):
            """Construct a button widget with the parent MASTER which
            opens a window via the run function of class TARGET."""
            super().__init__(master,text=target.TITLE,command=self.open)
            self.master = master
            self.target = target
        
        def grid(self,position:int,padding:int):
            """Position a widget in the parent widget in a grid."""
            super().grid(row=position,column=self.COLUMN,
                         sticky=self.STICKY_DIRECTIONS,pady=padding/2)

        def open(self):
            """Opens a sub window with the master window as its parent."""
            subwindow = self.target(self.master)
            subwindow.run()


    def __init__(self,title:str,entries:Sequence[Type]):
        """Initializes a main menu."""

        self.window = tk.Tk()
        width = self.DEFAULT_BUTTON_WIDTH+2*self.PADDING
        height = (self.DEFAULT_BUTTON_HEIGHT+self.PADDING)*len(entries)+self.PADDING
        min_width = self.MIN_BUTTON_WIDTH+2*self.PADDING
        min_height = (self.MIN_BUTTON_HEIGHT+self.PADDING)*len(entries)+self.PADDING
        self.window.geometry(f'{str(width)}x{str(height)}')
        self.window.minsize(min_width,min_height)
        self.window.title(title)

        self.frame = ttk.Frame(self.window,padding=(self.PADDING,self.PADDING/2))
        self.frame.pack(fill='both',expand=1)
        self.frame.rowconfigure(tuple(range(len(entries))),weight=1)
        self.frame.columnconfigure(0,weight=1)

        sorted_entries = sorted(entries,key=lambda entry: entry.MENU_PRIORITY,
                                reverse=True)

        for i,entry in enumerate(sorted_entries):
            btn = self.Button(self.frame,entry)
            btn.grid(position=i,padding=self.PADDING/2)

    def run(self):
        """Opens the main menu."""
        self.window.mainloop()


class SubWindow():
    """
    Describes a sub window which is to be opened via a different window.

    It has designated space for content.
    """

    TITLE = ''
    MENU_PRIORITY = 0 # Higher priority = higher position in parent menu
    EXPAND_CONTENT = False

    DEFAULT_WIDTH = 320
    DEFAULT_HEIGHT = 240
    MIN_WIDTH = 160
    MIN_HEIGHT = 120
    PADDING = 12

    def __init__(self,parent:tk.Tk|tk.Toplevel):
        """Initializes a sub window and binds it to a parent."""

        self.window = tk.Toplevel(parent)
        self.window.geometry(f'{str(self.DEFAULT_WIDTH)}x{str(self.DEFAULT_HEIGHT)}')
        self.window.minsize(self.MIN_WIDTH,self.MIN_HEIGHT)
        self.window.title(self.TITLE)

        self.frame = ttk.Frame(self.window,padding=self.PADDING)
        self.frame.pack(fill='both',expand=1)
        self.frame.rowconfigure(0,weight=1)
        self.frame.columnconfigure(0,weight=1)

        self.content = ttk.Frame(self.frame)
        self.content.grid(row=0,column=0,
                          sticky="nesw" if self.EXPAND_CONTENT else "ns")
        self._populate(self.content)
    
    def alert(self,title:str,message:str,detail:str|None=None,
              error:bool=False,warning:bool=False):
        """
        Show an OS message box.
        """
        if error:
            messagebox.showerror(
                title,message,detail=detail,parent=self.window)
        elif warning:
            messagebox.showwarning(
                title,message,detail=detail,parent=self.window)
        else:
            messagebox.showinfo(
                title,message,detail=detail,parent=self.window)

    def _populate(self,frame:tk.Widget):
        """
        Creates the content of the sub window
        and places it in the designated frame.
        """
        print('default')

    def run(self):
        """
        Opens this sub window and prevents interaction
        with the parent window until this window is closed.
        """

        self.window.grab_set()
        self.window.focus_force()
    

class InputWindow(SubWindow):
    """
    Describes a sub window which is to be opened via a different window.

    It has designated space for content and also a button at the bottom.
    """

    BUTTON_LABEL = ''
    BUTTON_WIDTH = 12

    def __init__(self,parent:tk.Tk|tk.Toplevel):

        super().__init__(parent)

        self.exec_button = ttk.Button(self.frame,text=self.BUTTON_LABEL,
                                          width=self.BUTTON_WIDTH,
                                          command=self.execute)
        self.exec_button.grid(row=1,pady=(self.PADDING,0))
        
    def execute(self):
        """Function to be run when the button is pressed."""
        self.window.destroy()
