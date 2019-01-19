import collections
import random


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


class Game():
    # States
    STATE_LOADED = "loaded"
    STATE_INITIALISED = "initialised"
    STATE_RUNNING = "running"
    STATE_GAME_OVER = "Game Over"

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
        self.kingdom.initialise(self.events)
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

    def play(self, dyke, fields, defend, rice_planted):
        if self.state != Game.STATE_INITIALISED:
            raise Exception("Can't play the game in current state {0}".format(self.state))

        self.kingdom.do_season(dyke, fields, defend, rice_planted)

        if self.kingdom.population <= 0 or self.kingdom.total_food <= 0:
            self.state = Game.STATE_GAME_OVER


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
                             Season.RICE_EATEN: 0,
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

        self.kingdom = kingdom
        self.year = kingdom.year
        self.dyke = dyke
        self.fields = fields
        self.defend = defend
        self.rice_planted = rice_planted

        if random.uniform(0, 5) > 5:
            self.calculate_attack()
            self.calculate_flood()
        else:
            self.calculate_flood()
            self.calculate_attack()

        self.calculated_season_end()

        # Wrap up
        self.calculated = True
        # print(self.population_changes)
        # print(self.food_changes)
        # print("Rice planted out in the fields={0}".format(self.rice_planted))

    # Thief attack calcs
    def calculate_attack(self):

        attack = random.randint(0, 10)
        do_attack = True

        # Season Winter
        if self.name == Season.WINTER:

            if attack < 5:
                do_attack = False
            else:
                attack_index = 200 + random.randint(0, 70) - self.defend

        # Season Growing
        elif self.name == Season.GROWING:

            if attack < 2:
                do_attack = False
            else:
                attack_index = 30 + random.randint(0, 200) - self.defend

        # Season Harvest
        elif self.name == Season.HARVEST:

            if attack < 6:
                do_attack = False
            else:
                attack_index = random.randint(0, 400) - self.defend

        if do_attack is True:
            attack_index = max(0, attack_index)

            thief_deaths = int(self.defend * attack_index / 400)
            self.population_changes[Season.DEATH_KILLED_BY_THIEVES] = thief_deaths * -1

            stolen_food = attack_index * self.kingdom.total_food / 729 + random.randint(0, int(
                2000 - self.defend + thief_deaths)) / 10
            stolen_food = max(0, stolen_food)
            if stolen_food > 2000:
                stolen_food = 1900 + random.randint(0, 200)

            self.food_changes[Season.RICE_STOLEN] = int(stolen_food) * -1

    # Flood calcs
    def calculate_flood(self):

        # Season Winter
        if self.name == Season.WINTER:
            flood_index = random.randint(0, 330) / (self.dyke + 1)

        # Season Growing
        elif self.name == Season.GROWING:
            flood_index = (random.randint(0, 100) + 60) / (self.dyke + 1)

        # Season Harvest
        elif self.name == Season.HARVEST:
            flood_index = 0

        if flood_index >= 1:

            if flood_index < 2:
                flood_index = random.uniform(0, 2)
            else:
                flood_index = random.uniform(0, 4)

            # villages_flooded = random.randint(0, len(self.kingdom.villages))
            villages_flooded = self.kingdom.map.flood(flood_index)
            self.kingdom.add_event(Event("VILLAGE FLOODED",
                                         "{0} villages flooded".format(villages_flooded),
                                         Event.GAME))


            # Calculate flood impact on population
            dyke_survivors = int((self.dyke / 10) * (10 - flood_index))
            field_survivors = int((self.fields / 10) * (10 - flood_index))
            defend_survivors = int((self.defend / 6) * (6 - villages_flooded))
            self.population_changes[Season.DEATH_BY_FLOODING] = (self.kingdom.population
                                                                 - dyke_survivors
                                                                 - field_survivors
                                                                 - defend_survivors) * -1

            # Calculate flood impact on stored rice
            self.food_changes[Season.RICE_FLOODED] = int(self.kingdom.total_food * villages_flooded / 6) * -1

            # Calculate flood impact on planted rice
            # Season Growing
            if self.name == Season.GROWING:
                self.rice_planted *= (20 - flood_index) / 20

            # Season Harvest
            elif self.name == Season.HARVEST:
                self.rice_planted = (10 - flood_index) / 10

            self.rice_planted = int(self.rice_planted)

    # Food, Births and Deaths
    def calculated_season_end(self):

        # Rice planting and growing calcs

        # No rice planted if it is winter, or u have no one working
        if self.name == Season.WINTER or self.fields == 0 or self.rice_planted < 1:
            self.rice_planted = 0
        # Calculate how much rice will grow based on resources assigned
        elif self.name == Season.GROWING:
            if self.rice_planted > 1000:
                self.rice_planted = 1000
            self.rice_planted *= (self.fields - 10) / self.fields
            self.kingdom.add_event(Event("RICE PLANTED",
                                         "{0} baskets of rice have been successfully planted".format(self.rice_planted),
                                         Event.GAME))
        # Calculate how much rice is harvested based on how much planted and resources
        elif self.name == Season.HARVEST:
            rice_grown = int(18 * (11 + random.uniform(0, 3)) * (0.05 - 1 / self.fields) * self.rice_planted)
            self.rice_planted = 0
            self.food_changes[Season.RICE_GROWN] = rice_grown
            self.kingdom.add_event(Event("RICE HARVESTED",
                                         "{0} baskets of rice have been harvested".format(rice_grown),
                                         Event.GAME))

        self.rice_planted = int(self.rice_planted)

        # Starvation calcs
        starvation_deaths = 0
        new_population = self.kingdom.population + self.population_change
        new_total_food = self.kingdom.total_food + self.food_change

        # Check we still have people alive...
        if new_population > 0:
            # Get ratio of food to people and tweak it to curb people's appetites
            t = new_total_food / new_population
            if t > 5:
                t = 4
            elif t < 2:
                starvation_deaths = new_population
            elif t > 4:
                t = 3.5
            else:
                starvation_deaths = int(self.kingdom.population * (7 - t) / 7)
                t = 3

            # Record how many people starved
            self.population_changes[Season.DEATH_STARVATION] = starvation_deaths * -1

            # Calculate how much food was eaten
            new_population -= starvation_deaths
            rice_eaten = int(new_population * t - starvation_deaths * t / 2)

            self.food_changes[Season.RICE_EATEN] = rice_eaten * -1

            self.kingdom.add_event(Event("RICE EATEN",
                                         "{0} baskets of rice eaten.".format(rice_eaten),
                                         Event.GAME))

            # If population is running low see if any thieves want to join?
            if new_population < 200 and random.randint(0, 3) == 1:
                new_villagers = 50 + random.randint(1, 100)
                self.population_changes[Season.ADD_THIEVES] = new_villagers
                self.kingdom.add_event(Event("THIEVES",
                                             "{0} thieves have joined the villages.".format(new_villagers),
                                             Event.GAME))

            # Birth calcs
            new_villagers = int(new_population * 0.045)
            self.population_changes[Season.ADD_BIRTHS] = new_villagers
            self.kingdom.add_event(Event("BIRTHS",
                                         "{0} new births in the villages.".format(new_villagers),
                                         Event.GAME))

        else:
            self.kingdom.add_event(Event(Event.EVENT_GAME_OVER, "All villagers have died!", Event.GAME))

        if new_total_food <= 0:
            self.kingdom.add_event(Event(Event.EVENT_GAME_OVER, "There is no food left!", Event.GAME))


