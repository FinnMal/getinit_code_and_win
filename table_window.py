from tkinter import *

# Table Window: tkinter window with table to manage database entries
class TableWindow:
    def __init__(self):

        # default values
        self.objects = []
        self.row_vars = []
        self.master = None
        self.row_elements = [[]]
        self.new_object_vars = []
        self.new_object_window = None
        self.selected_background_color = None

        # check if child has labels variable
        # create one if it doesn't have one
        if not self.labels:
            self.labels = []

        # check if child has row_values variable
        # create one if it doesn't have one
        if not self.row_values:
            self.row_values = []

        self.columns = len(self.labels)
        self.render()

    # marks a row in table
    def select_row(self, event):
        # get row number of "FocusIn" event
        row = event.widget.grid_info()['row']

        # move object "selected_background_color" to new row
        self.selected_background_color.grid(row=row, column=0, sticky='ew', columnspan=4)

        # set every background to default color
        for elements in self.row_elements:
            if len(elements) > 0:
                for element in elements:
                    element.config(highlightthickness=2)
                    element.config(bg='#2C2C2E')
                    element.config(fg='white')

        # set selected background color
        for element in self.row_elements[row]:
            element.config(highlightcolor='#0D84FF', highlightthickness=3)
            element.config(bg='#3A3A3C')
            element.config(fg='white')

    # clears the table
    def clear(self):
        self.objects = []
        self.row_vars = []
        self.row_elements = [[]]

        # remove input boxes, buttons and labels
        for widget in self.master.winfo_children():
            widget.destroy()

    # close callback
    def on_close(self):
        print('on close')

    # opens new window with input boxes to create new entry
    def on_create(self):
        # create tkinter toplevel window
        self.new_object_window = Toplevel(self.master)
        self.new_object_window.configure(background='#2C2C2E')

        # render background color for a selected row
        self.selected_background_color.grid(row=0, column=0, sticky='ew', columnspan=4)

        i = 0
        self.new_object_vars = []
        for label in self.labels:
            # render labels
            Label(self.new_object_window, text=label, bg='#2C2C2E', fg='white').grid(row=i)
            
            # render input box (entry)
            var = StringVar(self.new_object_window, value='')
            Entry(self.new_object_window, textvariable=var, width=20, fg='white', bg='#2C2C2E',
                  highlightcolor='#0D84FF',
                  highlightthickness=2).grid(row=i, column=1, padx=5, pady=5)
            self.new_object_vars.append(var)

            i = i + 1
        
        # render save and cancel buttons
        Button(self.new_object_window, text='Speichern', command=self.create_new).grid(row=5, column=1, pady=15)
        Button(self.new_object_window, text='Abbrechen', command=lambda: self.new_object_window.destroy()).grid(row=5, column=0, pady=15)
    
    # loads the table content
    def load_table_content(self, row_values=self.row_values):
        # remove old entries
        self.clear()

        # render background color for selection
        self.selected_background_color = Label(self.master, text='', fg='#3A3A3C', bg="#3A3A3C", font='Helvetica 16 bold')
        self.selected_background_color.grid(row=0, column=0, sticky='ew', columnspan=6)
        
        # render header background color
        header_background = Label(self.master, text='', fg='#0D84FF', bg='#0D84FF', font='Helvetica 16 bold')
        header_background.grid(row=0, column=0, sticky='ew', columnspan=6)

        i = 0
        for label in self.labels:
            # render label at the top
            Label(self.master, text=label, bg='#0D84FF', fg='white', font='Helvetica 16 bold').grid(row=0, column=i)
            i = i + 1

        i = 1
        # render rows
        for row in row_values:
            string_vars = []
            input_boxes = []

            c = 0
            for value in row:
                # render input box
                var = StringVar(self.master, value=value)
                input_box = Entry(self.master, textvariable=var, fg='white', bg='#2C2C2E',
                                  highlightbackground='#2C2C2E', highlightcolor='#2C2C2E', highlightthickness=2,
                                  borderwidth=1)
                input_box.grid(row=i, column=c, padx=5, pady=5)
                # set focus listener to select the row
                input_box.bind("<FocusIn>", self.select_row)

                # save var and input box
                string_vars.append(var)
                input_boxes.append(input_box)
                c = c + 1

            self.row_vars.append(string_vars)
            self.row_elements.append(input_boxes)

            # render delete button
            Button(self.master, text='Löschen', command=lambda i=i: self.on_delete(i)).grid(row=i, column=4, padx=5)

            i = i + 1

        # render "create new ...", reset, cancel and done buttons
        Button(self.master, text=self.new_button_label, command=self.on_create).grid(row=i + 1, column=0, pady=6)
        Button(self.master, text='Felder zurücksetzen', command=self.on_reset).grid(row=i + 1, column=1, pady=6)
        Button(self.master, text='Abbrechen', command=lambda: self.master.destroy()).grid(row=i + 1, column=2, pady=6)
        Button(self.master, text='Fertig', command=self.on_done).grid(row=i + 1, column=3, pady=6, padx=15)

    # renders the tkinter window
    def render(self):
        self.master = Toplevel(self.root)
        self.master.configure(background='#2C2C2E')

        self.load_table_content(self.row_values)
