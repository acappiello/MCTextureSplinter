# Author: Alex Cappiello
# Date: 12/21/12
# Updated: 12/21/12

import Tkinter, tkFileDialog, Grid, os
from terrain import terrain_map

class Gui:
    def launch_deconstruct (obj):
        terrain_path = obj.terrain_path.get()
        if (terrain_path == ""):
            terrain_path = "terrain.png"
        working_path = obj.working_path.get()
        if (working_path == ""):
            working_path = os.getcwd()
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
            e.delete(0, Tkinter.END)
            e.insert(0, path)

    @staticmethod
    def browse_for_folder (e):
        path = tkFileDialog.askdirectory()
        if (path != ""):
            e.delete(0, Tkinter.END)
            e.insert(0, path)

    def init_path_inputs (obj):
        Tkinter.Label(obj.canvas, text="Location of terrain.png:").pack(anchor="w")
        terrain = Tkinter.Frame(obj.canvas)
        terrain_path = Tkinter.Entry(terrain, width=80)
        terrain_path.pack(side=Tkinter.LEFT)
        obj.terrain_path = terrain_path
        terrain_browse = Tkinter.Button(terrain, text="Browse",
                                        command=lambda:
                                            Gui.browse_for_file(terrain_path))
        terrain_browse.pack(side=Tkinter.LEFT)
        terrain.pack()

        Tkinter.Label(obj.canvas, text="Location of items.png:").pack(anchor="w")
        items = Tkinter.Frame(obj.canvas)
        items_path = Tkinter.Entry(items, width=80)
        items_path.pack(side=Tkinter.LEFT)
        obj.items_path = items_path
        items_browse = Tkinter.Button(items, text="Browse",
                                      command=lambda:
                                          Gui.browse_for_file(items_path))
        items_browse.pack(side=Tkinter.LEFT)
        items.pack()

        Tkinter.Label(obj.canvas, text="Working directory:").pack(anchor="w")
        working = Tkinter.Frame(obj.canvas)
        working_path = Tkinter.Entry(working, width=80)
        working_path.pack(side=Tkinter.LEFT)
        obj.working_path = working_path
        working_browse = Tkinter.Button(working, text="Browse",
                                        command=lambda:
                                            Gui.browse_for_folder(working_path))
        working_browse.pack(side=Tkinter.LEFT)
        working.pack()

    def init_res_checkboxes (obj):
        resolutions = [16, 32, 64, 128, 256, 512, 1024]
        checkboxes = Tkinter.Frame(obj.canvas)
        states = []
        for res in resolutions:
            label = str(res) + "x" + str(res)
            state = Tkinter.IntVar()
            states.append((res, state))
            box = Tkinter.Checkbutton(checkboxes, text=label, variable=state)
            box.pack(side=Tkinter.LEFT)
        obj.states = states
        checkboxes.pack()

    def build (obj):
        obj.init_path_inputs()
        obj.init_res_checkboxes()

        deconstruct = Tkinter.Button(obj.canvas, text="Deconstruct",
                                     command=lambda: obj.launch_deconstruct())
        deconstruct.pack(side=Tkinter.LEFT)
        reconstruct = Tkinter.Button(obj.canvas, text="Reconstruct",
                                     command=lambda: obj.launch_reconstruct())
        reconstruct.pack(side=Tkinter.LEFT)

    def __init__ (obj):
        root = Tkinter.Tk()

        window_width = 800
        window_height = 600

        obj.canvas = Tkinter.Canvas(root)#, width=window_width, height=window_height)
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
