from DeliveryGame.screen_object import ScreenObject


# Car class: car in canvas
class Car(ScreenObject):
    def __init__(self, car_id, master, canvas, objects_manager):
        super(Car, self).__init__(car_id, master, canvas, objects_manager)

        # set min distance to other objects
        # works not perfectly, I've invested a lot of time in debugging
        self.min_distance = 400

        # car images
        self.images = ['car_green.png', 'car_orange.png', 'car_pink.png', 'car_red.png', 'car_dark_green.png',
                       'car_light_blue.png']

    # returns the car speed depending on street speed and column
    def get_speed(self, street_speed):
        return street_speed - (-0.4 * self.get_column() + 3)
