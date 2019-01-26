import sys
import textwrap
import time

from colorama import init, Fore, Back

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
    BRIGHT_GREEN = GREEN + 60
    BRIGHT_YELLOW = YELLOW + 60
    BRIGHT_BLUE = BLUE + 60
    BRIGHT_MAGENTA = MAGENTA + 60
    BIGHT_CYAN = CYAN + 60
    BRIGHT_GREY = GREY + 60
    BRIGHT_WHITE = WHITE + 60

    @staticmethod
    def colour_codes(fg=Fore.WHITE, bg=Back.BLACK):
        return fg + bg
        # return "\x1B[" + str(fg+30) + ";" + str(bg+40) +"m"

    @staticmethod
    def reset():
        return "\x00"


class ObjectGraphics:
    object_to_char = {

        model.Map.DAM: "|",
        model.Map.WATER: "~",
        model.Map.VILLAGE: "#",
        model.Map.MOUNTAIN: "^",
        model.Map.THIEF: "T",
        model.Map.LOCUST:"@",
        model.Map.GRAVE:"+",
        model.Map.SNOW:"*",
        model.Map.EARTH:":",
        model.Map.ICE:"~",
        None: " "

    }

    object_to_colour = {
        model.Map.DAM: (Fore.BLUE, Back.CYAN),
        model.Map.WATER: (Fore.YELLOW, Back.LIGHTYELLOW_EX),
        model.Map.VILLAGE: (Fore.LIGHTGREEN_EX, Back.GREEN),
        model.Map.MOUNTAIN: (Fore.RED, Back.BLACK),
        model.Map.THIEF: (Fore.RED, Back.BLACK),
        model.Map.LOCUST: (Fore.GREEN, Back.BLACK),
        model.Map.GRAVE: (Fore.WHITE, Back.BLACK),
        model.Map.SNOW: (Fore.LIGHTWHITE_EX, Back.BLACK),
        model.Map.ICE: (Fore.LIGHTCYAN_EX, Back.LIGHTWHITE_EX),
        model.Map.EARTH: (Fore.RED, Back.LIGHTRED_EX),
        None: (Fore.LIGHTWHITE_EX, Back.BLACK),
    }


class TextView():

    WIDTH = 50
    DEFAULT_COLOURS = Fore.LIGHTWHITE_EX + Back.BLACK
    ALERT_COLOURS = Fore.LIGHTYELLOW_EX + Back.BLACK
    RITUAL_COLOURS = Fore.LIGHTCYAN_EX + Back.BLACK

    def __init__(self, model: model.Game):
        self.model = model
        self.wrapper = textwrap.TextWrapper(width=TextView.WIDTH)
        self.map_view = None

        if sys.stdout.isatty() is False:
            init(convert=False, strip=False)
        else:
            init(convert=True)

        print(TextView.DEFAULT_COLOURS)

    def initialise(self):
        self.map_view = MapView(self.model.kingdom.map)
        self.map_view.initialise()

        print(TextView.DEFAULT_COLOURS)

    def print_census(self):

        if self.model.state == model.Game.STATE_LOADED:
            raise Exception("Game not in a state to be printed ({0}).".format(self.model.state))

        kingdom = self.model.kingdom

        print(TextView.DEFAULT_COLOURS)

        header = "\n{0:^" + str(TextView.WIDTH) + "}\n"
        type(header.format("Census Results"))
        type("\n\n" + self.wrapper.fill(
            "At the start of the {0} season in year {1} of your reign this is the situation.".format(
                kingdom.current_season.name, kingdom.year)) + "\n")
        print("\nAllowing for births and deaths the population is {0}.".format(kingdom.population))
        print("\nThere are {0} baskets of rice in the village stores.".format(kingdom.total_food))

    def print_season(self):

        print(TextView.DEFAULT_COLOURS)

        season_view = SeasonTextView(self.model.kingdom.previous_season)
        season_view.print()

        self.print_game_over()

    def print_map(self):
        self.map_view.print()
        print(TextView.DEFAULT_COLOURS)

    def print_instructions(self):

        print(TextView.DEFAULT_COLOURS)

        type("\n\n" + self.wrapper.fill(
            "The kingdom is three villages. It is between the Yellow River and the mountains."))
        type(
            "\n\n" + self.wrapper.fill("You have been chosen to take all the important decisions. Your poor predecessor"
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

    def print_ritual(self):

        if self.model.state == model.Game.STATE_LOADED:
            raise Exception("Game not in a state to perform ritual ({0}).".format(self.model.state))

        print(TextView.RITUAL_COLOURS)

        msg = "{0}, we have survived for {1} seasons under your glorious control.".format(self.model.player_name,
                                                                                        self.model.kingdom.seasons)
        type("\n" + self.wrapper.fill(msg))

        msg = "By an ancient custom we must offer you the chance to lay down this terrible burden and resume a normal life."
        type("\n\n" + self.wrapper.fill(msg))

        msg = "In the time honoured fashion I will now ask the ritual question:"
        type("\n\n" + self.wrapper.fill(msg))

        msg = "Are you prepared to accept the burden of decision again?"
        type("\n\n" + self.wrapper.fill(msg))

        msg = "You need only answer Yes or No for the people will understand your reasons."
        type("\n\n" + self.wrapper.fill(msg) + "\n")

        print(TextView.DEFAULT_COLOURS)

    def print_game_over(self):

        print(TextView.ALERT_COLOURS)

        kingdom = self.model.kingdom

        if kingdom.total_food <= 0:
            msg = self.wrapper.fill(
                "There was no food left. All of the people have run off and joined up with the thieves" \
                " after {0} seasons of your misrule".format(kingdom.seasons))
            type("\n" + msg + "\n\n")
        elif kingdom.population <= 0:
            msg = self.wrapper.fill("There is no-one left! They have all been killed off by your "
                                    "decisions after only {0} year(s).".format(kingdom.year))

            type("\n" + msg + "\n\n")

        print(TextView.DEFAULT_COLOURS)

    def print_high_score_table(self):

        print(TextView.DEFAULT_COLOURS)

        msg = " " * TextView.WIDTH
        print("\n" + Back.LIGHTYELLOW_EX + Fore.BLACK + msg + Back.BLACK)
        msg = "{0:^" + str(TextView.WIDTH) + "}"
        msg = msg.format("***  Kingdom Legends  ***")
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + msg + Back.BLACK)
        msg = "{0:^" + str(TextView.WIDTH) + "}"
        msg = msg.format("***  " + self.model.mode + "  ***")
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + msg + Back.BLACK)
        msg = Back.LIGHTYELLOW_EX + " " * TextView.WIDTH + Back.BLACK
        print(msg + "\n" + TextView.DEFAULT_COLOURS)

        self.model.print_high_scores()

        print(TextView.DEFAULT_COLOURS)


