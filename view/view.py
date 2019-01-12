import model

class TextView():
    def __init__(self, model : model.Game):
        self. model = model

    def initialise(self):
        pass

    def print(self):
        print("Printing {0} game model...".format(self.model.name))