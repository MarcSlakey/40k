import random

class Squad(object):
	"""docstring for Squad"""
	def __init__(self):
		self.units = []

	def add_unit(self, unit):
		self.units.append(unit)

	def save_against_wound(self, weapon):
		#Wounds units in load order (units loaded first will die first)
		self.units_alive()[0].unit_save_against_wound(weapon)

	def units_alive(self):
		return [unit for unit in self.units if unit.alive()]

	def alive(self):
		return len(self.units_alive()) != 0