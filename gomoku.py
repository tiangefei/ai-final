
import random
import copy
import random
import math
import time

class Player():
    def __init__(self, name,symbol):
        self.name = name
        self.symbol = symbol

    #function that governs a turn
    def turn(self, game):
        correct = 0
        #ask where the player would like to place their piece
        while correct == 0:
            try:
                pos = input('Please type the position you would like to place your piece: ')
                if pos in game.remaining:
                    correct = 1
                else:
                    print "Error: invalid input, please try again!!!. \n"
            except:
                print "Error: invalid input, please try again, \n"

        game.remaining.remove(pos)
        self.replace(game, game.position_dict[pos])
        
    def replace(self, game, position):
        game.board[position[0]][position[1]] = self.symbol

class AI(Player):
    def __init__(self, name, symbol):
        #Borrows parent co-efficients
        Player.__init__(self, name, symbol)
        #initilise intelligence co-efficients
        self.VALUE = {'FIVE' : 999999999, 'FOUR' : 9999999, 'ATTACK' : 10, 'DEFEND' : 10, 'NEUTRAL' : 5, 'MINE' : 5, 'OTHER' : 5}
    
        if self.symbol == 'X':
            self.opponent = 'O'
        else:
            self.opponent = 'X'

    def turn(self, game):
        #intilise variables
        self.position_type = {}
        self.position_points = {}
        self.points_tally = {}
        for i in range(1,game.length**2+1):
            self.position_type[i] = [0,0]
            self.position_points[i] = [0,0,0] #[attack,defend,neutral]
            self.points_tally[i] = 0
        #thinks about all possible moves, adding points for all squares

        self.count_points(game)
        #decides the best turn and makes it
        for position in range(1,game.length**2+1):
           
            #Compute all other points through the elementwise vector multiplication
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
            checklist.append(game.pos_in_row(i))
            checklist.append(game.pos_in_col(i))
        checklist.append(game.pos_in_dia(0))
        checklist.append(game.pos_in_dia(1))

        for major_row in checklist:
            for row in major_row:
                row_tally = game.count_row(row)
                    
                for position in row:
                    if position in game.remaining:
                        
                        #condition 0.1: Imminent victory
                        if row_tally[self.symbol] == 5-1 and row_tally[self.opponent] == 0 and game.learning == 0:
                            self.points_tally[position] += self.VALUE['FIVE']
                        elif row_tally[self.symbol] == 5-2 and row_tally[self.opponent] == 0 and game.learning == 0:
                            self.points_tally[position] += self.VALUE['FOUR']
                        
                        #condition 0.2: Imminent defeat
                        elif row_tally[self.opponent] == 5-1 and row_tally[self.symbol] == 0 and game.learning == 0:
                            self.points_tally[position] += self.VALUE['FIVE']
                        elif row_tally[self.opponent] == 5-2 and row_tally[self.symbol] == 0 and game.learning == 0:
                            self.points_tally[position] += self.VALUE['FOUR']
                        
                        #condition 2: blank row
                        elif row_tally[self.symbol] + row_tally[self.opponent] == 0:
                            self.points_tally[position] += self.VALUE['NEUTRAL']
                        
                        #condition 1: Attacking row
                        elif row_tally[self.opponent] == 0:
                            self.position_type[position][int(math.fabs(index-1))] += 1
                            self.position_points[position][int(math.fabs(index-1))] += self.VALUE['ATTACK'] + row_tally[self.symbol]*self.VALUE['MINE']
                        
                        #condition 3: Defending row
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
        self.player1, self.player2 = self.startup()
        self.mode = 1
        self.length = 15
        self.active = 0
        self.speed = 0
        self.learning = 0
    
    #function to determine the game settings
    def startup(self):
        
        #Give the players appropriate names
        
        player1, player2 = Player('you', 'X'), AI('the Computer', 'O')
        
        #return variables
        return player1, player2


    #function which executes turns    
    def play_game(self, player1, player2):
        self.board = [[x*self.length+(y+1) for y in range(self.length)] for x in range(self.length)]
        self.remaining = [i for i in range(1,self.length**2+1)]    
        self.position_dict = {}
        
        #build the position dictionary
        for i in range(1,self.length**2+1):
            self.position_dict[i] = ((i-1)/self.length,(i-1)%self.length)

        self.draw_board()
        #loop to execute turns    
        for i in range(self.length**2):
            #determine whose turn it is
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
                    print '\n' + '/'*40 + '\nSorry! You lost!\n' + '/'*40 + '\n'
                    break
                else:
                    print '\n' + '/'*40+ '\n Congratulations! ' + winner.capitalize() +\
                    ' Won!\n' + '/'*40 + '\n'
                    break

        #condition if the game is a tie
        if win_symbol == None:
            print '\n' + '/'*40 + '\n' + 'The game is a draw.\n' + '/'*40 + '\n'


    #function to check if someone has won the game
    def check_winners(self):
        #build the list through which to check
        checklist = []
        for i in range(1, self.length+1):
            for element in self.pos_in_row(i):
                checklist.append(self.count_row(element))
            for element in self.pos_in_col(i):
                checklist.append(self.count_row(element))
        for element in self.pos_in_dia(0):
            checklist.append(self.count_row(element))
        for element in self.pos_in_dia(1):
            checklist.append(self.count_row(element))
    
        for check in checklist:
            if check['O'] == 5:
                return 'O'
            if check['X'] == 5:
                return 'X'


    #tallies the number of each piece in a row
    def count_row(self, row):
        row_tally = {'O': 0, 'X': 0, 0: 0}
        for position in row:
            val = self.board[self.position_dict[position][0]][self.position_dict[position][1]]
            if type(val) == int:
                val = 0
            row_tally[val] += 1
        return row_tally

    #function which returns list of positions in a row
    def pos_in_row(self, row_number):
        result = []
        for i in range(self.length-5+1):
            result.append(range((row_number-1)*self.length+1+i,(row_number-1)*self.length+1+i+5))
        return result

    #function which returns list of positions in a column
    def pos_in_col(self, col_number):
        result = []
        for i in range(self.length-5+1):
            result.append(range(col_number+i*(self.length), self.length*(5+i)+1, self.length))
        return result

    #funciton which returns list of positions in a diagonal (0 for left to right or 1 for right to left)
    def pos_in_dia(self, dia_number):
        x_pos = set([])
        y_pos = set([])
        result = []
        if dia_number == 0:
            for row_number in range(1, self.length-5+2):
                x_pos = x_pos.union(set(range((row_number-1)*self.length+1,(row_number-1)*self.length+self.length+1)))
                y_pos = y_pos.union(set(range(row_number, self.length**2+1, self.length)))
            for start_pos in x_pos.intersection(y_pos):
                result.append(range(start_pos,start_pos+(5-1)*(self.length+1)+1,self.length+1))
        if dia_number == 1:
            for row_number in range(1, self.length-5+2):
                x_pos = x_pos.union(set(range((row_number-1)*self.length+1,(row_number-1)*self.length+self.length+1)))
            for row_number in range(self.length, 5-1, -1):
                y_pos = y_pos.union(set(range(row_number, self.length**2+1, self.length)))
            for start_pos in x_pos.intersection(y_pos):
                result.append(range(start_pos, start_pos + (5-1)*(self.length-1) + 1,self.length-1))
        return result

    
    #function to draw the game board
    def draw_board(self):
        for row in range(1+self.length*2):
            if row%2 == 0:
                print '-',
                for i in range(self.length):
                    print '---',
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
        self.mock_round(old, new)
        if self.mock_round(old, new): old_v = old_v + 1
        else: new_v += 1
        
        if new.VALUE[value] - i > 0:
            new.VALUE[value] -= i
            self.mock_round(old, new)
            if self.mock_round(old, new): old_v = old_v + 1
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
        print "new: " + str(new)
        print "old: " + str(old)
