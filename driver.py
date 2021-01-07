class Driver:
    def __init__(self, driver_id, weight):
        self.id = driver_id
        self.weight = weight

    # returns the ID
    def get_id(self):
        return self.id

    # returns the weight in g
    def get_weight(self):
        return self.get_weight_kg()*1000

    # returns the weight in kg
    def get_weight_kg(self):
        return self.weight

