#Xiang Fan
#Gefei Tian
#
#


import random
import copy
import random
import math
import time

class Player():
    def __init__(self, name,symbol):
        self.name = name
        self.symbol = symbol

    def place_coin(self, game):
        correct = 0
        while correct == 0:
            try:
                pos = input('Choose the position of your piece by entering the number on board: ')
                if pos in game.remaining:
                    correct = 1
                else:
                    print "Error: invalid input. \n"
            except:
                print "Error: invalid input. \n"

        game.remaining.remove(pos)
        self.replace(game, game.position_dict[pos])
        
    def replace(self, game, position):
        game.board[position[0]][position[1]] = self.symbol

class AI(Player):
    def __init__(self, name, symbol):
        Player.__init__(self, name, symbol)
        self.VALUE = {'FIVE' : 999999999, 'FOUR' : 9999999, 'ATTACK' : 10, 'DEFEND' : 10, 'NEUTRAL' : 5, 'MINE' : 5, 'OTHER' : 5}
    
        if self.symbol == 'X':
            self.opponent = 'O'
        else:
            self.opponent = 'X'

    def moves(self, game):
        #intilise 
        self.position_type = {}
        self.position_points = {}
        self.points_tally = {}
        for i in range(1,game.length**2+1):
            self.position_type[i] = [0,0]
            self.position_points[i] = [0,0,0] 
            self.points_tally[i] = 0

        self.count_points(game)
        for position in range(1,game.length**2+1):
           
            self.points_tally[position] += self.position_points[position][0]*((self.position_type[position][0]**2))\
                                            + self.position_points[position][1]*((self.position_type[position][1]**2))
        
        highest = {'points' : 0, 'position' : 0}

        for position in self.points_tally:
            if self.points_tally[position] > highest['points']:
                highest['points'] = self.points_tally[position]
                highest['position'] = position

        if highest['position'] == 0:
            highest['position'] = game.remaining[0]


        self.replace(game, game.position_dict[highest['position']])
        game.remaining.remove(highest['position'])
            

    def count_points(self, game):
        if self.symbol == 'O':
            index = 1
        else:
            index = 0
        #counts the points in each row, column and diagonal
        checklist = []
        
        for i in range(1, game.length+1):
            checklist.append(game.row_position(i))
            checklist.append(game.col_position(i))
        checklist.append(game.dirction(0))
        checklist.append(game.dirction(1))

        for major_row in checklist:
            for row in major_row:
                row_tally = game.number_in_row(row)
                    
                for position in row:
                    if position in game.remaining:
                        
                        #conditions for different situations
                        if row_tally[self.symbol] == 5-1 and row_tally[self.opponent] == 0 and game.learning == 0:
                            self.points_tally[position] += self.VALUE['FIVE']
                        elif row_tally[self.symbol] == 5-2 and row_tally[self.opponent] == 0 and game.learning == 0:
                            self.points_tally[position] += self.VALUE['FOUR']                        
                        elif row_tally[self.opponent] == 5-1 and row_tally[self.symbol] == 0 and game.learning == 0:
                            self.points_tally[position] += self.VALUE['FIVE']
                        elif row_tally[self.opponent] == 5-2 and row_tally[self.symbol] == 0 and game.learning == 0:
                            self.points_tally[position] += self.VALUE['FOUR']
                        elif row_tally[self.symbol] + row_tally[self.opponent] == 0:
                            self.points_tally[position] += self.VALUE['NEUTRAL']
                        elif row_tally[self.opponent] == 0:
                            self.position_type[position][int(math.fabs(index-1))] += 1
                            self.position_points[position][int(math.fabs(index-1))] += self.VALUE['ATTACK'] + row_tally[self.symbol]*self.VALUE['MINE']
                        elif row_tally[self.symbol] == 0:
                            self.position_type[position][index] += 1
                            self.position_points[position][index] += self.VALUE['DEFEND'] + row_tally[self.opponent]*self.VALUE['OTHER']

    def switch(self, other):
        self.VALUE['FIVE'] = copy.copy(other.VALUE['FIVE'])
        self.VALUE['FOUR'] = copy.copy(other.VALUE['FOUR'])
        self.VALUE['NEUTRAL'] = copy.copy(other.VALUE['NEUTRAL'])
        self.VALUE['ATTACK'] = copy.copy(other.VALUE['ATTACK'])
        self.VALUE['DEFEND'] = copy.copy(other.VALUE['DEFEND'])
        self.VALUE['MINE'] = copy.copy(other.VALUE['MINE'])
        self.VALUE['OTHER'] = copy.copy(other.VALUE['OTHER'])
        
