"""Data creation module

Locates necessary model and weapon data by name and then creates as well as populates objects based on those names.

Functions:
	get_workbook_data
	find_string_in_column: searches relevant excel sheet for the model/weapon name and returns the row # where that name was found
	create_model_by_name: uses find_string_in_column() to generate a Model object
	create_ranged_weapon_by_name: uses find_string_in_column() to generate a Weapon object
"""

import openpyxl			#Module for interacting with excel spreadsheet
from settings import *
from sprites import Model
from weapon import *

def get_workbook_data(workbook = '40k_sim_workbook.xlsx'):
	wb = openpyxl.load_workbook(workbook)
	global model_sheet, ranged_weapon_sheet
	ranged_weapon_sheet = wb.get_sheet_by_name('Templar Ranged Weapons')
	model_sheet = wb.get_sheet_by_name('Templar Models')


def find_string_in_column(sheet, name, column, starting_row=0):
	'''Finds the given string ('name') in the relevant Excel sheet and returns its row number.
	
	Works by using .index(search_term, search_start_position).
	(not 100% that that is how this works)
	'''
	return [x.value for x in sheet.columns[column]].index(name, starting_row)


def create_model_by_name(name, game, x, y):
	"""Creates a model object and populates it.

	Uses find_string_in_column() to locate the given model's name in the relevant Excel sheet, creates a Model object named
		the same as the search term, and populates it with the rest of the contents of the term's row.
	"""
	NAME_COLUMN = 0
	SEARCH_START_ROW = 2
	name_row = find_string_in_column(model_sheet, name, NAME_COLUMN, SEARCH_START_ROW)
	model_row = model_sheet.rows[name_row]
	return Model(
		game = game,
		x = x,
		y = y,
		name = model_row[0].value,
		move = model_row[1].value * TILESIZE,
		weapon_skill = model_row[2].value,
		ballistic_skill = model_row[3].value,
		strength = model_row[4].value,
		toughness = model_row[5].value,
		wounds = model_row[6].value,
		attacks = model_row[7].value,
		leadership = model_row[8].value,
		save = model_row[9].value,
		invulnerable = model_row[10].value,
		radius = model_row[11].value
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
		w_range = weapon_row[1].value * TILESIZE,
		w_type = weapon_row[2].value,
		shot_dice = weapon_row[3].value,
		shots = weapon_row[4].value,
		strength = weapon_row[5].value,
		ap = weapon_row[6].value,
		damage_dice = weapon_row[7].value,
		damage = weapon_row[8].value
	)

def create_melee_weapon_by_name(name):
	"""Creates a MeleeWeapon object and populates it.

	Uses find_string_in_column() to locate the given weapon's name in the relevant Excel sheet, creates a RangedWeapon object named
		the same as the search term, and populates it with the rest of the contents of the term's row.
	"""
	NAME_COLUMN = 0
	SEARCH_START_ROW = 2
	name_row = find_string_in_column(ranged_weapon_sheet, name, NAME_COLUMN, SEARCH_START_ROW)
	weapon_row = ranged_weapon_sheet.rows[name_row]
	return RangedWeapon(
		name = weapon_row[0].value,
		strength = weapon_row[1].value,
		ap = weapon_row[2].value,
		damage_dice = weapon_row[3].value,
		damage = weapon_row[4].value
	)
