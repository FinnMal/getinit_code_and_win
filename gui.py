from tkinter import *
from DeliveryGame.game import Game

from driver_gui import DriverGUI
from devices_gui import DevicesGUI
from transporter_gui import TransporterGUI


# GUI class: handles the main GUI
class GUI:
    def __init__(self, db, do_packing_func):
        self.db = db
        self.do_packing_func = do_packing_func

        # default values
        self.master = None
        self.canvas = None
        self.transporter = []
        self.animation_status = 0
        self.loads_unit_counts = [[0]]

    # closes the window and saves the database
    def close(self):
        self.db.close()
        self.master.destroy()

    # starts the packing algorithm
    def start_packing(self):
        self.transporter = self.do_packing_func()

        t = 0
        self.loads_unit_counts = []

        # create counter for every device in load
        for transporter in self.transporter:
            self.loads_unit_counts.append([])
            for item in transporter.get_load():
                # set counter to 0
                self.loads_unit_counts[t].append(0)
            t = t + 1

        # show result in canvas
        self.render_canvas()
        self.animate_canvas()
        self.render_deliver_button()

    # renders the canvas object
    def render_canvas(self):
        self.animation_status = 0
        if self.canvas:
            self.canvas.delete('all')

        # create canvas
        self.canvas = Canvas(self.master, bg='#2C2C2E', highlightthickness=0)
        self.canvas.place(x=0, y=100)

        # render transporter icons
        # depending on how much transporters are used
        i = 0
        total_devices_count = 0
        for t in self.transporter:
            # get the device count of the last transporter
            # to get the right spacing between the icons
            last_transporter_devices_count = 0
            if i > 0:
                last_transporter_devices_count = len(self.transporter[i - 1].get_load())
            # count total devices for canvas height
            total_devices_count = total_devices_count + last_transporter_devices_count

            # place transporter icon
            truck_image = PhotoImage(file='./assets/img/truck_emoji.png')
            setattr(self.master, 'truck_image_'+str(i), truck_image)
            self.canvas.create_image((600, 3 + last_transporter_devices_count * 52), image=truck_image, anchor='nw', tags=('transporter_icon', 'transporter_' + str(i), ))
            i = i + 1

        # set canvas width and height depending on transporter and device count
        self.canvas['width'] = 500
        self.canvas['height'] = len(self.transporter) * 60 + total_devices_count * 52

        # adapt the window size to canvas
        self.master.geometry(self.canvas['width'] + 'x' + str(int(self.canvas['height']) + 120))

    # renders transporter labels in canvas
    def render_transporter_label(self):
        i = 0
        for t in self.transporter:
            # get the device count of the last transporter
            # to get the right spacing between the labels
            last_transporter_devices_count = 0
            if i > 0:
                last_transporter_devices_count = len(self.transporter[i - 1].get_load())

            # place the label
            self.canvas.create_text(150, 16 + last_transporter_devices_count * 52, text='  LIEFERUNG NR.' + str(i + 1),
                                    fill='white', tags=('transporter_label', 'transporter_label_' + str(i)),
                                    font=('Arial 15 bold'))
            i = i + 1

    # renders the counter for each device in canvas
    def render_devices_counter(self):
        t = 0
        for transporter in self.transporter:
            i = 0

            # get the device count of the last transporter
            # to get the right spacing between the counters
            last_transporter_devices_count = 0
            if t > 0:
                last_transporter_devices_count = len(self.transporter[t - 1].get_load())

            # for every item in transporter load
            for item in transporter.get_load():
                device = item['device']

                # position, id and text
                y_pos = i * 33 + 60 + last_transporter_devices_count * 52
                canvas_id = 'transporter_' + str(t) + '_text_' + str(device.get_id())
                canvas_text = device.get_name() + ': ' + str(item['units']) + ' Stück'

                # place the counter text in canvas
                self.canvas.create_text(0, y_pos, text='  ' + canvas_text, fill='white', tags=(canvas_id,),
                                        font=('Arial 14'))
                i = i + 1
            t = t + 1

    # animates counter and position of the transporter load in canvas
    # does one tick in the animation
    # returns True if the animation is done
    def animate_transporter_load(self, transporter, t):
        i = 0
        done = True
        # for every item in transporter load
        for item in transporter.get_load():
            device = item['device']
            device_text_id = 'transporter_' + str(t) + '_text_' + str(device.get_id())

            # move the counter to x = 10
            x1, y1, x2, y2 = self.canvas.bbox(device_text_id)
            if x1 < 10:
                done = False
                self.canvas.move(device_text_id, 2, 0)

            # animate counter text if count is not done
            if self.loads_unit_counts[t][i] < item['units']:
                done = False
                self.loads_unit_counts[t][i] = self.loads_unit_counts[t][i] + 1

                # configure the counter text
                text = device.get_name() + ': ' + str(self.loads_unit_counts[t][i]) + ' Stück'
                self.canvas.itemconfigure(device_text_id, text='  ' + text)

            i = i + 1
        return done

    # animates the canvas elements
    def animate_canvas(self):
        if self.animation_status == 0:
            # move the transporter icon to x = 70
            x1, y1, x2, y2 = self.canvas.bbox('transporter_0')
            if x2 > 55:
                self.canvas.move('transporter_icon', -3.5, 0)
            else:
                # if animation is done
                # create counter and transporter label
                self.animation_status = 1
                self.render_devices_counter()
                self.render_transporter_label()
        elif self.animation_status == 1:
            # animate the transporter loads

            t = 0
            animation_done = True
            for transporter in self.transporter:
                done = self.animate_transporter_load(transporter, t)
                # save if transporter animation is not done
                if not done:
                    animation_done = False
                t = t + 1

            # switch status if animation is done
            if animation_done:
                self.animation_status = 2

        # start next tick
        # with 60 FPS
        if self.animation_status != 2:
            self.canvas.after(1000 // 60, self.animate_canvas)

    # renders the deliver button
    def render_deliver_button(self):
        Button(self.master, text='Ausliefern', command=lambda: Game(self.master, self.transporter).render()).place(x=150, y=10)

    # renders the GUI
    def render(self):
        self.master = Tk()
        self.master.title('LKW Manager v.1.0')
        self.master.geometry('480x80')
        self.master.configure(background='#2C2C2E')
        self.master.protocol("WM_DELETE_WINDOW", self.close)

        Button(self.master, text='Ladeliste erstellen', command=self.start_packing).place(x=10, y=10)
        Button(self.master, text='Geräte bearbeiten', command=lambda: DevicesGUI(self.db, self.master)).place(x=10,
                                                                                                              y=40)
        Button(self.master, text='Transporter bearbeiten', command=lambda: TransporterGUI(self.db, self.master)).place(
            x=150, y=40)
        Button(self.master, text='Fahrer bearbeiten', command=lambda: DriverGUI(self.db, self.master)).place(x=340,
                                                                                                             y=40)
        mainloop()
