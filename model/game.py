import logging

class Game():

    STATE_LOADED = "loaded"
    STATE_INITIALISED = "initialised"
    START_RUNNING = "running"

    def __init__(self, name : str):
        self.name = name
        self._state = Game.STATE_LOADED

    def initialise(self):
        self._state = Game.STATE_INITIALISED




