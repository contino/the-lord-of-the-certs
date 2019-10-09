from classes.colours import bcolors
from classes.battle import Person
from classes.magic import *
from classes.inventory import *
from storytext import *
from logos import *
import random

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, cure]
player_items = [{"item": potion, "quantity": 5}, {"item": hipotion, "quantity": 5}, {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5}, {"item": hielixer, "quantity": 5}, {"item": grenade, "quantity": 5}]

# Instantiate players
player1 = Person("Cloud    :", 1, 600, 432, 34, player_spells, player_items)
player2 = Person("Barrett  :", 1, 400, 270, 34, player_spells, player_items)
player3 = Person("Tifa     :", 1, 350, 297, 34, player_spells, player_items)
players = [player1, player2, player3]
total_players = len(players)

# Instantiate enemies
enemy1 = Person("Soldier   :", 1, 1000, 600, 25, enemy_spells, [])
enemy2 = Person("Sephiroth :", 1, 3765, 999, 25, enemy_spells, [])
enemy3 = Person("Soldier   :", 1, 1000, 600, 25, enemy_spells, [])
enemies = [enemy1, enemy2, enemy3]
total_enemies = len(enemies)

# Set the defeated player and emey variables to zero
defeated_enemies = 0
defeated_players = 0

running = True
i = 0

# Print the title intro
intro_text()

# Print the logo
main_logo()

# Battle message displays
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:

    print("\n==============================\n")
    # Print the health bars of all participants
    print("NAME                      HP                                       MP")
    for player in players:
        player.get_stats()
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    # If battle is ongoing, proceed with turn
    for player in players:   

        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        # Index 0 is the "Attack" option
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("\n" + player.name.replace(" ", "").replace(":", ""), "attacked", enemies[enemy].name.replace(" ", "").replace(":", ""), "for", dmg, "damage.")

            if enemies[enemy].get_hp() == 0:
                print("\n" + enemies[enemy].name.replace(" ", "").replace(":", "") + " has been defeated!")
                del enemies[enemy]
                defeated_enemies += 1

        # Index 1 is the "Magic" option
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) -1
                
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP to cast that!\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + player.name.replace(" ", "").replace(":", "") + " cast " + spell.name + " against " + enemies[enemy].name.replace(" ", "").replace(":", "") +  " dealing", str(magic_dmg), "damage.\n" + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "").replace(":", "") + " has been defeated!")
                    del enemies[enemy]
                    defeated_enemies += 1

        # Index 2 is the "Item" option
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue
                
            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "damage to " + enemies[enemy].name.replace(" ", "").replace(":", "") + "." + "\n" + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "").replace(":", "") + " has been defeated!\n")
                    del enemies[enemy]
                    defeated_enemies += 1
    
        # Check if player won
        if defeated_enemies == total_enemies:
            print(bcolors.OKGREEN + "\n" "You have defeated the enemy!" + bcolors.ENDC)
            running = False
            break
        # Check if enemy won
        elif defeated_players == total_players:
            print(bcolors.FAIL + "The enemies have defeated you!" + bcolors.ENDC)
            running = False
            break
        
    time.sleep(1)

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Choose attack
            target = random.randrange(0, len(players))
            enemy_dmg = enemy.generate_damage()
        
            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + bcolors.BOLD + "\n" + enemy.name.replace(" ", "").replace(":", ""), "attacks " + 
            players[target].name.replace(" ", "").replace(":", ""), "for", enemy_dmg, "points of damage." + bcolors.ENDC)

            if players[target].get_hp() == 0:
                print(bcolors.FAIL + bcolors.BOLD + players[target].name.replace(" ", "").replace(":", "") + " has been defeated!")
                del players[target]
                defeated_players += 1
        
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "").replace(":", "") , "cast", spell.name + ", which heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
               
                target = random.randrange(0, len(players))

                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "").replace(":", "") + " cast " + spell.name + 
                " against " + players[target].name.replace(" ", "").replace(":", "") +  " dealing", str(magic_dmg), "damage." + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(bcolors.FAIL + bcolors.BOLD + players[target].name.replace(" ", "").replace(":", "") + " has been defeated!")
                    del players[target]
                    defeated_players += 1

        # Check if player won
        if defeated_enemies == total_enemies:
            print(bcolors.OKGREEN + "\n" "You have defeated the enemy!" + bcolors.ENDC)
            running = False
            break
        # Check if enemy won
        elif defeated_players == total_players:
            print(bcolors.FAIL + "\nThe enemies have defeated you!" + bcolors.ENDC)
            running = False
            break
    
    time.sleep(1)

    