import cmd
import model
import view

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
        self.view.print()


    def do_start(self, args):
        self.model.initilaise()
        self.view.initialise()
