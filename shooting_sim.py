import sys					#Allows sys.exit()
import random				#Allows dice rolling
import openpyxl				#Module for interacting with excel spreadsheet
from unit import Unit
from weapon import Weapon
from squad import Squad
from army import Army

def get_workbook_data(workbook = '40k_sim_workbook.xlsx'):
	wb = openpyxl.load_workbook(workbook)
	weapon_sheet = wb.get_sheet_by_name('Templar Ranged Weapons')
	unit_sheet = wb.get_sheet_by_name('Templar Units')

def main():
	blue = Army()
	red = Army()

	blue.add_squad(Squad())
	red.add_squad(Squad())



if __name__ == '__main__':
	main()