#        print """\n%s\n%s\n%s\nFinished learning! %d games in %d seconds.
#Final intelligence scores:\n (co1: %d co2: %d, co3: %d, co4: %d, co5: %d)\n%s\n%s\n%s\n""" % ('/'*40,'/'*40,'/'*40, counter,\
#                                                                 time.clock() - start_time,\
#                                                                 player.co1, player.co2, player.co3, player.co4, player.co5,\
#                                                                         '/'*40,'/'*40,'/'*40)
                                                                 
    #controller of a mock game
    def mock_round(self, old_ai, new_ai):

#        if self.speed != 3:
#            print new_ai.co1, new_ai.co2, new_ai.co3, new_ai.co4, new_ai.co5, 'NEW AI Intelligence'
#            print old_ai.co1, old_ai.co2, old_ai.co3, old_ai.co4, old_ai.co5, 'OLD AI Intelligence'
        if self.play_mock_game(old_ai, new_ai, 1) == 'O':
            old_ai.switch(new_ai)
       

        if self.speed != 3:
#            print "\n%s\nEnd of game: %d. Current intelligence scores: \n (co1: %d co2: %d, co3: %d, co4: %d, co5: %d).\n%s\n"\
#                  % ('/'*40, counter, old_ai.co1, old_ai.co2, old_ai.co3, old_ai.co4, old_ai.co5, '/'*40)
            time.sleep(0.3)
            
        new_ai.switch(old_ai)
        return (self.play_mock_game(old_ai, new_ai, 1) == 'O')

        
        
    #the mock counterpart of play_game(), plays a mock game
    def play_mock_game(self, player1, player2, active):
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
                player1.turn(self)
            else:
                if self.speed == 1:
                    print "It is new AI's turn. " + "(O)"
                    self.draw_board()
                    time.sleep(0.3)
                player2.turn(self)

            active += 1
            
        

            #if self.speed == 1: self.draw_board()
                
            #check for winners
            win_symbol = self.check_winners()
            if win_symbol != None:
                if win_symbol == 'X':
                    winner = player1.name + '(X)'
                else:
                    winner = player2.name + '(O)'
                if self.speed != 3: print "\n%s\n%s Won!\n%s\n" % ('/'*40, winner, '/'*40)
                if self.speed == 2: self.draw_board()
                return win_symbol
        

        #condition if the game is a tie
        if win_symbol == None:
            if self.speed != 3: print '\n' + '/'*40 + '\n' + 'The game is a draw.\n' + '/'*40 + '\n'
        if self.speed == 2: self.draw_board()
        return win_symbol
        
    


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