class Game(object):
    def __init__(self):
        self.player1, self.player2 = self.setup()
        self.mode = 1
        self.length = 15
        self.active = 0
        self.speed = 0
        self.learning = 0
    
    def setup(self):
        
        print "This is our Gomoku porject for CS5150 by Xiang Fan and Gefei Tian, this game will play against itself and start learning in 10 seconds..."
        print "Please make sure to have the terminal window big enough to see the whole game"
        time.sleep(15)
        player1, player2 = Player('you', 'X'), AI('the Computer', 'O')
        
        return player1, player2

  
    def play_game(self, player1, player2):
        self.board = [[x*self.length+(y+1) for y in range(self.length)] for x in range(self.length)]
        self.remaining = [i for i in range(1,self.length**2+1)]    
        self.position_dict = {}
        
        for i in range(1,self.length**2+1):
            self.position_dict[i] = ((i-1)/self.length,(i-1)%self.length)

        self.draw_board()
 
        for i in range(self.length**2):
            #determine turns
            if self.active%2 == 0:
                if self.mode == 1:
                    print "It is your turn." + " (X)"
                else:
                    print "It is Player 1's turn. (X)"
                player1.turn(self)
            else:
                print "It is " + player2.name + "'s turn. " + "(O)"
                player2.turn(self)

            self.active += 1

            self.draw_board()
                
            #check for winners
            win_symbol = self.check_winners()
            if win_symbol != None:
                if win_symbol == 'X':
                    winner = player1.name + '(X)'                  
                else:
                    winner = player2.name + '(O)'
                if self.mode == 1 and winner == player2.name + '(O)':
                    print '\n' + '**'*20 + '\n You lost, better luck next time!\n' + '**'*20 + '\n'
                    break
                else:
                    print '\n' + '**'*20+ '\n Congratulations, you won! ' + winner.capitalize() +\
                    '\n' + '**'*20 + '\n'
                    break

        #check tie
        if win_symbol == None:
            print '\n' + '=='*20 + '\n' + 'The game is a draw.\n' + '=='*20 + '\n'


    def check_winners(self):
        checklist = []
        for i in range(1, self.length+1):
            for element in self.row_position(i):
                checklist.append(self.number_in_row(element))
            for element in self.col_position(i):
                checklist.append(self.number_in_row(element))
        for element in self.dirction(0):
            checklist.append(self.number_in_row(element))
        for element in self.dirction(1):
            checklist.append(self.number_in_row(element))
    
        for check in checklist:
            if check['O'] == 5:
                return 'O'
            if check['X'] == 5:
                return 'X'


    def number_in_row(self, row):
        row_tally = {'O': 0, 'X': 0, 0: 0}
        for position in row:
            val = self.board[self.position_dict[position][0]][self.position_dict[position][1]]
            if type(val) == int:
                val = 0
            row_tally[val] += 1
        return row_tally

    def row_position(self, row_number):
        result = []
        for i in range(self.length-5+1):
            result.append(range((row_number-1)*self.length+1+i,(row_number-1)*self.length+1+i+5))
        return result

    def col_position(self, col_number):
        result = []
        for i in range(self.length-5+1):
            result.append(range(col_number+i*(self.length), self.length*(5+i)+1, self.length))
        return result

    def dirction(self, dia_number):
        x_pos = set([])
        y_pos = set([])
        result = []
        if dia_number == 0:
            for row_number in range(1, self.length-5+2):
                x_pos = x_pos.union(set(range((row_number-1)
                  *self.length+1,(row_number-1)
                  *self.length+self.length+1)))
                y_pos = y_pos.union(set(range(row_number, self.length**2+1, self.length)))
            for start_pos in x_pos.intersection(y_pos):
                result.append(range(start_pos,start_pos+(5-1)
                  *(self.length+1)+1,self.length+1))
        if dia_number == 1:
            for row_number in range(1, self.length-5+2):
                x_pos = x_pos.union(set(range((row_number-1)
                  *self.length+1,(row_number-1)*self.length+self.length+1)))
            for row_number in range(self.length, 5-1, -1):
                y_pos = y_pos.union(set(range(row_number, self.length**2+1, self.length)))
            for start_pos in x_pos.intersection(y_pos):
                result.append(range(start_pos, start_pos + 
                  (5-1)*(self.length-1) + 1,self.length-1))
        return result

    def draw_board(self):
        for row in range(1+self.length*2):
            if row%2 == 0:
                print '-',
                for i in range(self.length):
                    print '===',
                    print '-',
                print
            else:
                for column in range(1+self.length*2):
                    if column%2 ==0:
                        print '|',
                    else:
                        if self.board[row/2][column/2] == 225:
                            print "225 |",
                            break
                        elif len(str(self.board[row/2][column/2])) == 1:
                            print str(self.board[row/2][column/2]) + "  ",
                        elif len(str(self.board[row/2][column/2])) == 2:
                            print str(self.board[row/2][column/2]) + " ",
                        else:
                            print self.board[row/2][column/2],
                print
        print

    def adjust(self, old, new, value, i):
        old_v = 0
        new_v = 0
        
        new.VALUE[value] += i
        self.self_play(old, new)
        if self.self_play(old, new): old_v = old_v + 1
        else: new_v += 1
        
        if new.VALUE[value] - i > 0:
            new.VALUE[value] -= i
            self.self_play(old, new)
            if self.self_play(old, new): old_v = old_v + 1
            else: new_v += 1
        

    #begins the learning routine
    def learn(self, player, speed):
        old = 0
        new = 0
        old_ai = AI('Old AI', 'X')
        new_ai = AI('New AI', 'O')
        self.speed = speed
        counter = 0
        self.learning = 1
        start_time = time.clock()
        
        for i in range(10,0,-1):
            self.adjust(old_ai, new_ai, 'NEUTRAL', i)
            self.adjust(old_ai, new_ai, 'ATTACK', i)
            self.adjust(old_ai, new_ai, 'DEFEND', i)
            self.adjust(old_ai, new_ai, 'MINE', i)
            self.adjust(old_ai, new_ai, 'OTHER', i)
        

        player.switch(old_ai)
        self.learning = 0
                                                                 
    def self_play(self, old_ai, new_ai):

        if self.self_game_play(old_ai, new_ai, 1) == 'O':
            old_ai.switch(new_ai)
       

        if self.speed != 3:
            time.sleep(0.3)
            
        new_ai.switch(old_ai)
        return (self.self_game_play(old_ai, new_ai, 1) == 'O')

        
        
    #the mock counterpart of play_game(), plays a mock game
    def self_game_play(self, player1, player2, active):
        self.board = [[x*self.length+(y+1) for y in range(self.length)] for x in range(self.length)]
        self.remaining = [i for i in range(1,self.length**2+1)]    
        self.position_dict = {}
        
        #build the position dictionary
        for i in range(1,self.length**2+1):
            self.position_dict[i] = ((i-1)/self.length,(i-1)%self.length)
        for i in range(self.length**2):
            #determine whose turn it is
            if active%2 == 0:
                if self.speed == 1:
                    print "It old AI's turn " + " (X)"
                    self.draw_board()
                    time.sleep(0.3)
                player1.moves(self)
            else:
                if self.speed == 1:
                    print "It is new AI's turn. " + "(O)"
                    self.draw_board()
                    time.sleep(0.3)
                player2.moves(self)

            active += 1
            
        

            #if self.speed == 1: self.draw_board()
                
            #check for winners
            win_symbol = self.check_winners()
            if win_symbol != None:
                if win_symbol == 'X':
                    winner = player1.name + '(X)'
                else:
                    winner = player2.name + '(O)'
                if self.speed != 3: print "\n%s\n%s Won!\n%s\n" % ('**'*40, winner, '**'*40)
                if self.speed == 2: self.draw_board()
                return win_symbol
        

        #condition if the game is a tie
        if win_symbol == None:
            if self.speed != 3: print '\n' + '**'*40 + '\n' + 'The game is a draw.\n' + '**'*40 + '\n'
        if self.speed == 2: self.draw_board()
        return win_symbol
        
    


def main():
    game = Game()
    player1 = game.player1
    player2 = game.player2

    #AI Learning
    if game.mode  == 1:
        speed = 2
        game.learn(player2,speed)
        
    #randomly determine the game order
    print "\nThe order of the game is randomly decided: "
    if random.randint(0,1) == 0:
        game.active = 0 #sets active player
        print player1.name.capitalize() + ' (X) play first, ' +\
              player2.name + ' (O) play second.'
    else:
        game.active = 1
        print player2.name.capitalize() + ' (O) play first, ' +\
              player1.name + ' (X) play second.'
        
    raw_input("\n%s\nLearning has completed, please hit enter to start the game.\n%s\n" %('*'*40, '*'*40))
            
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


