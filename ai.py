
from player import Player
import copy
import random
import math

class AI(Player):
    def __init__(self, name, symbol):
        #Borrows parent co-efficients
        Player.__init__(self, name, symbol)
        #initilise intelligence co-efficients
        self.VALUE = {'FIVE' : 999999999, 'FOUR' : 9999999, 'ATTACK' : 10, 'DEFEND' : 10, 'NEUTRAL' : 5, 'MINE' : 5, 'OTHER' : 5}
    
        
#        self.co1 = 10
#        self.co2 = 10
#        self.co3 = 10
#        self.co4 = 10
#        self.co5 = 10
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
        
