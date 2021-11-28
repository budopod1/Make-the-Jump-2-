from play import Play
import menu
from threading import Thread


def start():
  game = Play()
  game.menu = menu.go
  game.start()


if __name__ == "__main__":
  # print("\nSorry, but Make the Jump 2! is down for maintenance. It will be up in 11/20\n")
  # input("Press enter to attempt to boot anyway")
  main_thread = Thread(target=start)
  main_thread.start()
  main_thread.join()
  # Testing
