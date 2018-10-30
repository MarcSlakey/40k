"""40k small-scale battle simulator

Allows for custom creation of two armies with any amount of squads and units.
Structured with nested classe objects: Army > Squad > Unit > Weapon.
Armies, squads, units, and weapons are all chosen in the main() function of this module.
Units are individually assigned weapons (currently no limit).
Units are automatically targetted and killed in the order in which they were created.
Additionally, units fire their weapons in the order in which they were created.
Which army moves first can be changed just above main()

Currently only handles one of the four 40k turn phases: the shooting phase.

Functions:
	get_workbook_data
	find_string_in_column: searches relevant excel sheet for the unit/weapon name and returns the row # where that name was found
	create_unit_by_name: uses find_string_in_column() to generate a Unit object
	create_ranged_weapon_by_name: uses find_string_in_column() to generate a Weapon object
	army_attack_army: Makes each unit in a given army fire its weapon until either every unit has fired all of its shots or the enemy army is dead
	countdown_timer: counts down the time until the program will proceed to the next information screen
"""


import os 					#Allows clearing command prompt output with clear()
import sys					#Allows sys.exit()
import random				#Allows dice rolling
import openpyxl				#Module for interacting with excel spreadsheet
from time import sleep		#Allows delay
from unit import Unit
from weapon import *
from squad import Squad
from army import Army

clear = lambda: os.system('cls')


def get_workbook_data(workbook = '40k_sim_workbook.xlsx'):
	wb = openpyxl.load_workbook(workbook)
	global unit_sheet, ranged_weapon_sheet
	ranged_weapon_sheet = wb.get_sheet_by_name('Templar Ranged Weapons')
	unit_sheet = wb.get_sheet_by_name('Templar Units')


def find_string_in_column(sheet, name, column, starting_row=0):
	'''Finds the given string ('name') in the relevant Excel sheet and returns its row number.
	
	Works by using .index(search_term, search_start_position).
	(not 100% that that is how this works)
	'''
	return [x.value for x in sheet.columns[column]].index(name, starting_row)


def create_unit_by_name(name):
	"""Creates a unit object and populates it.

	Uses find_string_in_column() to locate the given unit's name in the relevant Excel sheet, creates a Unit object named
		the same as the search term, and populates it with the rest of the contents of the term's row.
	"""
	NAME_COLUMN = 0
	SEARCH_START_ROW = 2
	name_row = find_string_in_column(unit_sheet, name, NAME_COLUMN, SEARCH_START_ROW)
	unit_row = unit_sheet.rows[name_row]
	return Unit(
		name = unit_row[0].value,
		move = unit_row[1].value,
		weapon_skill = unit_row[2].value,
		ballistic_skill = unit_row[3].value,
		strength = unit_row[4].value,
		toughness = unit_row[5].value,
		wounds = unit_row[6].value,
		attacks = unit_row[7].value,
		leadership = unit_row[8].value,
		save = unit_row[9].value,
		invulnerable = unit_row[10].value
	)


def create_ranged_weapon_by_name(name):
	"""Creates a RangedWeapon object and populates it.

	Uses find_string_in_column() to locate the given weapon's name in the relevant Excel sheet, creates a RangedWeapon object named
		the same as the search term, and populates it with the rest of the contents of the term's row.
	"""
	NAME_COLUMN = 0
	SEARCH_START_ROW = 2
	name_row = find_string_in_column(ranged_weapon_sheet, name, NAME_COLUMN, SEARCH_START_ROW)
	weapon_row = ranged_weapon_sheet.rows[name_row]
	return RangedWeapon(
		name = weapon_row[0].value,
		w_range = weapon_row[1].value,
		w_type = weapon_row[2].value,
		shot_dice = weapon_row[3].value,
		shots = weapon_row[4].value,
		strength = weapon_row[5].value,
		ap = weapon_row[6].value,
		damage_dice = weapon_row[7].value,
		damage = weapon_row[8].value
	)


def army_attack_army(army1, army2):
	"""Makes all of one army's units attack the opposing army's squads.

	Iterates through Squads, Units, and Weapons in creation order.
	Units will attack with all their weapons. (This assumes armies are only attacking in ranged phase) 
	"""
	for squad in army1.squads_alive():
		for unit in squad.units_alive():
			for i in range(len(unit.weapons)):			#There's probably a better way to do this
				if not army2.alive():
					return
				unit.attack_with_weapon(i, army2.squads_alive()[0])


def countdown_timer(sleep_time):
	count = sleep_time
	print('\n')
	for i in range(sleep_time):
		print('Changing screens in: {}'.format(count), end='\r', flush=True)
		count -= 1
		sleep(1)


"""Main loop; runs army creation and loops until at least one army has no more units left.

Define squads and units in main().
(army1/army2).add_squad(Squad('Name')) to make new squad.
Must make new "for" loop for each type of unit within a given squad.
Squads and units take damage in order of creation (first created are first to take damage)
"""
def main():

	clear()

	#Army creation stage; Army() expects 1 'name' argument
	army1 = Army('Black Templars')
	army1.add_squad(Squad('Crusader Squad(1)'))

	for i in range(10):
		init = create_unit_by_name('Initiate')
		init.add_weapon(create_ranged_weapon_by_name('Bolter'))
		init.add_weapon(create_ranged_weapon_by_name('Bolt pistol'))
		army1.squads[0].add_unit(init)

	army2 = Army('Orks')
	army2.add_squad(Squad('Boyz'))
	army2.add_squad(Squad('Flash Gitz'))

	for i in range(10):
		ork = create_unit_by_name('Ork Boy')
		ork.add_weapon(create_ranged_weapon_by_name('Shoota'))
		army2.squads[0].add_unit(ork)

	for i in range(2):
		ork = create_unit_by_name('Flash Git')
		ork.add_weapon(create_ranged_weapon_by_name('Snazzgun'))
		army2.squads[1].add_unit(ork)

	#Change first move advantage here
	first_move_army = army1
	second_move_army = army2

	#Time delay (in seconds) between output screens
	sleep_time = 6		

	#Start of actual turn loop
	print('STARTING SIMULATION')

	#Turn loop; runs until one army has no more units.
	turn_count = 0
	while army1.alive() and army2.alive():
		clear()
		turn_count += 1

		print('\n--------------REPORT: TURN {}--------------'.format(turn_count))
		sleep(2)
		print("{} report:".format(army1.name))
		print(army1)
		print("\n{} report:".format(army2.name))
		print(army2)
		countdown_timer(sleep_time)
		print("\nstarting turn...")
		sleep(2)
		clear()

		print('\n--------------{} TURN {}--------------'.format(first_move_army.name.upper(), turn_count))
		army_attack_army(first_move_army, second_move_army)
		countdown_timer(sleep_time)
		clear()

		if army2.alive():
			print('\n--------------{} TURN {}--------------'.format(second_move_army.name.upper(), turn_count))
			army_attack_army(second_move_army, first_move_army)
			countdown_timer(sleep_time)
			clear()
		
		print('\n--------------END OF TURN {}--------------'.format(turn_count))
		countdown_timer(sleep_time)
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

