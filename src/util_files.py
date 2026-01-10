# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:32:00 2024.

The National Geographic CD is named NGS_Year1_Year2, where year 1 is
    the first year whose magazine is on the CD and Year2 is the last
    year on the CD.  On the CD, each magazine in a folder under the
    IMAGES primary folder.  Folder names are ###L 3 number + letter
    combinations.  The first character tells the century, 1=1800,
    2=1900.  The second and third character of the folder name tell
    the year of the NG magazine.  The last L represents the month of
    the NG magizine, A=Janurary, ... L=December.

    Within each magazine folder, the files are labeled with the year
    and month as above combined with a 1 digit alphanumeric value.
    If this 4 digit value is all numeric, it represents the actual
    page number in the magazine. If the file name ends with A or Z,
    it is an advertisement page.  If the last 4 characters of the
    file name are C01A, this is the cover for the magazine.

@author: Bob
"""
import datetime
import os
import psutil
import re
import tkinter as tk
import tkinter as Grid
import tkinter.ttk as ttk
import win32api

from pathlib import Path
from PIL import ImageTk

import util_ngs as util
# %% Build a list of our files and folders.
# This section computes the dictionary that gives the user
# a view of the magazines by month and year, instead of the
# obtuse NGS folder names.  The result is a dictionary with
# keys of month and year and values of the path to that
# month and year's page images.
# %% Find where our CD lives.

# %%% Get the drive letter where the CD is mounted.


def get_drive_label(drive_letter="D:\\"):
    """
    Return two strings containing the drive title and file system type.

    Drive data returned by win32api.GetVolumeInformation(drive_letter)
    function. Tuple has 4 components (drive_name, drive_size,
    drive_space_used, drive_format).

    Parameters
    ----------
    drive_letter : path or string
        This should be one of the mounted drives on this system.

    Returns
    -------
    string
        DESCRIPTION.

    """
    try:
        drive_data = win32api.GetVolumeInformation(f"{drive_letter}")
        return drive_data[0], [-1]
    except Exception as e:
        return str(e)
# %%% Get the IMAGE folder path and CD date ranges.


def get_directory(to_find="NGS", folder="IMAGES"):
    """
    Find a folder on a National Geographic CD.

    Find the location of folders on a National Geographic
    CD if it exists.  The default folder is "IMAGES", where the
    pages of the NG Magazines are stored.

    Look at the volume name of all the mounted volumes (on Windows
    the disk drive letters) to determine if the volume name contains the
    to_find string. The default string is 'NGS' for National Geographic
    Society.  If the name contains the to_find string, return the
    location of the folder on this CD and for images, the date range.

    Parameters
    ----------
    to_find : str, optional
        A string identifying a drive name or partial name.
        The default is "NGS".
    folder : str, optional
        A string identifying a folder on the CD. Default is "IMAGES".
        Other valid values include, "BUTTONS", "EXIT", and "INTRO".
        All other folders on the NGS CD are associated with the NGS
        provided application, which no longer works with modern
        Windows OS.

    Returns
    -------
    tuple
        Returns a tuple containing the drive label, the drive format,
        and the path to the IMAGE file on the disk.

    """
    partitions = psutil.disk_partitions()  # find mounted drives.
    # print("Partitions: ", partitions, "\n\n")
    p1 = ""
    date_range = []
    # Go through drives to see if the name of one contains our search string.
    for partition in partitions:
        # Get the drive letter of the mounted partition
        drive_letter = partition.device
        drive_data = get_drive_label(drive_letter)
        # print("drive letter =", drive_letter, ": ", drive_data)
        # Look for a drive label containing the to_find string.
        if to_find in drive_data[0]:
            # ngs1 = re.search(to_find, drive_data[0])
            # print("We found our drive drive.")
            # if ngs1 is not None:
            # NGS CDs contain the year range of magazines that are
            # on the disk.  While we are here, capture it for the
            # main window title.
            date_range = re.split("_", drive_data[0])

            # The drive letter + the directory name 'IMAGES'
            # gives us the location of all the magazine folders.
            p = os.path.join(drive_letter, folder)
            if os.path.isdir(p):
                p1 = p
            if "IMAGES" in folder:
                return p1, [date_range[1], date_range[2]]
            else:
                return p1    # return the folder's complete path.
    # if to_find not in drive_data:
        # raise NameError("Unable to find National Geographic CD.")
    # If we go through all the drive names and don't find a NGS CD
    # then return a blank.
    print("Not a NGS disk", to_find, ": ", drive_data)
    return '', ['', '']


# %%% Buid a magazine index. Build a list of folders


def build_magazine_index(base_path, date_range):
    """
    Build an index of National Geographic magazine months from CD.

    Each National Geographic CD has the images of the magazine
    pages divided up into folders.  Each folder contains one
    month's magazine page images.  This function builds a
    dictionary that contains the month and year as a key, and
    the path to the directory for that month and year's images.

    Parameters
    ----------
    base_path : TYPE
        DESCRIPTION.
    date_range : TYPE
        DESCRIPTION.

    Returns
    -------
    magazine_index : TYPE
        DESCRIPTION.

    """
    p = Path(base_path)
    mag_indx = {}
    for child in p.iterdir():
        if os.path.isdir(child):
            yr, mo, child = decode_dir_name(child)
            # If the year is already in the dictionary,
            # add the new month to the value.
            if yr in mag_indx:
                val = mag_indx[yr]
                val[mo] = child
            # else create a new yer.
            else:
                mag_indx.setdefault(yr, {mo: child})
    return mag_indx
# %% Decode the directory name into years and months and a path
# to the files for this magazine.


def decode_dir_name(child):
    """Decode a NGS CD directory name into a month, year, and path."""
    sname = str(child.stem)
    century = 1900
    if sname[0] == 1:
        century = 1800
    if sname[1:3].isdigit():
        yr = century + int(sname[1:3])
    else:
        yr = str(century)[0:2] + str(sname[1:3])
    lt = sname[-1]
    if not util.test_string(lt):
        raise ValueError(
            f"Value must be a letter A to L. {lt} given.\
             {child}, {sname}")
    mo = util.lmonth(lt)
    return yr, mo, child
# %%% Build Page List.
# Given a folder, build a list of the files in that folder.


def build_page_list(m_path, include_adds=False):
    """
    Create a list of all the JPG page image files in a given folder.

    The National Geographic CD has each magazine in a folder under the
    IMAGES primary folder.  Given a folder name, return a list of
    all the pages (JPG files) in the folder.

    The user selects a year and month for a magazine to look at. This
    function creates a list of all the pages in the selected magazine.
    page_list[0] is always the selected months magazine cover.

    Parameters
    ----------
    m_path : str or path or Path object
        A string or path object describing the location of a folder
        on the CD, containing one National Geographic magazine.
    include_adds : boolean
        The National Geographic CD differentates pages that are
        advertisements.  This option could allow a user to choose
        to not include adds in threir view of the magazines.

    Returns
    -------
    page_list : list
        returns a list containing paths to all the JPG files in the
        given folder. JPG[0] corresponds to page 1 of the magazine
        JPG[len(JPG)] corresponds to the last page of the magazine.

    """
    p = Path(m_path)
    page_list = []
    for child in p.iterdir():
        if os.path.isfile(child):
            # if the child points to a JPG file, add it to the list.
            osp = os.path.splitext(child)
            if osp[1] == ".JPG"\
                    or osp[1] == ".jpg":
                # When we find the cover, put it in position 0
                if "C01A" in str(child):
                    page_list.insert(0, child)
                elif include_adds and (str(child)[:-1] == "A"
                                       or str(child)[:-1] == "Z"):
                    pass  # skip all the advertisements
                else:
                    page_list.append(child)
    return page_list

# %%% Get the image file that represents the selected page.


def get_image(df, page_list, page_no=0):
    """
    Read in the image of the selected page and add it to the target frame.

    Given a frame, folder and page number, read in the image
    and store it in the frame for viewing.

    Parameters
    ----------
    df : tk.Frame
        The display frame where we will put the page image.
    page_list : list
        A list of pages in the currently selected magazine.
    page_no : int, optional
        The integer describing the current page. The default is 0.

    Returns
    -------
    None.

    """
    # We found and put the cover as the first element of the page_list.
    # Consequently, we now start our page numbers with zero, instead
    # of one. 12/13/24 RHB.
    image_path = page_list[page_no]
    # Clear the frame of all old widgets.
    # Read in our new image
    img = ImageTk.PhotoImage(file=image_path)

    _clear_frame(df)

    display = tk.Label(df, text='Center', justify=tk.CENTER)
    display.grid(column=0, row=1, columnspan=True, rowspan=True)

    # and add it to our display label widget

    ht = int(img.height())+20
    wd = int(img.width())+30
    parent = df.winfo_parent()
    parent_widget = df.nametowidget(parent)

    display.config(image=img, width=wd, height=ht, padx=10, pady=10)
    display.image = img

    str_geom = f"{wd+20}x{ht + 20}"
    parent_widget.geometry(str_geom)


def get_image_canvas(df, page_list, page_no=0):
    """
    Get the image and put it into a canvas widget.

    Parameters
    ----------
    df:  container -Frame
        The display frame for this widget.
    page_list : list
        a list containing paths to all pages of the current NGS
        magazine.
    page_no : integer, optional
        Page number in the current magazine. The default is page 0,
        the cover.

    Returns
    -------
    None.

    """
    df.columnconfigure(0, weight=1)  # add column
    df.rowconfigure(0, weight=1)
    df.grid(column=0, row=1,  columnspan=True, rowspan=True,
            sticky='nsew')

    # print("get_image: Creating Scrollable Canvas")
    # container.columnconfigure(1, weight=1)
    # df.columnconfigure(1, weight=1)  # add column
    # df.rowconfigure(1, weight=1)  # add row"""

    # Load our image.
    # print("get_image: Created Scrollable Canvas")
    # Get our target path.
    image_path = page_list[page_no]
    # print(f"image_path = {image_path}")
    # Read in our new image
    # print("get_image: loading image.")
    img = ImageTk.PhotoImage(file=image_path)
    # capture image in df so it does not get garbage collected.
    df.image = img

    # Clear the frame of all old widgets.
    # print("get_image: Clear the frame of all old widgets.")
    _clear_frame(df)

    # top = df.winfo_toplevel()
    # canvas = top.build_scrollable_canvas(df)

    canvas = tk.Canvas(df, bg='red')
    scrollbar_x = ttk.Scrollbar(df, orient="horizontal",
                                command=canvas.xview)
    scrollbar_y = ttk.Scrollbar(df, orient="vertical",
                                command=canvas.yview)
    canvas.configure(xscrollcommand=scrollbar_x.set,
                     yscrollcommand=scrollbar_y.set)
    canvas.grid(column=0, row=0, padx=2, pady=2, sticky='nesw')
    scrollbar_x.grid(column=0, row=1, padx=2, pady=2, sticky='nesw')
    scrollbar_y.grid(column=1, row=0, padx=2, pady=2, sticky='nesw')

    # print("Adding image to canvas.")
    canvas.create_image(0, 0, anchor="nw", image=img)
    ht, wd = get_size(df, img)
    # ht = int(img.height())
    # wd = int(img.width())
    # canvas.config(image=img, width=wd, height=ht, padx=5, pady=5)
    canvas.config(width=wd, height=ht)  # , padx=5, pady=5)
    canvas.config(scrollregion=canvas.bbox(tk.ALL))

    canvas.columnconfigure(0, weight=1)
    canvas.rowconfigure(0, weight=1)
    df.rowconfigure(0, weight=1)

    # set_size(df, img)
    str_geom = f"{wd+20}x{ht+20}"
    top = df.winfo_toplevel()
    top.resizable(True, True)
    # top.bind("<Configure>", on_window_resize)
    top.geometry(str_geom)


