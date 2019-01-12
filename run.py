import controller
import logging

def main():

    logging.basicConfig(level = logging.ERROR)

    c = controller.GameCLI()
    c.run()
    return

if __name__ == "__main__":
    main()
    exit(0)