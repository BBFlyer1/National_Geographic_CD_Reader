# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 16:07:14 2024.

A class that extends the BaseApp class to provide methods to address
the needs of a National Geographic Society CD Magazine Reader.

@author: R. H. Bumpous
"""
# from pathlib import Path
import pathlib
import tkinter as tk
# from tkinter import ttk

# from app_class import BaseApp
import app_class as a_class
# from util_files import (build_magazine_index, build_page_list,
#                        decode_dir_name, get_image, get_directory,
#                        _clear_frame)
import util_files as u_files
# from util_ngs import get_first_mo_yr
import util_ngs as u_ngs
# from util_mov import (play_intro_1, play_intro_2, play_intro_3,
#                      play_intro_4, play_credits)
import util_mov as u_mov


class NgsApp(a_class.BaseApp):
    """
    Application to display National Geographic Magazines from a CD.

    NGSApp extends BaseApp.

    This is an application to display National Geographic magazines from
    The National Geographic CD set.
    """
    

    def __init__(self, menus: dict = None, title='', about=''):
        """Initialize the NgsApp class.

        The code to create this menu, must occur after the call to
        NgsApp.__init__ occurs, so that the NgsApp object will exist
        because the named methods are contained in this and the BaseApp
        class.
        """
        if menus is None:
            # Note: This is a NGS specific menu.  We will add the
            # current CD's Year range as top level menus later.
            menus = {'File': {'Exit': self.exit_with_credits},
                     "Help": {'Help Index': self._not_implemented,
                              'About': self.about
                              },
                     'NGS Movies': {
                             'NGS Globe': u_mov.play_intro_1,
                             'NGS Interactive': u_mov.play_intro_2,
                             'Kodak Film': u_mov.play_intro_3,
                             'NGS Magazines': u_mov.play_intro_4,
                             'Credits Movie': u_mov.play_credits
                             }
                     }

        # Note: the above menu will be extended with a menu
        # of years and months if a NGS CD is loaded.

        # Initialize the BaseApp class.
        super(NgsApp,
              self).__init__(menus, title, about)

        # Play the NGS Credits movie when closing app.
        # Default is no.
        self.play_credits = False

        # save the original title for update when we change CDs.
        self.original_title = title

        # set initial geometry, Approximate size of NGS Magazine
        # self.geometry('625x975+1500-50')
        self.geometry('625x1000')

        # Build the NGS application framework
        self._build_header()
        self._build_body()
        self._build_footer()
        # Create class to validate data entry.
        self.valid = self.ValidatedPages(self.page_entry)
        # create class to enable-disable buttons
        self._update_btns = self.SetButtonsState(self.fwd_btn,
                                                 self.back_btn,
                                                 self.valid)

        # Update the display based on whether there is a NGS CD in the
        # CDROM drive.
        self.CD = True
        # self._update_display()  # Temporarily remove this from __init__
        # self.process_results(None)

        # The following insures that the app will be displayed on top
        # but not locked there.
        self.lift()
        self.attributes('-topmost', True)
        self.after_idle(self.attributes, '-topmost', False)
        self._bring_to_top_focus()

    def exit_with_credits(self):
        """Play the NGS Credits movie before exiting the app."""
        if self.play_credits:
            print('Exiting the NGS application.')
            u_mov.play_credits()
        self.exit()

    def _build_header(self):
        """
        Populate the header.

        Create additional columns for all widgets and add the header buttons
        and labels for the NGS application.
        """
        # NOTE: self.header, self.body, self.footer are ttk.Frames
        # constructed in base class and configured here.
        self.header.config(height=10)
        self.header.grid(column=0, row=0, sticky='nsew')  # Put this at the top
        self.header.columnconfigure(4, weight=1)  # add column
        self.header.columnconfigure(5, weight=1)  # add column

        self._config_hdr_buttons()
        self._config_hdr_labels()
        self._config_hdr_page_entry()

    def _config_hdr_buttons(self):
        """
        Set the configuration for the header fwd and back buttons.

        Returns
        -------
        None.

        """
        btn_style = tk.ttk.Style()
        btn_style.configure('dir.TButton', font=('calibre', 12, 'bold'),
                            foreground="black", background="white")
        # Backward Button
        self.back_btn = tk.ttk.Button(self.header, style="dir.TButton",
                                   text='< Backward', command=self.backward)
        self.back_btn.grid(column=0, row=0, padx=2, pady=2)
        # State is not part of style, so use the following to disable btn.
        # self.back_btn.config(state='disabled')
        # Forward Button
        self.fwd_btn = tk.ttk.Button(self.header, style='dir.TButton',
                                  text='Forward >', command=self.forward)
        self.fwd_btn.grid(column=4, row=0, padx=2, pady=2)

    def _config_hdr_labels(self):
        """
        Set configuration of header page, pages and month-year lables.

        Returns
        -------
        None.

        """
        # Page & Pages Label Style
        pg_label_style = tk.ttk.Style()
        pg_label_style.configure('pg.TLabel', font=('calibre', 12, 'bold'),
                                 foreground="black", background="white",
                                 width=6)
        # Page Label
        self.page_lbl = tk.ttk.Label(self.header, style='pg.TLabel',
                                  text="Page: ")
        self.page_lbl.grid(column=1, row=0, padx=2, pady=2)
        # Pages Label
        self.pages_lbl = tk.ttk.Label(self.header, style='pg.TLabel',
                                   text=" of ")
        self.pages_lbl.grid(column=3, row=0, padx=2, pady=2)
        # Month Year Label Style
        mo_yr_style = tk.ttk.Style()
        mo_yr_style.configure('mo_yr.TLabel', font=('calibre', 12, 'bold'),
                              foreground="white", background="green",
                              justify='center')
        # Month Year Label
        self.mon_yr_lbl = tk.ttk.Label(self.header, style='mo_yr.TLabel',
                                    text=(str() + " " + str()),
                                    anchor=tk.CENTER)
        self.mon_yr_lbl.grid(column=5, row=0, padx=2, pady=2)

    def _config_hdr_page_entry(self):
        """
        Set configuration of the header page entry field.

        Returns
        -------
        None.

        """
        entry_style = tk.ttk.Style()
        entry_style.configure('en.TEntry', font=('calibre', 12, 'bold'),
                              foreground="black", fieldbackground="blue",
                              justify='right')
        self.page_entry = tk.ttk.Entry(self.header, font=('calibre', 12, 'bold'),
                                    justify='right', width=5,
                                    background="blue")
        self.page_entry.grid(column=2, row=0, padx=2, pady=2)
        # bind get_user_page to the enter key is pressed.
        self.page_entry.bind('<Return>', self.get_user_page)
        self.page_entry.focus()

    def _build_body(self):
        """
        Build the Body frame.

        Configure the body frame, which was created in BaseApp
        for this app
        """
        self.body.grid(column=0, row=1, sticky='nsew')
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)
        # self.body.config(width=400, height=400)
        # self.body.grid(column=0, row=0, columnspan=True, rowspan=True,
        #                sticky='nsew')
        # Create a scrollable canvas item in the body frame.
        # print("_build_body: Creating Scrollable Canvas")
        # self.canvas = self.build_scrollable_canvas(self.body)
        # print("_build_body: Created Scrollable Canvas")

    def _build_footer(self):
        """
        Build the footer frame for  the app.

        Parameters
        ----------
        None :

        Returns
        -------
        None.
            Constructs the visual elements of the application.
            References are saved as object attributes.
        """
        # self.footer.config(width=400, height=10)
        self.footer.grid(column=0, row=2)

    def _build_NGS_menus(self, ng_base_path, ng_date_range,
                         after=False):
        """Define the NGS menus and items.

        Adds year menus and month sub-menus based on the specific NGS
        CD in the CD reader.
        """
        # Get a dictionary of dictionaries that contains the years
        # and months of each magazine folder on this disk and
        # the folder that contains that magazine.
        self.mag_mo_yr_indx = u_files.build_magazine_index(ng_base_path, ng_date_range)
        menu_bar = self.menubar
        # Create the main menu and add it to the root window
        # if after = False ie, there are no other menus
        if after:
            # When after = True, we will add to menubar
            ngs_menu = tk.Menu(menu_bar)
            self.config(menu=ngs_menu)  # menu_bar
        else:
            ngs_menu = tk.Menu(self)
            self.config(menu=ngs_menu)

        # The top level menu will be the year from the CD
        # the menu_items are the months of magazine folders on this CD.

        for menu_label, menu_items in self.mag_mo_yr_indx.items():
            menu = tk.Menu(ngs_menu, tearoff=0)
            # Add the years as top level menu columns.
            if after:
                menu_bar.insert_cascade(menu_bar.index("Help"),
                                        label=menu_label, menu=menu)
            else:
                ngs_menu.add_cascade(label=menu_label, menu=menu)
            # var = tk.StringVar()
            # now for each month in the year located on this CD,
            # create a cascaded menu item.
            for item_label, file_path in menu_items.items():
                title = f"{menu_label} {item_label} {file_path}"
                menu.add_command(label=item_label,
                                 command=lambda x=title:
                                 self._change_magazine(x))

    def _file_action(self, path):
        """
        Decode selected path to the month and year of the magazine.

        National Geographic CDs have directory names that encode
        the month and year of each magazine on the disk.  Decode
        the directory name to that of a specific magazine and
        switch to that one

        """
        if self.CD is False:
            self.__init__()
        else:
            # "year month filepath"
            child = pathlib.Path(path)
            # year, month, file_path = arg.split(" ")
            self.current_year, self.current_month, \
                file_path = u_files.decode_dir_name(child)
            arg = f"{self.current_year}, {self.current_month}, {file_path}"
            self._change_magazine(arg)

    def _initial_magazine(self):
        """
        Initialize with the first magazine on the National Graphic CD.

        The first time through, read the first NG magazine on the disk
        and load the first page into our app.

        Returns
        -------
        None.

        """
        self.current_month, self.current_year = \
            u_ngs.get_first_mo_yr(self.mag_mo_yr_indx)

        d1 = self.mag_mo_yr_indx[self.current_year]
        m_path = d1[self.current_month]
        arg = f"{self.current_year} {self.current_month} {m_path}"
        self._change_magazine(arg)

    def _change_magazine(self, arg):
        """
        Change the magazine.

        Parameters
        ----------
        arg : str
            Arg has to be split into year, month, and file_path.

        Returns
        -------
        None.

        """
        # print("_change_magazine:", end="")
        year, month, file_path = arg.split(" ")

        self.page_list = u_files.build_page_list(file_path)

        # Validate pages and page.
        self.valid.pages = (len(self.page_list)-1)
        self.valid.page = 0
        self.pages_lbl.config(text=f" of {self.valid.pages}")

        # Update magazine month and year display.
        text = f"{month} {year}"
        self.mon_yr_lbl.config(text=text, width=len(text)+2)

        # Change to page image.
        self.change_page()
        # Update buttons state.
        # self._update_btns.state()

        # print("    get_image")
        # Note: when we change magazines, we default to the cover page.
        # get_image(self.body, self.page_list)
        # get_image(self.canvas, self.page_list, self.valid.page)

    def backward(self):
        # def backward(self, l_pages):
        """
        Move the image to the previous image in the current folder.

        Returns
        -------
        None.

        """
        print("backward:", end="")
        if self.valid.page > 0:
            self.valid.page -= 1
            self.change_page()

            # get_image(self.body, self.page_list, self.valid.page)
            # print("get_image")
            # get_image(self.canvas, self.page_list, self.valid.page)
            # self._update_page_no(self.page, self.back_btn)
            # Class in init to update button states.
            # self._update_btns.state()

    def forward(self):
        """
        Move the image to the next image in the current folder.

        Returns
        -------
        None.

        """
        print("forward:", end="")
        if self.valid.page < self.valid.pages:
            self.valid.page += 1
            self.change_page()

            # get_image(self.body, self.page_list, self.valid.page)
            # print("get_image")
            # get_image(self.canvas, self.page_list, self.valid.page)
            # self._update_page_no(self.page, self.fwd_btn)
            # Class in init to update button states.
            # self._update_btns.state()

    def change_page(self):
        """Load a new page set by the calling routine."""
        print("    get_image{}".format(self.valid.page))
        u_files.get_image(self.body, self.page_list, self.valid.page)
        # Class in init to update button states.
        self._update_btns.state()

    def get_user_page(self, x):
        """
        Get the user entered page number value from the page_entry widget.

        The user interface contains a tkinter page_entry widget which
        displays the current page number in the current National Geographic
        magazine.  The user can change this value one of two ways
        1st the user can use the backward and forward buttons to page
        through the magazine.  The current page number will be displayed
        in the page_entry widget.  In addition, the user can enter a
        specific page number in the page_entry widget.  When the user
        presses the enter key, the value is tested to determine if it
        is in the page range, ie the page number entered by the user
        is between 0 and the maximum number of pages in the magazine.
        If the page number is in range, the get_image function is
        called, with the user entered page number as the target.
        This reads a new page from the NG CD and displays it.

        Parameters
        ----------
        x : str
            A value from the page_entry  widget of the User Interface.
        page_no : int
            The location in the pl array .

        Returns
        -------
        None.

        """
        pg = int(self.page_entry.get())
        print("get_user_page: ", pg, end="")
        # Only accept valid page numbers.
        if pg < self.valid.pages and pg >= 0:
            self.valid.page = pg
            print("get_valid_page: {}".format(self.valid.page))
            self.change_page()
        else:
            self.page_entry.delete(0, "end")   # remove everything
            self.page_entry.insert(0, str(self.valid.page))   # insert new text

        """
        try:
            self.valid.page = self.page_entry.get()
            print("get_valid_page: {}".format(self.valid.page))
            self.change_page()

            # get_image(self.body, self.page_list, self.valid.page)
            # print("get_image")
            # get_image(self.canvas, self.page_list, self.valid.page)
            # self._update_btns.state()
        except ValueError as error:
            error = error
            self.page_entry.delete(0, 'end')
            self.page_entry.insert(0, self.valid.page)
            """
        """
        # self.page_entry.insert(0, self.page)
        # inp = int(self.page_entry.get())
        # If out user input is within the limits of the current magazine,
        # set the page number to that value and redisplay that file.
        # changed min page input to 0 for Cover 12/13/24 RHB
        # if inp >= 0 and inp <= self.pages:
        if inp >= 0 and inp <= self.valid.pages:
            # self.page = inp
            get_image(self.body, self.page_list, self.valid.page)
        # else reset the page_entry number to the current page number.
        else:
            self._update_page_display(self.page, self.back_btn)
            self._update_page_display(self.page, self.fwd_btn)"""

    def print_page(self):
        """
        Print out the current page on the default printer.

        Returns
        -------
        None.

        """
        self._not_implemented()

    def process_results(self, results=None):
        """Update the CDROM drawer status."""
        if results is None:
            pass
        elif results:
            self.CD = True
        else:
            self.CD = False
        self._update_display()

    def _update_display(self):
        """Update the display when we startup or change CDs."""
        # Check if CDROM drawer is closed and has NGS CD.
        if self.CD:
            self._has_cd()
            date_rng = f"{self.ng_date_range[0]} to {self.ng_date_range[1]}"
            self.title(f"{self.original_title}  {date_rng}")

        else:
            self._no_cd()
            self.title(f"{self.original_title}")

    def _has_cd(self):
        """Upsate the display if we have a NGS CD in the CDROM drive."""
        self.ng_base_path, self.ng_date_range = u_files.get_directory()
        # change the menu bar to the original menu.
        # On initialization, the super builds this menu, so
        # we do not have to do it again. on changes of CD, the open
        # CD drawer should have built this.
        # if "File" not in self.menubar.keys():
        self.menubar = self._build_menus(self, self.menus)

        # building the NGS Menu.
        # self._build_NGS_menus(self.ng_base_path, self.ng_date_range, True)
        # and add in the year and month menus.
        self._build_NGS_menus(self.ng_base_path, self.ng_date_range, True)
        self.config(menu=self.menubar)
        # Now initialize to the first magazine on the CD.
        self._initial_magazine()

    def _no_cd(self):
        """
        If no NGS CD is in the drive, post a message.

        Returns
        -------
        None.

        """
        # When the CDROM drawer is opened, remove the NGS menu.
        self.menubar = self._build_menus(self, self.menus)
        # and post the No NGS Message.
        self.config(menu=self.menubar)
        self.pages_lbl.config(text="")
        # Set the page numbers to 0 and disable both buttons.
        # self._update_page_no(-1, self.back_btn)
        # self._update_page_no(-1, self.fwd_btn)
        # Class in init to update button states.
        self._update_btns.disable()
        self.mon_yr_lbl.config(text="", width=10)
        self._cd_message()

    def _cd_message(self):
        """
        Display a No NGC CD message to the user.

        Clear the image from the body frame and put in a text
        message that says we don't have a NGS CD.'

        Returns
        -------
        None.

        """
        # Remove the existing image from the body frame.
        u_files._clear_frame(self.body)  # from util_files
        message = """


        No National Geographic CD mounted

        Insert CD

        Remember CDROM drives are mechanical and slow!"""

        document = self.build_text_frame(self.body)
        document.config(bg='lightyellow', fg='red',
                        font=('calibre', 12, 'bold'))
        # Clear any old messages from the document frame.
        document.delete(1.0, 'end')  # probably not needed.
        document.insert("end", message)
        document.grid(column=0, row=0)
        document['state'] = 'disabled'

    class ValidatedPages():
        """Validate page and pages are integers and in the valid range."""

        def __init__(self, pg_entry):
            self._entry = pg_entry
            self._page = 0
            self._pages = 0

        @property
        def page(self):
            """
            Return the current page number.

            Return the current page number as an integer, after validating
            it is in the allowed page range.

            Returns
            -------
            int
                Returns the current page number.

            """
            return self._page

        @page.setter
        def page(self, value):
            """
            Update the current page number.

            Update the current page number, after validating that it is
            an integer and it is in the allowed page range, 0 to pages.

            Parameters
            ----------
            value : int
                The current page number.

            Raises
            ------
            ValueError
                Raise a ValueError if the value is not an integer and
                is not within the page range 0-self.pages.

            Returns
            -------
            None.

            """
            if not isinstance(value, int):
                self._entry.delete(0, 'end')
                self._entry.insert(0, f"{self._page}")
                raise ValueError
            if (value > self._pages or value < 0):
                self._entry.delete(0, 'end')
                self._entry.insert(0, f"{self._page}")
                raise ValueError
            else:
                self._page = value
                self._entry.delete(0, 'end')
                self._entry.insert(0, f"{self._page}")

        @property
        def pages(self):
            """
            Return the total pages in the current magazine.

            Return the number of pages in the current National
            Geographic Society magazine.

            Returns
            -------
            int
                Returns the current page number.

            """
            return self._pages

        @pages.setter
        def pages(self, value):
            """
            Change the total page count.

            Change the number of available pages. Typically called when a
            new National Geographic society magazine is loaded.  This
            change occurs after validating that the new number of pages
            is an integer.

            Parameters
            ----------
            value : int
                The current page number.

            Raises
            ------
            ValueError
                Raise a ValueError if the value is not an integer and
                is not within the page range 0-self.pages.

            Returns
            -------
            None.

            """
            if not isinstance(value, (int)) or self._page < 0:
                raise ValueError("Pages must be an integer.")
            # if self._page < 0:
            #     raise ValueError("Pages must be >= 0.")
            else:
                self._pages = value

    class SetButtonsState():
        """
        Enable or disable Forward and Backward buttons.

        This class is designed to compare the current page of a
        National Geographic Society magazine with the minimum (0)
        and maximum number of pages, val_pgs.pages(). If either
        extreme is reached, the button for browsing in that direction
        is disabled.  As soon as the user moves away from the extreme,
        the buttons for travel in both directions are enabled.
        """

        def __init__(self, f_btn, b_btn, val_pgs):
            """
            Initialize the SetButtonsState Class.

            Capture the buttons, f_btn and b_btn, and the valid pages,
            val_pgs, for future use.

            Parameters
            ----------
            f_btn : tkinter.ttk.Button
                The forward button in the page control panel.
            b_btn : tkinter.ttk.Button
                The backward button in the page control panel.
            val_pg : ValidatedPages class
                this is a ValidatedPages object which has both a current
                page, page and a maximum page.

            Returns
            -------
            None.

            """
            self.fwd_button = f_btn
            self.back_button = b_btn
            self.valid = val_pgs

        def state(self):
            """Test the valid_page and set the state to normal or disabled.

            Valid pages are in the range zero to max page of magazine,
            valid_pages.  If valid_page enable the buttons. If
            valid_page = 0, disable the back button.  If valid_page
            = valid_pages, disable the forward button.  If valid page
            is neither 0 or valid_pages, enable both buttons.

            Returns
            -------
            None.

            """
            if self.valid.page >= 1:
                self.back_button.config(state='normal')
            else:
                self.back_button.config(state='disabled')
            if self.valid.page < self.valid.pages:
                self.fwd_button.config(state='normal')
            else:
                self.fwd_button.config(state='disabled')

        def disable(self):
            """
            Disable both buttons and set valid_page to 0.

            This method is used whenever the cdrom drive drawer is open.

            Returns
            -------
            None.

            """
            self.back_button.config(state='disabled')
            self.fwd_button.config(state='disabled')
            self.valid_page = 0
            self.valid_pages = 0


