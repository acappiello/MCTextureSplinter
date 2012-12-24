"""Tkinter-based GUI for MCTextureSplinter."""

import os
from Tkinter import *
import tkFileDialog
import TextureGrid
from terrain import terrain_map

__author__ = "Alex Cappiello"
__license__ = "See LICENSE.txt"


class CallerInfo:
    """Collects all information needed to build a TextureGrid.Grid object for
    each file we work with."""
    def __init__(self, mapping):
        """Initially, only the mapping is needed. Additional information is
        added as needed."""
        self.map = mapping


class Gui:
    """Everything needed for the Tkinter GUI."""
    def make_grid(self, item, entry):
        """Construct a TextureGrid.Grid object by pulling information from the
        GUI."""
        working_path = self.working_path.get()
        if (working_path == ""):
            working_path = os.getcwd()

        path = entry.path.get()
        if (path == ""):
            path = item
        subdir = os.sep + os.path.splitext(item)[0]
        return TextureGrid.Grid(path, entry.map, working_path + subdir)

    def launch_deconstruct(self):
        """Loop over all files, calling deconstruct."""
        for (item, entry) in self.texture_parts.items():
            if (entry.state.get()):
                grid = self.make_grid(item, entry)
                grid.deconstruct()

    def launch_reconstruct(self):
        """Loop over all files, calling reconstruct."""
        working_path = self.working_path.get()
        if (working_path == ""):
            working_path = os.getcwd()
        for (item, entry) in self.texture_parts.items():
            if (entry.state.get()):
                grid = self.make_grid(item, entry)
                resolutions = []
                for (res, state) in self.res_options:
                    if (state.get()):
                        resolutions.append(res)
                grid.reconstruct(resolutions)

    @staticmethod
    def browse_for_file(e):
        """Pull up a file browsing dialog and dump the resulting path into the
        Tkinter.Entry widget e."""
        path = tkFileDialog.askopenfilename(filetypes=[("PNG", ".png")])
        if (path != ""):  # Unless they hit cancel.
            e.delete(0, END)
            e.insert(0, path)

    @staticmethod
    def browse_for_folder(e):
        """Pull up a folder browsing dialog and dump the resulting path into
        the Tkinter.Entry widget e."""
        path = tkFileDialog.askdirectory()
        if (path != ""):  # Unless they hit cancel.
            e.delete(0, END)
            e.insert(0, path)

    def init_dict(self):
        """All texture pack files to be split at added here."""
        d = dict()
        d["terrain.png"] = CallerInfo(terrain_map)
        d["items.png"] = CallerInfo(None)
        self.texture_parts = d

    def init_path_inputs(self):
        """Add an Entry field to the GUI for each file and one for the working
        directory. Each is in its own Frame with a browse Button."""
        # Need this to evaluate input argument immediately.
        # Faking a curried function. Thanks 15-150.
        browse_wrapper = lambda v: lambda: Gui.browse_for_file(v)

        for item in self.texture_parts.keys():
            Label(self.canvas, text="Location of %s:" % item).pack(anchor="w")
            container = Frame(self.canvas)
            path = Entry(container, width=80)
            path.pack(side=LEFT)
            cmd = browse_wrapper(path)
            self.texture_parts[item].path = path
            browse = Button(container, text="Browse",
                            command=cmd)
            browse.pack(side=LEFT)
            container.pack()

        Label(self.canvas, text="Working directory:").pack(anchor="w")
        working = Frame(self.canvas)
        working_path = Entry(working, width=80)
        working_path.pack(side=LEFT)
        self.working_path = working_path
        working_browse = Button(working, text="Browse",
                                command=lambda:
                                Gui.browse_for_folder(working_path))
        working_browse.pack(side=LEFT)
        working.pack()

    def init_res_checkboxes(self, parent):
        """Add checkboxes to the GUI for each possible output resolution."""
        resolutions = [16, 32, 64, 128, 256, 512, 1024]
        checkboxes = Frame(parent)
        Label(checkboxes, text="Resolutions:").pack()
        states = []
        for res in resolutions:
            label = str(res) + "x" + str(res)
            state = BooleanVar()
            states.append((res, state))
            box = Checkbutton(checkboxes, text=label, variable=state)
            box.pack(anchor="w")
            if (len(states) == 1):
                box.select()
        self.res_options = states
        checkboxes.pack(side=LEFT)

    def init_parts(self, parent):
        """Add checkboxes to the GUI for each file to decide whether to process
        it. All are initially enabled."""
        parts_box = Frame(parent)
        Label(parts_box, text="Files to process:").pack()
        for item in self.texture_parts.keys():
            state = BooleanVar()
            button = Checkbutton(parts_box, text=item, variable=state)
            button.select()
            button.pack(anchor="w")
            self.texture_parts[item].state = state

        parts_box.pack()

    def init_options(self):
        """Wrapper for calling everything in the Frame for various options."""
        opt_box = Frame(self.canvas)
        self.init_res_checkboxes(opt_box)
        self.init_parts(opt_box)
        opt_box.pack(anchor="w")

    def build(self):
        """Wrapper for calling init functions for various other pieces of the
        GUI."""
        self.init_dict()
        self.init_path_inputs()
        self.init_options()

        deconstruct = Button(self.canvas, text="Deconstruct",
                             command=lambda: self.launch_deconstruct())
        deconstruct.pack(side=LEFT)
        reconstruct = Button(self.canvas, text="Reconstruct",
                             command=lambda: self.launch_reconstruct())
        reconstruct.pack(side=LEFT)

    def __init__(self):
        """Create the root and canvas. Then, build the GUI and run."""
        root = Tk()

        self.canvas = Canvas(root)
        self.canvas.pack()
        #root.resizable(width=0, height=0)

        self.build()
        # set up events
        #root.bind("<Key>", lambda e: keyPressed(e, canvas))
        #timerFired(canvas, speedMultiplier)
        # and launch the app
        # This call BLOCKS (so your program waits until you close the window!)
        root.mainloop()
