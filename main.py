from gui import GUI
from database import Database


# starts the packing algorithm
# this function gets called by the GUI
def do_packing():
    # create driver and device objects
    driver = db.get_driver()
    devices = db.get_devices(sorted=True)
    transporter_list = db.get_transporter()

    # for every transporter object
    for transporter in transporter_list:
        # check if a driver is available for the truck
        if len(driver) > 0:

            # set the first driver as driver,
            # and remove the object from list
            db.save_driver(driver.pop(0), transporter)

            for device in devices:
                # check if any units of device are available to pack
                if device.get_units() > 0:
                    # calculate how many devices of this type fit on the transporter
                    max_units = transporter.get_maximum_pacable_units(device)
                    if max_units > 0:
                        # pack the devices on the transporter
                        db.pack_device(device, max_units, transporter)

            # print the load for the transporter
            transporter.print_load()
        else:
            print('Fehler: Keinen Fahrer für Transporter Nr.' + str(transporter.get_id() + 1) + ' gefunden')

    return transporter_list


# create database object
db = Database()

# show GUI
gui = GUI(db, do_packing)
gui.render()
