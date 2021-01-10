import random
import time
from DeliveryGame.car import Car


# Objects Manager class: manages cars and packages in canvas
class ObjectsManager:
    def __init__(self, master, canvas):
        self.canvas = canvas
        self.master = master

        self.objects = []
    
    # adds a object to list
    def add(self, o):
        for obj in self.objects:
            if o.get_id() == obj.get_id():
                return
        self.objects.append(o)
    
    # removes a object from list
    def remove(self, o):
        self.objects.remove(o)
    
    # returns a placeable position for object
    def find_position(self, obj):
        # save started timestamp for timeout
        started_at = time.time()
        
        while True:
            # check for timeout
            if time.time() - started_at > .1:
                print('[OBJECTS_MANAGER] timeout in find_position')
                return False
            
            # generate random column and y_pos
            column = random.randint(0, 4)
            y_pos = random.randint(-1000, -130)
            
            # check if object can be placed at generated pos
            if self.can_place_object(obj, column, y_pos, obj.get_min_distance()):
                return [column, y_pos]
    
    # returns True if object can be placed at given position
    def can_place_object(self, obj, column, y_pos, min_placeable_distance):
        distance_ok = True
        
        # for every managed object in canvas
        for o in self.objects:
            # if object is a car
            if o is not obj and type(o) == Car:
                # if column of obj is left or right from pos
                if o.get_column() in range(column - 1, column + 1):
                    # get the exact position of object
                    x1, y1, x2, y2 = o.get_position(True)
                    
                    # get distance to generated point
                    distance = abs(y_pos - y1)
                    
                    # check if distance is ok
                    if distance < o.get_min_distance() or distance < min_placeable_distance:
                        distance_ok = False
        return distance_ok

    # converts a column to x coordinate
    def get_x_pos(self, column):
        return column * 82.5 + 5
    
    """
    def get_cars_in_front(self, car, max_distance=200):
        cars = self.columns[car.get_column()]

        cars_in_front = []
        if car in cars:
            search_range = range(car.get_position(False)[1], car.get_position(False)[1] + max_distance)
            print(search_range)

            for c in cars:
                if c != car:
                    if c.get_position(False)[1] in search_range:
                        cars_in_front.append(c)
        return cars_in_front
    """
