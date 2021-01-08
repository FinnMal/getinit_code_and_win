from table_window import TableWindow


# Devices GUI class: manages the table in table window for devices
class DevicesGUI(TableWindow):
    def __init__(self, db, root):
        self.db = db
        self.root = root

        # default values
        self.devices = None
        self.new_button_label = 'Neues Gerät'
        self.labels = ['Hardware', 'benötigte Anzahl', 'Gewicht (in g)', 'Nutzwert']

        self.row_values = self.get_devices()
        super(DevicesGUI, self).__init__()

    # returns row values for each device as array
    def get_devices(self):
        row_values = []
        self.devices = self.db.get_devices(False)
        for device in self.devices:
            row_values.append([device.get_name(), device.get_units(), device.get_weight(), device.get_benefit()])
        return row_values

    # reloads the table content
    def reload(self):
        self.load_table_content(self.get_devices())

    # delete button callback
    def on_delete(self, row):
        device_id = self.devices[row - 1].get_id()
        self.db.delete_one('devices', device_id)
        self.reload()

    # reset button callback
    def on_reset(self):
        self.db.delete_all('devices')
        self.db.create_device("Notebook Büro 13'", 205, 2451, 40)
        self.db.create_device("Notebook Büro 14'", 420, 2978, 35)
        self.db.create_device('Notebook outdoor', 450, 3625, 80)
        self.db.create_device('Mobiltelefon Büro', 60, 717, 30)
        self.db.create_device('Mobiltelefon Outdoor', 157, 988, 60)
        self.db.create_device('Mobiltelefon Heavy Duty', 220, 1220, 65)
        self.db.create_device('Tablet Büro klein', 620, 1405, 40)
        self.db.create_device('Tablet Büro groß', 250, 1455, 40)
        self.db.create_device('Tablet outdoor klein', 540, 1690, 45)
        self.db.create_device('Tablet outdoor groß', 370, 1980, 68)
        self.reload()

    # done button callback
    def on_done(self):
        i = -1
        for row in self.row_vars:
            self.db.update_device(self.devices[i], row[0].get(), row[1].get(), row[2].get(),
                                  row[3].get())
            i = i + 1
        self.master.destroy()

    # creates a new device
    def create_new(self):
        params = self.new_object_vars
        self.db.create_device(params[0].get(), params[1].get(), params[2].get(), params[3].get())
        self.new_object_window.destroy()
        self.load_table_content(self.get_devices())
