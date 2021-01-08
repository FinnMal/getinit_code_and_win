from table_window import TableWindow


# Transporter GUI class: manages the table in table window for transporters
class TransporterGUI(TableWindow):
    def __init__(self, db, root):
        self.db = db
        self.root = root

        # default values
        self.transporter = None
        self.labels = ['Kapazität (in kg)']
        self.new_button_label = 'Neuer Transporter'

        self.row_values = self.get_transporter()
        super(TransporterGUI, self).__init__()

    # returns row values for each transporter as array
    def get_transporter(self):
        row_values = []
        self.transporter = self.db.get_transporter()
        for transporter in self.transporter:
            row_values.append([transporter.get_total_capacity_kg()])
        return row_values

    # reloads the table content
    def reload(self):
        self.load_table_content(self.get_transporter())

    # delete button callback
    def on_delete(self, row):
        self.db.delete_one('transporter', self.transporter[row - 1])
        self.reload()

    # reset button callback
    def on_reset(self):
        self.db.delete_all('transporter')
        self.db.create_transporter(1100)
        self.db.create_transporter(1100)

        row_values = self.get_transporter()
        self.load_table_content(row_values)

    # done button callback
    def on_done(self):
        i = -1
        for row in self.row_vars:
            self.db.update_transporter(self.transporter[i], row[0].get())
            i = i + 1
        self.master.destroy()

    # creates a new transporter
    def create_new(self):
        self.db.create_transporter(self.new_object_vars[0].get())
        self.new_object_window.destroy()
        self.load_table_content(self.get_transporter())
