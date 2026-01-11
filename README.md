# National_Geographic_CD_Reader
A Python National Geographic CD reader program for Windows.
"""
Created on Thu Dec 12 09:06:15 2024.

@author: Bob
"""

    **Description:**
    In 1997, the National Geographic Society sold a set of CD rom disks
    containing the first 100 years of NGS magazines on CD. This was
    designed to	run on a windows 98/Macintosh 68030 or greater operating
    system.	When Microsoft and Apple improved/changed their operating systems,
    National Geographic choose to discontinue support for this application
    and move access to their magazines to the internet. Recently when
    we tried to run these disks, they would not work with Windows 11 OS.
    However, in looking at the CDs, I determined that the magazine page
	data was in standard .JPG or Quicktime.mov formats.  This application
	is an attempt to construct a modern reader that will display the National
	Geographic magazines in this cd collection.

    **NGS CD Format:**
	The NGS CDs are labeled NGS_StartYear_EndYear, I.E. NGS_1943_1946.
	This is decoded by the application and displayed in the program
	header.

	Within each CD there are a number of folders.  We are interested in
	three of the folders that appear on each CD.  They are **EXIT**,
	**IMAGES**, and **INTRO**. EXIT and INTRO contain NGS Quicktime movies:
	0 INTRO01 contains a movie of the NGS Globe.
	0 INTRO02 contains a movie about NGS Interactive,
	0 INTRO03 contains an advertisement for Kodak film and other
    	products. I suspect that Kodak was a sponsor of the
		construction of the CD set.
	0 INTRO04 contains a movie of select NGS magazine covers.
	0 EXIT contains a movie showing credits for the
		CD project.

	In addition to the above folders, there is the IMAGES folder.
	Each magazine is given its own subfolder within the IMAGES folder.
    The subfolders names can be decoded to the century, year and month
    of the magazine. The naming format of the subfolders is
	a 4 digit string ###L. The first digit is 1 for 1800s or 2
	for magazines in the 1900s.	The 2nd and 3rd digit are the year the
	magazine was published.	The 4th character is a capital 'A' through
	capital 'L' which represent the months Janurary throught December
	respectively.  For example, a folder named 273L would contain the
	magazine December 1973. The images of each page of this magazine
	would be in this subfolder.

    Within this folder, 273L, the individual pages are labeled 273L0729 -
    273K0874. Note, National Geographic numbers their magazine pages
	starting the first edition of each year with page 1 and continuing
	the page count through the year.  The names of each file in the
	273L folder reflect the pages of the December 1973 issue of the
	magazine as page 0729 through 0874.  The cover page is labeled
	273LC01A.  The code finds this C01A substring which is near the
	bottom in the alphanumeric sort of pages and inserts it as
	element 0 in the magazine page list.  The back cover of the
	NGS magazines turns out to be an add, so I skipped showing this.

	**Note:** Currently, this application does not support the
	NGS extended page numbering format. Instead, each magazine is
	displayed in the user page selector as page 1 through X and
	the cover is called page 0.

	Two other folders on the CD may be of future interest.  They are
	0 NAVDB Desc=National Geographic Archives Navigational Database.
	0 SEARCHDB Desc=National Geographic Archives Search Database.

	**Note 1:** The NGS folders	**NAVDB** and the **SEARCHDB**, appear
	to contain databases that I assume point to the locations of articles
	by name or articles by Authors, and may contain other interesting
	information. I consulted Microsoft's Edge AI, Copilot about this.
	Copilot tells me that NGS used a proprietary, non standard format
	for its search and navigation databases, so it is unlikely that
	I will ever be willing to put in the time to decode these
	databases.  Unless someone wants to build a sqlLite or
	some other db and manually enter the article name and author data,
	any user will just have to explore the disks or use the online NGS
	article	database to find specific articles or authors.

    **Application Architecture:**
    This application uses Python and extends the Python Tkinter
    TK class to create an application to find the various magazines
    and display their content.

    The application presents some base menus that includes 'File' with a
    submenus 'Exit' Also, it has a 'Help' menu with submenus 'Help Index',
    not implemented, and 'About'. In addition there is a menu ngs_mov which
    opens the .mov files using an external application called VLC.  VLC
    is available for free from the Microsoft Store.  I extended the menu
    to add a 3rd high level
	menu, called 'NGS Movies',  Since all the Movies are the same on all
	the CDs, I hard coded their names into the util_mov.py file.
    Currently only 'Open Magazine', 'Exit' and 'About' are implemented.

    If the application is started after a National Geographic Society CD
    is inserted in a CD/DVD drive, or when a new National Geographic
    Society CD is mounted in the systems CD/DVD drive, the application
    reads the CD and determines the year range of the magazines on the
    disk and adds this information to the title of the window.

    When the application opens or a new CD is inserted, the application
    finds the first magazine on the currently mounted CD and opens that
    magazine in the reader.  At the same time, the application builds a
    set of menus of the magazine years that are on the mounted CD and
	and generates menus for each year and submenus of each month that
	is available on the CD for that year.  The user can then select from
	the year and month menus whichever magazine they want to open.  These
	year and menus and submenus are installed and removed automatically
	between the 'File' and 'Help" menus.

    The user can switch between any of the National Geographic CDs to view
    any of the magazines in the Society's first 100 years.  The application
    will display a message when the CD is removed and will read the first
    magazine on the CD when a new CD is inserted in the CD/DVD drive.

    A planned followup project is to create a print capability, so that
    specific pages may be printed.