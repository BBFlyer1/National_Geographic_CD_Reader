# -*- coding: utf-8 -*-
"""
National Geographic Society Magazine reader application.

This Python application is designed to read a National Geographic
Society (NGS) Compact Disk (CD).  These were produced in the 1990s
and sold as a set of the first 100 years of National Geographic
Magazines.  The software written at the time is now obsolete, but
the disks contain standard JPG format images of all the magazines
that NGS put out from the 1880s to the 1990s.

The CDs are set up so all the magazines that fit on one CD are
in the top level IMAGES folder.  Witin the IMAGES folder,
each magazine appears in a named folder.  The names start with a
number 1 = 1800, 2 = 1900.  The next two characters are the year
of the magazine, ie 76, etc. The final character in the folder
name is a letter from A to L representing the months A= Janurary,
... L = December.

Change Notes:

debug and print statements removed, unnecessary modules util_print
and util_general removed.

Created on Sun Nov 10 10:45:23 2024.

@author: R. H. Bumpous
"""
# from ngs_class import NgsApp as appl
import ngs_class as ngc
# from util_monitors import cdrom_drawer_monitor
import util_monitors as u_monitors
# from util_files import get_compile_time as gct
import util_files as u_files
# from os.path import abspath
import os.path as o_path

# %% Main routine for


version = 1.1

# Set the about string.
about = f"National Geographic Society Magazines on CD\n\
            Reader Application\n\
by Robert Bumpous -- BBFlyer1@comcast.net\n\
Version {version}\n\
{u_files.get_compile_time(o_path.abspath(__file__))}"

# set window title
title = "NGS Magazines on CD"

app = ngc.NgsApp(title=title, about=about)

cdrom_monitor = u_monitors.cdrom_drawer_monitor(app)
cdrom_monitor.start()

app.after(100, cdrom_monitor.monitor_queue)

app.mainloop()
