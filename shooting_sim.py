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
	row = find_string_in_column(unit_sheet, name, NAME_COLUMN, SEARCH_START_ROW)
	print(row)
	

def main():
	blue = Army()
	red = Army()

	blue.add_squad(Squad())
	red.add_squad(Squad())

	# blue.squads[0].add_unit(Unit())
	# red.squads[0].add_unit(Unit())



if __name__ == '__main__':
	get_workbook_data()
	create_unit_by_name('Initiate')
	#main()

