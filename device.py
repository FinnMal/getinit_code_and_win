class Device:
    def __init__(self, device_id, name, units, weight, benefit):
        self.id = device_id
        self.name = name
        self.units = units
        self.weight = weight
        self.benefit = benefit

    # returns the database ID
    def get_id(self):
        return self.id

    # returns the name
    def get_name(self):
        return self.name

    def set_name(self, n):
        self.name = n

    # returns the available units
    # this is not the database value
    # if a device gets packet on the transporter,
    # the available units will decrease
    def get_units(self):
        return self.units

    def set_units(self, u):
        self.units = u

    # returns the weight in g
    def get_weight(self):
        return self.weight

    def set_weight(self, w):
        self.weight = w

    # returns the benefit ("Nutzwert")
    def get_benefit(self):
        return self.benefit

    def set_benefit(self, b):
        self.benefit = b

    # sets the available units,
    # after the devices were packed
    # on the transporter
    def pack(self, units):
        self.units = self.units-units

    # returns the type of the device
    def get_type(self):
        name = self.get_name()
        if 'Mobiltelefon' in name:
            return 'smartphone'
        if 'Tablet' in name:
            return 'tablet'
        return 'notebook'

    # returns an emoji that matches the device type
    def get_emoji(self):
        if self.get_type() == 'smartphone':
            return '📱'
        return '💻'


