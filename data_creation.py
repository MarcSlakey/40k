"""data_creation module



"""

import openpyxl			#Module for interacting with excel spreadsheet
from unit import Unit
from weapon import *

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

