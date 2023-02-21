#Telium - the game

import random
import time

#Global Variables

num_modules = 17        #The number of modules in the space station
module = 1              #The module of the space station we are in
last_module = 0         #The last module we were in
possible_moves = []     #List of the possible moves we can make
alive = True            #Whether the player is alive or dead
won = False             #Whether the player has won
power = 100             #The amount of power the space station has
fuel = 500              #The amount of fuel the player has in the flamethrower
locked = 0              #The module that has been locked by the player
queen = 0               #Location of the queen
vent_shafts = []        #Location of the ventilation shaft enterances
info_panels = []        #Location of the information panels
workers = []            #Location of the workers/NPCs

#Procedure/Function declarations

#Loads space station module data
def load_module():
        global module, possible_moves
        possible_moves = get_modules_from(module)
        output_module()

#Gets modules the player can move to
def get_modules_from(module):
        moves = []
        text_file = open("Charles_Darwin/module" + str(module) + ".txt", "r")
        for counter in range(0,4):
                move_read = text_file.readline()
                move_read = int(move_read.strip())
                if move_read != 0:
                        moves.append(move_read)
        text_file.close()
        return moves

#Outputs where user is in the game
def output_module():
        global module
        print()
        print("-----------------------------------------------------------------------------------------------------------------------------------------------")
        print()
        print("You are in module", module)
        print()

#Outputs to the user where they can move
def output_moves():
        global possible_moves
        print()
        print("From here you can move to modules: | ", end='')
        for move in possible_moves:
                print(move, '| ', end='')
        print()

#Spawns the NPC aliens
def spawn_npcs():
        global num_modules, main_npc, vent_shafts, info_panels, npc_worker
        module_set = []
        for counter in range(2, num_modules + 1):
                module_set.append(counter)
        random.shuffle(module_set)
        i = 0
        main_npc = module_set[i]
        for counter in range(0,3):
                i = i+1
                vent_shafts.append(module_set[i])

        for counter in range(0,2):
                i = i+1
                info_panels.append(module_set[i])

        for counter in range(0,3):
                i = i+1
                workers.append(module_set[i])

#Gets action of the user
def get_action():
        global module, last_module, possible_moves
        valid_action = False
        while valid_action == False:
                print("What do you want to do next? (MOVE, SCANNER, LOAD, or STORY)")
                action = input(">")
                if action.upper() == "MOVE" or action.lower() == "m":
                        move = int(input("Enter the module to move to: "))
                        if move in possible_moves:
                                valid_action = True
                                last_module = module
                                module = move
                        else:
                                print("The module must be connected to the current module.")
                elif action.upper() == "LOAD" or action.lower() == "l":
                        print("loading instructions...\n")
                        time.sleep(1)
                        text_file = open("instructions.txt", "r")
                        print(text_file.read())
                        text_file.close()
                        time.sleep(15)
                        valid_action = False
                elif action.upper() == "STORY" or action.lower() == "s":
                        print("loading story...\n")
                        time.sleep(1)
                        text_file = open("story.txt", "r")
                        
                        print(text_file.read())
                        text_file.close()
                        time.sleep(15)
                        valid_action = False

#Main program starts here

print('Space Station Game version 1.1\n21/02/2023\nLoad instructions using LOAD command...\n')

spawn_npcs()
print("Main Alien NPC is located in module: " , main_npc)
print("(sus) vents are located in modules: " , vent_shafts)
print("Info panels are located in modules: " , info_panels)
print("Worker NPC are located in modules:", workers)
while alive and not won:
        load_module()
        if won == False and alive == True:
                output_moves()
                get_action()

if won == True:
        print("The Main Alien NPC is trapped and you burn it to death with your flamethrower.\nGame over. You win!")
if alive == False:
        print("The station has run out of power. Unable to sustain life support, you die.")
