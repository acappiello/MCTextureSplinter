# Author: Alex Cappiello
# Date: 12/21/12
# Updated: 12/21/12

import Tkinter, tkFileDialog, Grid, os
from terrain import terrain_map

def launch_deconstruct (canvas):
    terrain_path = canvas.data.terrain_path.get()
    if (terrain_path == ""):
        terrain_path = "terrain.png"
    working_path = canvas.data.working_path.get()
    if (working_path == ""):
        working_path = os.getcwd()
    terrain = Grid.Grid(terrain_path, terrain_map, working_path + "/terrain")
    terrain.deconstruct()

def launch_reconstruct (canvas):
    terrain_path = canvas.data.terrain_path.get()
    working_path = canvas.data.working_path.get()
    if (working_path == ""):
        working_path = os.getcwd()
    terrain = Grid.Grid(terrain_path, terrain_map, working_path + "/terrain")
    resolutions = []
    for (res, state) in canvas.data.states:
        if (state.get()):
            resolutions.append(res)
    terrain.reconstruct(resolutions)

def browse_for_file (e):
    path = tkFileDialog.askopenfilename(filetypes=[("PNG", ".png")])
    if (path != ""):
        e.delete(0, Tkinter.END)
        e.insert(0, path)

def browse_for_folder (e):
    path = tkFileDialog.askdirectory()
    if (path != ""):
        e.delete(0, Tkinter.END)
        e.insert(0, path)

def init_path_inputs (canvas):
    Tkinter.Label(canvas, text="Location of terrain.png:").pack(anchor="w")
    terrain = Tkinter.Frame(canvas)
    terrain_path = Tkinter.Entry(terrain, width=80)
    terrain_path.pack(side=Tkinter.LEFT)
    canvas.data.terrain_path = terrain_path
    terrain_browse = Tkinter.Button(terrain, text="Browse",
                                    command=lambda:
                                        browse_for_file(terrain_path))
    terrain_browse.pack(side=Tkinter.LEFT)
    terrain.pack()

    Tkinter.Label(canvas, text="Location of items.png:").pack(anchor="w")
    items = Tkinter.Frame(canvas)
    items_path = Tkinter.Entry(items, width=80)
    items_path.pack(side=Tkinter.LEFT)
    canvas.data.items_path = items_path
    items_browse = Tkinter.Button(items, text="Browse",
                                    command=lambda:
                                        browse_for_file(items_path))
    items_browse.pack(side=Tkinter.LEFT)
    items.pack()

    Tkinter.Label(canvas, text="Working directory:").pack(anchor="w")
    working = Tkinter.Frame(canvas)
    working_path = Tkinter.Entry(working, width=80)
    working_path.pack(side=Tkinter.LEFT)
    canvas.data.working_path = working_path
    working_browse = Tkinter.Button(working, text="Browse",
                                    command=lambda:
                                        browse_for_folder(working_path))
    working_browse.pack(side=Tkinter.LEFT)
    working.pack()

def init_res_checkboxes (canvas):
    resolutions = [16, 32, 64, 128, 256, 512, 1024]
    checkboxes = Tkinter.Frame(canvas)
    states = []
    for res in resolutions:
        label = str(res) + "x" + str(res)
        state = Tkinter.IntVar()
        states.append((res, state))
        box = Tkinter.Checkbutton(checkboxes, text=label, variable=state)
        box.pack(side=Tkinter.LEFT)
    canvas.data.states = states
    checkboxes.pack()

def init (canvas):
    init_path_inputs(canvas)
    init_res_checkboxes(canvas)

    deconstruct = Tkinter.Button(canvas, text="Deconstruct",
                                 command=lambda: launch_deconstruct(canvas))
    deconstruct.pack(side=Tkinter.LEFT)
    reconstruct = Tkinter.Button(canvas, text="Reconstruct",
                                 command=lambda: launch_reconstruct(canvas))
    reconstruct.pack(side=Tkinter.LEFT)

def run ():
    root = Tkinter.Tk()

    window_width = 800
    window_height = 600

    canvas = Tkinter.Canvas(root)#, width=window_width, height=window_height)
    canvas.pack()
    #root.resizable(width=0, height=0)

    # Set up canvas data and call init
    class Struct: pass

    canvas.data = Struct()
    canvas.data.window_width = window_width
    canvas.data.window_height = window_height

    init(canvas)
    # set up events
    #root.bind("<Key>", lambda e: keyPressed(e, canvas))
    #timerFired(canvas, speedMultiplier)
    # and launch the app
    # This call BLOCKS (so your program waits until you close the window!)
    root.mainloop()
