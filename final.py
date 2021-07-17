class Location:
    def __init__(self, name, description):
        # YOUR CODE HERE
        self.name = name
        self.description = description
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        
    def possible_moves(self):
        # YOUR CODE HERE
        p_locations = []
        if self.north != None:
            p_locations += [self.north]
        if self.south != None:
            p_locations += [self.south]
        if self.east != None:
            p_locations += [self.east]
        if self.west != None:
            p_locations += [self.west]
        return p_locations
        
    def __str__(self):
        # YOUR CODE HERE
        length = len(self.name) + 4
        return '{}\n# {} #\n{}\n\n{}\n'.format('#'*length, self.name, '#'*length, self.description)

# Create locations
water_pavilion = Location('Water Pavilion','Welcome to the Water Pavilion!')
bridge_center = Location('Bridge: Center','Welcome to the center of the bridge!')
bridge_north = Location('Bridge: North','Welcome to the north part of the bridge!')
bridge_east = Location('Bridge: East','Welcome to the east part of the bridge!')
bridge_west = Location('Bridge: West','Welcome to the west part of the bridge!')
cc_east_ent = Location('Conference Center: East Entrance','Welcome to the east entrance of conference center!')

# Set relationships among locations
water_pavilion.north = bridge_center
bridge_center.south = water_pavilion
bridge_center.north = bridge_north
bridge_center.west = bridge_west
bridge_center.east = bridge_east
bridge_east.west = bridge_center
bridge_north.south = bridge_center
bridge_west.west = cc_east_ent
bridge_west.east = bridge_center
cc_east_ent.east = bridge_west

import random

class Character:
    def __init__(self, name, loc, sym):
        self.name = name
        self.location = loc
        self.sym = sym
        self.hp = 50
        self.total_hp = 50
        self.speed = 5
        self.strength = 5
        self.role = None
            
    def __str__(self):
        length = len(self.name) + 4
        return '{}\n# {} #\n{}\n\nHP: {} / {}\nSpeed: {}\nStrength: {}\nLocation: {}\n'.format('#'*length, self.name, '#'*length, self.hp, self.total_hp, self.speed, self.strength, self.location.name)
        
    def __gt__(self, other):
        if random.random() <= self.speed / (self.speed + other.speed):
            return True
        return False

    def attack(self, enemy):
        if self > enemy:
            damage = int(random.random() * self.strength) + 1
            enemy.hp -= damage
            return '{} attacks {} for {} damage!'.format(self.name, enemy.name, damage)
        else:
            return '{} attacks {} but misses!'.format(self.name, enemy.name)
    
    def flee(self, enemy):
        if self > enemy:
            direction = int(random.random() * (len(self.location.possible_moves())))
            self.location = self.location.possible_moves()[direction]
            return True
        return False
        
    def move(self, direction):
        if direction == 'n':
            if self.location.north != None:
                self.location = self.location.north
                return True
            return False
        if direction == 's':
            if self.location.south != None:
                self.location = self.location.south
                return True
            return False
        if direction == 'e':
            if self.location.east != None:
                self.location = self.location.east
                return True
            return False
        if direction == 'w':
            if self.location.west != None:
                self.location = self.location.west
                return True
            return False
        
    def is_dead(self):
        if self.hp <= 0:
            return True
        return False
    
    def reset(self):
        self.hp = self.total_hp


class Warrior(Character):
    def __init__(self, name, loc, sym):
        super().__init__(name, loc, sym)
        self.role = 'Warrior'
        self.strength = 10
        
    def __str__(self):
        length = len(self.name) + 4
        return '{}\n# {} #\n{}\n\nRole: {}\nHP: {} / {}\nSpeed: {}\nStrength: {}\nLocation: {}\n'.format('#'*length, self.name, '#'*length, self.role, self.hp, self.total_hp, self.speed, self.strength, self.location.name)
        
