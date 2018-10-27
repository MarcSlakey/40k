#This is the weapon class for the basic 40k sim

class Weapon(object):
	"""docstring for Weapon"""
	def __init__(self, name, w_range, w_type, shot_dice, shots, strength, ap, damage_dice, damage, hit_function=None, wound_function=None, save_function=None):
		self.name = name
		self.w_range = w_range
		self.w_type = w_type
		self.shot_dice = shot_dice
		self.shots = shots
		self.strength = strength
		self.ap = ap
		self.damage_dice = damage_dice
		self.damage = damage
		self.hit_function = hit_function
		self.wound_function = wound_function
		self.save_function = save_function