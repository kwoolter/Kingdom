from .StatEngine import *
import random

class KingdomStats(StatEngine):

    # Kindgom level inputs
    INPUT_SEASON_COUNT = "Season Count"
    INPUT_CURRENT_POPULATION = "Current Population"
    INPUT_CURRENT_FOOD = "Current Food"
    INPUT_VILLAGE_COUNT = "Village Count"

    # Season level inputs
    INPUT_PEOPLE_DYKE = "People Dyke"
    INPUT_PEOPLE_FIELDS = "People Fields"
    INPUT_PEOPLE_VILLAGES = "People Defend Villages"
    INPUT_RICE_TO_PLANT = "Rice to Plant"
    INPUT_RICE_ANNUAL_TITHES = "Rice annual tithes"

    INPUTS = (INPUT_CURRENT_FOOD, INPUT_CURRENT_POPULATION, INPUT_PEOPLE_DYKE, INPUT_PEOPLE_FIELDS,
              INPUT_PEOPLE_VILLAGES, INPUT_RICE_TO_PLANT, INPUT_SEASON_COUNT, INPUT_VILLAGE_COUNT,
              INPUT_RICE_ANNUAL_TITHES)

    def __init__(self):

        super(KingdomStats, self).__init__("Kingdom")

    def initialise(self):

        # Add the core input stats
        for core_stat_name in KingdomStats.INPUTS:
            self.add_stat(CoreStat(core_stat_name, "INPUTS", 0))

        # Add derived game stats
        self.add_stat(CurrentYear())
        self.add_stat(CurrentSeason())
        self.add_stat(PeoplePerVillage())
        self.add_stat(FoodPerVillage())
        self.add_stat(FoodPerPerson())

        # Add events
        self.add_stat(LocustFoodAttack())
        self.add_stat(HarvestDrought())
        self.add_stat(DiseaseAttack())
        self.add_stat(FreakWinter())
        self.add_stat(RiceAnnualTithes())

        # Add totalers
        self.add_stat(TotalPeopleChanges())
        self.add_stat(TotalFoodChanges())


class PeoplePerVillage(DerivedStat):

    NAME = "People per village"

    def __init__(self):

        super(PeoplePerVillage,self).__init__(PeoplePerVillage.NAME,"GAME")

        self.add_dependency(KingdomStats.INPUT_VILLAGE_COUNT)
        self.add_dependency(KingdomStats.INPUT_CURRENT_POPULATION)

    def calculate(self):

        village_count = self.get_dependency_value(KingdomStats.INPUT_VILLAGE_COUNT)
        current_population = self.get_dependency_value(KingdomStats.INPUT_CURRENT_POPULATION)

        return int(current_population / village_count)

class FoodPerVillage(DerivedStat):

    NAME = "Food per village"

    def __init__(self):

        super(FoodPerVillage,self).__init__(FoodPerVillage.NAME,"GAME")

        self.add_dependency(KingdomStats.INPUT_VILLAGE_COUNT)
        self.add_dependency(KingdomStats.INPUT_CURRENT_FOOD)

    def calculate(self):

        village_count = self.get_dependency_value(KingdomStats.INPUT_VILLAGE_COUNT)
        current_food = self.get_dependency_value(KingdomStats.INPUT_CURRENT_FOOD)

        return int(current_food / village_count)

class FoodPerPerson(DerivedStat):

    NAME = "Food per person"

    def __init__(self):

        super(FoodPerPerson,self).__init__(FoodPerPerson.NAME,"GAME")

        self.add_dependency(KingdomStats.INPUT_CURRENT_POPULATION)
        self.add_dependency(KingdomStats.INPUT_CURRENT_FOOD)

    def calculate(self):

        current_population = self.get_dependency_value(KingdomStats.INPUT_CURRENT_POPULATION)
        current_food = self.get_dependency_value(KingdomStats.INPUT_CURRENT_FOOD)

        return int(current_food / current_population)


