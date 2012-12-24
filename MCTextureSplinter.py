# Author: Alex Cappiello
# Date: 12/19/12
# Updated: 12/21/12

import TkGUI
from terrain import terrain_map

"""
A tool for combining and splitting Minecraft texture packs.
"""

__author__ = "Alex Cappiello"
__version__ = ".17a"


def print_blocks(blocks, width, height):
    """Print the data in the map."""
    for i in xrange(width):
        for j in xrange(height):
            if (i, j) in blocks:
                block = blocks[(i, j)]
                print "name: " + block.name + " width: " + str(block.width) \
                    + " height: " + str(block.height)


def main():
    """Start the program."""
    TkGUI.Gui()


if __name__ == "__main__":
    main()
