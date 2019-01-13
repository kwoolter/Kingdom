import collections
import random


class Game():
    # States
    STATE_LOADED = "loaded"
    STATE_INITIALISED = "initialised"
    START_RUNNING = "running"

    # Events
    EVENT_TICK = "Tick"
    EVENT_GAME_OVER = "game over"

    def __init__(self, name: str):
        self.name = name
        self._state = Game.STATE_LOADED
        self.kingdom = None
        self.player_name = None
        self.events = EventQueue()

    def initialise(self, kingdom_name: str, player_name: str = "John Doe"):
        self.state = Game.STATE_INITIALISED
        self.kingdom = Kingdom(kingdom_name)
        self.kingdom.initialise()
        self.player_name = player_name

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._old_state = self.state
        self._state = new_state

        self.events.add_event(Event(self._state,
                                    "Game state change from {0} to {1}".format(self._old_state, self._state),
                                    Event.STATE))

    @property
    def current_season(self):
        return self.kingdom.current_season

    def __str__(self):

        if self.state == Game.STATE_INITIALISED:
            _str = "{0} ({1}): {2} played by {3}".format(self.name, self.state, self.kingdom.name, self.player_name)
            _str += "\n" + str(self.kingdom)
        else:
            _str = "{0} ({1})".format(self.name, self.state)

        return _str

    def get_next_event(self):

        next_event = None
        if self.events.size() > 0:
            next_event = self.events.pop_event()

        return next_event

    def play(self, dyke, fields,defend, rice_planted):
        if self.state != Game.STATE_INITIALISED:
            raise Exception("Can't play the game in current state {0}".format(self.state))

        self.kingdom.do_season(dyke, fields,defend, rice_planted)


class Season():
    WINTER = "Winter"
    GROWING = "Growing"
    HARVEST = "Harvest"
    NAMES = [WINTER, GROWING, HARVEST]

    DEATH_STARVATION = "starvation"
    DEATH_KILLED_BY_THIEVES = "thief killing"
    DEATH_BY_FLOODING = "flood deaths"
    ADD_BIRTHS = "births"
    ADD_THIEVES = "add thieves"

    RICE_GROWN = "rice grown"
    RICE_STOLEN = "rice stolen"
    RICE_FLOODED = "rice flooded"
    RICE_EATEN = "rice eaten"

    def __init__(self, name: str, year: int):
        self.name = name
        self.year = year
        self.calculated = False
        self.population_changes = {Season.DEATH_STARVATION: 0,
                                   Season.DEATH_KILLED_BY_THIEVES: 0,
                                   Season.DEATH_BY_FLOODING: 0,
                                   Season.ADD_BIRTHS: 0,
                                   Season.ADD_THIEVES: 0
                                   }

        self.food_changes = {Season.RICE_GROWN: 0,
                             Season.RICE_EATEN : 0,
                             Season.RICE_STOLEN: 0,
                             Season.RICE_FLOODED: 0}

    def __str__(self):
        return "{0} of year {1}".format(self.name, self.year)

    @property
    def population_change(self):
        return sum(list(self.population_changes.values()))

    @property
    def food_change(self):
        return sum(list(self.food_changes.values()))

    def get_next_season_name(self):
        next_season_index = Season.NAMES.index(self.name) + 1
        if next_season_index >= len(Season.NAMES):
            next_season_index = 0
        return Season.NAMES[next_season_index]

    def calculate(self, kingdom, dyke: int, fields: int, defend: int, rice_planted: int = 0):


        # Thief attack calcs
        attack = random.randint(0,10)
        do_attack = True

        # Season Winter
        if self.name == Season.WINTER:

            if attack < 5:
                do_attack = False
            else:
                attack_index = 200 + random.randint(0,70) - defend

        # Season Growing
        elif self.name == Season.GROWING:

            if attack < 2:
                do_attack = False
            else:
                attack_index = 30 + random.randint(0, 200) - defend

        # Season Harvest
        elif self.name == Season.HARVEST:

            if attack < 6:
                do_attack = False
            else:
                attack_index = random.randint(0, 400) - defend


        if do_attack is True:
            attack_index = max(0, attack_index)

            thief_deaths = int(defend * attack_index / 400)
            self.population_changes[Season.DEATH_KILLED_BY_THIEVES] = thief_deaths * -1

            stolen_food = attack_index * kingdom.total_food / 729 + random.randint(0, int(2000 - defend + thief_deaths)) / 10
            stolen_food = max(0, stolen_food)
            if stolen_food > 2000:
                stolen_food = 1900 + random.randint(0,200)

            self.food_changes[Season.RICE_STOLEN] = int(stolen_food) * -1

        # Flood calcs
        # Season Winter
        if self.name == Season.WINTER:

            flood_index = random.randint(0, 330) / (dyke + 1)

        # Season Growing
        elif self.name == Season.GROWING:

            flood_index = (random.randint(0, 100) + 60) / (dyke + 1)

        # Season Harvest
        elif self.name == Season.HARVEST:

            flood_index = 0
            rice_planted = 18 * (11 + random.uniform(0,3)) * (0.05 - 1 / fields) * rice_planted


        if flood_index >= 1:

            villages_flooded = random.randint(0, len(kingdom.villages))
            villages_flooded = 0

            if flood_index < 2:
                flood_index = random.uniform(0,2)
            else:
                flood_index = random.uniform(0,4)

            dyke_survivors = int((dyke / 10) * (10 - flood_index))
            field_survivors = int((fields / 10) * (10 - flood_index))
            defend_survivors = int((defend / 6) * (6 - villages_flooded))

            self.population_changes[Season.DEATH_BY_FLOODING] = (kingdom.population - dyke_survivors - field_survivors - defend_survivors) * -1
            self.food_changes[Season.RICE_FLOODED] = int(kingdom.total_food * villages_flooded / 6) * -1

        # Food calcs
        if self.name == Season.WINTER or fields == 0 or rice_planted < 1:
            rice_grown = 0
        elif self.name == Season.GROWING:
            if rice_planted > 1000:
                rice_planted = 1000
            rice_grown = rice_planted * (fields - 10)/fields
        elif self.name == Season.HARVEST:
            rice_grown = 18 * (11+random.uniform(0,3)) * (0.05 - 1/fields) * rice_planted

        self.food_changes[Season.RICE_GROWN] = int(rice_grown)

        # Starvation calcs
        starvation_deaths = 0
        new_population = kingdom.population + self.population_change
        new_total_food = kingdom.total_food + self.food_change

        if new_population > 0:
            t = new_total_food/new_population
            if t > 5:
                t = 4
            elif t < 2:
                starvation_deaths = new_population
            elif t > 4:
                t = 3.5
            else:
                starvation_deaths = int(kingdom.population * (7 - t) / 7)
                t=3

            self.population_changes[Season.DEATH_STARVATION] = starvation_deaths * -1
            new_population -= starvation_deaths
            rice_eaten = int(new_population * t - starvation_deaths*t/2)

            self.food_changes[Season.RICE_EATEN] = rice_eaten * -1

            # Thief add calc
            if new_population < 200 and random.randint(0,3) == 1:
                self.population_changes[Season.ADD_THIEVES] = 50 + random.randint(1, 100)

            # Birth calcs
            self.population_changes[Season.ADD_BIRTHS] = int(new_population * 0.045)

        # Wrap up
        self.calculated = True
        print(self.population_changes)
        print(self.food_changes)