class SeasonTextView():
    WIDTH = 50
    DEFAULT_COLOURS = Fore.LIGHTWHITE_EX + Back.BLACK
    ALERT_COLOURS = Fore.LIGHTYELLOW_EX + Back.BLACK

    def __init__(self, season: model.Season):
        self.season = season
        self.wrapper = textwrap.TextWrapper(width=SeasonTextView.WIDTH)

    def print(self):

        print(SeasonTextView.DEFAULT_COLOURS)

        header = "\n{0:^" + str(SeasonTextView.WIDTH) + "}\n"
        type(header.format("Village Leader's Report"))

        kingdom = self.season.kingdom

        # Print deaths impact
        population_impact = abs(kingdom.population / (kingdom.current_season.population_change + 1))
        food_impact = abs(kingdom.total_food / (kingdom.current_season.food_change + 1))
        max_impact = (min(population_impact, food_impact))

        msg = None
        if max_impact < 2:
            msg = "Disastrous Losses!"
        elif max_impact < 4:
            msg = "Worrying Losses!"
        elif max_impact < 8:
            msg = "You got off lightly!"

        if msg is not None:
            print(SeasonTextView.ALERT_COLOURS)
            banner = "{0:^" + str(SeasonTextView.WIDTH) + "}"
            print("\n" + banner.format(msg))

        # Print food supply impact
        msg = None
        t = kingdom.total_food / (kingdom.population + 1)
        if t < 4:
            msg = "Food supply is low."
        elif t < 2:
            msg = "Starvation Imminent!"
        if msg is not None:
            print(SeasonTextView.ALERT_COLOURS)
            banner = "{0:^" + str(SeasonTextView.WIDTH) + "}"
            print("\n" + banner.format(msg))

        print(SeasonTextView.DEFAULT_COLOURS)

        # Print status
        type("\n" + self.wrapper.fill(
            "In the {0} season of year {1} of your reign, the kingdom has suffered these losses:".format(
                self.season.name, self.season.year)) + "\n\n")
        print("Deaths from floods: {0}".format(abs(self.season.population_changes[model.Season.DEATH_BY_FLOODING])))
        print("Deaths from the attacks: {0}".format(
            abs(self.season.population_changes[model.Season.DEATH_KILLED_BY_THIEVES])))
        print("Deaths from starvation: {0}".format(abs(self.season.population_changes[model.Season.DEATH_STARVATION])))
        print("Baskets of rice lost during the floods: {0}".format(
            abs(self.season.food_changes[model.Season.RICE_FLOODED])))
        print("Baskets of rice lost during the attacks: {0}".format(
            abs(self.season.food_changes[model.Season.RICE_STOLEN])))


class MapView():

    def __init__(self, map: model.Map):
        self.map = map

    def initialise(self):
        pass

    def print(self):

        header = Fore.LIGHTYELLOW_EX + Back.BLACK + \
                 "{0:^" + str(self.map.width) + "}" + Back.BLACK

        print(header.format("Yellow River Kingdom"))

        for y in range(3, self.map.height):
            row = ""
            for x in range(0, self.map.width):
                obj = ObjectGraphics.object_to_char[self.map.get(x, y)]
                fg, bg = ObjectGraphics.object_to_colour[self.map.get(x, y)]
                row += fg + bg + obj

            row += Back.BLACK

            print(row)

            footer = Fore.LIGHTWHITE_EX + Back.BLACK + \
                     "   DYKE        VILLAGES      MOUNTAINS  " + \
                     Back.BLACK

        print(footer)


def type(text: str, wait=0.01):
    for i in range(0, len(text)):
        sys.stdout.write(text[i])
        sys.stdout.flush()
        time.sleep(wait)
