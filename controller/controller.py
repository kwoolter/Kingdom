import cmd
import model
import view
import logging

class GameCLI(cmd.Cmd):

    intro = "Welcome to The Kingdom.\nType 'start' to get going!\nType 'help' for a list of commands."
    prompt = "What next?"

    def __init__(self):

        super(GameCLI, self).__init__()

        self.model = model.Game("Kingdom")
        self.view = view.TextView(self.model)

    def run(self):
        self.cmdloop()

    def do_print(self, args):
        """Print the Game View"""
        self.view.print()

    def do_start(self, args):
        """Start the Game"""
        player_name = input("What is your name?")
        kingdom_name = input("What is your kingdom's name?")
        self.model.initialise(kingdom_name, player_name)
        self.view.initialise()

        event = self.model.get_next_event()
        while event is not None:
            print(event)
            event = self.model.get_next_event()


    def do_play(self,args):
        """Play the next round of the game"""

        if self.model.state == model.Game.STATE_GAME_OVER:
            raise Exception("Can't plat as Game is Over!")


        # Print the current state
        self.view.print_census()

        print("\nHow many people should:")
        dyke = int(input("Defend the dyke?"))
        fields = int(input("Work in  the fields?"))

        # Auto calculate number of defenders
        defend = self.model.kingdom.population - dyke - fields
        print("Defend the villages? {0}".format(defend))

        # Extra input for the growing season
        if self.model.kingdom.current_season.name == model.Season.GROWING:
            rice_planted = int(input("Baskets of rice to plant?"))
        else:
            rice_planted = 0

        # Run the model with the inputted resources
        self.model.play(dyke, fields, defend, rice_planted)

        event = self.model.get_next_event()
        while event is not None:
            print(event)
            event = self.model.get_next_event()

        self.view.print_season()




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
