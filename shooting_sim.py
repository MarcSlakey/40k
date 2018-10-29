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
	return [x.value for x in sheet.columns[column]].index(name, starting_row)

def create_unit_by_name(name):
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
	for squad in army1.squads_alive():
		for unit in squad.units_alive():
			if not army2.alive():
				return
			unit.attack_with_weapon(0, army2.squads_alive()[0])

"""
Define squads and units in main().
army1/army2.add_squad(Squad('Squad Name')) to make new squad.
Must make new "for" loop for each type of unit within a given squad.
Squads and units take damage in order of creation (first created are first to take damage)
"""
def main():
	clear()
	#Army creation stage; Army() expects 1 'name' argument
	army1 = Army('Black Templars')
	army1.add_squad(Squad('Crusader Squad(1)'))
	army1.add_squad(Squad('Crusader Squad(2)'))

	for i in range(5):
		init = create_unit_by_name('Initiate')
		init.add_weapon(create_ranged_weapon_by_name('Bolter'))
		army1.squads[0].add_unit(init)

	for i in range(5):
		init = create_unit_by_name('Initiate')
		init.add_weapon(create_ranged_weapon_by_name('Bolter'))
		army1.squads[1].add_unit(init)

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
	#Time delay (in seconds) between screens
	sleep_time = 6

	#Start of actual turn loop
	print('STARTING SIMULATION')

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
		sleep(sleep_time)
		print("starting turn...")
		sleep(2)
		clear()
		print('\n--------------{} TURN {}--------------'.format(first_move_army.name.upper(), turn_count))
		army_attack_army(first_move_army, second_move_army)
		sleep(sleep_time)
		if army2.alive():
			clear()
			print('\n--------------{} TURN {}--------------'.format(second_move_army.name.upper(), turn_count))
			army_attack_army(second_move_army, first_move_army)
			sleep(sleep_time)
		print('\n--------------END OF TURN {}--------------'.format(turn_count))
		sleep(2)

	print()

	if army2.alive():
		print("{} TEAM WON!".format(army2.name.upper())
		print(army2)

	if army1.alive():
		print("{} TEAM WON!".format(army1.name..upper())
		print(army1)



if __name__ == '__main__':
	get_workbook_data()
	main()

