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
		pass

	def add_unit(self, unit):
		self.units.append(unit)