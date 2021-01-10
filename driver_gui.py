from table_window import TableWindow


# Driver GUI class: manages the table in table window for drivers
class DriverGUI(TableWindow):
    def __init__(self, db, root):
        self.db = db
        self.root = root

        # default values
        self.driver = []
        self.labels = ['Gewicht (in kg)']
        self.new_button_label = 'Neuer Fahrer'

        self.row_values = self.get_driver()
        super(DriverGUI, self).__init__()

    # returns row values for each driver as array
    def get_driver(self):
        row_values = []
        self.driver = self.db.get_driver()
        for driver in self.driver:
            row_values.append([driver.get_weight_kg()])
        return row_values

    # reloads the table content
    def reload(self):
        self.load_table_content(self.get_driver())

    # delete button callback
    def on_delete(self, row):
        self.db.delete_one('driver', self.driver[row - 1])
        self.reload()

    # reset button callback
    def on_reset(self):
        self.db.delete_all('driver')
        self.db.create_driver('72.4')
        self.db.create_driver('85.7')
        self.reload()

    # done button callback
    def on_done(self):
        i = -1
        for row in self.row_vars:
            self.db.update_driver(self.driver[i], row[0].get())
            i = i + 1
        self.master.destroy()

    # creates a new driver
    def create_new(self):
        self.db.create_driver(self.new_object_vars[0].get())
        self.new_object_window.destroy()
        self.reload()
