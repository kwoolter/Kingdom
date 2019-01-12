import model
import sys
import time

class TextView():
    def __init__(self, model : model.Game):
        self. model = model

    def initialise(self):
        pass

    def print(self):
        print("Printing {0} game model...".format(self.model.name))
        type(str(self.model))
        print()

def type(text: str, wait=0.1):
    for i in range(0, len(text)):
        sys.stdout.write(text[i])
        sys.stdout.flush()
        time.sleep(wait)
