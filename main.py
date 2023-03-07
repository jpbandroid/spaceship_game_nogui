#Telium - the game

import random
import time

#Global Variables

num_modules = 20        #The number of modules in the spaceship
module = 1              #The module of the spaceship we are in
last_module = 0         #The last module we were in
possible_moves = []     #List of the possible moves we can make
alive = True            #Whether the player is alive or dead
won = False             #Whether the player has won
power = 500             #The amount of power the spaceship has
fuel = 500              #The amount of fuel the player has in the flamethrower
locked = 0              #The module that has been locked by the player
queen = 0               #Location of the queen
vent_shafts = []        #Location of the ventilation shaft enterances
info_panels = []        #Location of the information panels
workers = []            #Location of the workers/NPCs

#Procedure/Function declarations

#Loads spaceship's module data
def load_module():
        global module, possible_moves
        possible_moves = get_modules_from(module)
        output_module()

#Gets modules the player can move to
def get_modules_from(module):
        moves = []
        text_file = open("spaceship/module" + str(module) + ".txt", "r")
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
        if module == main_npc:
                        print("You are in the same module as the Main Alien NPC (Telium)")
        elif module == vent_shafts[0] or module == vent_shafts[1] or module == vent_shafts[2]:
                print("You are inside a vent shaft. (sus...)")
        elif module == info_panels[0] or module == info_panels[1]:
                print("You are inside a module with an info panel.")
        elif module == workers[0] or module == workers[1] or module == workers[2]:
                print("You are in the same module as worker NPC.")

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

#Checks the ventilation shafts
def check_vent_shafts():
        global num_modules, module, vent_shafts, fuel
        if module in vent_shafts:
                print("There is a bank of fuel cells here\nYour player has loaded some into its flamethrower...")
                fuel_gained = random.randint(50, 100)
                print('Fuel was', fuel, 'fuel is now', fuel + fuel_gained)
                fuel = fuel + fuel_gained
                print('Vent shafts have closed.\nMoving down the vent shaft...')
                last_module = module
                module = random.randint(1, num_modules)
                load_module()

#Lets player lock a module
def lock():
        global num_modules, power, locked
        new_lock = int(input('Enter module to lock:\n'))
        if new_lock < 0 or new_lock > num_modules:
                print("Invalid module. Operation failed.")
        elif new_lock == main_npc:
                print("Operation failed. Unable to lock module.")
        else:
                locked = new_lock
                print("NPCs cannot enter module", locked)
        power_used = 25 + 5 * random.randint(0,5)
        power = power - power_used
                        
#Gets action of the user
def get_action():
        global module, last_module, possible_moves
        valid_action = False
        while valid_action == False:
                print("What do you want to do next? (MOVE, SCANNER, INSTRUCTIONS, or STORY)")
                action = input(">")
                if action.upper() == "MOVE" or action.lower() == "m":
                        move = int(input("Enter the module to move to: "))
                        if move in possible_moves:
                                valid_action = True
                                last_module = module
                                module = move
                        else:
                                print("The module must be connected to the current module.")
                elif action.upper() == "SCANNER" or action.lower() == "s-c":
                        command = input("Scanner ready. Enter command\nCommands available: LOCK\n")
                        if command.upper() == "LOCK" or command.lower == "l":
                                lock()
                        elif command.upper() == "POWER" or command.lower == "p":
                                print("Current power of the ship:", power)
                
                elif action.upper() == "INSTRUCTIONS" or action.lower() == "i":
                        print("loading instructions...\n")
                        time.sleep(1)
                        text_file = open("instructions.txt", "r")
                        print(text_file.read())
                        text_file.close()
                        #time.sleep(15)
                        valid_action = False
                elif action.upper() == "STORY" or action.lower() == "s-t":
                        print("loading story...\n")
                        time.sleep(1)
                        text_file = open("story.txt", "r")
                        
                        print(text_file.read())
                        text_file.close()
                        #time.sleep(15)
                        valid_action = False

#Intuition functionality
def intuition():
        global possible_moves, workers, vent_shafts
        #Check what is in each of the possible moves
        for connected_module in possible_moves:
                if connected_module in workers:
                        print("I can hear something scuttling!")
                if connected_module in vent_shafts:
                        print("I can feel cold air!")

