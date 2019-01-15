import sys
import time

import model


class TextView():
    def __init__(self, model: model.Game):
        self.model = model

    def initialise(self):
        pass

    def print_census(self):
        kingdom = self.model.kingdom

        print("\n{0:^50}".format("Census Results"))
        print("\nAt the start of the {0} season in year {1} of your reign this is the situation.".format(
            kingdom.current_season.name, kingdom.year))
        print("\nAllowing for births and deaths the population is {0}".format(kingdom.population))
        print("\nThere are {0} baskets of rice in the village stores.".format(kingdom.total_food))

    def print_season(self):
        season_view = SeasonTextView(self.model.kingdom.previous_season)
        season_view.print()


class SeasonTextView():

    def __init__(self, season: model.Season):
        self.season = season

    def print(self):

        print("\n{0:^50}".format("Village Leader's Report"))

        kingdom = self.season.kingdom

        # Print deaths impact
        population_impact = abs(kingdom.population / (kingdom.current_season.population_change + 1))
        food_impact = abs(kingdom.total_food / (kingdom.current_season.food_change + 1))
        max_impact = (max(population_impact, food_impact))

        msg = None
        if max_impact < 2:
            msg = "Disastrous Losses!"
        elif max_impact < 4:
            msg = "Worrying Losses!"
        elif max_impact < 8:
            msg = "You got off lightly!"

        if msg is not None:
            print("\n{0:^50}".format(msg))

        # Print food supply impact
        msg = None
        t = kingdom.total_food / (kingdom.population+1)
        if t < 4:
            msg = "Food supply is low."
        elif t < 2:
            msg = "Starvation Imminent!"
        if msg is not None:
            print("\n{0:^50}".format(msg))

        # Print status
        print("\nIn the {0} season of year {1} of your reign, the kingdom has suffered these losses:\n".format(
            self.season.name, self.season.year))
        print("Deaths from floods: {0}".format(abs(self.season.population_changes[model.Season.DEATH_BY_FLOODING])))
        print("Deaths from the attacks: {0}".format(
            abs(self.season.population_changes[model.Season.DEATH_KILLED_BY_THIEVES])))
        print("Deaths from starvation: {0}".format(abs(self.season.population_changes[model.Season.DEATH_STARVATION])))
        print("Baskets of rice lost during the floods: {0}".format(
            abs(self.season.food_changes[model.Season.RICE_FLOODED])))
        print("Baskets of rice lost during the attacks: {0}".format(
            abs(self.season.food_changes[model.Season.RICE_STOLEN])))

        print("")

def type(text: str, wait=0.1):
    for i in range(0, len(text)):
        sys.stdout.write(text[i])
        sys.stdout.flush()
        time.sleep(wait)
