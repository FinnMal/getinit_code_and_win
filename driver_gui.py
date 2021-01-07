class DriverGUI(TableWindow):
    def __init__(self, db, root):
        self.driver = None
        self.db = db
        self.root = root

        self.labels = ['Gewicht (in kg)']
        self.new_button_label = 'Neuer Fahrer'
        self.row_values = self.get_driver()
        super(DriverGUI, self).__init__()

    def get_driver(self):
        row_values = []
        self.driver = self.db.get_driver()
        for driver in self.driver:
            row_values.append([driver.get_weight_kg()])
        return row_values

    def reload(self):
        self.load_table_content(self.get_driver())

    def on_close(self):
        print('on close')

    def on_delete(self, row):
        driver_id = self.driver[row-1].get_id()
        self.db.fetchall('DELETE FROM driver WHERE ID = '+str(driver_id))
        self.reload()

    def on_reset(self):
        self.db.fetchall('DELETE FROM driver')
        self.db.fetchall('INSERT INTO driver(weight) VALUES (72.4),(85.7)')
        self.reload()

    def on_done(self):
        i = -1
        for row in self.row_vars:
            self.db.fetchall(
                'UPDATE driver SET weight = "' + str(row[0].get()) + '" WHERE ID = ' + str(self.driver[i].get_id()))
            i = i + 1
        self.master.destroy()

    def do_create(self):
        self.db.create_driver(self.new_object_vars[0].get())
        self.new_object_window.destroy()
        self.reload()