class LocustFoodAttack(DerivedStat):

    NAME = "Locust Attack Food"
    DESCRIPTION = "A plague of locusts swarms across the Kingdom."

    FOOD_LEVEL = 2000
    SEASON_LEVEL = 4

    def __init__(self):

        super(LocustFoodAttack, self).__init__(LocustFoodAttack.NAME,
                                               "OUTPUT",
                                               description=LocustFoodAttack.DESCRIPTION)

        self.add_dependency(FoodPerVillage.NAME)
        self.add_dependency(CurrentSeason.NAME)
        self.add_dependency(KingdomStats.INPUT_VILLAGE_COUNT)
        self.add_dependency(KingdomStats.INPUT_SEASON_COUNT)

    def calculate(self):

        food_per_village = self.get_dependency_value(FoodPerVillage.NAME)
        current_season = self.get_dependency_value(CurrentSeason.NAME)
        village_count = self.get_dependency_value(KingdomStats.INPUT_VILLAGE_COUNT)
        season_count = self.get_dependency_value(KingdomStats.INPUT_SEASON_COUNT)

        food_lost = 0

        # Only calculate if you are so many seasons into the game and have an over capacity issue
        if current_season != CurrentSeason.WINTER and \
                season_count >= LocustFoodAttack.SEASON_LEVEL and \
                food_per_village > LocustFoodAttack.FOOD_LEVEL:

            over_capacity = LocustFoodAttack.FOOD_LEVEL - food_per_village
            food_lost = over_capacity * random.randint(0, village_count) / village_count

            if current_season == CurrentSeason.WINTER:
                food_lost = 0
            elif current_season == CurrentSeason.GROWING:
                food_lost *= random.uniform(0, 2) / 2
            elif current_season == CurrentSeason.HARVESTING:
                food_lost *= random.uniform(0, 3) / 3

        return int(food_lost)


class DiseaseAttack(DerivedStat):

    NAME = "Disease Attack"
    DESCRIPTION = "Overcrowding in the villages spreads a fatal disease!"

    PEOPLE_LEVEL = 150
    SEASON_LEVEL = 4

    def __init__(self):

        super(DiseaseAttack, self).__init__(DiseaseAttack.NAME,
                                            "OUTPUT",
                                            description = DiseaseAttack.DESCRIPTION)

        self.add_dependency(PeoplePerVillage.NAME)
        self.add_dependency(CurrentSeason.NAME)
        self.add_dependency(KingdomStats.INPUT_VILLAGE_COUNT)
        self.add_dependency(KingdomStats.INPUT_SEASON_COUNT)

    def calculate(self):

        people_per_village = self.get_dependency_value(PeoplePerVillage.NAME)
        current_season = self.get_dependency_value(CurrentSeason.NAME)
        village_count = self.get_dependency_value(KingdomStats.INPUT_VILLAGE_COUNT)
        season_count = self.get_dependency_value(KingdomStats.INPUT_SEASON_COUNT)

        people_lost = 0

        # Only calculate if you are so many seasons into the game and have an over capacity issue
        if season_count >= DiseaseAttack.SEASON_LEVEL and \
                people_per_village > DiseaseAttack.PEOPLE_LEVEL:

            over_capacity = DiseaseAttack.PEOPLE_LEVEL - people_per_village
            people_lost = over_capacity * random.randint(0, village_count) / village_count

            if current_season == CurrentSeason.WINTER:
                people_lost *= random.uniform(0, 1)
            elif current_season == CurrentSeason.GROWING:
                people_lost *= random.uniform(0, 2) / 2
            elif current_season == CurrentSeason.HARVESTING:
                people_lost *= random.uniform(0, 3) / 3

        return int(people_lost)


class FreakWinter(DerivedStat):

    NAME = "Freak Winter"
    DESCRIPTION = "A long and harsh winter descends on the Kingdom."

    # How often does this event occur in years?
    YEAR_FREQUENCY = 1

    # When does the event kick in during the game?
    SEASON_LEVEL = 0

    def __init__(self):

        super(FreakWinter, self).__init__(FreakWinter.NAME, "OUTPUT", description=FreakWinter.DESCRIPTION)

        self.add_dependency(CurrentSeason.NAME)
        self.add_dependency(CurrentYear.NAME)
        self.add_dependency(KingdomStats.INPUT_CURRENT_POPULATION)

    def calculate(self):

        current_season = self.get_dependency_value(CurrentSeason.NAME)
        current_year = self.get_dependency_value(CurrentYear.NAME)
        current_population = self.get_dependency_value(KingdomStats.INPUT_CURRENT_POPULATION)

        people_lost = 0

        # Only calculate if it is winter and the event occurs this year...
        if current_season == CurrentSeason.WINTER and current_year % FreakWinter.YEAR_FREQUENCY == 0:
            people_lost = -1 * current_population * random.uniform(0, 2) / 10

        return int(people_lost)

class HarvestDrought(DerivedStat):

    NAME = "Harvest Drought"
    DESCRIPTION = "Barely any rain falls during the Harvest season."

    # How often does this event occur in years?
    YEAR_FREQUENCY = 1

    # When does the event kick in during the game?
    SEASON_LEVEL = 0

    def __init__(self):

        super(HarvestDrought, self).__init__(HarvestDrought.NAME,
                                             "OUTPUT",
                                             description=HarvestDrought.DESCRIPTION)

        self.add_dependency(CurrentSeason.NAME)
        self.add_dependency(CurrentYear.NAME)
        self.add_dependency(KingdomStats.INPUT_RICE_TO_PLANT)
        self.add_dependency(KingdomStats.INPUT_CURRENT_FOOD)

    def calculate(self):

        current_season = self.get_dependency_value(CurrentSeason.NAME)
        current_year = self.get_dependency_value(CurrentYear.NAME)
        current_food = self.get_dependency_value(KingdomStats.INPUT_CURRENT_FOOD)
        rice_planted = self.get_dependency_value(KingdomStats.INPUT_RICE_TO_PLANT)

        rice_lost = 0

        # Only calculate if it is harvest time and the event occurs this year...
        if current_season == CurrentSeason.HARVESTING and current_year % HarvestDrought.YEAR_FREQUENCY == 0:
            rice_lost = -1 * rice_planted * random.uniform(0, 2) / 10

        return int(rice_lost)


