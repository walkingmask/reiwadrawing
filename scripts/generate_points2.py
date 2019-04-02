import json
from pathlib import Path
import random
import tkinter as tk

from PIL import Image, ImageTk


cropped_path = './cropped'
output_path = './points.json'


IMAGE_WIDTH = 364
IMAGE_HEIGHT = 236
IMAGE_POS_X = IMAGE_WIDTH // 2
IMAGE_POS_Y = IMAGE_HEIGHT // 2

CANVAS_WIDTH = IMAGE_WIDTH
CANVAS_HEIGHT = IMAGE_HEIGHT
CANVAS_POS_X = 20
CANVAS_POS_Y = 20

CANVAS_BG = 'red'
CANVAS_COURSOR = 'plus'

WINDOW_WIDTH = CANVAS_WIDTH + CANVAS_POS_X * 2
WINDOW_HEIGHT = CANVAS_HEIGHT + CANVAS_POS_Y * 2
WINDOW_POS_X = 500
WINDOW_POS_Y = 300
WINDOW_SETTINGS = "{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT,
                                       WINDOW_POS_X, WINDOW_POS_Y)

POINT_SIZE = 7
POINT_R = POINT_SIZE // 2
POINTS_INITIAL_POS = [
    [
        IMAGE_WIDTH // 4 - POINT_R,
        IMAGE_HEIGHT // 4 - POINT_R,
        IMAGE_WIDTH // 4 + POINT_R,
        IMAGE_HEIGHT // 4 + POINT_R,
    ],
    [
        IMAGE_WIDTH // 4 * 3 - POINT_R,
        IMAGE_HEIGHT // 4 - POINT_R,
        IMAGE_WIDTH // 4 * 3 + POINT_R,
        IMAGE_HEIGHT // 4 + POINT_R,
    ],
    [
        IMAGE_WIDTH // 4 * 3 - POINT_R,
        IMAGE_HEIGHT // 4 * 3 - POINT_R,
        IMAGE_WIDTH // 4 * 3 + POINT_R,
        IMAGE_HEIGHT // 4 * 3 + POINT_R,
    ],
    [
        IMAGE_WIDTH // 4 - POINT_R,
        IMAGE_HEIGHT // 4 * 3 - POINT_R,
        IMAGE_WIDTH // 4 + POINT_R,
        IMAGE_HEIGHT // 4 * 3 + POINT_R,
    ],
]

# start tk
root = tk.Tk()
root.geometry(WINDOW_SETTINGS)

# make canvas
canvas = tk.Canvas(root,
                   bg=CANVAS_BG, bd=0,
                   highlightthickness=0, width=CANVAS_WIDTH,
                   height=CANVAS_HEIGHT, cursor=CANVAS_COURSOR)
canvas.place(x=CANVAS_POS_X, y=CANVAS_POS_Y)

# draw initial points
# 01
# 32
points = {
    '0': canvas.create_oval(POINTS_INITIAL_POS[0],
                            outline='green', fill='green', tags='points'),
    '1': canvas.create_oval(*POINTS_INITIAL_POS[1],
                            outline='blue', fill='blue', tags='points'),
    '2': canvas.create_oval(*POINTS_INITIAL_POS[2],
                            outline='yellow', fill='yellow', tags='points'),
    '3': canvas.create_oval(*POINTS_INITIAL_POS[3],
                            outline='cyan', fill='cyan', tags='points'),
}

def get_points_coords(flatten=True):
    coords = []
    for point in points.values():
        _coords = canvas.coords(point)
        if flatten:
            coords.append(_coords[0] + POINT_R)
            coords.append(_coords[1] + POINT_R)
        else:
            coords.append([_coords[0] + POINT_R, _coords[1] + POINT_R])
    return coords

# draw initial line
# 0-1
# | |
# 3-2
points_pos = get_points_coords()
line = canvas.create_line(*points_pos, *points_pos[:2], fill='red', width=1)
canvas.tag_lower(line)

# place initial image
images = [ImageTk.PhotoImage(Image.open(p).convert('RGB'))
          for p in sorted(Path(cropped_path).absolute().glob('*png'))]
image_index = 0
image = images[image_index]
image_item = canvas.create_image(IMAGE_POS_X, IMAGE_POS_Y, image=images[0], tags='image')
canvas.tag_lower('image')

def move(e):
    point = canvas.find_closest(e.x, e.y)[0]
    if not point in points.values(): return
    canvas.coords(point, e.x - POINT_R, e.y - POINT_R, e.x + POINT_R, e.y + POINT_R)
    global line
    canvas.delete(line)
    points_pos = get_points_coords()
    line = canvas.create_line(*points_pos, *points_pos[:2], fill='red', width=1)
    canvas.tag_lower(line, 'points')

def skip(e):
    global points_record
    global image_index
    points_record[image_index] = None
    print(image_index, ':', points_record[image_index])
    image_index += 1
    if image_index == len(images):
        dump(None)
    image = images[image_index]
    canvas.itemconfig(image_item, image=image)

def record(e):
    global points_record
    global image_index
    points_record[image_index] = get_points_coords(False)
    print(image_index, ':', points_record[image_index])
    image_index += 1
    if image_index == len(images):
        dump(None)
    image = images[image_index]
    canvas.itemconfig(image_item, image=image)

def dump(e):
    global points_record
    with open('./points.json', 'w') as f:
        json.dump(points_record, f)
    exit()

points_record = {}

canvas.tag_bind('points', '<Button1-Motion>', move)
canvas.bind_all('<s>', skip) 
canvas.bind_all('<r>', record) 
canvas.bind_all('<d>', dump) 

root.mainloop()
