# Author: Alex Cappiello
# Date: 12/21/12
# Updated: 12/21/12

import tkFileDialog, Grid, os
from terrain import terrain_map
from Tkinter import *

class CallerInfo:
    def __init__ (obj):
        pass

class Gui:
    def launch_deconstruct (obj):
        terrain_path = obj.terrain_path.get()
        if (terrain_path == ""):
            terrain_path = "terrain.png"
        working_path = obj.working_path.get()
        if (working_path == ""):
            working_path = os.getcwd()

        if (obj.run_terrain):
            terrain = Grid.Grid(terrain_path, terrain_map, \
                                    working_path + "/terrain")
            terrain.deconstruct()

    def launch_reconstruct (obj):
        terrain_path = obj.terrain_path.get()
        working_path = obj.working_path.get()
        if (working_path == ""):
            working_path = os.getcwd()
        terrain = Grid.Grid(terrain_path, terrain_map, \
                                working_path + "/terrain")
        resolutions = []
        for (res, state) in obj.states:
            if (state.get()):
                resolutions.append(res)
        terrain.reconstruct(resolutions)

    @staticmethod
    def browse_for_file (e):
        path = tkFileDialog.askopenfilename(filetypes=[("PNG", ".png")])
        if (path != ""):
            e.delete(0, END)
            e.insert(0, path)

    @staticmethod
    def browse_for_folder (e):
        path = tkFileDialog.askdirectory()
        if (path != ""):
            e.delete(0, END)
            e.insert(0, path)

    def init_dict (obj):
        d = dict()
        d["terrain.png"] = CallerInfo()
        d["items.png"] = CallerInfo()
        obj.texture_parts = d

    def init_path_inputs (obj):
        Label(obj.canvas, text="Location of terrain.png:").pack(anchor="w")
        terrain = Frame(obj.canvas)
        terrain_path = Entry(terrain, width=80)
        terrain_path.pack(side=LEFT)
        obj.terrain_path = terrain_path
        terrain_browse = Button(terrain, text="Browse",
                                        command=lambda:
                                            Gui.browse_for_file(terrain_path))
        terrain_browse.pack(side=LEFT)
        terrain.pack()

        Label(obj.canvas, text="Location of items.png:").pack(anchor="w")
        items = Frame(obj.canvas)
        items_path = Entry(items, width=80)
        items_path.pack(side=LEFT)
        obj.items_path = items_path
        items_browse = Button(items, text="Browse",
                                      command=lambda:
                                          Gui.browse_for_file(items_path))
        items_browse.pack(side=LEFT)
        items.pack()

        Label(obj.canvas, text="Working directory:").pack(anchor="w")
        working = Frame(obj.canvas)
        working_path = Entry(working, width=80)
        working_path.pack(side=LEFT)
        obj.working_path = working_path
        working_browse = Button(working, text="Browse",
                                        command=lambda:
                                            Gui.browse_for_folder(working_path))
        working_browse.pack(side=LEFT)
        working.pack()

    def init_res_checkboxes (obj, parent):
        resolutions = [16, 32, 64, 128, 256, 512, 1024]
        checkboxes = Frame(parent)
        Label(checkboxes, text="Resolutions:").pack()
        states = []
        for res in resolutions:
            label = str(res) + "x" + str(res)
            state = IntVar()
            states.append((res, state))
            box = Checkbutton(checkboxes, text=label, variable=state)
            box.pack(anchor="w")
        obj.states = states
        checkboxes.pack(side=LEFT)

    def init_parts (obj, parent):
        parts_box = Frame(parent)
        Label(parts_box, text="Files to process:").pack()
        obj.run_terrain = BooleanVar()
        terrain = Checkbutton(parts_box, text="terrain.png", \
                                  variable = obj.run_terrain)
        terrain.select()
        terrain.pack(anchor="w")
        obj.run_items = BooleanVar()
        items = Checkbutton(parts_box, text="items.png", variable=obj.run_items)
        items.select()
        items.pack(anchor="w")
        parts_box.pack()

    def init_options (obj):
        opt_box = Frame(obj.canvas)
        obj.init_res_checkboxes(opt_box)
        obj.init_parts(opt_box)
        opt_box.pack(anchor="w")

    def build (obj):
        obj.init_dict()
        obj.init_path_inputs()
        obj.init_options()

        deconstruct = Button(obj.canvas, text="Deconstruct",
                                     command=lambda: obj.launch_deconstruct())
        deconstruct.pack(side=LEFT)
        reconstruct = Button(obj.canvas, text="Reconstruct",
                                     command=lambda: obj.launch_reconstruct())
        reconstruct.pack(side=LEFT)

    def __init__ (obj):
        root = Tk()

        window_width = 800
        window_height = 600

        obj.canvas = Canvas(root)#, width=window_width, height=window_height)
        obj.canvas.pack()
        #root.resizable(width=0, height=0)

        obj.window_width = window_width
        obj.window_height = window_height

        obj.build()
        # set up events
        #root.bind("<Key>", lambda e: keyPressed(e, canvas))
        #timerFired(canvas, speedMultiplier)
        # and launch the app
        # This call BLOCKS (so your program waits until you close the window!)
        root.mainloop()
