"""Weapon module

Classes:
	Weapon
	RangedWeapon
	MeleeWeapon
"""


class Weapon(object):

	"""Summary.
	
	Weapon objects are stored in a list in Model objects.
	
	Attributes:
		name (str): weapon's name
		strength (int): used to determine minimum roll required successfully wound
		ap (int): armor piercing value; used to determine the minimum roll required to save against a wound
		damage_dice (int): number of dice used to roll damage calculation; 0 indicates the damage value is static (no dice are used)
		damage (int): indicates number of sides of the dice used to roll for damage; simply indicates damage inflicted if damage_dice = 0 
		hit_function: placeholder
		wound_function: placeholder
		save_function: placeholder

	"""
	
	def __init__(self, name, strength, ap, damage_dice, damage, hit_function=None, wound_function=None, save_function=None, damage_function=None):
		"""The constructor for Weapon class objects

		All parameter values are pulled from excel workbook/sheets defined in shooting_sim.py.
		"""
		self.name = name
		self.strength = strength
		self.ap = ap
		self.damage_dice = damage_dice
		self.damage = damage
		self.hit_function = hit_function
		self.wound_function = wound_function
		self.save_function = save_function
		self.damage_function = damage_function

	def __str__(self):
		"""Operator overloading: runs this function on print(Weapon) or str().

		Prints the name, strength, and damage of a weapon
		"""
		return "{}, {}, {}".format(self.name, self.strength, self.damage)

class RangedWeapon(Weapon):
	"""docstring for RangedWeapon"""
	def __init__(self, name, w_range, w_type, shot_dice, shots, strength, ap, damage_dice, damage, hit_function=None, wound_function=None, save_function=None, damage_function=None):
		#Run the __init__ function on yourself of the super/parent of the RangedWeapon class (which is the Weapon class)
		super(RangedWeapon, self).__init__(name, strength, ap, damage_dice, damage, hit_function, wound_function, save_function)
		self.w_range = w_range
		self.w_type = w_type
		self.shot_dice = shot_dice
		self.shots = shots

class MeleeWeapon(Weapon):
	"""docstring for MeleeWeapon"""
	def __init__(self, name, strength, ap, damage_dice, damage, hit_function=None, wound_function=None, save_function=None, damage_function=None, attacks_function=None):
		#Run the __init__ function on yourself of the super/parent of the MeleeWeapon class (which is the Weapon class)
		super(MeleeWeapon, self).__init__(name, strength, ap, damage_dice, damage, hit_function, wound_function, save_function)
		self.attacks_function = attacks_function	#Special attacks_function placeholder since melee weapons can modify a model's attack stat