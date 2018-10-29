import random

class Squad(object):
	"""docstring for Squad"""
	def __init__(self, name):
		self.name = name
		self.units = []

	#Operator overloading: runs this function on print(Squad) or str()
	#Prints the number of units alive within the squad as well as the wounds remaining on those units
	def __str__(self):
		text = "{} has {} unit(s) left\n".format(self.name, len(self.units_alive()))
		for unit in self.units_alive():
			text += "    {}\n".format(unit)
		return text

	def add_unit(self, unit):
		self.units.append(unit)

	def save_against_wound(self, weapon):
		if not self.alive():
			return

		#Wounds units in load order (units loaded first will die first)
		self.units_alive()[0].unit_save_against_wound(weapon)

	#Returns the number of units alive in the squad
	def units_alive(self):
		return [unit for unit in self.units if unit.alive()]

	#Returns true as long as at least one unit is alive in the given squad
	def alive(self):
		return len(self.units_alive()) != 0