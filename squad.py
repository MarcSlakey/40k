"""Summary

"""

import random

class Squad(object):

	"""
	
	Attributes:
		name (str): squad's name, used solely for output 
		squads (Unit): list of this squad's Unit-class objects

	"""
	
	def __init__(self, name=''):
		"""Summary.


		"""
		self.name = name
		self.units = []

	def __str__(self):
		"""Operator overloading: runs this function on print(Squad) or str()
		
		Prints the number of units alive within the squad as well as the wounds remaining on those units
		"""
		text = '{} has {} unit(s) left\n'.format(self.name, len(self.units_alive()))
		for unit in self.units_alive():
			text += "    {}\n".format(unit)
		return text

	def add_unit(self, unit):
		"""Adds a Unit-class object to the squad's list of units"""
		self.units.append(unit)

	def save_against_wound(self, weapon):
		"""Summary."""
		if not self.alive():
			return

		#Wounds units in load order (units loaded first will die first)
		self.units_alive()[0].unit_save_against_wound(weapon)

	def units_alive(self):
		"""Returns the number of units alive in the squad"""
		return [unit for unit in self.units if unit.alive()]

	def alive(self):
		"""Returns true as long as at least one unit is alive in the given squad."""
		return len(self.units_alive()) != 0