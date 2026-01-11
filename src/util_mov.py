# -*- coding: utf-8 -*-
"""
National Geographic Society CD Movies.

This module allows the NgsApp to optionally open these files.  I
would have used the Windows Media Player, but it can not open the
NGS .MOV file type.  The vlc media player is a free app that is
available through the Microsoft Store.

Note: The NGS Magazine CDs have four introduction and one exit movies
available on all NGS Magazine CDs.  These files are:
 -- "INTRO01.MOV"  The NGS Globe.
 -- "INTRO02.MOV"  National Geographic Interactive promotion.
 -- "INTRO03.MOV"  An advertisement for Kodak Kotochrome film
 -- "INTRO04.MOV"  National Geographic Magazine Covers.
and
 -- "EXIT.MOV"  National Geographic Magazine Credits for the CDs.

how to embed VLC inside a Tkinter window

Created on Wed Jan  7 11:22:33 2026.

@author: Bob
"""
# from tkinter import messagebox
import tkinter.messagebox as messagebox

import os
import subprocess


from util_files import get_directory
# %%


def play_intro_1():
    """
    Play the Intro 01 Movie, a movie of the NGS Globe.

    Returns
    -------
    None.

    """
    _play_ngs_mov(folder="INTRO", filename="INTRO01.MOV")
# %%


def play_intro_2():
    """
    Play the Intro 02 Movie, a movie about NGS Interactive.

    Returns
    -------
    None.

    """
    _play_ngs_mov(folder="INTRO", filename="INTRO02.MOV")
# %%


def play_intro_3():
    """
    Play the Intro 03 Movie, an advertisement for Kodak film and CDs.

    Returns
    -------
    None.

    """
    _play_ngs_mov(folder="INTRO", filename="INTRO03.MOV")
# %%


def play_intro_4():
    """
    Play the Intro 01 Movie, a movie of NGS Magazine Covers.

    Returns
    -------
    None.

    """
    _play_ngs_mov(folder="INTRO", filename="INTRO04.MOV")
# %%


def play_credits():
    """
    Play the EXIT 01 Movie.

    Returns
    -------
    None.

    """
    _play_ngs_mov(folder="EXIT", filename="EXIT01.MOV")
# %%


def _play_ngs_mov(folder="EXIT", filename="EXIT01.MOV"):
    """
    Play the NGS exit video.

    The following code optionally allows one of the NGS movies to play
    when the movie is selected from the help menu.  (Future: the Movie
    plays when the NGS Reader app opens or closes).
    """
    program_location = r"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
    if not os.path.isfile(program_location):
        _requires()
        return

    # self.geometry('625x1000')
    # Screen location given by "--video_x=, --video_y= or
    # --fullscreen
    movie_options = ("--play-and-exit, --qt-minimal-view, ",
                     "--width=625", "--height=1000",
                     "--no-video-title-show",
                     "--autoscale")
    # open a windows program with a .MOV file.
    fn = str(get_directory(folder=folder))
    print("Path name is ", fn)
    pth = os.path.join(fn, filename)
    print(pth)

    sp = subprocess.Popen([
        program_location,
        pth,
        "--play-and-exit",
        "--qt-minimal-view",
        "--width=625",
        "--height=1000"
        ])

    # If this is an exit (Credits)  wait for it to complete
    # Before allowing any other actions.  This is if we
    # decide to add the credits movie to the exit routine.
    if "EXIT" in folder:
        sp.wait()
        print("VLC has finished playing!")


# %%


def test():
    """Tests the requires dialog box."""
    _requires()

# %%


def _requires():
    """Open the requires dialog box for this app."""
    program = "VLC media player"
    msg = ("This programs requires an external app, ",
           "VLC media player to display movies.",
           " VLC media player is available",
           " free from the Microsoft Store.")
    req_title = 'Requires {}'.format(program)
    req_message = '{}'.format(msg)
    messagebox.showinfo(req_title, req_message)
