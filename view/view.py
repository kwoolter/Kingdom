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

        kingdom = self.model.kingdom


        _str = "\nThe Kingdom of {0}: year={1}, season={2}, population={3}, food={4}".format(kingdom.name,
                                                                                   kingdom.year,
                                                                                   kingdom.current_season.name,
                                                                                   kingdom.population,
                                                                                    kingdom.total_food)

        # for village in kingdom.villages:
        #     _str += "\n" + str(village)

        #type(str(self.model), 0.01)

        _str += "\n"

        print(_str)

        population_impact = kingdom.population / (kingdom.current_season.population_change+1)
        food_impact = kingdom.total_food / (kingdom.current_season.food_change+1)

        if population_impact < 2 or food_impact < 2:
            print("Disastrous")
        elif  population_impact < 4 or food_impact < 4:
            print("Worrying")
        elif  population_impact < 8 or food_impact < 8:
            print("Got off lightly")

def type(text: str, wait=0.1):
    for i in range(0, len(text)):
        sys.stdout.write(text[i])
        sys.stdout.flush()
        time.sleep(wait)
