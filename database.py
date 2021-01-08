import sqlite3
from device import Device
from driver import Driver
from transporter import Transporter


# returns '0' if var is int
# or replaces >"< with >'< in strings
# returns a string to save in database
def parse_var(var, is_int=False):
    if not is_int:
        return str(var).replace('"', "'")

    if is_int:
        try:
            var = int(var)
        except Exception as e:
            var = 0
        return str(var)


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()

        # remove old values
        self.delete_all('loads')
        self.delete_all('transporter_driver')

    # saves and closes the database
    def close(self):
        self.conn.commit()
        self.conn.close()

    # returns the "fetchall" result of the command
    def fetchall(self, command):
        self.c.execute(command)
        return self.c.fetchall()

    # returns sorted array with device objects from database
    def get_devices(self, sorted=True):
        devices = []
        if sorted:
            # select devices from SQL, sorted by the best (lowest) ratio between weight and profit
            data = self.fetchall('SELECT * FROM devices ORDER BY weight/benefit')  # <- the magic
        else:
            data = self.fetchall('SELECT * FROM devices')
        for d in data:
            # create device object
            device = Device(d[0], d[1], d[2], d[3], d[4])
            devices.append(device)
        return devices

    # returns array with transporter objects from database
    def get_transporter(self):
        transporter = []
        data = self.fetchall('SELECT * FROM transporter')
        for d in data:
            # create transporter object
            t = Transporter(d[0], d[1])
            transporter.append(t)
        return transporter

    # returns array with driver objects from database
    def get_driver(self):
        driver = []
        data = self.fetchall('SELECT * FROM driver')
        for d in data:
            # create driver object
            e = Driver(d[0], d[1])
            driver.append(e)
        return driver

    # save the driver of the transporter
    def save_driver(self, driver, transporter):
        transporter.add_driver(driver)
        self.c.execute(
            'INSERT INTO transporter_driver(driver_ID, transporter_ID) VALUES (' + str(driver.get_id()) + ', ' + str(
                transporter.get_id()) + ')')

    # saves new load to database
    def save_load(self, device, units, transporter):
        self.c.execute(
            'INSERT INTO loads(device_ID, transporter_ID, units) VALUES (' + str(device.get_id()) + ', ' + str(
                transporter.get_id()) + ', ' + str(units) + ')')

    # packs devices on the transporter
    def pack_device(self, device, units, transporter):
        device.pack(units)
        transporter.pack_device(device, units)
        self.save_load(device, units, transporter)

    # deletes every entry in given table
    def delete_all(self, table):
        self.c.execute('DELETE FROM ' + table)

    def delete_one(self, table, obj):
        self.c.execute('DELETE FROM ' + str(table) + ' WHERE ID = ' + str(obj.get_id()))

    # creates a new device
    def create_device(self, name, units, weight, benefit):
        self.c.execute(
            'INSERT INTO devices(name, units, weight, benefit) VALUES ("' + parse_var(name) + '", "' + parse_var(units,
                                                                                                                 True) + '", "' + parse_var(
                weight, True) + '", "' + parse_var(benefit, True) + '")')
        return Device(self.c.lastrowid, name, units, weight, benefit)

    # updates a device entry
    def update_device(self, device, name, units, weight, benefit):
        device.set_name(name)
        device.set_units(units)
        device.set_weight(weight)
        device.set_benefit(benefit)
        self.c.execute('UPDATE devices SET name = "' + parse_var(name) + '", units = "' + parse_var(units,
                                                                                                    True) + '", weight = "' + parse_var(
            weight, True) + '", benefit = "' + parse_var(benefit, True) + '"  WHERE ID = ' + str(device.get_id()))

    # creates a new transporter
    def create_transporter(self, capacity):
        self.c.execute('INSERT INTO transporter(capacity) VALUES ("' + parse_var(capacity, True) + '")')

    # updates a transporter entry
    def update_transporter(self, transporter, capacity):
        transporter.set_capacity(capacity)
        self.c.execute('UPDATE transporter SET capacity = "' + parse_var(capacity, True) + '" WHERE ID = ' + str(
            transporter.get_id()))

    # creates a new driver
    def create_driver(self, weight):
        self.c.execute('INSERT INTO driver(weight) VALUES ("' + parse_var(weight, True) + '")')

    # updates a driver entry
    def update_driver(self, driver, weight):
        driver.set_weight(weight)
        self.c.execute(
            'UPDATE driver SET weight = "' + parse_var(weight, True) + '" WHERE ID = ' + str(driver.get_id()))
