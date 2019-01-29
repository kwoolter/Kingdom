import cmd
import logging
import os

import model
import view


class GameCLI(cmd.Cmd):
    intro = "Welcome to The Kingdom - Remastered.\nType 'start' to get going!\nType 'help' for a list of commands."
    prompt = "What next?"

    def __init__(self):

        super(GameCLI, self).__init__()

        self.model = model.Game("Kingdom")
        self.view = view.TextView(self.model)

    def run(self):
        self.cmdloop()

    def emptyline(self):
        pass

    def do_print(self, args):
        """Print the current census report"""
        try:

            if self.model.state != model.Game.STATE_LOADED:
                self.view.print_census()
                print(self.model)
            else:
                print("\nGame not started!")
                print(str(self.model))

        except Exception as err:
            print(str(err))

    def do_hst(self, args):
        """ Print the high score tables"""

        try:

            self.view.print_high_score_table()

        except Exception as err:
            print(str(err))

    def do_quit(self, arg):
        """Quit the game"""
        try:

            if confirm("Are you sure you want to quit?") is True:
                print("\nThanks for playing.")
                print(str(self.model))
                is_high_score = self.model.do_game_over()
                if is_high_score is True:
                    print("\nYou got into the high score table!")
                print("\nBye bye.")
                #exit(0)

        except Exception as err:
            print(str(err))

    def do_start(self, args):
        """Start the Game"""
        try:

            if self.model.state == model.Game.STATE_INITIALISED:
                if confirm("Are you sure you want to stop the current game") is False:
                    return
                else:
                    self.model.do_game_over()

            player_name = input("What is your name?")
            kingdom_name = "Yellow River Kingdom"
            mode = pick("Game Mode", model.Game.GAME_MODES)
            self.model.initialise(kingdom_name, player_name, mode)
            self.view.initialise()

            event = self.model.get_next_event()
            if event is not None:
                print("\nGame event(s)...")
            while event is not None:
                print(" * " + str(event))
                event = self.model.get_next_event()

            self.view.print_high_score_table()

            print("\nType 'play' to get started or 'instructions' got get some help.\n")

        except Exception as err:
            print(str(err))

    def do_instructions(self, args):
        """Print the game instructions"""

        try:
            self.view.print_instructions()
        except Exception as err:
            print(str(err))

    def do_play(self, args):
        """Play the next round of the game"""

        os.system('cls')

        try:

            if self.model.state == model.Game.STATE_GAME_OVER:
                raise Exception("Can't play as Game is Over!  You need to start again.")

            # Print the current state
            self.view.print_census()

            # Get the next round of decisions
            print("\nHow many people should:")

            # Get how many people should defend the dyke
            loop = True
            while loop is True:
                dyke = is_numeric(input("Defend the dyke?"))
                if dyke is None:
                    print("Not a valid number.  Please re-enter.")
                else:
                    dyke = int(dyke)

                    if dyke <= self.model.kingdom.population:
                        loop = False
                    else:
                        print("You don't have enough people!")

            # Get how many people should work in the fields if you have not assigned them all to teh dyke!
            loop = (self.model.kingdom.population - dyke) > 0
            if loop is False:
                fields = 0
                print("Work in the fields? 0")

            while loop is True:
                fields = is_numeric(input("Work in the fields?"))
                if fields is None:
                    print("Not a valid number.  Please re-enter.")
                else:
                    fields = int(fields)
                    if (self.model.kingdom.population - dyke - fields) >= 0:
                        loop = False
                    else:
                        print("You don't have enough people!")

            # Auto calculate number of defenders
            defend = int(self.model.kingdom.population - dyke - fields)
            print("Defend the villages? {0}".format(defend))

            # Extra input for the growing season
            if self.model.kingdom.current_season.name == model.Season.GROWING:
                loop = True
                while loop is True:
                    rice_planted = is_numeric(input("Baskets of rice to plant?"))
                    if rice_planted is None:
                        print("Not a valid number.  Please re-enter.")
                    else:
                        rice_planted = int(rice_planted)
                        if rice_planted <= self.model.kingdom.total_food:
                            loop = False
                        else:
                            print("You don't have that much food to plant!")
            else:
                rice_planted = 0

            # Run the model with the inputted resources
            self.model.play(dyke, fields, defend, rice_planted)

            # Print the season results
            self.view.print_season()

            # Print any events that got raised
            event = self.model.get_next_event()
            if event is not None:
                print("Game event(s)...")

            ritual = False

            while event is not None:

                print(" * " + str(event))

                # See if it is time for a ritual...?
                if self.model.state != model.Game.STATE_GAME_OVER and event.name == model.Kingdom.EVENT_RITUAL:
                    ritual = True

                event = self.model.get_next_event()

            # Print the map
            self.view.print_map()

            # If it is time for a ritual then run the ritual
            if ritual is True:
                self.view.print_ritual()
                self.do_quit("")

            print("")

        except Exception as err:
            print(str(err))

    def do_stats(self, args):

        self.model.kingdom.update_stats()

        self.model._stats.print()


# Function to ask the user a simple Yes/No confirmation and return a boolean
def confirm(question: str):
    choices = ["Yes", "No"]

    while True:
        print(question)
        for i in range(0, len(choices)):
            print("%i. %s" % (i + 1, choices[i]))
        choice = input("Choice?")
        if is_numeric(choice) and int(choice) > 0 and int(choice) <= (len(choices) + 1):
            break
        else:
            print("Invalid choice.  Try again!")

    return (int(choice) == 1)


def pick(object_type: str, objects: list, auto_pick: bool = False):
    '''pick() -  Function to present a menu to pick an object from a list of objects
    auto_pick means if the list has only one item then automatically pick that item'''

    selected_object = None
    choices = len(objects)
    vowels = "AEIOU"
    if object_type[0].upper() in vowels:
        a_or_an = "an"
    else:
        a_or_an = "a"

    # If the list of objects is no good the raise an exception
    if objects is None or choices == 0:
        raise (Exception("No %s to pick from." % object_type))

    # If you selected auto pick and there is only one object in the list then pick it
    if auto_pick is True and choices == 1:
        selected_object = objects[0]

    # While an object has not yet been picked...
    while selected_object == None:

        # Print the menu of available objects to select
        print("Select %s %s:-" % (a_or_an, object_type))

        for i in range(0, choices):
            print("\t%i) %s" % (i + 1, str(objects[i])))

        # Along with an extra option to cancel selection
        print("\t%i) Cancel" % (choices + 1))

        # Get the user's selection and validate it
        choice = input("%s?" % object_type)
        if is_numeric(choice) is not None:
            choice = int(choice)

            if 0 < choice <= choices:
                selected_object = objects[choice - 1]
                logging.info("pick(): You chose %s %s." % (object_type, str(selected_object)))
            elif choice == (choices + 1):
                raise (Exception("You cancelled. No %s selected" % object_type))
            else:
                print("Invalid choice '%i' - try again." % choice)
        else:
            print("You choice '%s' is not a number - try again." % choice)

    return selected_object


def is_numeric(s):
    try:
        x = int(s)
    except:
        try:
            x = float(s)
        except:
            x = None
    return x