class Goblin(Character):
    def __init__(self, name, loc, sym):
        super().__init__(name, loc, sym)
        self.role = 'Goblin'
        self.hp = 35
        self.total_hp = 35
        self.strength = 5
        self.speed = 3

    def __str__(self):
        length = len(self.name) + 4
        return '{}\n# {} #\n{}\n\nRole: {}\nHP: {} / {}\nSpeed: {}\nStrength: {}\nLocation: {}\n'.format('#'*length, self.name, '#'*length, self.role, self.hp, self.total_hp, self.speed, self.strength, self.location.name)
        
    def move(self):
        moves = self.location.possible_moves()
        direction = random.randint(0,len(moves)-1)
        self.location = moves[direction]

class Map:
    def __init__(self, start):
        self.start = start
        self.map = None

        coord = (0,0)
        n,s,w,e = 0,0,0,0

        visited = []
        visited = {}
        queue = [(self.start,coord)]

        while len(queue) > 0:
            tup = queue[0]
            queue = queue[1:]

            loc = tup[0]
            coord = tup[1]

            visited[coord] = loc

            if loc.north and (coord[0]+1,coord[1]) not in visited:
                if coord[0]+1 > n:
                    n += 1
                queue.append((loc.north,(coord[0]+1,coord[1])))
            if loc.south and (coord[0]-1,coord[1]) not in visited:
                if coord[0]-1 < s:
                    s -= 1
                queue.append((loc.south,(coord[0]-1,coord[1])))
            if loc.east and (coord[0],coord[1]+1) not in visited:
                if coord[1]+1 > e:
                    e += 1
                queue.append((loc.east,(coord[0],coord[1]+1)))
            if loc.west and (coord[0],coord[1]-1) not in visited:
                if coord[1]-1 < w:
                    w -= 1
                queue.append((loc.west,(coord[0],coord[1]-1)))

        self.n = n
        self.w = w

        rows = n-s+1
        cols = e-w+1
        
        result = []
        for i in range(rows):
            col = []
            for j in range(cols):
                coord = (-(i-n),j+w)
                if coord in visited.keys():
                    col.append(visited[coord])
                else:
                    col.append(None)
            result.append(col)
        
        self.map = result
    
    def str_w_chars(self, characters):
        rows = len(self.map)
        cols = len(self.map[0])
        
        result = '-' * ((cols * 2) + 1) + '\n'
        for row in range(rows):
            result += '|'
            for col in range(cols):
                sym = 'X'
                if self.map[row][col] != None:
                    for c in characters:
                        if self.map[row][col] == c.location:
                            sym = c.sym
                    if sym == 'X':
                        sym = ' '
                result += sym + '|'
            result += '\n'
            result += '-' * ((cols * 2) + 1) + '\n'

        return result
        
    def __str__(self):
        rows = len(self.map)
        cols = len(self.map[0])

        result = '-' * ((cols * 2) + 1) + '\n'
        for row in range(rows):
            result += '|'
            for col in range(cols):
                sym = 'X'
                if self.map[row][col]:
                    sym = ' '
                result += sym + '|'
            result += '\n'
            result += '-' * ((cols * 2) + 1) + '\n'

        return result

