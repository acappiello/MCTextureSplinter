"""Misc. utilities for MCTextureSplinter."""

import sys
import Tkinter
import tkMessageBox

__author__ = "Alex Cappiello"
__license__ = "See LICENSE.txt"


def raise_error(msg):
    """Handle when things go wrong in some reasonable way.
    For now, abort."""
    print "Error: %s" % (msg)
    try:
        root = Tkinter.Tk()
        root.withdraw()
        tkMessageBox.showerror("Error", msg)
    finally:
        sys.exit(1)
