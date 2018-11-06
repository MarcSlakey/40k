"""Army module

"""

class Army(object):

	"""Class for unit objects.
	
	Attributes:
		name (str): army's name, used solely for output 
		units (Unit): list of this army's Unit-class objects

	"""

	def __init__(self, name='Army Name'):
		"""The constructor for Army class
		
		Parameters:
			name (str): army's name, used solely for output 
			units (Unit): list of this army's Unit objects
		"""
		self.name = name
		self.units = []

	#Operator overloading: runs this function on print(Army) or str()
	#Ultimately prints the number of units alive within the army as well as the models alive within each of those units
	def __str__(self):
		text = 'Army has {} unit(s) left\n'.format(len(self.units_alive()))
		for unit in self.units_alive():
			text += "  {}".format(unit)
		return text

	def add_unit(self, unit):
		self.units.append(unit)

	#Returns the number of units in the army with at least one model alive
	def units_alive(self):
		return [unit for unit in self.units if unit.alive()]

	#Returns true if any units in the army are alive
	def alive(self):
		return len(self.units_alive()) != 0

