"""Class for storing information about each block in a texture map."""

__author__ = "Alex Cappiello"
__license__ = "See LICENSE.txt"


class BlockInfo:
    """Information needed for each block in the map."""
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