class Kingdom():
    VILLAGES = 3
    INITIAL_SEASON = Season.WINTER

    def __init__(self, name: str):
        self.name = name
        self.villages = None
        self.year = 0
        self.years = {}
        self.current_season = None
        self.previous_season = None
        self.map = Map()

    def initialise(self, event_queue: EventQueue):
        self._events = event_queue
        self.year = 1
        self.current_season = self.previous_season = Season(Kingdom.INITIAL_SEASON, self.year)
        self._population = 300 + random.randint(0, 100)
        self._food = 5000 + random.randint(0, 2000)

        self.years[self.year] = {}
        self.years[self.year][self.current_season.name] = self.current_season

        self.villages = []
        for i in range(Kingdom.VILLAGES):
            self.villages.append(Village())
            self.villages[i].initialise()

        self.map.initliaise()

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, new: int):
        self._population = new

    @property
    def total_food(self):
        return self._food

    @total_food.setter
    def food(self, new: int):
        self._food = new

    def add_event(self, new_event: Event):
        self._events.add_event(new_event)

    def flood(self, flood_index: int):
        self.map.flood(flood_index)

    def do_season(self, dyke: int = 0, fields: int = 0, defend: int = 0, rice_planted: int = 0):

        if rice_planted > self.total_food:
            raise Exception(
                "Trying to plant {0} food which is more than {1} in the store!".format(rice_planted, self.total_food))

        if dyke + fields + defend > self.population:
            raise Exception(
                "Trying to assign {0} people when you only have {1}!".format(dyke + fields + defend, self.population))

        # Reset the kingdom map
        self.map.initliaise()

        # Store season against the current year
        self.years[self.year][self.current_season.name] = self.current_season

        # No rice planted in winter
        if self.current_season.name == Season.WINTER:
            self.rice_planted = 0
        # Remember how much rice we planted in the growing season and deduct from total food
        elif self.current_season.name == Season.GROWING:
            self.rice_planted = rice_planted
            self._food -= rice_planted

        # See what happens in this season
        self.current_season.calculate(self, dyke, fields, defend, self.rice_planted)

        # Update how much rice remains planted after the season
        self.rice_planted = self.current_season.rice_planted

        # Make changes to population and food supplies
        self._population += self.current_season.population_change
        self._food += self.current_season.food_change

        # Move to the next season
        self.previous_season = self.current_season
        self.current_season = Season(self.current_season.get_next_season_name(), self.year)

        # If we got back to Winter we have started a new year!
        if self.current_season.name == Season.WINTER:
            self.year += 1
            self.years[self.year] = {}

    def __str__(self):
        _str = "The Kingdom of {0}: year={1}, season={2}, population={3}, food={4}".format(self.name, self.year,
                                                                                           self.current_season,
                                                                                           self.population,
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


class Map():
    WIDTH = 40
    HEIGHT = 25
    DAM_X = 1
    VILLAGE = "V"
    DAM = "|"
    WATER = "~"
    MOUNTAIN = "^"

    def __init__(self):

        self.map = [[None for y in range(Map.HEIGHT)] for x in range(Map.WIDTH)]
        self.villages = []

    def initliaise(self):

        self.villages = []
        self.villages.append((13, 8))
        self.villages.append((21, 12))
        self.villages.append((22, 18))

        for vx, vy in self.villages:
            for y in range(0,2):
                for x in range (-1,1):
                    self.set(vx+x, vy+y, Map.VILLAGE)

        for vy in range(3, 23):
            self.set(0, vy, Map.WATER)
            self.set(Map.DAM_X, vy, Map.DAM)
            self.set(Map.DAM_X+1, vy, Map.DAM)
            for i in range(0,9):
                self.set(28+i, vy, Map.MOUNTAIN)

    @property
    def width(self):
        return len(self.map)

    @property
    def height(self):
        return len(self.map[0])

    def is_valid_xy(self, x: int, y: int):
        result = False

        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            result = True

        return result

    def get(self, x: int, y: int):

        if self.is_valid_xy(x, y) is False:
            raise Exception("Trying to get tile at ({0},{1}) which is outside of the floorplan!".format(x, y))

        return self.map[x][y]

    def set(self, x: int, y: int, c):
        if self.is_valid_xy(x, y) is False:
            raise Exception("Trying to set tile at ({0},{1}) which is outside of the floorplan!".format(x, y))

        self.map[x][y] = c

    def flood(self, flood_index: int):

        print("Flooding with FI={0}".format(flood_index))

        fy = random.randint(0, 8) + 10
        fx = Map.DAM_X
        flooded_villages = set()
        self.set(fx, fy, Map.WATER)
        fx += 1
        self.set(fx, fy, Map.WATER)

        for i in range(int(flood_index * 100)):

            if (fx, fy) in self.villages:
                flooded_villages.add((fx, fy))
                print("village hit by flooding at {0},{1}".format(fx,fy))

            i = random.randint(0, 3)
            if i == 0:
                fx = min(fx + 1, self.width - 1)
            elif i == 1:
                fx = max(fx - 1, Map.DAM_X + 1)
            elif i == 2:
                fy = min(fy + 1, self.height - 1)
            elif i == 3:
                fy = max(fy - 1, 0)

            self.set(fx, fy, Map.WATER)

        print("Flooded villages = {0}".format(flooded_villages))

        return len(flooded_villages)
