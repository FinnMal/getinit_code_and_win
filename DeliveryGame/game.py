import time
import random
import threading
import PIL.Image
from tkinter import *
from pynput import keyboard
from playsound import playsound
from DeliveryGame.car import Car
from DeliveryGame.alert import Alert
from DeliveryGame.truck import Truck
from DeliveryGame.cars_manager import CarsManager
from DeliveryGame.objects_manager import ObjectsManager
from DeliveryGame.packages_manager import PackagesManager
from DeliveryGame.background_music import BackgroundMusic
from DeliveryGame.street_marker_manager import StreetMarkersManager


# Game Class: handles the game strategy and objects
class Game:
    def __init__(self, parent_window, transporter):
        self.transporter = transporter
        self.parent_window = parent_window

        # default values
        self.alert = None
        self.truck = None
        self.master = None
        self.canvas = None
        self.game_status = 0
        self.street_speed = 8
        self.cars_manager = None
        self.objects_manager = None
        self.packages_manager = None
        self.street_markers_manager = None
        self.current_transporter_index = 0
        self.background_music = BackgroundMusic()

        # create window as child of parent_window
        self.master = Toplevel(self.parent_window)
        self.master.title('Delivery Game v.1.0')
        self.master.configure(background='#2C2C2E')
        self.master.protocol("WM_DELETE_WINDOW", self.close)

        # start keyboard listener
        threading.Thread(target=self.start_keyboard_listener, ).start()

    # starts the game
    def start(self):
        # close alert if one is open
        if self.alert:
            self.alert.close()

        # set game status to 1 = running
        self.game_status = 1

        # start the loops
        self.cars_manager.start_loop()
        self.packages_manager.start_loop()

        # start background music
        self.background_music.start()

        # start tick loop
        self.canvas.after(1000 // 60, self.tick)

    # restarts the game
    def restart(self):
        self.stop_loops()

        # restart to default
        self.alert = None
        self.truck = None
        self.canvas = None
        self.street_speed = 8
        self.cars_manager = None
        self.objects_manager = None
        self.packages_manager = None
        self.street_markers_manager = None

        # re-render and start game (without alert)
        self.render()
        self.start()

    # stops the music and closes the window
    def close(self):
        self.background_music.stop()
        self.master.destroy()

    # stops the music and manager loops
    def stop_loops(self):
        self.background_music.stop()
        self.cars_manager.stop_loop()
        self.packages_manager.stop_loop()

    # keyboard listener
    def on_press(self, key):
        try:
            # pass pressed key to alert
            if self.alert and self.game_status != 1:
                self.alert.on_key_press(key)

            # pass pressed key to truck
            if self.truck and self.game_status == 1:
                self.truck.on_key_press(key)

            # speed control
            if self.game_status == 1:
                if key.char == 'w':
                    # increase street speed
                    self.street_speed = self.street_speed + 1.2

                if key.char == 's':
                    # decrease street speed
                    if self.street_speed > 5:
                        self.street_speed = self.street_speed * 0.5
        except AttributeError:
            # handler for special keys

            # speed control
            if self.game_status == 1:
                if key is key.up:
                    # increase street speed
                    self.street_speed = self.street_speed + 1.2

                if key is key.down:
                    # decrease street speed
                    if self.street_speed > 5:
                        self.street_speed = self.street_speed * 0.5

    # starts the keyboard listener
    def start_keyboard_listener(self):
        with keyboard.Listener(
                on_press=self.on_press) as listener:
            listener.join()

    # does one tick (frame)
    def tick(self):
        # if game running
        if self.game_status == 1:
            # increase the game speed
            self.street_speed = self.street_speed + 0.00205

            # pass street speed for speed display in canvas
            self.truck.show_street_speed(self.street_speed)

            # check for collisions
            overlaps = self.truck.get_overlapping_canvas_ids()
            if self.cars_manager.has_overlaps(overlaps):
                self.game_status = 2
            # check if package should be collected
            self.packages_manager.check_for_overlaps(overlaps)

            # move cars, packages and markers
            self.cars_manager.move_cars(self.street_speed)
            self.packages_manager.move_packages(self.street_speed)
            self.street_markers_manager.move_markers(self.street_speed)

            # check if every package is collected
            if self.packages_manager.is_game_done():
                self.game_status = 3

            if self.game_status == 1:
                # if game running
                # set timeout for next tick (60 fps)
                self.canvas.after(1000 // 60, self.tick)
            elif self.game_status == 2:
                # if truck has collision
                self.stop_loops()

                # show alert
                self.alert = Alert(self.canvas, 'Unfall! Dein LKW ist zerstört')
                self.alert.add_button('Neu starten', self.restart)
                self.alert.add_button('Schließen', self.close)
                self.alert.open()

            elif self.game_status == 3:
                # if all packages have been collected
                self.stop_loops()

                # show alert
                self.alert = Alert(self.canvas, 'Fertig! Du hast alle Pakete ausgeliefert')
                self.alert.add_button('Neu starten', self.restart)

                # check if there is a next truck
                if self.has_next_transporter():
                    self.alert.add_button('Nächste Lieferung', self.start_game_with_next_transporter)

                self.alert.add_button('Schließen', self.close)
                self.alert.open()

    # returns True if there is a next truck
    def has_next_transporter(self):
        return self.current_transporter_index < len(self.transporter) - 1

    # starts the game with the next transporter
    def start_game_with_next_transporter(self):
        if len(self.transporter) > self.current_transporter_index:
            self.current_transporter_index = self.current_transporter_index + 1
            self.restart()

    # renders objects
    def render(self, start_game_after_render=False):
        # create canvas for game
        self.canvas = Canvas(self.master, bg='#2C2C2E', highlightthickness=0)
        self.canvas.grid(row=9)

        # set window size
        self.canvas['width'] = 400
        self.canvas['height'] = 850

        # create and render the truck
        self.truck = Truck(self.master, self.canvas)
        self.truck.render()

        # create manager for objects
        self.objects_manager = ObjectsManager(self.master, self.canvas)

        # start street markers manager and spawn the markers
        self.street_markers_manager = StreetMarkersManager(self.master, self.canvas)
        self.street_markers_manager.add_markers()

        # start cars manager and add one car
        self.cars_manager = CarsManager(self.master, self.canvas, self.objects_manager)
        self.cars_manager.add_car()

        # create packages manager
        self.packages_manager = PackagesManager(self.master, self.canvas, self.objects_manager)

        # create packages according to the transporter load
        for d in self.transporter[self.current_transporter_index].get_load():
            self.packages_manager.add_device(d['device'], d['units'])
        # create the upper info text
        self.packages_manager.render_info_text()

        # show alert
        self.alert = Alert(self.canvas,
                           'Sammle die Pakete mit deinem LKW ein')
        self.alert.add_button('Starten', self.start)
        self.alert.add_button('Schließen', self.close)
        self.alert.open()
