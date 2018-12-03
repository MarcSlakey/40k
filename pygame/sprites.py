import pygame
from math import *
from settings import *

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
	
	def __init__(self, game, name, x, y, radius, color):
		self.game = game
		self.name = name
		self.groups = [game.all_sprites]	
		pygame.sprite.Sprite.__init__(self, self.groups)			#always needed for basic sprite functionality
		self.image = pygame.Surface((TILESIZE, TILESIZE))
		#self.image.fill(color)
		self.rect = self.image.get_rect()
		self.base_radius = radius
		self.radius	= radius
		self.vx, self.vy = (0, 0)
		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.rect.center = (self.x, self.y)
		self.original_pos = (self.x, self.y)
		self.dest_x = self.x
		self.dest_y = self.y
		self.shot_dest_x = 0
		self.shot_dest_y = 0
		self.weapon_range = 500
		self.speed = 1
		self.rot = 0
		self.vel = vec(0,0)
		self.acc = vec(0,0)
		self.max_move = 320
		self.original_max_move = (self.max_move)
		print("\nSprite created. at {},{}.".format(self.x, self.y))	

	def update(self):
		temp_x = self.x	
		temp_y = self.y
		current_move = 0
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
			if self.max_move > 0 and current_move <= self.max_move:
				model_pos = vec(self.x, self.y)
				dest_pos = vec(self.dest_x, self.dest_y)
				self.rot = (dest_pos - model_pos).angle_to(vec(1,0))	#Calculates the angle between desired vector and basic x vector
				self.acc = vec(self.speed, 0).rotate(-self.rot)		#Sets the acceleration vector's to angle and magnitude
				self.acc += self.vel * -.4	#Friction coefficient; the higher the velocity, the higher this number is.
				self.vel += self.acc

				print("\nRot: {}, Acc: {}, Vel: {}".format(self.rot, self.acc, self.vel))
				print("Vel Hypotenuse calc: {}".format(find_hypotenuse(self.vel[0], self.vel[1])))

				pixels_x = int(self.vel[0])
				pixels_y = int(self.vel[1])

				self.x += pixels_x
				self.y += pixels_y
				self.rect.center = (self.x, self.y)

				#Max move reduced if model moved at all
				if self.x != temp_x or self.y != temp_y:	
					self.max_move -= find_hypotenuse(pixels_x, pixels_y)
					print("\nMax move reduced by {}".format(find_hypotenuse(pixels_x, pixels_x)))

				print("\nPost-move coord: ({},{})".format(self.x, self.y))

				#Collision detection
				for sprite_x in self.game.all_sprites:
					if sprite_x != self:
						if pygame.sprite.collide_circle(self, sprite_x):
							#print("Collision with between self and {}".format(sprite_x.name))
							self.x = temp_x
							self.y = temp_y
							self.rect.center = (self.x, self.y)
							self.max_move += self.speed
							self.dest_x = self.x
							self.dest_y = self.y

				
			else:
				print("\nMOVE CANCELED: Current move of {} > Remaining max move of {}".format(current_move, self.max_move))
				self.dest_x = self.x
				self.dest_y = self.y

		else:
			self.dest_x = self.x
			self.dest_y = self.y
			self.rect.center = (self.x, self.y)

		

