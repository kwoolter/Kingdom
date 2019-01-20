import sys
import time
import textwrap
import model


class ObjectColours:

    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    GREY = 7
    WHITE = 8

    BRIGHT_RED = RED + 60
    BRIGHT_GREEN = GREEN +60
    BRIGHT_YELLOW = YELLOW + 60
    BRIGHT_BLUE = BLUE + 60
    BRIGHT_MAGENTA = MAGENTA + 60
    BIGHT_CYAN = CYAN + 60
    BRIGHT_GREY = GREY + 60
    BRIGHT_WHITE = WHITE + 60

    @staticmethod
    def colour_codes(fg = BLACK, bg = WHITE):
        return "\x1B[" + str(fg+30) + ";" + str(bg+40) +"m"

    @staticmethod
    def reset():
        return "\x00"

class ObjectGraphics:

    object_to_char = {

        model.Map.DAM : "|",
        model.Map.WATER : "~",
        model.Map.VILLAGE : "#",
        model.Map.MOUNTAIN : "^",
        model.Map.THIEF : "T",
        None : " "

    }

    object_to_colour = {
        model.Map.DAM : (ObjectColours.BLUE,ObjectColours.CYAN),
        model.Map.WATER : (ObjectColours.YELLOW,ObjectColours.BRIGHT_YELLOW),
        model.Map.VILLAGE : (ObjectColours.BRIGHT_GREEN, ObjectColours.GREEN),
        model.Map.MOUNTAIN: (ObjectColours.RED, ObjectColours.BLACK),
        model.Map.THIEF: (ObjectColours.RED, ObjectColours.BLACK),
        None : (ObjectColours.BLACK, ObjectColours.BLACK),
    }


class TextView():

    def __init__(self, model: model.Game):
        self.model = model
        self.wrapper = textwrap.TextWrapper(width=60)
        self.map_view = None

    def initialise(self):
        self.map_view = MapView(self.model.kingdom.map)
        self.map_view.initialise()

    def print_census(self):
        kingdom = self.model.kingdom

        type("\n{0:^50}\n".format("Census Results"))
        type("\nAt the start of the {0} season in year {1} of your reign this is the situation.\n".format(
            kingdom.current_season.name, kingdom.year))
        print("\nAllowing for births and deaths the population is {0}.".format(kingdom.population))
        print("\nThere are {0} baskets of rice in the village stores.".format(kingdom.total_food))

    def print_season(self):
        season_view = SeasonTextView(self.model.kingdom.previous_season)
        season_view.print()

    def print_map(self):
        self.map_view.print()

    def print_instructions(self):
        type("\n\n"+ self.wrapper.fill("The kingdom is three villages. It is between the Yellow River and the mountains."))
        type("\n\n" + self.wrapper.fill("You have been chosen to take all the important decisions. Your poor predecessor"
                                    " was executed by thieves who live in the nearby mountains."))
        type("\n\n" + self.wrapper.fill("These thieves live off the villagers and often attack. "
                                    "The rice stored in the villages"
           " must be protected at all times."))
        type("\n\n" + self.wrapper.fill("The year consists of three long seasons, Winter, Growing and Harvest. "
                                    "rice is planted every Growing Season."
           " You must decide how much is planted."))
        type("\n\n" + self.wrapper.fill("The river is likely to flood the fields and the villages."
                                    " The high dyke between the river and the fields"
           " must be kept up to prevent a serious flood."))
        type("\n\n" + self.wrapper.fill("The people live off the rice that they have grown. It is a very poor living."
           " You must decide what the people will work at each season so that they prosper under your leadership."))

        print("\n")

class SeasonTextView():

    def __init__(self, season: model.Season):
        self.season = season

    def print(self):

        type("\n{0:^50}\n".format("Village Leader's Report"))

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
        type("\nIn the {0} season of year {1} of your reign, the kingdom has suffered these losses:\n".format(
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


class MapView():

    def __init__(self, map : model.Map):
        self.map = map

    def initialise(self):
        pass

    def print(self):

        header = ObjectColours.colour_codes(fg=ObjectColours.BRIGHT_YELLOW, bg=ObjectColours.BLACK) + \
                 "{0:^" + str(self.map.width) + "}" + \
                 ObjectColours.colour_codes(bg=ObjectColours.WHITE)

        print(header.format("Yellow River Kingdom"))

        for y in range(3, self.map.height):
            row = ""
            for x in range(0, self.map.width):
                obj = ObjectGraphics.object_to_char[self.map.get(x,y)]
                fg, bg = ObjectGraphics.object_to_colour[self.map.get(x,y)]
                codes = ObjectColours.colour_codes(fg, bg)
                row += codes + obj

            row += ObjectColours.colour_codes(bg=ObjectColours.WHITE)

            print(row)

            footer = ObjectColours.colour_codes(fg=ObjectColours.BRIGHT_GREY, bg=ObjectColours.BLACK) + \
                        "   DYKE        VILLAGES      MOUNTAINS  " + \
                        ObjectColours.colour_codes(bg=ObjectColours.WHITE)

        print(footer)

def type(text: str, wait=0.05):
    for i in range(0, len(text)):
        sys.stdout.write(text[i])
        sys.stdout.flush()
        time.sleep(wait)
