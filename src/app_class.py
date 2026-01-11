# -*- coding: utf-8 -*-
"""
app_class.py, baseline application class.

This class extends the tkinter.Tk class to build a base application
     that can be extended without having to reinvent all the components.
     Features:
     -- This class provides a minimum default menu capability.

     -- This class has the ability to add potential menus and button items
     on the fly.

     -- The base application class can associate icon files with buttons
     or menu items. If no icon file is associated with a menu item,
     only the text name of the function is displayed.  For buttons,
     that have no icon file associated, the button display a default icon.

@author: R. H. Bumpous
2/27/2023

"""

__version__ = "0.5"

__author__ = "Bob Bumpous <BBFlyer@comcast.net>"

# from tkinter import filedialog
# from tkinter import messagebox, ttk
# from tkinter import Menu

import threading
import tkinter as tk


class BaseApp(tk.Tk):
    """
    ClassBaseApp is a framework for more advanced apps.

    This class provides a basic extensible application framework based
    on Tkinter.  It provides basic window, menu, functions, and allows
    a user to add additional menus. By default the command name is the
    name of the menu or button, but may be changed by the user.

    Menus or toolbars may be nested to arbitrary depths.  Commands may
    be associated with any depth of the menu or toolbar heirarchy.

    The framework provides a tool, by default called 'Customize' on
    the 'Tools' menu that allows a user to associate a menu item
    with any available command on any menu or toolbar. (not implemented.)
    """

    def __init__(self, menus: dict = None, title='', about=''):
        # Make sure our window is on top.
        super().__init__()
        # Initially bring window to top.
        self.wm_attributes("-topmost", True)
        # after finished startup, allow it to fall behing others.
        self.after_idle(self.wm_attributes, '-topmost', False)
        self.geometry('400x400')

        # Create three frames for the base application.
        self.frame = None  # ttk.Frame(self)
        self._create_header_frame()
        self._create_body_frame()
        self._create_footer_frame()

        self.default_title = "Basic Python - \
            Tkinter Application with a Default Menu"
        # Set the title our window will display.

        if title == '':
            self.title(self.default_title)
        else:
            self.title(title)

        if about == '':
            self.about = "Default About Message."
        else:
            self.about = about

        # make a place to store our base path and out current path
        self.bpath = ""
        self.cpath = ""
        # Create a dictionary to store file types we know how to read
        # and links to the commands to read and write them.
        # they will look like {"jpg": "read_jpg" }
        self.read_file_types = {}
        self.read_file_types = {}

        # Setup a dictionary of all available application functions.
        # format{"name": [method, args, **kargs]}
        self.available_commands = {"not_implemented": [self._not_implemented,
                                                       None],
                                   "build_text_frame": [self.build_text_frame],
                                   "open_dir": [self.open_dir],
                                   "open_file": [self.open_file],
                                   "Exit": [self.exit, None],
                                   "About": [self.about, "?"]}
        # Setup a dictionary of default app menus

        # A more compact way of building menus. With this and the build_menues
        # method, to add menus or menu items.  Here is the basic set of menus,
        # if we want additional menus, pass them in as part of the
        #  __init__ in the same format as the following.
        #
        # Note: do not put () after the commands as this causes the system
        # to execute them immediately!
        # Note: passing a menu dictionary fails because the commands are
        # Not passed correctly.  Have to define the the path to the
        # commands better.
        #
        self.base_menus = {"File": {'New': self._not_implemented,
                                    'Open': self.open_file,
                                    'Save': self._not_implemented,
                                    'SaveAs': self._not_implemented,
                                    'Close': self._not_implemented,
                                    'Separator': '',
                                    'Exit': self.exit},
                           "Edit": {"Cut": self._not_implemented,
                                    "Copy": self._not_implemented,
                                    "Paste": self._not_implemented,
                                    "Delete": self._not_implemented,
                                    "Select All": self._not_implemented},
                           "Tools": {"Customize": self._not_implemented,
                                     "Options": self._not_implemented},
                           "Help": {"Help Index": self._not_implemented,
                                    "About": self.about}}

        # Defensive programming: Copy our base menus into a new menus
        # object so they can't be destroyed accidently when we add more menus.
        # A new dictionary item with the same name will overwrite the base
        # menu item.
        if menus is None:
            self.menus = self.base_menus.copy()
        else:
            self.menus = menus

        # Uncomment out the following to set a background color
        # self.configure(background='green')

        self.menubar = self._build_menus(self, self.menus)
        self.config(menu=self.menubar)

    def _bring_to_top_focus(self):
        """Bring this window to top and give it the focus.

        The following insures that the app will be initially displayed
        on top of all other windows but not locked there. It also
        makes sure the window has the focus.
        """
        self.lift()
        self.attributes('-topmost', True)
        self.after(1, lambda: self.focus_force())
        self.after_idle(self.attributes, '-topmost', False)

    def _create_header_frame(self):
        """
        Define the header frame.

        This could be used for a toolbar, with icon buttons for menu
        or other actions.

        Set up the self.header variable which is stored in the class
        and can be used by subclasses to build GUIs for specific apps.
        """
        if isinstance(self.frame, tk.ttk.Frame):
            self.header = tk.ttk.Frame(self.frame)
        else:
            self.header = tk.ttk.Frame(self)
        # by default, we are going to have 3 widgets, the center
        #    entry should be given preference.
        self.header.columnconfigure(0, weight=1)
        self.header.columnconfigure(1, weight=1)
        self.header.columnconfigure(2, weight=1)
        self.header.columnconfigure(3, weight=1)

    def _create_body_frame(self):
        """Create a centeral body frame for the window.

        Here is where most of the action happens.

        Set up a self.body variable which is stored in the class
        and can be used by subclasses to build GUIs for specific apps.
        """
        if isinstance(self.frame, tk.ttk.Frame):
            self.body = tk.ttk.Frame(self.frame)
        else:
            self.body = tk.ttk.Frame(self)
        self.body.columnconfigure(0, weight=1)

    def _create_footer_frame(self):
        """Create a footer frame.

        Typically, the footer is used to display progress or status
        information for the application.

        Sets up the self.footer variable which is stored in the class
        and can be used by subclasses to build GUIs for specific apps.
        """
        if isinstance(self.frame, tk.ttk.Frame):
            self.footer = tk.ttk.Frame(self.frame)
        else:
            self.footer = tk.ttk.Frame(self)
        self.footer.columnconfigure(0, weight=1)
        self.footer.columnconfigure(1, weight=10)
        self.footer.columnconfigure(2, weight=1)

    def _build_menus(self, container, d: dict = {}):
        """
        Build a tkinter menu from a dictionary.

        The top level keys are used as the top level menu items.
        If the value associated with that key is a new
        dictionary it is used to create submenus names and commands
        under the top level menu.  Alternatively, the key may return
        the string separator, in which case we want to add a
        separator between menu or submenu items.  Eventually,
        we would like to be able to use the routine recursively
        to add submenus under the master menu items using the
        same methods.

        For example if a key is "File", and it returns a dictionary
        that contain {"New": self.new_window,
                    "Open": self.donothing,
                    "Save": self.donothing,
                    "Save as...": self.donothing,
                    "Exit": self.Exit)}
        this routine will build a File top level menu and add New, Open
        Save, Save As, and Close items to this menu and associate the
        correct commands with each item.  To make larger menus, add
        additional items to the menus dictionary! No additional code
        changes are needed.

        Parameters
        ----------
        mb         The window menu bar that is created

        """
        mb = tk.Menu(container)
        for menu_key in d.keys():
            mnu = tk.Menu(mb, tearoff=0)
            menu_items = d.get(menu_key)
            for mi in menu_items.keys():
                # cmd could be a callable function or method.
                # cmd could be a separator
                # cmd could be another dictionary that a submenu to the
                # current menu item. (not implemented.)
                cmd = menu_items.get(mi)
                if isinstance(mi, str) and callable(cmd):
                    mnu.add_command(label=mi, command=cmd)
                if isinstance(cmd, type(dict)):
                    # Add a submenu to the menubar.
                    smb = self._build_menus(mb, cmd)
                    mb.add_cascade(smb)
                elif 'separator' in mi:
                    mnu.add_separator()
                else:
                    # Ignore anything that is not a menu item or a separator.
                    pass

            if isinstance(menu_key, str):
                mb.add_cascade(label=menu_key, menu=mnu)
        return mb

    def build_scrollable_canvas(self, container):
        """
        Build a public scrollable canvas to hold images.

        This method builds a scrollable canvas for the body frame.
        it is not usable with the utilities files get_image because
        of the way the ngs app displays open CDROM or missing NGS
        CD information.

        Parameters
        ----------
        container : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # container.columnconfigure(1, weight=1)
        container.columnconfigure(1, weight=1)  # add column
        container.rowconfigure(1, weight=1)  # add row
        # Put canvas here.
        container.grid(column=0, row=0, sticky='nw')
        # Put vertical scrollbar here.
        container.grid(column=0, row=1, sticky='e')
        # Put horizontal scrollbar here.
        container.grid(column=1, row=0, sticky='s')

        canvas = tk.Canvas(container)
        scrollbar_x = tk.ttk.Scrollbar(container, orient="horizontal",
                                       command=canvas.xview)
        scrollbar_y = tk.ttk.Scrollbar(container, orient="vertical",
                                       command=canvas.yview)
        canvas.configure(xscrollcommand=scrollbar_x.set,
                         yscrollcommand=scrollbar_y.set)

        canvas.grid(column=0, row=0, padx=2, pady=2, sticky='nesw')
        scrollbar_x.grid(column=0, row=1, padx=2, pady=2, sticky='nesw')
        scrollbar_y.grid(column=1, row=0, padx=2, pady=2, sticky='nesw')
        return canvas

    def build_text_frame(self, container):
        """
        Build a public scrollable text box Frame where we can enter data.

        Add a text widget and scroll bars on the right and bottom
        of a container (frame).  This is a helper method, so we do
        not have to figure out how to do this again in the future,
        just add text to the self.document using the instructions
        for a text widget.

        Parameters
        ----------
        container : Frame or ttk.Frame
            Adds a text widget with vertical and horizontal scrollbars
            to the passed in frame.  Stores the result in in the class
            variable self.document where other elements of the application
            can take advantage of the pre-existing compound component.

        Returns
        -------
        var   tk text widget
            A text widget that the user can store and modify as needed.
        """
        document = tk.Text(container)
        document.grid(column=0, row=0, sticky=tk.NSEW)
        # initially make the document 20 Rows tall and 80 characters wide.
        # self.document.config(height=20, width=80)

        # add vertical and horizontal scroll bars.
        scrollbar_v = tk.ttk.Scrollbar(container,
                                       orient='vertical',
                                       command=document.yview)
        scrollbar_v.grid(column=1, row=0, sticky=tk.NS)
        document['yscrollcommand'] = scrollbar_v.set

        scrollbar_h = tk.ttk.Scrollbar(container,
                                       orient='horizontal',
                                       command=document.xview)
        scrollbar_h.grid(column=0, row=1, sticky=tk.EW)
        document['yscrollcommand'] = scrollbar_h.set
        return document

    def _not_implemented(self):
        """Place holder for the appropriate methods."""
        # self.T.delete('1.0', END)
        # self.T.insert('1.0', 'This function has not yet been implemented.')
        # str_title = 'Function not implemented!'
        # str_message = '{}'.format(self.title())
        str_message = "This function is not yet implemented."
        tk.messagebox.showinfo(self.title(), str_message)
    # Method for closing window

    def about(self):
        """Open the about dialog box for this app."""
        about_title = 'About {}'.format(self.title())
        about_message = '{}'.format(self.about)
        tk.messagebox.showinfo(about_title, about_message)

    def exit(self):
        """Close all open windows and exit the application."""
        # If we have any threads running, stop them here.
        try:
            for thread in threading.enumerate():
                if thread.name == "MainThread":
                    pass
                else:
                    if threading.Lock().locked():
                        thread.release()
                    try:
                        thread._stop()
                    except AssertionError as error:
                        error = error
                        pass
        except NameError as error:
            error = error
            pass

        self.destroy()

    def open_dir(self):
        """
        Open a directory.

        Returns
        -------
        directory : path
            Open the user selected directory and set the current
            directory object.

        """
        try:
            path = tk.filedialog.askdirectory(
                    # initialdir=self.cpath)
                    initialdir='/')

            if path:
                self._file_action(path)

        except FileNotFoundError:
            tk.messagebox.showerror("Directory Not Found",
                                    "The selected directory was not found.")
        self.path = path
        return path

    def open_file(self):
        """
        Open a file.

        Returns
        -------
        file : TYPE
            DESCRIPTION.

        """
        try:
            path = tk.filedialog.\
                askopenfilename(
                    initialdir=self.cpath,
                    filetypes=self.file_types)

            if path:
                self._file_action(path)

        except FileNotFoundError:
            tk.messagebox.showerror("File Not Found",
                                    "The selected file was not found.")
        self.path = path
        return path

    def _file_action(self, path):
        pass

    def read_config(self):
        """
        Read the configuration from disk from a file called config.py.

        Returns
        -------
        dict    dictionary
                Returns a dictionary of Configuration dictionaries.

                Returns the dictionary containing the current menu
                settings and the dictionary of curent toolbars

        """
        self._not_implemented()

    def save_config(self):
        """
        Save the current configuration of the application.

        Saves the current configuration of the application. Generally
        called when the user changes the application configuration
        and closes the 'Customize' dialog box.  The configuration is
        saved in a file called config.py in the

        Returns
        -------
        None.

        """
        self._not_implemented()
