import logging

class Game():

    STATE_LOADED = "loaded"
    STATE_INITIALISED = "initialised"
    START_RUNNING = "running"

    def __init__(self, name : str):
        self.name = name
        self._state = Game.STATE_LOADED

    def initialise(self, name : str):
        self._state = Game.STATE_INITIALISED
        self.kingdom_name = name

    @property
    def state(self):
        return self._state

    def __str__(self):

        if self.state == Game.STATE_INITIALISED:
            str = "{0} ({1}): {2}".format(self.name, self.state, self.kingdom_name)
        else:
            str = "{0} ({1})".format(self.name, self.state)

        return str




