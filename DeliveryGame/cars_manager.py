import time
import threading
from DeliveryGame.car import Car


# Cars Manager class: manages cars in canvas
class CarsManager:
    def __init__(self, master, canvas, objects_manager):
        self.master = master
        self.canvas = canvas
        self.objects_manager = objects_manager

        self.cars = []
        self.canvas_counter = 0
        self.loop_active = False
        self.max_cars_in_canvas = 20

    # adds a car to canvas
    def add_car(self):
        car_id = 'car_' + str(self.canvas_counter)
        car = Car(car_id, self.master, self.canvas, self.objects_manager)
        car.add_to_canvas()

        # append car to array for further managing
        self.cars.append(car)
        self.canvas_counter = self.canvas_counter + 1

    # returns True if any car is in ids_list
    def has_overlaps(self, ids_list):
        for car in self.cars:
            if car.get_canvas_id() in ids_list:
                return True
        return False

    # moves the cars with speed
    def move_cars(self, speed):
        for car in self.cars:
            threading.Thread(target=car.move, args=(speed,)).start()

    # spans new cars if needed
    def spawn_car(self):
        if self.loop_active:
            # wait x seconds depending on how much cars are in canvas
            time.sleep(self.canvas_counter * 1.4)

            # check if the maximum number of cars has been reached
            if self.canvas_counter < self.max_cars_in_canvas:
                self.add_car()
                threading.Thread(target=self.spawn_car).start()

    # starts the "spawn_car" loop
    def start_loop(self):
        self.loop_active = True
        threading.Thread(target=self.spawn_car).start()

    # stops the "spawn_car" loop
    def stop_loop(self):
        self.loop_active = False
