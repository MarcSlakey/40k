import random
from weapon import *

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

	def attack_with_weapon(self, weapon_index, target_squad):
		weapon_used = self.weapons[weapon_index]
		if isinstance(weapon_used, RangedWeapon):
			if weapon_used.shot_dice == 0:
				shot_count = weapon_used.shots
			else:
				shot_count = 0
				for i in range(weapon_used.shot_dice):
					roll = random.randint(1, weapon_used.shots)
					shot_count += roll 
			
		elif isinstance(weapon_used, MeleeWeapon):
			#TODO
			pass

		print('{} takes {} shots against {} with {}.'.format(self.name, shot_count, target_squad, weapon_used.name))

		for i in range(shot_count):
			print('Taking shot {}'.format(i))
			self.single_shot(weapon_used, target_squad)

	def unit_save_against_wound(self, weapon):
		roll = random.randint(1,6)
		if (self.invulnerable == None) or (self.invulnerable <= self.save):
			if roll >= self.save + weapon.ap:
				print('{} saved against {} wound.'.format(self.name, weapon.name))
				return
		else:
			if roll >= self.invulnerable:
				print('{} saved against {} wound.'.format(self.name, weapon.name))
				return

		if weapon.damage_dice == 0:
			self.wounds -= weapon.damage
			print('{} took {} damage from {} .'.format(self.name, weapon.damage, weapon.name))
		else:
			for i in range(weapon.damage_dice):
				roll = random.randint(1, weapon.damage)
				self.wounds -= roll
				print('{} took {} damage from {} .'.format(self.name, roll, weapon.name))



	def single_shot(self, weapon, target_squad):
		roll = random.randint(1,6)
		if roll < self.ballistic_skill:
			print('{} missed single shot with {}.'.format(self.name, weapon.name))
			return

		# target_squad.hit_with_weapon(weapon)

		roll = random.randint(1,6)
		#Target toughness is always homogeneous within a squad
		target_toughness = target_squad.units[0].toughness
		if weapon.strength >= 2*target_toughness:
			wound_roll = 2
		elif weapon.strength > target_toughness:
			wound_roll = 3
		elif weapon.strength == target_toughness:
			wound_roll = 4
		elif weapon.strength < target_toughness:
			wound_roll = 5
		elif weapon.strength <= target_toughness/2:
			wound_roll = 6

		if roll < wound_roll:
			print('{} single shot with {} failed to wound.'.format(self.name, weapon.name))
			return

		target_squad.save_against_wound(weapon)

