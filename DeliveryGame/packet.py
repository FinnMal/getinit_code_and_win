from DeliveryGame.screen_object import ScreenObject


# Packet class: class for packet in canvas
class Packet(ScreenObject):
    def __init__(self, device_id, master, canvas, objects_manager):
        super(Packet, self).__init__(device_id, master, canvas, objects_manager)
        
        # default values
        self.content = []
        self.min_distance = 0
        self.collected = False
        self.images = ['packet.png']
        self.content = {'name': '', 'units': 0}
    
    # packs an new device into packet
    def pack_device(self, name, units):
        self.content['name'] = name
        self.content['units'] = units
    
    # resets the content of the packet
    def reset_content(self):
        self.content = []
    
    # collects the packet
    def collect(self):
        self.remove()
        self.collected = True
    
    # returns True if the packet is collected
    def is_collected(self):
        return self.collected
    
    # returns the name of device in packet
    def get_name(self):
        return self.content['name']

    # returns the number of device in packet
    def get_units(self):
        return self.content['units']
