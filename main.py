from gui import Main
from map import Map


def main(width, height):
    game = Main(Map(width, height))
    game.run()

if __name__ == '__main__':
    main(150, 80)
