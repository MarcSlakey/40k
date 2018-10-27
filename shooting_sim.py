import sys					#Allows sys.exit()
import random				#Allows dice rolling
import openpyxl				#Module for interacting with excel spreadsheet
from unit import Unit
from weapon import Weapon
from squad import Squad
from army import Army


def get_workbook_data(workbook = '40k_sim_workbook.xlsx'):
	wb = openpyxl.load_workbook(workbook)
	global unit_sheet, weapon_sheet
	weapon_sheet = wb.get_sheet_by_name('Templar Ranged Weapons')
	unit_sheet = wb.get_sheet_by_name('Templar Units')

def find_string_in_column(sheet, name, column, starting_row=0):
	return [x.value for x in sheet.columns[column]].index(name, starting_row)

def create_unit_by_name(name):
	NAME_COLUMN = 0
	SEARCH_START_ROW = 2
	name_row = find_string_in_column(unit_sheet, name, NAME_COLUMN, SEARCH_START_ROW)
	print(name_row)
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


def main():
	blue = Army()
	red = Army()

	blue.add_squad(Squad())
	red.add_squad(Squad())

	blue.squads[0].add_unit(create_unit_by_name('Initiate'))
	# red.squads[0].add_unit(Unit())



if __name__ == '__main__':
	get_workbook_data()
	unit1 = create_unit_by_name('Sword Brother')
	print(dir(unit1))
	print(unit1.attacks)
	#main()