class RiceAnnualTithes(DerivedStat):

    NAME = "Annual Rice Tithes"
    DESCRIPTION = "The villagers pay their annual tithes to their Gods."

    # When does the event kick in during the game?
    SEASON_LEVEL = 0
    FOOD_PER_PERSON_THRESHOLD = 1

    def __init__(self):

        super(RiceAnnualTithes, self).__init__(RiceAnnualTithes.NAME,
                                             "OUTPUT",
                                             description=RiceAnnualTithes.DESCRIPTION)

        self.add_dependency(CurrentSeason.NAME)
        self.add_dependency(KingdomStats.INPUT_RICE_ANNUAL_TITHES)
        self.add_dependency(KingdomStats.INPUT_CURRENT_POPULATION)
        self.add_dependency(FoodPerPerson.NAME)

    def calculate(self):

        current_season = self.get_dependency_value(CurrentSeason.NAME)
        food_per_person = self.get_dependency_value(FoodPerPerson.NAME)
        current_population = self.get_dependency_value(KingdomStats.INPUT_CURRENT_POPULATION)
        tithe_rate = self.get_dependency_value(KingdomStats.INPUT_RICE_ANNUAL_TITHES)

        rice_lost = 0

        # Only calculate if it is harvest time and enough food to take the tithe ...
        if current_season == CurrentSeason.HARVESTING and \
                food_per_person >= RiceAnnualTithes.FOOD_PER_PERSON_THRESHOLD:

            rice_lost = -1 * tithe_rate * current_population

        return int(rice_lost)

class TotalPeopleChanges(DerivedStat):

    NAME = "Total People Changes"

    # Season outputs - people
    OUTPUT_PEOPLE = (DiseaseAttack.NAME, FreakWinter.NAME)

    def __init__(self):

        super(TotalPeopleChanges,self).__init__(TotalPeopleChanges.NAME,"OUTPUT")

        for output_name in TotalPeopleChanges.OUTPUT_PEOPLE:
            self.add_dependency(output_name, optional=True, default_value=0)

    def calculate(self):

        people_change = 0

        for output_name in TotalPeopleChanges.OUTPUT_PEOPLE:
            people_change += self.get_dependency_value(output_name)

        return int(people_change)


class TotalFoodChanges(DerivedStat):

    NAME = "Total Food Changes"

    # Season outputs - food
    OUTPUT_FOOD = (LocustFoodAttack.NAME, HarvestDrought.NAME, RiceAnnualTithes.NAME)

    def __init__(self):

        super(TotalFoodChanges, self).__init__(TotalFoodChanges.NAME, "OUTPUT")

        for output_name in TotalFoodChanges.OUTPUT_FOOD:
            self.add_dependency(output_name, optional=True, default_value=0)

    def calculate(self):

        food_change = 0

        for output_name in TotalFoodChanges.OUTPUT_FOOD:
            food_change += self.get_dependency_value(output_name)

        return int(food_change)


class CurrentYear(DerivedStat):

    NAME = "Current Year"

    SEASONS_PER_YEAR = 3

    def __init__(self):

        super(CurrentYear,self).__init__(CurrentYear.NAME,"GAME")

        self.add_dependency(KingdomStats.INPUT_SEASON_COUNT)

    def calculate(self):

        season_count = self.get_dependency_value(KingdomStats.INPUT_SEASON_COUNT)

        return ((season_count - 1) // CurrentYear.SEASONS_PER_YEAR) + 1


class CurrentSeason(DerivedStat):

    NAME = "Current Season"

    WINTER = 1
    GROWING = 2
    HARVESTING = 3

    def __init__(self):

        super(CurrentSeason, self).__init__(CurrentSeason.NAME, "GAME")

        self.add_dependency(KingdomStats.INPUT_SEASON_COUNT)

    def calculate(self):

        season_count = self.get_dependency_value(KingdomStats.INPUT_SEASON_COUNT)
        current_season = (season_count % CurrentYear.SEASONS_PER_YEAR)
        if current_season == 0:
            current_season = CurrentYear.SEASONS_PER_YEAR

        return current_season
