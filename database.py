import sqlite3
from device import Device
from driver import Driver
from transporter import Transporter


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()

        # remove old values
        self.c.execute('DELETE FROM loads')
        self.c.execute('DELETE FROM transporter_driver')

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

    # creates a new device
    def create_device(self, name, units, weight, benefit):
        self.c.execute('INSERT INTO devices(name, units, weight, benefit) VALUES ("' + str(name) + '", "' + str(units) + '", "' + str(weight) + '", "' + str(benefit) + '")')
        return Device(self.c.lastrowid, name, units, weight, benefit)

    # creates a new transporter
    def create_transporter(self, capacity):
        self.c.execute('INSERT INTO transporter(capacity) VALUES ("' + str(capacity) + '")')

    # creates a new driver
    def create_driver(self, weight):
        self.c.execute('INSERT INTO driver(weight) VALUES ("' + str(weight) + '")')
