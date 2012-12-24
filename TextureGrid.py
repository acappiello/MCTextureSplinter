"""Class for manipulating texture pack PNGs.

Author: Alex Cappiello
Date: 12/20/12
Updated: 12/21/12
"""

import os
from PIL import Image
import utils


class Grid:
    """Holds all of the information and logic for moving data between the
    joined pngs and the individual block pngs."""
    def __init__(obj, img_path, mapping, workdir,
                 grid_width=16, grid_height=16):
        obj.img_path = img_path
        obj.map = mapping
        obj.workdir = workdir
        obj.grid_width = grid_width
        obj.grid_height = grid_height

    def construct_filename(obj, x, y, block):
        """Of form 'xx_yy_name.png'."""
        filename = obj.workdir + os.sep
        if (x < 10):
            filename = filename + "0"
        filename = filename + str(x) + "_"
        if (y < 10):
            filename = filename + "0"
        filename = filename + str(y) + "_" + block.name + ".png"
        return filename

    def construct_location(obj, x, y, block):
        """Find the location of a block in the combined image."""
        tlx = x * obj.block_size
        tly = y * obj.block_size
        brx = tlx + (block.height * obj.block_size)
        bry = tly + (block.width * obj.block_size)
        return (tly, tlx, bry, brx)

    def write_block_to_file(obj, x, y, block):
        """Extract the raw data for an individual block in the source image
        and save it to a file."""
        block_img = obj.source.crop(obj.construct_location(x, y, block))

        filename = obj.construct_filename(x, y, block)

        block_img.save(filename)

    def deconstruct(obj):
        """Deconstruct an entire combined image file into the individual
        blocks."""

        # Do some sanity checks on input.
        if (not os.path.exists(obj.img_path)):
            utils.raise_error("Input file does not exist: " + obj.img_path)
        obj.source = Image.open(obj.img_path)
        (source_width, source_height) = obj.source.size

        if ((source_width % obj.grid_width != 0) or
                (source_height % obj.grid_height != 0)):
            utils.raise_error("Invalid image size.")

        obj.block_size = source_width / obj.grid_width
        if (obj.block_size != (source_height / obj.grid_height)):
            utils.raise_error("Blocks not square.")

        # Loop over everything, ignoring blank spaces.
        for i in xrange(obj.grid_width):
            for j in xrange(obj.grid_height):
                if (i, j) in obj.map:
                    block = obj.map[(i, j)]
                    obj.write_block_to_file(i, j, block)

    def read_and_paste_block(obj, x, y, block):
        """Read a block from file and place it in the grid.
        Blocks are scaled as needed."""
        filename = obj.construct_filename(x, y, block)

        # Some checks on inputs.
        if (not os.path.exists(filename)):
            utils.raise_error("Could not open: " + filenema)

        block_img = Image.open(filename)
        (width, height) = block_img.size
        if (width / block.width != height / block.height):
            utils.raise_error("Invalid block proportion: " + filename)

        if ((width / block.width) != obj.block_size):
            new_width = obj.block_size * block.width
            new_height = obj.block_size * block.height
            block_img = block_img.resize((new_width, new_height),
                                         Image.BICUBIC)

        obj.output.paste(block_img, obj.construct_location(x, y, block))

    def reconstruct(obj, res=[16]):
        """Assemble the grid from the individual block files.
        If more than one resolution is desired, the largest resolution is
        used and the end result is scaled down. The output files will have
        the size denoted in the filename."""
        res = list(set(res))  # Squish duplicates.
        if (len(res) == 0):
            utils.raise_error("Empty output.")
        res.sort(reverse=True)
        obj.block_size = res.pop(0)

        obj.output = Image.new("RGBA", (obj.block_size * obj.grid_width,
                               obj.block_size * obj.grid_height),
                               (0, 0, 0, 0))

        # Loop over everything, ignoring empty spaces.
        for i in xrange(obj.grid_width):
            for j in xrange(obj.grid_height):
                if (i, j) in obj.map:
                    block = obj.map[(i, j)]
                    obj.read_and_paste_block(i, j, block)

        # Save the primary output size.
        ext = "_" + str(obj.block_size) + "x" + str(obj.block_size) + ".png"
        outfile = obj.img_path.replace(".png", ext)
        obj.output.save(outfile)

        # Save additional output sizes.
        for size in res:
            ext = "_" + str(size) + "x" + str(size) + ".png"
            outfile = obj.img_path.replace(".png", ext)
            dims = (size * obj.grid_width, size * obj.grid_height)
            img = obj.output.resize(dims, Image.BICUBIC)
            img.save(outfile)
