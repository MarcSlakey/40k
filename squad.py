import random

class Squad(object):
	"""docstring for Squad"""
	def __init__(self, name="dumbos"):
		self.name = name
		self.units = []

	def add_unit(self, unit):
		self.units.append(unit)

	def save_against_wound(self, weapon):
		if not self.alive():
			return

		#Wounds units in load order (units loaded first will die first)
		self.units_alive()[0].unit_save_against_wound(weapon)

	def units_alive(self):
		return [unit for unit in self.units if unit.alive()]

	def alive(self):
		return len(self.units_alive()) != 0

	def __str__(self):
		text = "Squad has {} unit(s) left\n".format(len(self.units_alive()))
		for unit in self.units_alive():
			text += "  {}\n".format(unit)
		return text
