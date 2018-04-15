

from player import Player
from ai import AI
from game import Game
import random

def main():
    game = Game()
    player1 = game.player1
    player2 = game.player2

    #AI Learning
    if game.mode  == 1:
        speed = 3
        game.learn(player2,speed)
        
    #randomly determine the game order
    print "\nThe turn order has been randomly determined: "
    if random.randint(0,1) == 0:
        game.active = 0 #sets active player
        print player1.name.capitalize() + ' (X) will go first, ' +\
              player2.name + ' (O) will go second.'
    else:
        game.active = 1
        print player2.name.capitalize() + ' (O) will go first, ' +\
              player1.name + ' (X) will go second.'
        
    raw_input("\n%s\nGame Ready. Press Enter to begin.\n%s\n" %('/'*50, '/'*50))
            
    #plays the game
    while True:
        game.play_game(player1, player2)
        rematch = input("""Press 1 to rematch or 2 to leave this game: """)
        if rematch != 1:
            print "\nGame Ended"
            break
        print "\n\n\n\n"
    

while True:
    main()
    again = input("Press 1 to restart the program, or 2 to exit: ")
    if again != 1:
        break
    print "\n\n\n\n"


