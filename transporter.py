import math
import table
from driver import Driver


class Transporter:
    def __init__(self, transporter_id, capacity):
        self.id = transporter_id
        self.capacity = capacity

        self.reaming_capacity = self.get_total_capacity()
        self.benefit = 0
        self.load = []

    # returns the ID
    def get_id(self):
        return self.id

    # returns the total capacity
    def get_total_capacity(self):
        return self.capacity*1000

    # returns the total capacity in kg
    def get_total_capacity_kg(self):
        return self.capacity

    # returns the reaming capacity
    def get_reaming_capacity(self):
        if self.reaming_capacity > 0:
            return self.reaming_capacity
        return 0

    # returns the total benefit ("Nutzwert") of the packed transporter
    def get_benefit(self):
        return self.benefit

    # subtracts the weight of the driver from the reaming capacity
    def add_driver(self, driver):
        self.reaming_capacity = self.reaming_capacity - driver.get_weight()

    # returns the maximum number of devices that can be packed on the transporter
    def get_maximum_pacable_units(self, device):
        # round down with "math.floor" to prevent overload
        max_units = math.floor(self.get_reaming_capacity() / device.get_weight())
        if max_units > device.get_units():
            # return the available units of the device,
            # if more could be packed on the transporter
            return device.get_units()
        return max_units

    # pack a device on the transporter
    def pack_device(self, device, units):
        self.benefit = self.benefit + device.get_benefit() * units
        self.reaming_capacity = self.reaming_capacity - device.get_weight() * units
        self.load.append({'device': device, 'units': units})

    def get_load(self):
        return self.load

    # print the current load to the console
    def print_load(self):
        table_load_list = [
            ['Gerät', 'Anzahl'],
        ]

        for l in self.load:
            table_load_list.append([l['device'].get_name(), l['units']])

        print('🚚 TRANSPORTER NR.' + str(self.get_id() + 1))
        table.printTable(table_load_list, useFieldNames=True)
        print('➡️ ges. Nutzwert: ' + str(self.get_benefit()))
        print('➡️ freie Kapazität: ' + str(round(self.get_reaming_capacity())) + ' g')
        print('\n')
