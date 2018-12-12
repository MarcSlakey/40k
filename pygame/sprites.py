import pygame
from math import *
from settings import *
from ray_casting import *

vec = pygame.math.Vector2		#Pygame's vector functions (Vector2 indicates 2-dimensional vector)
								#	Example usage: self.vel = pygame.math.Vector2(x, y)
								#	or with this assignment, self.vel = vect(x, y)

def find_hypotenuse(x, y):
	hypotenuse = sqrt(x*x + y*y)
	return hypotenuse

def one_inch_scale():		#Scales the collision circle to the one inch out from the model's base
	pass

class Model(pygame.sprite.Sprite):

	"""Model class
	
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
		original_pos: tuple to store the sprite's spawn location
		radius: represents the model's base in the tabletop game
		dest_x: stores mouse click location during movements
		dest_y: same as above
		shot_dest_x: placeholder attribute that allows crude shooting; should probably be in a different class later
		shot_dest_y: same as above
		weapon_range: same as above
		max_move: a model's moves are subtracted from this value during the move phase
		original_max_move: tuple; stores the max_move so it can be reset 

	"""
	
	def __init__(self, game, x, y, name, move, weapon_skill, ballistic_skill, strength, toughness, wounds, attacks, leadership, save, invulnerable, radius):
		self.groups = [game.all_sprites, game.all_models]	
		pygame.sprite.Sprite.__init__(self, self.groups)			#always needed for basic sprite functionality
		self.game = game
		self.image = pygame.Surface((TILESIZE, TILESIZE))
		self.rect = self.image.get_rect()
		self.radius = radius 		#represents the model's base size

		self.melee_ratio = (self.radius + TILESIZE/2)/self.radius 			#the coefficient by which the radius can be mulitplied to achieve the base radius + 1/2 inch
		self.true_melee_ratio = (self.radius + TILESIZE)/self.radius
		self.melee_radius = int(self.radius * self.melee_ratio)				#gives half the melee radius (1/2 inch) to each sprite to simulate 1" melee radius
		self.true_melee_radius = int(self.radius * self.true_melee_ratio) 	#the "true" 1" melee radius

		self.cohesion_ratio = (self.radius + TILESIZE)/self.radius 			#the coefficient by which the radius can be mulitplied to achieve the base radius + one inch
		self.true_cohesion_ratio = (self.radius + 2*TILESIZE)/self.radius
		self.cohesion_radius = int(self.radius * self.cohesion_ratio)		#gives half the cohesion radius (1 inch) to each sprite to simulate 2" cohesion radius
		self.true_cohesion_radius = int(self.radius * self.true_cohesion_ratio) #the "true" 2" cohesion radius
		self.cohesion = True

		self.vx, self.vy = (0, 0)
		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.rect.center = (self.x, self.y)
		self.original_pos = (self.x, self.y)

		self.dest_x = self.x
		self.dest_y = self.y
		self.shot_dest_x = 0
		self.shot_dest_y = 0
		#self.weapon_range = 24*TILESIZE
		self.speed = 1
		self.rot = 0
		self.vel = vec(0,0)
		self.acc = vec(0,0)

		self.name = name
		self.max_move = move
		self.original_max_move = (self.max_move)
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
		self.valid_shots = []	# List of valid shooting targets
		

	def add_weapon(self, weapon):
		"""Adds a weapon to a given model's list of weapons"""
		self.weapons.append(weapon)

	def die(self):
		self.kill()


	def update(self):
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
				print("Coordinates reverted to ({},{})".format(self.x, self.y))

			if self.dest_x != self.x and self.dest_y != self.y:
				print("\n\n-------NEW STEP-------")
				print("Pre-move coord: ({},{})".format(self.x, self.y))
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
								print("\n!Collision with between self and model!")
								revert_move()
								self.rect.center = (self.x, self.y)
								self.dest_x = self.x
								self.dest_y = self.y

					#Melee collision
					for sprite_x in self.game.targets:
						if sprite_x != self:
							if pygame.sprite.collide_circle_ratio(sprite_x.melee_ratio)(self, sprite_x):
								print("\n!Collision with between self and enemy melee radius!")
								revert_move()
								self.rect.center = (self.x, self.y)
								self.dest_x = self.x
								self.dest_y = self.y

					#Terrain collision
					for sprite_x in self.game.walls:
						if pygame.sprite.collide_rect(self, sprite_x):
							print("\n!Collision with between self and terrain!")
							revert_move()
							self.rect.center = (self.x, self.y)
							self.dest_x = self.x
							self.dest_y = self.y

					#Max move reduced if model moved at all
					if self.x != temp_x or self.y != temp_y:	
						self.max_move -= distance_moved
						print("\nSuccessful move!")
						print("Max move reduced by {} (rounded velocity hypotenuse)".format(distance_moved))
						print("Max move Remaining: {}".format(self.max_move))
						print("\nPost-move coord: ({},{})".format(self.x, self.y))
					else:
						print("\nFailed move.")
						print("Coordinates unchanged.")

					
					
				else:
					print("\nMOVE CANCELED: Current move of {} > Remaining max move of {}".format(current_move, self.max_move))
					self.dest_x = self.x
					self.dest_y = self.y

			else:
				self.dest_x = self.x
				self.dest_y = self.y
				self.rect.center = (self.x, self.y)

			for sprite in self.game.selectable_models:
				if sprite != self and pygame.sprite.collide_circle_ratio(self.cohesion_ratio)(self, sprite):
					self.cohesion = True

		if self.game.current_phase == "Shooting Phase":
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


class Wall(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = [game.all_sprites, game.walls]	
		pygame.sprite.Sprite.__init__(self, self.groups)			#always needed for basic sprite functionality
		self.game = game
		self.image = pygame.Surface((TILESIZE, TILESIZE))
		self.image.fill(LIGHTGREY)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE


class Bullet(pygame.sprite.Sprite):
	def __init__(self, game, weapon, shooter, target):
		self.groups = [game.all_sprites, game.bullets]	
		pygame.sprite.Sprite.__init__(self, self.groups)			#always needed for basic sprite functionality
		self.game = game
		self.weapon = weapon
		self.image = pygame.Surface((10, 10))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
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
			self.target.die()


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

class SightBullet(pygame.sprite.Sprite):
	def __init__(self, game, weapon, shooter, target):
		self.groups = [game.all_sprites]	
		pygame.sprite.Sprite.__init__(self, self.groups)			#always needed for basic sprite functionality
		self.game = game
		self.weapon = weapon
		self.image = pygame.Surface((10, 10))
		self.rect = self.image.get_rect()
		self.x = shooter.x
		self.y = shooter.y
		self.rect.center = (self.x, self.y)
		self.speed = 5
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
