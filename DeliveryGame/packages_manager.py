import time
import random
import threading
from DeliveryGame.packet import Packet


# Packages Manager: manages the packages objects
class PackagesManager:
    def __init__(self, master, canvas, objects_manager):
        self.master = master
        self.canvas = canvas
        self.objects_manager = objects_manager

        # default values
        self.packages = []
        self.canvas_counter = 0
        self.loop_active = False
        self.device_counters = {}
    
    # adds x units of device
    def add_device(self, device, units):
        # create counter for device
        self.device_counters[device.get_name()] = {}
        self.device_counters[device.get_name()]['total'] = units
        self.device_counters[device.get_name()]['collected'] = 0
        self.device_counters[device.get_name()]['in_canvas'] = 0
    
    # starts the "spawn_device" loop
    def start_loop(self):
        self.loop_active = True
        threading.Thread(target=self.spawn_device).start()

    # stops the "spawn_device" loop
    def stop_loop(self):
        self.loop_active = False
    
    # spawns a device
    def spawn_device(self):
        if self.loop_active:
            time.sleep(0.5)
            if len(self.packages) < 10:
                device_name = random.choice(list(self.device_counters))
                info = self.device_counters[device_name]
                reaming = info['total'] - info['collected'] - info['in_canvas']
                if reaming > 0:
                    packet = Packet('packet_' + str(self.canvas_counter), self.master, self.canvas,
                                    self.objects_manager)
                    packet.pack_device(device_name, 25 if reaming > 24 else reaming)
                    packet.add_to_canvas()
                    self.packages.append(packet)
                    self.canvas_counter = self.canvas_counter + 1
                    self.device_counters[device_name]['in_canvas'] = info['in_canvas'] + packet.get_units()

            threading.Thread(target=self.spawn_device).start()
    
    # renders the info text in upper half of canvas
    def render_info_text(self):
        i = 0
        # for every device
        for device_name in self.device_counters:
            total = self.device_counters[device_name]['total']
            collected = self.device_counters[device_name]['collected']

            # render text
            self.canvas.create_text(200, i * 20 + 50, fill='black', font='Arial 13 bold',
                                    text=device_name + ' ' + str(collected) + '/' + str(total),
                                    tags=('device_counters', device_name,))

            # render text background
            b = self.canvas.create_rectangle(self.canvas.bbox(device_name), fill="white", tags=('background_color', device_name + '_background_color',))

            # place text over of background
            self.canvas.tag_lower(b, device_name)

            i = i + 1

    # updates the info text for given device
    def update_counter(self, device_name):
        total = self.device_counters[device_name]['total']
        collected = self.device_counters[device_name]['collected']

        # check if every unit is collected
        if total > collected:
            # configure text
            self.canvas.itemconfigure(device_name, text=device_name + ' ' + str(collected) + '/' + str(total))

            # delete old background, because width of text could have changed
            self.canvas.delete(device_name + '_background_color')

            # render new background
            b = self.canvas.create_rectangle(self.canvas.bbox(device_name), fill="white",
                                             tags=('background_color', device_name + '_background_color',))
            # place background under text
            self.canvas.tag_lower(b, device_name)
        else:
            # delete counter if every unit is collected
            self.canvas.delete(device_name)
            self.canvas.delete(device_name + '_background_color')

    # checks for overlaps with any package
    def check_for_overlaps(self, ids_list):
        # for every packet in list
        for packet in self.packages:
            # check if packet has a overlap
            if packet.get_canvas_id() in ids_list:
                # collect and remove from list
                packet.collect()
                self.packages.remove(packet)

                # count the collected item
                collected = self.device_counters[packet.get_name()]['collected']
                self.device_counters[packet.get_name()]['collected'] = collected + packet.get_units()

                # decrease device units count in canvas
                in_canvas = self.device_counters[packet.get_name()]['in_canvas']
                self.device_counters[packet.get_name()]['in_canvas'] = in_canvas - packet.get_units()

                self.update_counter(packet.get_name())

    # moves every package
    def move_packages(self, speed):
        for packet in self.packages:
            threading.Thread(target=packet.move, args=(speed,)).start()

    # returns True if every package is collected
    def is_game_done(self):
        for device_name in self.device_counters:
            counter = self.device_counters[device_name]
            if counter['total'] > counter['collected']:
                return False
        return True
