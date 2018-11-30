import pygame
from math import *
from settings import *

#vect = pygame.math.Vector2		#Pygame's vector functions (Vector2 indicates)
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
		self.max_move = 320
		self.original_max_move = (self.max_move)
		print("\nSprite created. at {},{}.".format(self.x, self.y))	

	#def 

	def get_angle(origin, destination):
	    """Returns angle in radians from origin to destination.
	    This is the angle that you would get if the points were
	    on a cartesian grid. Arguments of (0,0), (1, -1)
	    return .25pi(45 deg) rather than 1.75pi(315 deg).
	    """
	    x_dist = destination[0] - origin[0]
	    y_dist = destination[1] - origin[1]
	    return atan2(-y_dist, x_dist) % (2 * pi)

	def project(pos, angle, distance):
	    """Returns tuple of pos projected distance at angle
	    adjusted for pygame's y-axis.
	    """
	    return (pos[0] + (cos(angle) * distance),
	            pos[1] - (sin(angle) * distance))


	def update(self):
		temp_x = self.x	
		temp_y = self.y
		current_move = 0
		if self.dest_x != self.x and self.dest_y != self.y:
			delta_x = self.x - self.dest_x
			delta_y = self.y - self.dest_y
			current_move = find_hypotenuse(delta_x, delta_y)
		
			if self.max_move > 0 and current_move <= self.max_move:
				self.x = int(self.dest_x)
				self.y = int(self.dest_y)
				self.rect.center = (self.x, self.y)
				self.max_move -= int(current_move)
				
				for sprite_x in self.game.all_sprites:
					if sprite_x != self:
						if pygame.sprite.collide_circle(self, sprite_x):
							#print("Collision with between self and {}".format(sprite_x.name))
							pygame.mouse.set_pos(temp_x, temp_y)
							self.x = temp_x
							self.y = temp_y
							self.rect.center = (self.x, self.y)
							self.max_move += int(current_move)
							self.dest_x = self.x
							self.dest_y = self.y

				
			else:
				self.dest_x = self.x
				self.dest_y = self.y

		else:
			self.dest_x = self.x
			self.dest_y = self.y
			self.rect.center = (self.x, self.y)

		

