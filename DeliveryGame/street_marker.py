# Street Marker class: class for street lines
# INFO: street markers are not handled by the objects manager,
#       because they are unnecessary for other objects
class StreetMarker:
    def __init__(self, marker_id, master, canvas, street_marker_handler):
        self.id = marker_id
        self.master = master
        self.canvas = canvas
        self.street_marker_handler = street_marker_handler

    # returns the ID as string
    def get_id(self):
        return str(self.id)

    # renders the marker
    def render(self, c, r):
        self.canvas.create_rectangle(80 + c * 80, 40 + r * 80, 80 + c * 80, 80 + r * 80,
                                     outline="white", fill='white', tags=(self.get_id(),))

    # moves the marker
    def move(self, speed):
        x1, y1, x2, y2 = self.canvas.bbox(self.get_id())
        if y1 < int(self.canvas['height']):
            self.canvas.move(self.get_id(), 0, speed)
        else:
            self.canvas.move(self.get_id(), 0, int(self.canvas['height']) * (-1) - 100)
