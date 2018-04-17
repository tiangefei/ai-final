#Xiang Fan
#Gefei Tian

import copy
import math
from graphics import*

class Player():
    def __init__(self,color):
        self.color = color

    def move(self, game):
        flag = 0
        while flag == 0:
            try:
                pos = input('Enter a number: ')
                if pos in game.remaining:
                    flag = 1
                else:
                    print "Invalid input. \n"
            except:
                print "Invalid input. \n"

        game.remaining.remove(pos)
        self.replace(game, game.position_dict[pos])

        y = (pos - 1) // 15
        x = (pos - 1) % 15
            
        game.q[x][y]=Circle(game.p[x][y],10)
        game.q[x][y].draw(game.window)
        game.q[x][y].setFill(self.color)

    def replace(self, game, position):
        game.board[position[0]][position[1]] = self.color

class AI(Player):
    def __init__(self,color):
        Player.__init__(self,color)
        self.VALUE = {'FOUR' : 9999999, 'THREE' : 99999, 'ATTACK' : 0, 'DEFEND' : 0, 'NEUTRAL' : 0, 'MINE' : 0, 'OTHER' : 0}
        
        self.learn = 1
        
        if self.color == 'black':
            self.opponent = 'white'
        else:
            self.opponent = 'black'

    def move(self, game):
        self.position_type = {}
        self.position_points = {}
        self.points_list = {}
        for i in range(1,15**2+1):
            self.position_type[i] = [0,0]
            self.position_points[i] = [0,0,0] 
            self.points_list[i] = 0

        self.count_points(game)
        for position in range(1,15**2+1):
           
            self.points_list[position] += self.position_points[position][0]*((self.position_type[position][0]**2))\
                                            + self.position_points[position][1]*((self.position_type[position][1]**2))
        
        highest = {'points' : 0, 'position' : 0}

        for position in self.points_list:
            if self.points_list[position] > highest['points']:
                highest['points'] = self.points_list[position]
                highest['position'] = position

        if highest['position'] == 0:
            highest['position'] = game.remaining[0]
        
        
        pos_y = (highest['position'] - 1) // 15
        pos_x = (highest['position'] - 1) % 15
        
        
        game.q[pos_x][pos_y]=Circle(game.p[pos_x][pos_y],10)
        if self.learn == 1:
            game.q[pos_x][pos_y].draw(game.window)
            game.q[pos_x][pos_y].setFill(self.color)

        self.replace(game, game.position_dict[highest['position']])
        game.remaining.remove(highest['position'])

    def count_points(self, game):
        if self.color == 'O':
            index = 1
        else:
            index = 0
        
        checklist = []
        
        for i in range(1, 16):
            checklist.append(game.row_position(i))
            checklist.append(game.col_position(i))
        checklist.append(game.diagonal_position(0))
        checklist.append(game.diagonal_position(1))

        for major_row in checklist:
            for row in major_row:
                row_list = game.number_in_row(row)
                    
                for position in row:
                    if position in game.remaining:
                        
                        if row_list[self.color] == 4 and row_list[self.opponent] == 0 and game.learning == 0:
                            self.points_list[position] += self.VALUE['FOUR']
                        elif row_list[self.color] == 3 and row_list[self.opponent] == 0 and game.learning == 0:
                            self.points_list[position] += self.VALUE['THREE']
            
                        elif row_list[self.opponent] == 4 and row_list[self.color] == 0 and game.learning == 0:
                            self.points_list[position] += self.VALUE['FOUR']
                        elif row_list[self.opponent] == 3 and row_list[self.color] == 0 and game.learning == 0:
                            self.points_list[position] += self.VALUE['THREE']
                        
                        elif row_list[self.color] + row_list[self.opponent] == 0:
                            self.points_list[position] += self.VALUE['NEUTRAL']
                        elif row_list[self.opponent] == 0:
                            self.position_type[position][int(math.fabs(index-1))] += 1
                            self.position_points[position][int(math.fabs(index-1))] += self.VALUE['ATTACK'] + row_list[self.color]*self.VALUE['MINE']
                        elif row_list[self.color] == 0:
                            self.position_type[position][index] += 1
                            self.position_points[position][index] += self.VALUE['DEFEND'] + row_list[self.opponent]*self.VALUE['OTHER']

    def switch(self, other):
        self.VALUE['FOUR'] = copy.copy(other.VALUE['FOUR'])
        self.VALUE['THREE'] = copy.copy(other.VALUE['THREE'])
        self.VALUE['NEUTRAL'] = copy.copy(other.VALUE['NEUTRAL'])
        self.VALUE['ATTACK'] = copy.copy(other.VALUE['ATTACK'])
        self.VALUE['DEFEND'] = copy.copy(other.VALUE['DEFEND'])
        self.VALUE['MINE'] = copy.copy(other.VALUE['MINE'])
        self.VALUE['OTHER'] = copy.copy(other.VALUE['OTHER'])
        
