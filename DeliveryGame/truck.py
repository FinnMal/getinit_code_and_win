import time
from tkinter import *


# Truck class: handles the truck object in canvas
class Truck:
    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas

        # default values
        self.column = 0
        self.speed_kmh = 0
        self.move_delay = 0.00001

    # renders the truck
    def render(self):
        # save width, height of canvas
        canvas_width = int(self.canvas['width'])
        canvas_height = int(self.canvas['height'])

        # create truck with canvas image
        truck_image = PhotoImage(file='./assets/img/truck.png')
        self.master.truck_image = truck_image
        self.canvas.create_image((5, canvas_height - 250), image=truck_image, anchor='nw', tags=('truck',))

        # create speed text
        self.canvas.create_text(canvas_width/2, 10, fill='white', font='Arial 13 bold', text='Speed: 0 km/h', tags=('truck_speed',))

    # keyboard listener
    def on_key_press(self, key):
        try:
            if key.char == 'a':
                self.move_left()

            if key.char == 'd':
                self.move_right()
        except Exception as e:
            # handler for special keys
            if key is key.left:
                self.move_left()

            if key is key.right:
                self.move_right()

    # moves the truck one column to left
    def move_left(self):
        # if can move left
        if self.column > 0:
            # set current column
            self.column = self.column - 1

            # animate truck to left column
            for i in range(81):
                time.sleep(self.move_delay)
                self.canvas.move('truck', -1, 0)

    # moves the truck one column to right
    def move_right(self):
        # if can move right
        if self.column < 4:
            # set current column
            self.column = self.column + 1

            # animate truck to right column
            for i in range(81):
                time.sleep(self.move_delay)
                self.canvas.move('truck', 1, 0)

    # returns the canvas ids that overlap the truck
    def get_overlapping_canvas_ids(self):
        x1, y1, x2, y2 = self.canvas.bbox('truck')
        return self.canvas.find_overlapping(x1, y1, x2, y2)

    # shows the current truck speed in canvas (as km/h)
    def show_street_speed(self, speed):
        self.speed_kmh = round(speed * 6.5)
        self.canvas.itemconfigure('truck_speed', text='Speed: ' + str(self.speed_kmh) + ' km/h')
