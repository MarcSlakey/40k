import pygame, random
from os import path
from math import *
from settings import *
from ray_casting import *

vec = pygame.math.Vector2		# Pygame's vector functions (Vector2 indicates 2-dimensional vector)
								#	Example usage: self.vel = pygame.math.Vector2(x, y)
								#	or with this assignment, self.vel = vect(x, y)

def find_hypotenuse(x, y):
	hypotenuse = sqrt(x*x + y*y)
	return hypotenuse

class Spritesheet:
	# utility class for loading and parsing spritesheets
	def __init__(self, filename):
		self.spritesheet = pygame.image.load(filename).convert()

	def get_image(self, x, y, width, height):
		# grab a particular image off the spritesheet
		image = pygame.Surface((width, height))
		image.blit(self.spritesheet, (0,0), (x, y, width, height))
		return image

class Model(pygame.sprite.Sprite):

	""" Model class
	
	Model sprite object. Basic game unit used to represent a single tabletop model. 

	Attributes:
		game: game to which this sprite belongs
		name: string name of sprite
		groups: sets the list of groups that contain this sprite
		image:
		rect:
		x: spawn coordinates; allows initializing with a tile number which is then converted to pixels
		y: same as above
		rect.center: the location of the sprite's center point
		original_pos: tuple to store the sprite's start of turn location
		radius: represents the model's base in the tabletop game
		dest_x: stores mouse click location during movements
		dest_y: same as above
		shot_dest_x: placeholder attribute that allows crude shooting; should probably be in a different class later
		shot_dest_y: same as above
		weapon_range: same as above
		max_move: a model's moves are subtracted from this value during the move phase
		original_max_move: tuple; stores the max_move so it can be reset 
		charge_move: distance the model can move during charge phase. This is rolled (D6) each time a new charge is declared.

	"""
	
	def __init__(self, game, x, y, name, move, weapon_skill, ballistic_skill, strength, toughness, wounds, attacks, leadership, save, invulnerable, radius):
		self.groups = [game.all_sprites, game.all_models]	
		pygame.sprite.Sprite.__init__(self, self.groups)			#always needed for basic sprite functionality
		self.game = game
		#image_surf = pygame.image.load(path.join(self.game.img_dir, 'marine_bolter_cropped.png')).convert()
		#self.image = pygame.transform.scale(image_surf, (26, 35))
		self.image = pygame.image.load(path.join(self.game.img_dir, 'Ork Slugga 3.png')).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.radius = radius 		#represents the model's base size

		self.melee_ratio = (self.radius + TILESIZE/2)/self.radius 			#the coefficient by which the radius can be multiplied to achieve the base radius + 1/2 inch
		self.true_melee_ratio = (self.radius + TILESIZE)/self.radius 		#the coefficient by which the radius can be multiplied to achieve the base radius + 1/2 inch
		self.melee_radius = int(self.radius * self.melee_ratio)				#gives half the melee radius (1/2 inch) to each sprite to simulate 1" melee radius
		self.true_melee_radius = int(self.radius * self.true_melee_ratio) 	#the "true" 1" melee radius, used for display purposes

		self.cohesion_ratio = (self.radius + TILESIZE)/self.radius 			#the coefficient by which the radius can be mulitplied to achieve the base radius + one inch
		self.true_cohesion_ratio = (self.radius + 2*TILESIZE)/self.radius
		self.cohesion_radius = int(self.radius * self.cohesion_ratio)		#gives half the cohesion radius (1 inch) to each sprite to simulate 2" cohesion radius
		self.true_cohesion_radius = int(self.radius * self.true_cohesion_ratio) #the "true" 2" cohesion radius
		
		self.vx, self.vy = (0, 0)
		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.rect.center = (self.x, self.y)
		self.original_pos = (self.x, self.y)

		self.dest_x = self.x
		self.dest_y = self.y
		self.shot_dest_x = 0
		self.shot_dest_y = 0
		self.speed = 1
		self.rot = 0
		self.vel = vec(0,0)
		self.acc = vec(0,0)

		self.name = name
		self.max_move = move 	#multiplied by TILESIZE in data_creation
		self.original_max_move = move
		self.weapon_skill = weapon_skill
		self.ballistic_skill = ballistic_skill
		self.strength = strength
		self.toughness = toughness
		self.wounds = wounds
		self.attacks = attacks
		self.leadership = leadership
		self.save = save
		self.invulnerable = invulnerable
		self.ranged_weapons = []
		self.melee_weapons = []
		self.unit = None

		self.valid_shots = []	# List of valid shooting targets
		self.enemies_within_melee = []		#List of enemy models within 1"
		self.squadmates_within_melee = []	#List of models in same unit within 1"
		self.combined_melee = []			#List of all the MODELS this model can target (see main.py multiple_melee_selection)
		self.melee_unit_targets = []		#List of all UNITS which this model can attack during the fight phase (see main.py multiple_melee_selection)

		self.charge_move = 0
		self.pile_in_move = 3*TILESIZE
		self.pile_in_move_max = 3*TILESIZE
		self.consolidate_move = 3*TILESIZE
		self.consolidate_move_max = 3*TILESIZE


		#Special flags
		self.cohesion = True
		self.in_melee = False
		self.fought = False
		self.charged = False
		self.advanced = False
		self.fell_back = False
		

	def __str__(self):
		text = '{}'.format(self.name)
		return text

	def add_ranged_weapon(self, weapon):
		"""Adds a weapon to a given model's list of weapons"""
		self.ranged_weapons.append(weapon)

	def add_melee_weapon(self, weapon):
		self.melee_weapons.append(weapon)

	def die(self):
		if self.game.selected_unit != None:
			if self in self.game.selected_unit.valid_shots:
				self.game.selected_unit.valid_shots.remove(self)

		for model in self.game.selectable_models:
			if self in model.valid_shots:
				model.valid_shots.remove(self)

		self.unit.models.remove(self)
		if self.game.current_phase != "Morale Loss Allocation":
			self.unit.recent_deaths.append(self)
			print("[{}] died!".format(self.name))
		elif self.game.current_phase == "Morale Loss Allocation":
			print("[{}] flees in fear!".format(self.name))
		self.kill()

	def update(self):
		if self.wounds <= 0:
			self.die()

		if self.game.current_phase == "Movement Phase":
			if self.valid_shots != None:
				self.valid_shots.clear()

			temp_x = self.x	
			temp_y = self.y
			current_move = 0
			self.cohesion = False

			def revert_move():
				self.x = temp_x
				self.y = temp_y
				self.rect.center = (self.x, self.y)
				self.dest_x = self.x
				self.dest_y = self.y
				#print("Coordinates reverted to ({},{})".format(self.x, self.y))

			#Performs movement once destination is set by mouse event input
			if self.dest_x != self.x and self.dest_y != self.y:
				#print("\n\n-------NEW STEP-------")
				#print("Pre-move coord: ({},{})".format(self.x, self.y))
				delta_x = self.x - self.dest_x
				delta_y = self.y - self.dest_y
				current_move = find_hypotenuse(delta_x, delta_y)
				"""
				print("Current coordinates: {},{}".format(self.x, self.y))
				print("Target coordinate: {},{}".format(self.dest_x, self.dest_y))
				print("delta_x: {} pixels".format(delta_x))
				print("delta_y: {} pixels".format(delta_y))
				print("delta hypot: {} pixels".format(current_move))
				"""

				#Attempts to move the model if the desired move is within the unit's max move
				if self.max_move > 0:
					model_pos = vec(self.x, self.y)
					dest_pos = vec(self.dest_x, self.dest_y)
					self.rot = (dest_pos - model_pos).angle_to(vec(1,0))	#Calculates the angle between desired vector and basic x vector
					self.acc = vec(self.speed, 0).rotate(-self.rot)		#Sets the acceleration vector's to angle and magnitude
					self.acc += self.vel * -.4	#Friction coefficient; the higher the velocity, the higher this number is.
					self.vel += self.acc

					#print("\nRot: {}, Acc: {}, Vel: {}".format(self.rot, self.acc, self.vel))
					#print("Velocity vector magnitude: {}".format(find_hypotenuse(self.vel[0], self.vel[1])))

					pixels_x = int(self.vel[0])
					pixels_y = int(self.vel[1])
					distance_moved = find_hypotenuse(pixels_x, pixels_y)

					self.x += pixels_x
					self.y += pixels_y
					self.rect.center = (self.x, self.y)

					#Model base collision
					for sprite_x in self.game.all_models:
						if sprite_x != self:
							if pygame.sprite.collide_circle(self, sprite_x):
								print("\n!Collision with between self and {}!".format(sprite_x.name))
								revert_move()

					#Melee collision
					for sprite in self.game.targets:
						if pygame.sprite.collide_circle_ratio(self.game.melee_ratio(self, sprite))(self, sprite):
							print("\n!Collision with between self and enemy melee radius!")
							revert_move()

					#Terrain collision
					for sprite_x in self.game.walls:
						if pygame.sprite.collide_rect(self, sprite_x):
							print("\n!Collision with between self and terrain!")
							revert_move()

					#Max move reduced if model moved at all
					if self.x != temp_x or self.y != temp_y:	
						self.max_move -= distance_moved
						#print("\nSuccessful move!")
						#print("Max move reduced by {} (rounded velocity hypotenuse)".format(distance_moved))
						#print("Max move Remaining: {}".format(self.max_move))
						#print("\nPost-move coord: ({},{})".format(self.x, self.y))
					else:
						pass
						#print("\nFailed move.")
						#print("Coordinates unchanged.")
					
				else:
					print("\nMOVE HALTED: Current move of {} > Remaining max move of {}".format(current_move, self.max_move))
					self.dest_x = self.x
					self.dest_y = self.y

			else:
				self.dest_x = self.x
				self.dest_y = self.y
				self.rect.center = (self.x, self.y)

			#Unit cohesion checker
			for sprite in self.unit.models:
				if sprite != self and pygame.sprite.collide_circle_ratio(self.cohesion_ratio)(self, sprite):
					self.cohesion = True
				elif len(self.unit.models) <= 1:
					self.cohesion = True

		elif self.game.current_phase == "Shooting Phase":
			pass
			"""
			if self.game.selected_model == self:
				print("A model is selected")
				if not self.valid_shots:
					print("Valid shots is empty")
					x = 1
					for target in self.game.targets:
						Ray(self.game, self, target, (self.x, self.y), (target.x, target.y)).cast()
						print("{}".format(x))
						x += 1
			"""

		elif self.game.current_phase == "Charge Move":
			temp_x = self.x	
			temp_y = self.y
			current_move = 0
			self.cohesion = False

			def revert_move():
				self.x = temp_x
				self.y = temp_y
				self.rect.center = (self.x, self.y)
				self.dest_x = self.x
				self.dest_y = self.y
				#print("Coordinates reverted to ({},{})".format(self.x, self.y))

			if self.dest_x != self.x and self.dest_y != self.y:
				#print("\n\n-------NEW STEP-------")
				#print("Pre-move coord: ({},{})".format(self.x, self.y))
				delta_x = self.x - self.dest_x
				delta_y = self.y - self.dest_y
				current_move = find_hypotenuse(delta_x, delta_y)
				"""
				print("Current coordinates: {},{}".format(self.x, self.y))
				print("Target coordinate: {},{}".format(self.dest_x, self.dest_y))
				print("delta_x: {} pixels".format(delta_x))
				print("delta_y: {} pixels".format(delta_y))
				print("delta hypot: {} pixels".format(current_move))
				"""

				#Attempts to move the model if the desired move is within the unit's max move
				if self.charge_move > 0:
					model_pos = vec(self.x, self.y)
					dest_pos = vec(self.dest_x, self.dest_y)
					self.rot = (dest_pos - model_pos).angle_to(vec(1,0))	#Calculates the angle between desired vector and basic x vector
					self.acc = vec(self.speed, 0).rotate(-self.rot)		#Sets the acceleration vector's to angle and magnitude
					self.acc += self.vel * -.4	#Friction coefficient; the higher the velocity, the higher this number is.
					self.vel += self.acc

					#print("\nRot: {}, Acc: {}, Vel: {}".format(self.rot, self.acc, self.vel))
					#print("Velocity vector magnitude: {}".format(find_hypotenuse(self.vel[0], self.vel[1])))

					pixels_x = int(self.vel[0])
					pixels_y = int(self.vel[1])
					distance_moved = find_hypotenuse(pixels_x, pixels_y)

					self.x += pixels_x
					self.y += pixels_y
					self.rect.center = (self.x, self.y)

					#Model base collision
					for sprite_x in self.game.all_models:
						if sprite_x != self:
							if pygame.sprite.collide_circle(self, sprite_x):
								#print("\n!Collision with between self and model!")
								revert_move()
								
					#Melee collision
					for sprite in self.game.targets:
						if sprite.unit != self.game.charge_target_unit:
							if pygame.sprite.collide_circle_ratio(self.game.melee_ratio(self, sprite))(self, sprite):
								print("\n!Collision between self and enemy melee radius!")
								revert_move()

					#Terrain collision
					for sprite_x in self.game.walls:
						if pygame.sprite.collide_rect(self, sprite_x):
							#print("\n!Collision with between self and terrain!")
							revert_move()

					#Max move reduced if model moved at all
					if self.x != temp_x or self.y != temp_y:	
						self.charge_move -= distance_moved
						#print("\nSuccessful move!")
						#print("Max move reduced by {} (rounded velocity hypotenuse)".format(distance_moved))
						#print("Max move Remaining: {}".format(self.charge_move))
						#print("\nPost-move coord: ({},{})".format(self.x, self.y))
					else:
						pass
						#print("\nFailed move.")
						#print("Coordinates unchanged.")

				else:
					#print("\nMOVE CANCELED: Current move of {} > Remaining max move of {}".format(current_move, self.charge_move))
					self.dest_x = self.x
					self.dest_y = self.y

			else:
				self.dest_x = self.x
				self.dest_y = self.y
				self.rect.center = (self.x, self.y)

			#Unit cohesion checker
			for sprite in self.unit.models:
				if sprite != self and pygame.sprite.collide_circle_ratio(self.cohesion_ratio)(self, sprite):
					self.cohesion = True
				elif len(self.unit.models) <= 1:
					self.cohesion = True

		elif self.game.current_phase == "Pile In":
			temp_x = self.x	
			temp_y = self.y
			current_move = 0
			self.cohesion = False

			def revert_move():
				self.x = temp_x
				self.y = temp_y
				self.rect.center = (self.x, self.y)
				self.dest_x = self.x
				self.dest_y = self.y
				#print("Coordinates reverted to ({},{})".format(self.x, self.y))

			if self.dest_x != self.x and self.dest_y != self.y:
				#print("\n\n-------NEW STEP-------")
				#print("Pre-move coord: ({},{})".format(self.x, self.y))
				delta_x = self.x - self.dest_x
				delta_y = self.y - self.dest_y
				current_move = find_hypotenuse(delta_x, delta_y)
				"""
				print("Current coordinates: {},{}".format(self.x, self.y))
				print("Target coordinate: {},{}".format(self.dest_x, self.dest_y))
				print("delta_x: {} pixels".format(delta_x))
				print("delta_y: {} pixels".format(delta_y))
				print("delta hypot: {} pixels".format(current_move))
				"""

				#Attempts to move the model if the desired move is within the unit's max move
				if self.pile_in_move > 0:
					model_pos = vec(self.x, self.y)
					dest_pos = vec(self.dest_x, self.dest_y)
					self.rot = (dest_pos - model_pos).angle_to(vec(1,0))	#Calculates the angle between desired vector and basic x vector
					self.acc = vec(self.speed, 0).rotate(-self.rot)		#Sets the acceleration vector's to angle and magnitude
					self.acc += self.vel * -.4	#Friction coefficient; the higher the velocity, the higher this number is.
					self.vel += self.acc

					#print("\nRot: {}, Acc: {}, Vel: {}".format(self.rot, self.acc, self.vel))
					#print("Velocity vector magnitude: {}".format(find_hypotenuse(self.vel[0], self.vel[1])))

					pixels_x = int(self.vel[0])
					pixels_y = int(self.vel[1])
					distance_moved = find_hypotenuse(pixels_x, pixels_y)

					self.x += pixels_x
					self.y += pixels_y
					self.rect.center = (self.x, self.y)

					#Model base collision
					for sprite_x in self.game.all_models:
						if sprite_x != self:
							if pygame.sprite.collide_circle(self, sprite_x):
								#print("\n!Collision with between self and model!")
								revert_move()

					#Terrain collision
					for sprite_x in self.game.walls:
						if pygame.sprite.collide_rect(self, sprite_x):
							print("\n!Collision with between self and terrain!")
							revert_move()

					#Max move reduced if model moved at all
					if self.x != temp_x or self.y != temp_y:	
						self.pile_in_move -= distance_moved
						#print("\nSuccessful move!")
						#print("Max move reduced by {} (rounded velocity hypotenuse)".format(distance_moved))
						#print("Max move Remaining: {}".format(self.charge_move))
						#print("\nPost-move coord: ({},{})".format(self.x, self.y))
					else:
						pass
						#print("\nFailed move.")
						#print("Coordinates unchanged.")

				else:
					#print("\nMOVE CANCELED: Current move of {} > Remaining max move of {}".format(current_move, self.pile_in_move))
					self.dest_x = self.x
					self.dest_y = self.y

			else:
				self.dest_x = self.x
				self.dest_y = self.y
				self.rect.center = (self.x, self.y)

			#Unit cohesion checker
			for sprite in self.unit.models:
				if sprite != self and pygame.sprite.collide_circle_ratio(self.cohesion_ratio)(self, sprite):
					self.cohesion = True
				elif len(self.unit.models) <= 1:
					self.cohesion = True

		elif self.game.current_phase == "Consolidate":
			temp_x = self.x	
			temp_y = self.y
			current_move = 0
			self.cohesion = False

			def revert_move():
				self.x = temp_x
				self.y = temp_y
				self.rect.center = (self.x, self.y)
				self.dest_x = self.x
				self.dest_y = self.y
				#print("Coordinates reverted to ({},{})".format(self.x, self.y))

			if self.dest_x != self.x and self.dest_y != self.y:
				#print("\n\n-------NEW STEP-------")
				#print("Pre-move coord: ({},{})".format(self.x, self.y))
				delta_x = self.x - self.dest_x
				delta_y = self.y - self.dest_y
				current_move = find_hypotenuse(delta_x, delta_y)
				"""
				print("Current coordinates: {},{}".format(self.x, self.y))
				print("Target coordinate: {},{}".format(self.dest_x, self.dest_y))
				print("delta_x: {} pixels".format(delta_x))
				print("delta_y: {} pixels".format(delta_y))
				print("delta hypot: {} pixels".format(current_move))
				"""

				#Attempts to move the model if the desired move is within the unit's max move
				if self.consolidate_move > 0:
					model_pos = vec(self.x, self.y)
					dest_pos = vec(self.dest_x, self.dest_y)
					self.rot = (dest_pos - model_pos).angle_to(vec(1,0))	#Calculates the angle between desired vector and basic x vector
					self.acc = vec(self.speed, 0).rotate(-self.rot)		#Sets the acceleration vector's to angle and magnitude
					self.acc += self.vel * -.4	#Friction coefficient; the higher the velocity, the higher this number is.
					self.vel += self.acc

					#print("\nRot: {}, Acc: {}, Vel: {}".format(self.rot, self.acc, self.vel))
					#print("Velocity vector magnitude: {}".format(find_hypotenuse(self.vel[0], self.vel[1])))

					pixels_x = int(self.vel[0])
					pixels_y = int(self.vel[1])
					distance_moved = find_hypotenuse(pixels_x, pixels_y)

					self.x += pixels_x
					self.y += pixels_y
					self.rect.center = (self.x, self.y)

					#Model base collision
					for sprite_x in self.game.all_models:
						if sprite_x != self:
							if pygame.sprite.collide_circle(self, sprite_x):
								#print("\n!Collision with between self and model!")
								revert_move()

					#Terrain collision
					for sprite_x in self.game.walls:
						if pygame.sprite.collide_rect(self, sprite_x):
							print("\n!Collision with between self and terrain!")
							revert_move()

					#Max move reduced if model moved at all
					if self.x != temp_x or self.y != temp_y:	
						self.consolidate_move -= distance_moved
						#print("\nSuccessful move!")
						#print("Max move reduced by {} (rounded velocity hypotenuse)".format(distance_moved))
						#print("Max move Remaining: {}".format(self.charge_move))
						#print("\nPost-move coord: ({},{})".format(self.x, self.y))
					else:
						pass
						#print("\nFailed move.")
						#print("Coordinates unchanged.")

				else:
					#print("\nMOVE CANCELED: Current move of {} > Remaining max move of {}".format(current_move, self.pile_in_move))
					self.dest_x = self.x
					self.dest_y = self.y

			else:
				self.dest_x = self.x
				self.dest_y = self.y
				self.rect.center = (self.x, self.y)

			#Unit cohesion checker
			for sprite in self.unit.models:
				if sprite != self and pygame.sprite.collide_circle_ratio(self.cohesion_ratio)(self, sprite):
					self.cohesion = True
				elif len(self.unit.models) <= 1:
					self.cohesion = True

	def attack_with_ranged_weapon(self, target_unit, weapon_index=0):
		"""Initiates an attack against the next valid target in the opposing army.

		First determines how many shots the weapon has, then fires those shots one by one at the target. 
		"""
		weapon = self.ranged_weapons[weapon_index]
		if weapon.fired == True:
			print("\nWeapon has already fired this turn. Pick a different weapon or model.")
			return
		else:
			weapon.fired = True
			if True:
				if weapon.shot_dice == 0:
					shot_count = weapon.shots
				else:
					shot_count = 0
					for i in range(weapon.shot_dice):
						roll = random.randint(1, weapon.shots)
						shot_count += roll 
				
			print('\n{} takes {} shot(s) against {} with {}.'.format(self.name, shot_count, target_unit.name, weapon.name))
			for i in range(shot_count):
				print('Taking shot #{}'.format(i+1))
				self.single_shot(weapon, target_unit)
				x = random.randint(0, len(target_unit.models)-1)
				Bullet(self.game, self, target_unit.models[x])

	def attack_with_melee_weapon(self, target_unit, weapon_index=0):
		weapon = self.melee_weapons[weapon_index]
		attack_count = self.attacks
		print('\n{} makes {} attack(s) against {} with {}.'.format(self.name, attack_count, target_unit.name, weapon.name))
		for i in range(attack_count):
			print('Making attack #{}'.format(i+1))
			self.single_attack(weapon, target_unit)

	def single_attack(self, weapon, target_unit):
		roll = random.randint(1,6)
		if roll < self.weapon_skill:
			print('  Failed to hit (rolled a {}, needed a {} or higher).'.format(roll, self.weapon_skill))
			return

		if weapon.strength == 'User':
			attack_strength = self.strength
		else:
			attack_strength = self.strength + weapon.strength

		roll = random.randint(1,6)
		#Target toughness is always homogeneous within a unit
		target_toughness = target_unit.models[0].toughness
		if attack_strength >= 2*target_toughness:
			wound_roll = 2
		elif attack_strength > target_toughness:
			wound_roll = 3
		elif attack_strength == target_toughness:
			wound_roll = 4
		elif attack_strength < target_toughness:
			wound_roll = 5
		elif attack_strength <= target_toughness/2:
			wound_roll = 6

		if roll < wound_roll:
			print('  Failed to wound (rolled a {}, needed a {} or higher).'.format(roll, wound_roll))
			return

		target_unit.save_against_wound(weapon)

	def single_shot(self, weapon, target_unit):
		"""Summary."""
		roll = random.randint(1,6)
		if self.game.current_phase == "Shooting Phase":
			if roll < self.ballistic_skill:
				print('  Failed to hit (rolled a {}, needed a {} or higher).'.format(roll, self.ballistic_skill))
				return
		elif self.game.current_phase == "Overwatch":
			if roll != 6:
				print('  Overwatch shot failed to hit (rolled a {}, needed a 6).'.format(roll))
				return

		roll = random.randint(1,6)
		#Target toughness is always homogeneous within a unit
		target_toughness = target_unit.models[0].toughness
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
			print('  Failed to wound (rolled a {}, needed a {} or higher).'.format(roll, wound_roll))
			return

		target_unit.save_against_wound(weapon)

	def model_save_against_wound(self, weapon):
		"""Summary."""
		roll = random.randint(1,6)
		if (self.invulnerable == None) or (self.invulnerable <= self.save):
			if roll >= self.save + weapon.ap:
				print('  {} saved against {} wound.'.format(self.name, weapon.name))
				return
		else:
			if roll >= self.invulnerable:
				print('  {} saved against {} wound.'.format(self.name, weapon.name))
				return

		if weapon.damage_dice == 0:
			self.game.unallocated_wounds += weapon.damage
			print('!  {} took {} damage from {}!'.format(self.name, weapon.damage, weapon.name))
		else:
			for i in range(weapon.damage_dice):
				roll = random.randint(1, weapon.damage)
				self.game.unallocated_wounds += roll
				print('!  {} took {} damage from {}!'.format(self.name, roll, weapon.name))

