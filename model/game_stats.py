
from .StatEngine import CoreStat, DerivedStat


class CurrentYear(DerivedStat):

    SEASONS_PER_YEAR = 3

    def __init__(self):

        super(CurrentYear,self).__init__("Current Year","GAME")

        self.add_dependency("Season Count", optional=False)


    def calculate(self):

        season_count = self.get_dependency_value("Season Count")

        return ((season_count - 1) // CurrentYear.SEASONS_PER_YEAR) + 1


class CurrentSeason(DerivedStat):

    def __init__(self):

        super(CurrentSeason, self).__init__("Current Season", "GAME")

        self.add_dependency("Season Count", optional=False)

    def calculate(self):

        season_count = self.get_dependency_value("Season Count")
        current_season = (season_count % CurrentYear.SEASONS_PER_YEAR)
        if current_season == 0:
            current_season = CurrentYear.SEASONS_PER_YEAR

        return current_season
