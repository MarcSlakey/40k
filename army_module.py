"""Army module

"""
import unit_module


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
		text = 'Army has {} units in it\n'.format(len(self.units))
		for unit in self.units:
			text += '  {}'.format(unit)
		return text

	def add_unit(self, unit):
		self.units.append(unit)


def create_army1(game):
	army1 = Army('Black Templars')
	army1.add_unit(unit_module.Unit(game, 'Crusader Squad 1'))
	army1.add_unit(unit_module.Unit(game, 'Crusader Squad 2'))
	army1.add_unit(unit_module.Unit(game, 'Dreadnought 1'))
	return army1

def create_army2(game):
	army2 = Army('Orkz')
	army2.add_unit(unit_module.Unit(game, 'Ork Boyz 1'))
	army2.add_unit(unit_module.Unit(game, 'Ork Boyz 2'))
	army2.add_unit(unit_module.Unit(game, 'Ork Boyz 3'))
	army2.add_unit(unit_module.Unit(game, 'Ork Boyz 4'))
	return army2

