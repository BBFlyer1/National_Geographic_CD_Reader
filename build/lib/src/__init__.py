# -*- coding: utf-8 -*-
"""
Initialization code for this package, and public API


Created on Sun Nov 10 10:29:51 2024.

@author: Bob
"""

# The following is the API for this application. We only want to
# expose the main, so someone can programatically run the app.
# We also want to expose the NgsApp and BaseApp classes so they
# could be extended if necessary.

from app_class import BaseApp
from ngs_class import NgsApp
from NGS_CD_Reader import main
# import util_files
# import util_monitors
# import util_ngs
# import util_print

__all__ = ['main', 'BaseApp', 'NgsApp']
