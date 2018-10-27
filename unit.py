class Unit(object):
	"""docstring for Unit"""
	def __init__(self, name, move, weapon_skill, ballistic_skill, strength, toughness, wounds, attacks, leadership, save, invulnerable):
		super(Unit, self).__init__()
		self.name = name
		self.move = move
		self.weapon_skill = weapon_skill
		self.ballistic_skill = ballistic_skill
		self.strength = strength
		self.toughness = toughness
		self.wounds = wounds
		self.attacks = attacks
		self.leadership = leadership
		self.save = save
		self.invulnerable = invulnerable
		self.weapons = []

	def add_weapon(self, weapon):
		self.weapons.append(weapon)