class Game(object):
    def __init__(self):
        self.player1, self.player2 = self.setup()
        self.active = 0
        self.speed = 0
        self.learning = 0
        self.depth = 10
        
        self.p=[[0 for a in range(16)] for b in range(16)]
        self.q=[[0 for a in range(15)] for b in range(15)]
    
    def setup(self):
        player1, player2 = Player('black'), AI('white')
        
        return player1, player2

    def WinBoard(self):
        self.p=[[0 for a in range(16)] for b in range(16)]
        self.q=[[0 for a in range(15)] for b in range(15)]
        self.window = GraphWin('Gomoku',480,600)
        for i in range(15):
            for j in range(15):
                self.p[i][j] = Point(i*30+30,j*30+30)
                self.p[i][j].draw(self.window)
                Text(self.p[i][j], str(j * 15 + i + 1)).draw(self.window)


    def play_game(self, player1, player2):
        self.board = [[x*15+(y+1) for y in range(15)] for x in range(15)]
        self.remaining = [i for i in range(1,15**2+1)]
        self.position_dict = {}
        
        self.WinBoard()
        
        for i in range(1,15**2+1):
            self.position_dict[i] = ((i-1)/15,(i-1)%15)
        
        for i in range(15**2):
            if self.active%2 == 0:
                player1.move(self)
            else:
                player2.move(self)

            self.active += 1
            
            win_color = self.check_winners()
            if win_color != None:
                if win_color == 'black':
                    winner = 'player1' + '(black)'
                else:
                    winner = 'player2' + '(white)'
                if winner == 'player2' + '(white)':
                    print('you loss')
                    break
                else:
                    print('you win')
                    break
    
        if win_color == None:
            print('tie')
    

    def check_winners(self):
        checklist = []
        for i in range(1, 16):
            for element in self.row_position(i):
                checklist.append(self.number_in_row(element))
            for element in self.col_position(i):
                checklist.append(self.number_in_row(element))
        for element in self.diagonal_position(0):
            checklist.append(self.number_in_row(element))
        for element in self.diagonal_position(1):
            checklist.append(self.number_in_row(element))
    
        for check in checklist:
            if check['white'] == 5:
                return 'white'
            if check['black'] == 5:
                return 'black'


    def number_in_row(self, row):
        row_list = {'white': 0, 'black': 0, 0: 0}
        for position in row:
            num = self.board[self.position_dict[position][0]][self.position_dict[position][1]]
            if type(num) == int:
                num = 0
            row_list[num] += 1
        return row_list

    def row_position(self, row_number):
        result = []
        for i in range(11):
            result.append(range((row_number-1)*15+1+i,(row_number-1)*15+1+i+5))
        return result

    def col_position(self, col):
        result = []
        for i in range(11):
            result.append(range(col+i*(15), 15*(5+i)+1, 15))
        return result

    def diagonal_position(self, dia):
        x_pos = set([])
        y_pos = set([])
        result = []
        if dia == 0:
            for row_number in range(1, 12):
                x_pos = x_pos.union(set(range((row_number-1)
                  *15+1,(row_number-1)
                  *15+15+1)))
                y_pos = y_pos.union(set(range(row_number, 15**2+1, 15)))
            for start_pos in x_pos.intersection(y_pos):
                result.append(range(start_pos,start_pos+(4)
                  *(16)+1,16))
        if dia == 1:
            for row_number in range(1, 15-5+2):
                x_pos = x_pos.union(set(range((row_number-1)
                  *15+1,(row_number-1)*15+15+1)))
            for row_number in range(15, 5-1, -1):
                y_pos = y_pos.union(set(range(row_number, 15**2+1, 15)))
            for start_pos in x_pos.intersection(y_pos):
                result.append(range(start_pos, start_pos + 
                  (5-1)*(14) + 1,14))
        return result

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
        

    def start_learning(self, player, speed):
        old = AI('black')
        new = AI('white')
        self.speed = speed
        self.learning = 1
        
        for i in range(self.depth,0,-1):
            self.adjust(old, new, 'NEUTRAL', i)
            self.adjust(old, new, 'ATTACK', i)
            self.adjust(old, new, 'DEFEND', i)
            self.adjust(old, new, 'MINE', i)
            self.adjust(old, new, 'OTHER', i)
        
        player.switch(old)
        self.learning = 0
    
    
    def self_play(self, old, new):
        if self.self_game_play(old, new, 1) == 'white':
            old.switch(new)
       
        new.switch(old)
        print(old.VALUE['ATTACK'])
        print(old.VALUE['DEFEND'])
        print(old.VALUE['MINE'])
        print(old.VALUE['OTHER'])
        return (self.self_game_play(old, new, 1) == 'white')
        
        
    def self_game_play(self, player1, player2, active):
        self.WinBoard()
        self.board = [[x*15+(y+1) for y in range(15)] for x in range(15)]
        self.remaining = [i for i in range(1,15**2+1)]
        self.position_dict = {}
        
        for i in range(1,15**2+1):
            self.position_dict[i] = ((i-1)/15,(i-1)%15)
        
        for i in range(15**2):
            if active%2 == 0:
                player1.move(self)
            else:
                player2.move(self)

            active += 1
            
            win_color = self.check_winners()
            if win_color != None:
                if win_color == 'black':
                    winner = 'player1' + '(black)'
                else:
                    winner = 'player2' + '(white)'
                return win_color

def main():
    game = Game()
    player1 = game.player1
    player2 = game.player2
    
    game.depth = 15
    
    speed = 2
    
    if speed == 2 :
        game.start_learning(player2,speed)
    else: print("skip learning")
    
    print("The game is ready")

    while True:
        game.play_game(player1, player2)
        player2.learn = 0
        break

while True:
    main()
    break


