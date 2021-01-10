import time
import random
import threading

from tkinter import PhotoImage


class ScreenObject:
    def __init__(self, object_id, master, canvas, objects_manager):
        self.id = object_id
        self.canvas = canvas
        self.master = master

        # default values
        self.column = 0
        self.images = []
        self.canvas_id = -1
        self.position = None
        self.recyclable = True
        self.in_canvas = False
        self.min_distance = 200
        self.objects_manager = objects_manager
        self.last_position_update = time.time()

        # add self to objects manager
        self.objects_manager.add(self)

    # returns the ID
    def get_id(self):
        return str(self.id)

    # returns the canvas id
    def get_canvas_id(self):
        return self.canvas_id

    # returns the column
    def get_column(self):
        return self.column

    # adds an image that the object can have
    def add_image(self, path):
        self.images.append(path)

    # returns a random image from images list
    def get_random_image(self):
        if len(self.images) > 0:
            return random.choice(self.images)
        return False

    def set_recyclable(self, recyclable):
        self.recyclable = recyclable

    def is_recyclable(self):
        return self.recyclable

    # returns True if object is placed in canvas
    def is_in_canvas(self):
        return self.in_canvas

    # adds the object to canvas
    def add_to_canvas(self):
        # ask objects_manager to give new position
        new_pos = self.objects_manager.find_position(self)
        if new_pos:
            # save column and x, y coordinates
            self.column = new_pos[0]
            coordinates = self.objects_manager.get_x_pos(column=new_pos[0]), new_pos[1]

            # set image
            canvas_obj = PhotoImage(file='./assets/img/' + self.get_random_image())

            # render object
            setattr(self.master, self.get_id(), canvas_obj)
            self.canvas_id = self.canvas.create_image(coordinates, image=canvas_obj, anchor='nw', tags=(self.get_id(),))

            # places the object under every device counter
            self.canvas.tag_lower(self.get_id())

            self.in_canvas = True
            self.position = None
        else:
            print('[SCREEN_OBJECT] no new position for '+str(self.get_canvas_id())+' found, trying again ...')
            threading.Thread(target=self.add_to_canvas, ).start()

    # returns the exact position of the object in canvas
    # if exact is False, it returns the last saved position,
    # which is not older than one second
    def get_position(self, exact=True):
        if self.is_in_canvas():
            if not exact and self.position:
                # return inexact position
                diff = time.time() - self.last_position_update
                if diff < 1:
                    return self.position

            # save current position
            self.last_position_update = time.time()
            self.position = self.canvas.bbox(self.get_id())

            if self.position:
                return self.position

        # return dummy if no position were found
        return -1, -1, -1, -1

    # returns True if object is visible in canvas
    def is_visible(self):
        x1, y1, x2, y2 = self.get_position(False)
        return y1 < int(self.canvas['height'])

    # moves the object
    def move(self, speed):
        # adjust the speed if the get_speed function has been overwritten by child
        speed = self.get_speed(speed)

        if self.is_in_canvas():
            if self.is_visible():
                self.canvas.move(self.get_id(), 0, speed)
            else:
                # recycle if object is not in canvas
                self.in_canvas = False
                threading.Thread(target=self.recycle, ).start()

    # default function for custom speed
    # can be overwritten by child
    # e.g. see car.py line 21
    def get_speed(self, street_speed):
        return street_speed

    # removes the object from canvas and objects manager
    def remove(self):
        self.in_canvas = False
        self.canvas.delete(self.get_id())
        self.objects_manager.remove(self)

    # recycles the object
    def recycle(self):
        if self.is_recyclable():
            self.canvas.delete(self.get_id())
            threading.Thread(target=self.add_to_canvas, ).start()
        else:
            self.canvas.delete(self.get_id())
            self.objects_manager.remove(self)

    # returns the minimum possible distance to other objects
    def get_min_distance(self):
        return self.min_distance
