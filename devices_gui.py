class DevicesGUI(TableWindow):
    def __init__(self, db, root):
        self.db = db
        self.root = root
        self.devices = None
        self.labels = ['Hardware', 'benötigte Anzahl', 'Gewicht (in g)', 'Nutzwert']
        self.new_button_label = 'Neues Gerät'
        self.row_values = self.get_devices()
        super(DevicesGUI, self).__init__()

    def get_devices(self):
        row_values = []
        self.devices = self.db.get_devices(False)
        for device in self.devices:
            row_values.append([device.get_name(), device.get_units(), device.get_weight(), device.get_benefit()])
        return row_values

    def reload(self):
        self.load_table_content(self.get_devices())

    def on_close(self):
        print('on close')

    def on_delete(self, row):
        device_id = self.devices[row-1].get_id()
        self.db.fetchall('DELETE FROM devices WHERE ID = '+str(device_id))
        self.reload()

    def on_reset(self):
        self.db.fetchall('DELETE FROM devices')
        self.db.fetchall("INSERT INTO devices(name, units, weight, benefit) VALUES"
                         "("+'"'+"Notebook Büro 13'"+'"'+", 205, 2451, 40),"
                         "("+'"'+"Notebook Büro 14'"+'"'+", 420, 2978, 35),"
                         "("+'"'+"Notebook outdoor"+'"'+", 450, 3625, 80),"
                         "("+'"'+"Mobiltelefon Büro"+'"'+", 60, 717, 30),"
                         "("+'"'+"Mobiltelefon Outdoor"+'"'+", 157, 988, 60),"
                         "("+'"'+"Mobiltelefon Heavy Duty"+'"'+", 220, 1220, 65),"
                         "("+'"'+"Tablet Büro klein"+'"'+", 620, 1405, 40),"
                         "("+'"'+"Tablet Büro groß"+'"'+", 250, 1455, 40),"
                         "("+'"'+"Tablet outdoor klein"+'"'+", 540, 1690, 45),"
                         "("+'"'+"Tablet outdoor groß"+'"'+", 370, 1980, 68)")

        self.reload()

    def on_done(self):
        i = -1
        for row in self.row_vars:
            self.db.fetchall(
                'UPDATE devices SET name = "' + str(row[0].get().replace('"', "'")) + '", units = "' + str(
                    row[1].get()) + '", weight = "' + str(row[2].get()) + '", benefit = "' + str(
                    row[3].get()) + '" WHERE ID = ' + str(self.devices[i].get_id()))
            i = i + 1
        self.master.destroy()

    def do_create(self):
        params = self.new_object_vars
        self.db.create_device(params[0].get(), params[1].get(), params[2].get(), params[3].get())
        self.new_object_window.destroy()
        self.load_table_content(self.get_devices())