#Movement of Worker Aliens
def worker_aliens():
        global module, workers, fuel, alive
        #Output if Worker NPC encountered
        if module in workers:
                print("Startled, a Worker NPC scuttles across the floor.\nIt turns and leaps towards you...")
                #Get the player's action
                succesful_attack = False
                while succesful_attack == False:
                        print("You can:\n- Short blast your flamethrower to frighten it away.\n- Long blast your flamethrower to try to erase it.\nHow will you react? (S,L)")
                        action = 0
                        while action not in ("S", "L"):
                                action = input("Press the trigger: ")
                        fuel_used = int(input("How much fuel will you use? ..."))
                        fuel = fuel - fuel_used
                        #Check if player has run out of fuel
                        if fuel <= 0:
                                alive = False
                                return
                        #Work out how much fuel is needed
                        if action == "S":
                                fuel_needed = 30 + 10 * random.randint(0,5)
                        if action == "L":
                                fuel_needed = 90 + 10 * random.randint(0,5)
                        #Try again if not enough fuel was used
                        if fuel_used >= fuel_needed:
                                successful_attack = True
                        else:
                                print("The alien squeals but is not dead. It's angry.")
                #Successful action
                if action == "S":
                        print("The alien scuttles away into the corner of the room.")
                if action == "L":
                        print("The alien has been destroyed.")
                        #Remove it from the module
                        workers.remove(module)
                print()

#Movement logic for the Main Alien NPC
def move_mainNPC():
        global num_modules, module, last_module, locked, main_npc, won, vent_shafts, moves_to_make
        #If player is in the same module as the Main Alien NPC, this code is run
        escapes = [0]
        moves_to_make = random.randint(1,3)
        if module == main_npc:
                print("There it is! The Main Alien NPC is in this module...")
                #Decide how many moves the Main Alien NPC should take
                moves_to_make = random.randint(1,3)
                can_move_to_last_module = False
                while moves_to_make > 0:
                        #Get escape paths the Main Alien NPC can make
                        escapes = get_modules_from(main_npc)
                        #Remove the current module as an escape route
                        if module in escapes:
                                escapes.remove(module)
                        #Allow the Main Alien NPC to double back behind the player from another module
                        if last_module in escapes and can_move_to_last_module == False:
                                escapes.remove(last_module)
                        #Remove a module that is locked from the escape list
                        if locked in escapes:
                                escapes.remove(locked)
                        #If there is no escape for the Main Alien NPC, the player has won!!
                        if len(escapes) == 0:
                                won = True
                                moves_to_make = 0
                                print("... and the door is locked. The Main Alien NPC is trapped.")
        else:
                if moves_to_make == 1:
                        print("... and has escaped.")
                main_npc = random.choice(escapes)
                moves_to_make = moves_to_make - 1
                can_move_to_last_module = True
                #Handle the Main Alien NPC being in a module with a vent shaft
                while main_npc in vent_shafts:
                        #if moves_to_make > 1:
                                #print("... and has escaped.")
                        print("We can hear scuttling in the vent shafts...\nI think the alien is sus...")
                        valid_move = False
                        #The Main Alien NPC is unable to land in a module with another (sus) vent shaft...
                        while valid_move == False:
                                valid_move = True
                                main_npc = random.randint(1, num_modules)
                                if main_npc in vent_shafts:
                                        valid_move = False
                        #The Main Alien NPC always stops moving after travelling through the (sus) vent shaft
                        moves_to_make = 0

#Main program starts here

print('Spaceship Game version 2.3.5\n07/03/2023\nLoad instructions using INSTRUCTIONS command...\n')

spawn_npcs()
print("Main Alien NPC is located in module: " , main_npc)
print("(sus) vents are located in modules: " , vent_shafts)
print("Info panels are located in modules: " , info_panels)
print("Worker NPC are located in modules:", workers)
while alive and not won:
        load_module()
        check_vent_shafts()
        move_mainNPC()
        worker_aliens()
        if won == False and alive == True:
                output_moves()
                get_action()
                intuition()

if won == True:
        print("The Main Alien NPC is trapped and you burn it to death/destroy it with your flamethrower.\nGame over. You win!")
if alive == False:
        print("The station has run out of power. Unable to sustain life support, you die.")
