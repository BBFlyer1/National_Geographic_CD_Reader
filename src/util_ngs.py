# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:19:27 2024.

General utilities associated with the National Geographic Society
magazines on CD.

@author: Bob
"""

# from pathlib import Path
# %% Section 1
# Converts months and years into a user viewable string.


def month(mo: int):
    """
    Return the English name of the month.

    Given a month number between 1 and 12, return the name
    of the month.

    Raises an exception if the index is out of range.

    Parameters
    ----------
    mo : int
        An integer between 1 and 12 indicating the month.

    Returns
    -------
    str
        A string representing the English name of the month
        of the year.

    """
    month = ""
    if mo > 12 or mo < 1:
        raise ValueError(f"Value must be and integer i\
                         the range 1 to 12. {mo} given.")
    m = mo-1
    months = ['Janurary', 'February', 'March', 'April',
              'May', 'June', 'July', 'August', 'September',
              'October', 'November', 'December']
    try:
        month = months[m]
    except IndexError as e:
        raise e.add_note("Only integers between\
                   1 and 12 are allowed for months.")
    return month


def lmonth(ltr: str):
    """
    Convert the letters A-L into the month equivalent.

    National Geographic labeled their image folders with a
    4 character file name.  The right most character is the month the
    magazine in that folder was released.

    Parameters
    ----------
    ltr : str
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    valid_letters = ["A", "B", "C", "D", "E", "F",
                     "G", "H", "I", "J", "K", "L"]
    lt = ltr.upper()
    i = int(ord(lt) - ord("A")) + 1
    if lt in valid_letters:
        return month(i)
    else:
        raise ValueError(f"Value must be a letter in the range A to L.\
                         {lt} given.")

# %% Section 2


def test_string(ltr, strt="A", end="L"):
    """
    Test if a string is in the range strt, end.

    Parameters
    ----------
    str : str
        The string to be tested.
    strt : str, optional
        The start of the string to test against, typically a
        single character. The default is "A".
    end : str, optional
        The end of the string to test against, typically a
        single character. The default is "L".

    Returns
    -------
    bool
        returns whether the string (chr) is withing the
        strt, end range.
    """
    import re
    # pattern to match characters within range
    pattern = re.compile(f'[{strt}-{end}]')

    # using findall() to extract all matches
    matches = pattern.findall(ltr)
    if matches:
        return True
    else:
        return False


def get_first_mo_yr(mag_mo_yr):
    """
    Find the first year and month of the current National Geographic CD.

    Given the index of the current National Graphic CD, find
    the first month and year.  This is used to initialize the
    application with the first magazine, publication date wise,
    on the mounted NGS CD.

    Parameters
    ----------
    mag_mo_yr : dict
        The index of years and months of the current National
        Geographic CD.

    Returns
    -------
    mo : str
        The name of the first month of the first year on the
        current National Geographic CD.
    yr : str
        The name of the first year on the current National
        Geographic CD..

    """
    mo = ""
    yr = ""
    i = 0
    j = 0
    for k, v in mag_mo_yr.items():
        if i == 0:
            yr = k
        i += 1
        for m, p in v.items():
            if j == 0:
                mo = m
            j += 1
    return mo, yr
