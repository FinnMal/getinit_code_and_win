import threading
from DeliveryGame.street_marker import StreetMarker


# Street Markers Manager class: manages the street lines in canvas
class StreetMarkersManager:
    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas

        # default values
        self.canvas_counter = 0
        self.street_markers = []

    # adds a marker to canvas
    def add_marker(self, column, row):
        marker = StreetMarker('marker_' + str(self.canvas_counter), self.master, self.canvas, self)
        marker.render(column, row)
        self.street_markers.append(marker)
        self.canvas_counter = self.canvas_counter + 1

    # moves every marker
    def move_markers(self, speed):
        for marker in self.street_markers:
            threading.Thread(target=marker.move, args=(speed,)).start()

    # adds the needed markers to canvas
    def add_markers(self):
        for c in range(4):
            for r in range(0, round(int(self.canvas['height']) / 76.9230769231), 2):
                self.add_marker(c, r)
