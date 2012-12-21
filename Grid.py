import utils, os
from PIL import Image

class Grid:
    """Holds all of the information and logic for moving data between the
    joined pngs and the individual block pngs."""
    def __init__ (obj, img_path, mapping, workdir, res = [16], \
                      grid_width = 16, grid_height = 16):
        obj.img_path = img_path
        obj.map = mapping
        obj.workdir = workdir
        obj.res = res
        obj.grid_width = grid_width
        obj.grid_height = grid_height

    def write_block_to_file (obj, x, y, block):
        """Extract the raw data for an individual block in the source image
        and save it to a file."""

        # Something seems to be getting flipped around here.
        # Works now, but unsure what exactly was wrong.
        tlx = x * obj.block_size
        tly = y * obj.block_size
        brx = tlx + (block.height * obj.block_size)
        bry = tly + (block.width * obj.block_size)
        block_img = obj.source.crop((tly, tlx, bry, brx))

        # Of form 'xx_yy_name.png'.
        filename = obj.workdir + os.sep
        if (x < 10):
            filename = filename + "0"
        filename = filename + str(x) + "_"
        if (y < 10):
            filename = filename + "0"
        filename = filename + str(y) + "_" + block.name + ".png"

        block_img.save(filename)

    def deconstruct (obj):
        """Deconstruct an entire combined image file into the individual
        blocks."""

        # Do some sanity checks on input.
        if (not os.path.exists(obj.img_path)):
            utils.raise_error("Input file does not exist: " + obj.img_path)
        obj.source = Image.open(obj.img_path)
        (source_width, source_height) = obj.source.size

        if ((source_width % obj.grid_width != 0) or \
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