class Game:
    
    EXPLORE_HEADER = '>> EXPLORE <<\n\n'
    BATTLE_HEADER = '>> BATTLE <<\n\n'
    
    EXPLORE_CMDS = ['n','s','e','w','look','map','self','help']
    BATTLE_CMDS = ['attack','flee']
    
    def __init__(self,name,loc,sym):
        self.player = Warrior(name,loc,sym)
        self.enemy = Goblin('Grim',cc_east_ent,'+')
        self.map = Map(water_pavilion)
        
        self.mode = 'explore'
        
    def battle_info(self):
        response = self.BATTLE_HEADER
        response += '{} ({}/{}) vs. {} ({}/{})'.format(self.player.name,self.player.hp,self.player.total_hp,self.enemy.name,self.enemy.hp,self.enemy.total_hp)
        return response
        
    def intro(self):
        response =  '###########################\n'
        response += '#                         #\n'
        response += '#  DUKE DUNGEON EXPLORER  #\n'
        response += '#                         #\n'
        response += '###########################\n\n'
        response += 'You wake up in a new world...\n\n'
        response += '{}'.format(self.EXPLORE_CMDS)
        
        return response
            
    def process_cmd(self, cmd):
        response = ''
        
        if self.mode == 'explore':
            response = self.EXPLORE_HEADER
            
            if cmd not in self.EXPLORE_CMDS:
                response += '{}: invalid command\n'.format(cmd)
                response += '{}'.format(self.EXPLORE_CMDS)
            else:
                if cmd == 'look':
                    response += str(self.player.location)
                elif cmd == 'map':
                    response += str(self.map.str_w_chars([self.player]))
                elif cmd == 'self':
                    response += str(self.player)
                elif cmd == 'help':
                    response += 'Here are some helpful commands for you to use:\n\n'
                    response += '{}'.format(self.EXPLORE_CMDS)
                elif cmd in ['n','s','e','w']:
                    if self.player.move(cmd):
                        response += str(self.player.location)
                    else:
                        response += '{}: can\'t move in that direction'.format(cmd)
                    
                    if self.enemy:
                        if self.player.location == self.enemy.location:
                            self.mode = 'battle'
                            return self.battle_info()

                        self.enemy.move()

                        if self.player.location == self.enemy.location:
                            self.mode == 'battle'
                            return self.battle_info()

        elif self.mode == 'battle':
            response = self.BATTLE_HEADER
            
            mesg = ''
            vs_info = ''
            
            if cmd not in self.BATTLE_CMDS:
                mesg += '{}: invalid command\n'.format(cmd)
                mesg += '{}'.format(self.BATTLE_CMDS)
            else:
                if cmd == 'attack':
                    mesg += self.player.attack(self.enemy) + '\n'
                    
                    if self.enemy.is_dead():
                        mesg += '{} defeats {}!'.format(self.player.name,self.enemy.name)
                        vs_info = '{} ({}/{}) vs. {} ({}/{})\n\n'.format(self.player.name,self.player.hp,self.player.total_hp,self.enemy.name,self.enemy.hp,self.enemy.total_hp)
                        self.enemy = None
                        self.mode = 'explore'
                    else:
                        mesg += self.enemy.attack(self.player) + '\n'
                        
                        if self.player.is_dead():
                            mesg += '{} defeats {}!'.format(self.enemy.name,self.player.name)
                            self.mode = 'gameover'
                elif cmd == 'flee':
                    if self.player.flee(self.enemy):
                        mesg = '{} successfully flees from {}!\n'.format(self.player.name,self.enemy.name)
                        self.mode = 'explore'
                    else:
                        mesg = '{} fails to flee from {}!\n'.format(self.player.name,self.enemy.name)
                        
                        mesg += self.enemy.attack(self.player)
                        
                        if self.player.is_dead():
                            mesg += '{} defeats {}!'.format(self.enemy.name,self.player.name)
                            self.mode = 'gameover'
            if self.enemy:
                vs_info = '{} ({}/{}) vs. {} ({}/{})\n\n'.format(self.player.name,self.player.hp,self.player.total_hp,self.enemy.name,self.enemy.hp,self.enemy.total_hp)
            response = response + vs_info + mesg
            
        elif self.mode == 'gameover':
            response =  '#############\n'
            response += '#           #\n'
            response += '# GAME OVER #\n'
            response += '#           #\n'
            response += '#############\n\n'
            
            response += 'Thanks for playing!'

        return response


# Graphics

from tkinter import *
root = Tk()
root.title('DKU Role Playing Game')
root.geometry('550x350')
root.resizable(0,0)

frame = Frame(root,width=550,height=350)
frame.place(x=0,y=0)

game = Game('Zarko',water_pavilion,'Z')

def process_cmd(event):
    cmd = input_text.get().lower()
    input_text.set('')

    response = game.process_cmd(cmd)
    info_text.set(response)

info_text = StringVar()
info = Label(frame,font='Courier 11',anchor='n',textvariable=info_text,wraplength=490)
info.place(x=25,y=50,width=500,height=230)
info_text.set(game.intro())

input_text = StringVar()
user_input = Entry(frame,textvariable=input_text)
user_input.place(x=100,y=310,width=300,height=25)
user_input.bind('<Return>',process_cmd)

root.mainloop()