def all_children(wid, finList=None, indent=0):
    """List all children of the container wid."""
    finList = finList or []
    print(f"{'   ' * indent}{wid=}")
    children = wid.winfo_children()
    for item in children:
        finList.append(item)
        all_children(item, finList, indent + 1)
    return finList


def _clear_frame(frame):
    # Clear out old widgets before adding new ones.
    for widget in frame.winfo_children():
        widget.destroy()


def get_size(df, img):
    """
    Calculate the size we want to use to display the magazine.

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    img : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    # top = df.winfo_toplevel()
    # ht = top.height
    # wd = top.width
    # print(f"top width = {wd}, height = {ht}")
    # and add it to our display label widget
    iht = int(img.height())
    iwd = int(img.width())
    print(f"Image width = {iwd}, height = {iht}")
    swd = df.winfo_screenwidth()
    sht = df.winfo_screenheight()
    print(f"Monitor width = {swd}, height = {sht}")
    # Compute which ever is larger and use that as the
    # requested window size.
    # If magazine height > screen height
    if iht > sht:
        fht = int(sht*3/4)
    else:
        fht = iht
    # If
    if iwd > swd:
        fwd = int(swd*3/4)
    else:
        fwd = iwd

    return fht, fwd

    # display.config(image=img, width=iwd, height=iht, padx=5, pady=5)
    # display.image = img
    # str_geom = f"{int((3/4)*fwd+16)}x{int((3/4)*fht+20)}"
    # df.grid(row=0, column=0, sticky="nsew")
    # df.columnconfigure(0, weight=1)
    # df.rowconfigure(0, weight=1)
    # parent_widget.geometry(str_geom)
    # top = df.winfo_toplevel()
    # top.resizable(True, True)
    # top.bind("<Configure>", on_window_resize)
    # top.geometry(str_geom)


def on_window_resize(event):
    """
    Resize the top level window.

    Parameters
    ----------
    event : tkinter event
        event that occurs when the user resizes the top level window.

    Returns
    -------
    None.

    """
    width = event.width
    height = event.height
    print(f"Window resized to {width}x{height}")

# %%% get the time this application was last compiled.


def get_compile_time(file_path, fmt='%m-%d-%Y %H:%M:%S'):
    """
    Get the last time the calling program was modified.

    Get the last time the calling program was modified and
    return if as a formated string.  Used by the About
    Menu to provide information to the user about the appl.

    Parameters
    ----------
    file_path : path or string
        path or string to the calling program.
    fmt : string, optional
        A string using the standard datetime object formats
        describing when the calling file was last modified.
        The default is '%m-%d-%Y %H:%M:%S'.

    Returns
    -------
    mod_time : string
        A string in the given format describing when the last time the
        calling file was modified.

    """
    # Get the last modification time
    mod_time = os.path.getmtime(file_path)

    # Convert it to a readable format
    mod_time =\
        datetime.datetime.fromtimestamp(mod_time).\
        strftime(fmt)

    return mod_time
