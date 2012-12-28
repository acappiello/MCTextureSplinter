"""Class for manipulating texture pack PNGs."""

import os
from PIL import Image
import utils

__author__ = "Alex Cappiello"
__license__ = "See LICENSE.txt"


class Grid:
    """Holds all of the information and logic for moving data between the
    joined pngs and the individual block pngs."""
    def __init__(self, img_path, mapping, workdir,
                 grid_width=16, grid_height=16):
        # Inputs
        self.img_path = img_path
        self.map = mapping
        self.workdir = workdir
        self.grid_width = grid_width
        self.grid_height = grid_height

        # Other defaults
        self.filename_numbers = True

    def disable_filename_numbers(self):
        """Turn off numbering the position in the grid in the filenames."""
        self.filename_numbers = False

    def construct_filename(self, x, y, block):
        """Of form 'xx_yy_name.png'."""
        filename = self.workdir + os.sep
        if (self.filename_numbers):
            # Nice formatting would break if > 2 digits.
            if (x < 10):
                filename += "0"
            filename += "%d_" % (x)
            if (y < 10):
                filename += "0"
            filename += "%d_" % (y)
        filename +="%s.png" % (block.name)
        return filename

    def construct_location(self, x, y, block):
        """Find the location of a block in the combined image."""
        tlx = x * self.block_size
        tly = y * self.block_size
        brx = tlx + (block.height * self.block_size)
        bry = tly + (block.width * self.block_size)
        return (tly, tlx, bry, brx)

    def write_block_to_file(self, x, y, block):
        """Extract the raw data for an individual block in the source image
        and save it to a file."""
        block_img = self.source.crop(self.construct_location(x, y, block))

        filename = self.construct_filename(x, y, block)

        block_img.save(filename)

    def deconstruct(self):
        """Deconstruct an entire combined image file into the individual
        blocks."""
        # Do some sanity checks on input.
        if (not os.path.exists(self.img_path)):
            utils.raise_error("Input file does not exist: " + self.img_path)
        self.source = Image.open(self.img_path)
        (source_width, source_height) = self.source.size

        if ((source_width % self.grid_width != 0) or
                (source_height % self.grid_height != 0)):
            utils.raise_error("Invalid image size.")

        self.block_size = source_width / self.grid_width
        if (self.block_size != (source_height / self.grid_height)):
            utils.raise_error("Blocks not square.")

        # Loop over everything, ignoring blank spaces.
        for i in xrange(self.grid_width):
            for j in xrange(self.grid_height):
                if (i, j) in self.map:
                    block = self.map[(i, j)]
                    self.write_block_to_file(i, j, block)

    def read_and_paste_block(self, x, y, block):
        """Read a block from file and place it in the grid.
        Blocks are scaled as needed."""
        filename = self.construct_filename(x, y, block)

        # Some checks on inputs.
        if (not os.path.exists(filename)):
            utils.raise_error("Could not open: " + filename)

        block_img = Image.open(filename)
        (width, height) = block_img.size
        if (width / block.width != height / block.height):
            utils.raise_error("Invalid block proportion: " + filename)

        if ((width / block.width) != self.block_size):
            new_width = self.block_size * block.width
            new_height = self.block_size * block.height
            block_img = block_img.resize((new_width, new_height),
                                         Image.BICUBIC)

        self.output.paste(block_img, self.construct_location(x, y, block))

    def reconstruct(self, res=[16]):
        """Assemble the grid from the individual block files.
        If more than one resolution is desired, the largest resolution is
        used and the end result is scaled down. The output files will have
        the size denoted in the filename."""
        res = list(set(res))  # Squish duplicates.
        if (len(res) == 0):
            utils.raise_error("Empty output.")
        res.sort(reverse=True)
        self.block_size = res.pop(0)

        self.output = Image.new("RGBA", (self.block_size * self.grid_width,
                               self.block_size * self.grid_height),
                               (0, 0, 0, 0))

        # Loop over everything, ignoring empty spaces.
        for i in xrange(self.grid_width):
            for j in xrange(self.grid_height):
                if (i, j) in self.map:
                    block = self.map[(i, j)]
                    self.read_and_paste_block(i, j, block)

        # Save the primary output size.
        ext = "_" + str(self.block_size) + "x" + str(self.block_size) + ".png"
        outfile = self.img_path.replace(".png", ext)
        self.output.save(outfile)

        # Save additional output sizes.
        for size in res:
            ext = "_" + str(size) + "x" + str(size) + ".png"
            outfile = self.img_path.replace(".png", ext)
            dims = (size * self.grid_width, size * self.grid_height)
            img = self.output.resize(dims, Image.BICUBIC)
            img.save(outfile)
