"""40k small-scale battle simulator

Allows for custom creation of two armies with any amount of units and models.
Structured with nested class objects: Army > Unit > Model > Weapon.
Armies, units, models, and weapons are all chosen in the main() function of this module.
Models are individually assigned weapons (currently no limit).
Models are automatically targetted and killed in the order in which they were created.
Additionally, models fire their weapons in the order in which they were created.
Which army moves first can be changed just above main()

Currently only handles one of the five 40k turn phases: the shooting phase.

Functions:
	army_attack_army: Makes each model in a given army fire its weapon until either every model has fired all of its shots or the enemy army is dead
	countdown_timer: counts down the time until the program will proceed to the next information screen
"""


import os 					#Allows clearing command prompt output with clear()
import sys					#Allows sys.exit()
import random				#Allows dice rolling
from time import sleep		#Allows delay
from model import Model
from weapon import *
from unit import Unit
from army import Army
from data_creation import *

clear = lambda: os.system('cls')


def army_attack_army(army1, army2):
	"""Makes all of one army's models attack the opposing army's units.

	Iterates through Units, Models, and Weapons in creation order.
	Models will attack with all their weapons. (This assumes armies are only attacking in ranged phase) 
	"""
	for unit in army1.units_alive():
		for model in unit.models_alive():
			for i in range(len(model.weapons)):			#There's probably a better way to do this
				if not army2.alive():
					return
				model.attack_with_weapon(i, army2.units_alive()[0])


def countdown_timer(sleep_time):
	count = sleep_time
	print('\n')
	for i in range(sleep_time):
		print('Changing screens in: {}'.format(count), end='\r', flush=True)
		count -= 1
		sleep(1)


"""Main loop; runs army creation and loops until at least one army has no more models left.

Define units and models in main().
(army1/army2).add_unit(Unit('Name')) to make new unit.
Must make new "for" loop for each type of model within a given unit.
Units and models take damage in order of creation (first created are first to take damage)
"""
def main():

	clear()

	#Army creation stage; Army() expects 1 'name' argument
	army1 = Army('Black Templars')
	army1.add_unit(Unit('Crusader Unit(1)'))

	for i in range(10):
		init = create_model_by_name('Initiate')
		init.add_weapon(create_ranged_weapon_by_name('Bolter'))
		army1.units[0].add_model(init)

	army2 = Army('Orks')
	army2.add_unit(Unit('Boyz'))
	army2.add_unit(Unit('Flash Gitz'))

	for i in range(10):
		ork = create_model_by_name('Ork Boy')
		ork.add_weapon(create_ranged_weapon_by_name('Shoota'))
		army2.units[0].add_model(ork)

	for i in range(2):
		ork = create_model_by_name('Flash Git')
		ork.add_weapon(create_ranged_weapon_by_name('Snazzgun'))
		army2.units[1].add_model(ork)

	#Change first move advantage here
	first_move_army = army1
	second_move_army = army2


	#Time delay (in seconds) between output screens
	sleep_time = 6		

	#Start of actual turn loop
	print('STARTING SIMULATION')

	#Turn loop; runs until one army has no more models.
	turn_count = 0
	while army1.alive() and army2.alive():
		clear()
		turn_count += 1

		print('\n--------------START OF TURN REPORT: TURN {}--------------'.format(turn_count))
		print("\n{} report:".format(army1.name))
		print(army1)
		print("\n{} report:".format(army2.name))
		print(army2)
		input("\nPress Enter key to continue...")
		clear()

		print('\n-------------------{} TURN {}-------------------'.format(first_move_army.name.upper(), turn_count))
		army_attack_army(first_move_army, second_move_army)
		input("\n\nPress Enter key to continue...")
		clear()

		if army2.alive():
			print('\n-------------------{} TURN {}-------------------'.format(second_move_army.name.upper(), turn_count))
			army_attack_army(second_move_army, first_move_army)
			input("\n\nPress Enter key to continue...")
			clear()
		
		print('\n-------------------END OF TURN {}-------------------'.format(turn_count))
		input("\n\nPress Enter key to continue...")
		clear()

	if army2.alive():
		print("{} WIN (TURN {})!".format(army2.name.upper(), turn_count))
		print(army2)

	if army1.alive():
		print("{} WIN (TURN {})!".format(army1.name.upper(), turn_count))
		print(army1)



if __name__ == '__main__':
	get_workbook_data()
	main()