class Wall(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = [game.all_sprites, game.walls]	
		pygame.sprite.Sprite.__init__(self, self.groups)			#always needed for basic sprite functionality
		self.game = game
		self.image = pygame.Surface((TILESIZE, TILESIZE))
		self.image.fill(BLACK)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE

class Bullet(pygame.sprite.Sprite):
	def __init__(self, game, shooter, target):
		self.groups = [game.all_sprites, game.bullets]	
		pygame.sprite.Sprite.__init__(self, self.groups)			#always needed for basic sprite functionality
		self.game = game
		self.image = pygame.Surface((10, 10))
		self.image.fill(RED)
		self.rect = pygame.Rect(1, 1, 1, 1)
		self.x = shooter.x
		self.y = shooter.y
		self.rect.center = (self.x, self.y)
		self.speed = 8
		self.rot = 0
		self.vel = vec(0,0)
		self.acc = vec(0,0)

		self.target = target

		self.target_x = self.target.x
		self.target_y = self.target.y
		#print("\nSpawned a bullet!")

	def die(self):
		self.kill()

	def update(self):

		for sprite_x in self.game.walls:
			if pygame.sprite.collide_rect(self, sprite_x):
				self.die()

		if pygame.sprite.collide_rect(self, self.target):
			self.die()


		bullet_pos = vec(self.x, self.y)
		target_pos = vec(self.target_x, self.target_y)
		self.rot = (target_pos - bullet_pos).angle_to(vec(1,0))	#Calculates the angle between desired vector and basic x vector
		self.acc = vec(self.speed, 0).rotate(-self.rot)		#Sets the acceleration vector's to angle and magnitude
		self.acc += self.vel * -.4	#Friction coefficient; the higher the velocity, the higher this number is.
		self.vel += self.acc

		#print("\n Bullet Rot: {}, Acc: {}, Vel: {}".format(self.rot, self.acc, self.vel))
		#print("Bullet elocity vector magnitude: {}".format(find_hypotenuse(self.vel[0], self.vel[1])))

		pixels_x = int(self.vel[0])
		pixels_y = int(self.vel[1])
		distance_moved = find_hypotenuse(pixels_x, pixels_y)

		self.x += pixels_x
		self.y += pixels_y
		self.rect.center = (self.x, self.y)