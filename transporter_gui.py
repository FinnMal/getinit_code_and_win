class TransporterGUI(TableWindow):
    def __init__(self, db, root):
        self.db = db
        self.root = root
        self.transporter = None
        self.labels = ['Kapazität (in kg)']
        self.new_button_label = 'Neuer Transporter'
        self.row_values = self.get_transporter()
        super(TransporterGUI, self).__init__()

    def get_transporter(self):
        row_values = []
        self.transporter = self.db.get_transporter()
        for transporter in self.transporter:
            row_values.append([transporter.get_total_capacity_kg()])
        return row_values

    def reload(self):
        self.load_table_content(self.get_transporter())

    def on_close(self):
        print('on close')

    def on_delete(self, row):
        transporter_id = self.transporter[row-1].get_id()
        self.db.fetchall('DELETE FROM transporter WHERE ID = '+str(transporter_id))
        self.reload()

    def on_reset(self):
        self.db.fetchall('DELETE FROM transporter')
        self.db.fetchall('INSERT INTO transporter(capacity) VALUES (1100),(1100)')

        row_values = self.get_transporter()
        self.load_table_content(row_values)

    def on_done(self):
        i = -1
        for row in self.row_vars:
            self.db.fetchall(
                'UPDATE transporter SET capacity = "' + str(row[0].get()) + '" WHERE ID = ' + str(
                    self.transporter[i].get_id()))
            i = i + 1
        self.master.destroy()

    def do_create(self):
        self.db.create_transporter(self.new_object_vars[0].get())
        self.new_object_window.destroy()
        self.load_table_content(self.get_transporter())