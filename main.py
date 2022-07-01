import random
import re
from classes.magic import Spell
from classes.Game import Person, bcolors
from classes.Inventory import Item


# create damage magic
fire = Spell("Fire", 15, 100, "black")
thunder = Spell("Thunder", 30, 120, "black")
blizzard = Spell("Blizzard", 30, 120, "black")
meteor = Spell("Meteor", 70, 250, "black")
quake = Spell("Quake", 85, 320, "black")

# create healing magic
cure = Spell("cure", 15, 180, "white")
heal = Spell("Heal", 25, 250, "white")

player_spells = [fire, thunder, blizzard, meteor, quake, cure, heal]
enemy_spells = [fire, thunder, blizzard, meteor]


# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion =Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 300 HP", 300)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one part member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5}, {"item": superpotion, "quantity": 3}, {"item": elixer, "quantity": 2}, {"item": hielixer, "quantity": 1}, {"item": grenade, "quantity": 8}]

# Initiate Person
player1 = Person("Player", 830, 250, 100, 50, player_spells, player_items)
player2 = Person("Kratos", 980, 120, 190, 50, player_spells, player_items)
player3 = Person("Kraken", 550, 600, 60, 50, player_spells, player_items)

players = [player1, player2, player3]

enemy1 = Person("Ogre  ", 1200, 350, 105, 25, enemy_spells, [])
enemy2 = Person("Imp   ", 650, 120, 150, 25, [], [])
enemy3 = Person("Conman", 835, 100, 55, 25, [], player_items)

enemies = [enemy1, enemy2, enemy3]


running = True
print("\n\n\n")
print(bcolors.BOLD + "NAME                 HP                                   " + bcolors.ENDC)
for enemy in enemies:
    enemy.get_enemy_stats()
print(bcolors.FAIL + bcolors.FAIL + "AN ENEMY ATTACKS!" + bcolors.ENDC)

# Create battle system

while running:
    print("==============================")
    print(bcolors.BOLD + "NAME               HP                                   MP" + bcolors.ENDC)

    for player in players:
        player.get_stats()

    print("\n")

    for player in players:
        print("\n")

        if not enemies:
            print(bcolors.OKGREEN + bcolors.BOLD + "YOU WIN!" + bcolors.ENDC)
            running = False
            break


        player.choose_action()
        choice = input("    Choose Action: ")
        index = int(choice) - 1

        if (index == 0):
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("you attacked " + str(enemies[enemy].name.replace(" ", "")) + " for", dmg, "points of damage.")
            print("------------------------------------")
            print("\n")

            if enemies[enemy].get_hp() <= 0:
                print(str(enemies[enemy].name.replace(" ","" )) + bcolors.OKGREEN +" has been defeated!" + bcolors.ENDC)
                del enemies[enemy]

# create magic battle System
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose Spells:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            cost = spell.cost

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNOT ENOUGH MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            # healing and damage spell mechanics
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg),
                      "points of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() <= 0:
                    print(str(enemies[enemy].name.replace(" ", "")) + bcolors.OKGREEN +" has been defeated!" + bcolors.ENDC)
                    del enemies[enemy]

            print("------------------------------------")
            print("\n")


        # Creating Item system
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose Item ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n None left...." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1


            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for ", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for member in players:
                        member.hp = member.max_hp
                        member.mp = member.max_mp
                else:
                    player1.hp = player1.max_hp
                    player1.mp = player1.max_mp
                print(bcolors.OKGREEN + "\n" + item.name + " Fully Restores HP/MP" + bcolors.ENDC + "\n")
                for player in players:
                    player.get_stats()
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to" + enemies[enemy].name + bcolors.ENDC)
                if enemies[enemy].get_hp() <= 0:
                    print(str(enemies[enemy].name.replace(" ", "")) + bcolors.OKGREEN +" has been defeated!" + bcolors.ENDC)
                    del enemies[enemy]

            print("------------------------------------")
            print("\n")

    # Enemy mechanics
    for enemy in enemies:
        if not players:
            print(bcolors.FAIL + "The Enemy has defeated you!" + bcolors.ENDC)
            running = False
            break

        enemy_choice = random.randrange(0, 3)
        if enemy_choice == 0:
            target = random.randrange(0, 2)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            if players[target].get_hp() <= 0:
                print(str(players[target].name.replace(" ", "")) + bcolors.FAIL +" has been defeated!" + bcolors.ENDC)
                del players[target]

            print( bcolors.FAIL + str(enemy.name).replace(" ", ""), "attacks for" + " " + str(enemy_dmg) +
                   bcolors.ENDC + "\n" + str(players[target].name) + " HP: " +
                   bcolors.OKGREEN + str(players[target].get_hp()) + bcolors.ENDC)

        elif enemy_choice == 1:
            magic_choice = random.randrange(0, len(enemy.magic))
            spell = enemy.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            if enemy.mp < spell.cost:






    print("-----------------------------------")
    print("\n")
    if enemies:
        print(bcolors.BOLD + "NAME                      HP                                   " + bcolors.ENDC)
        for enemy in enemies:
            enemy.get_enemy_stats()
        print("\n")