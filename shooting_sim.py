import sys					#Allows sys.exit()
import random				#Allows dice rolling
import openpyxl				#Module for interacting with excel spreadsheet
from unit import Unit
from weapon import *
from squad import Squad
from army import Army


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


def main():
	blue = Army()
	blue.add_squad(Squad())
	blue.squads[0].add_unit(create_unit_by_name('Initiate'))
	blue.squads[0].units[0].add_weapon(create_ranged_weapon_by_name('Bolter'))

	red = Army()
	red.add_squad(Squad())
	red.squads[0].add_unit(create_unit_by_name('Initiate'))
	red.squads[0].units[0].add_weapon(create_ranged_weapon_by_name('Bolter'))

	red.squads[0].units[0].attack_with_weapon(0, blue.squads[0])

if __name__ == '__main__':
	get_workbook_data()
	main()

