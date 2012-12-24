"""Misc. utilities for MCTextureSplinter."""

import sys
import tkMessageBox

__author__ = "Alex Cappiello"
__license__ = "See LICENSE.txt"


def raise_error(msg):
    """Handle when things go wrong in some reasonable way.
    For now, abort."""
    print "Error: " + msg
    sys.exit(1)