class Kingdom():
    VILLAGES = 3
    INITIAL_SEASON = Season.WINTER

    def __init__(self, name: str):
        self.name = name
        self.villages = None
        self.year = 0
        self.years = {}

    def initialise(self):
        self.year = 1
        self.current_season = Season(Kingdom.INITIAL_SEASON, self.year)
        self._population = 300 + random.randint(0, 100)
        self._food = 5000 + random.randint(0, 2000)

        self.years[self.year] = {}
        self.years[self.year][self.current_season.name] = self.current_season

        self.villages = []
        for i in range(Kingdom.VILLAGES):
            self.villages.append(Village())
            self.villages[i].initialise()

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, new : int):
        self._population = new

    @property
    def total_food(self):
        return self._food

    @total_food.setter
    def food(self, new : int):
        self._food = new


    def do_season(self, dyke: int = 0, fields: int = 0, defend: int = 0, rice_planted: int = 0):
        if self.current_season.name == Season.WINTER:
            self.rice_planted = 0
        # Remeber how much rice we planted in the growing season
        elif self.current_season.name == Season.GROWING:
            self.rice_planted = rice_planted

        self.current_season.calculate(self, dyke, fields, defend, self.rice_planted)
        self._population += self.current_season.population_change
        self._food += self.current_season.food_change

        self.current_season = Season(self.current_season.get_next_season_name(), self.year)

        if self.current_season.name == Season.WINTER:
            self.year += 1
            self.years[self.year] = {}

        self.years[self.year][self.current_season.name] = self.current_season

    def __str__(self):
        _str = "The Kingdom of {0}: year={1}, season={2}, population={3}, food={4}".format(self.name, self.year,
                                                                                 self.current_season, self.population,
                                                                                           self.total_food)

        return _str


class Village():
    INITIAL_RICE = 500
    INITIAL_VILLAGERS = 200

    count = 0

    def __init__(self, name: str = None):
        Village.count += 1
        self.villagers = 0
        self.rice = 0

        if name is None:
            self.name = "Village {0}".format(Village.count)
        else:
            self.name = name

    def __str__(self):
        _str = "{0}: villagers={1}, rice={2}".format(self.name, self.villagers, self.rice)
        return _str

    def initialise(self, villagers: int = INITIAL_VILLAGERS, rice: int = INITIAL_RICE):
        self.villagers = villagers
        self.rice = rice


class Event():
    # Event Types
    DEFAULT = "default"
    STATE = "state"
    GAME = "game"

    def __init__(self, name: str, description: str = None, type: str = DEFAULT):
        self.name = name
        self.description = description
        self.type = type

    def __str__(self):
        return "{0}:{1} ({2})".format(self.name, self.description, self.type)


class EventQueue():
    def __init__(self):
        self.events = collections.deque()

    def add_event(self, new_event: Event):
        self.events.append(new_event)

    def pop_event(self):
        return self.events.pop()

    def size(self):
        return len(self.events)

    def print(self):
        for event in self.events:
            print(event)
