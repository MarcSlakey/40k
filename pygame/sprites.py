import pygame
from math import *
from settings import *

#vect = pygame.math.Vector2		#Pygame's vector functions (Vector2 indicates)
								#	Example usage: self.vel = pygame.math.Vector2(x, y)
								#	or with this assignment, self.vel = vect(x, y)

def find_hypotenuse(x, y):
	hypotenuse = sqrt(x*x + y*y)
	return hypotenuse

class Model(pygame.sprite.Sprite):

	"""Model class
	
	Model sprite.

	Attributes:
		groups: sets the list of groups that contain this sprite
		image:
		rect:
		x: spawn coordinates; allows initializing with a tile number which is then converted to pixels
		y: same as above
		rect.center:
		original_pos:
		radius: Standard melee detection radius; cohesion detection is twice this radius
		dest_x: stores mouse click location during movements
		dest_y: same as above
		shot_dest_x: placeholder attribute that allows crude shooting; should probably be in a different class later
		shot_dest_y: same as above
		weapon_range: same as above
		max_move: a model's moves are subtracted from this value during the move phase
		original_max_move: tuple; stores the max_move so it can be reset 

	"""
	
	def __init__(self, game, x, y, radius, color):
		self.game = game
		self.groups = [game.all_sprites]	
		pygame.sprite.Sprite.__init__(self, self.groups)			#always needed for basic sprite functionality
		self.image = pygame.Surface((TILESIZE, TILESIZE))
		#self.image.fill(color)
		self.rect = self.image.get_rect()
		self.radius	= radius
		self.vx, self.vy = (0, 0)
		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.rect.center = (self.x, self.y)
		self.original_pos = (self.x, self.y)

		pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
		
		self.dest_x = self.x
		self.dest_y = self.y
		self.shot_dest_x = 0
		self.shot_dest_y = 0
		self.weapon_range = 500
		self.max_move = 320
		self.original_max_move = (self.max_move)
		print("\nSprite created. at {},{}.".format(self.x, self.y))	

	def update(self):
		temp_x = self.x	
		temp_y = self.y
		current_move = 0

		for sprite in self.game.targets:
			if sprite.rect.collidepoint(self.dest_x, self.dest_y):
				return

		if self.dest_x != self.x and self.dest_y != self.y:
			delta_x = self.x - self.dest_x
			delta_y = self.y - self.dest_y
			current_move = find_hypotenuse(delta_x, delta_y)
		
			if current_move <= self.max_move and self.max_move > 0:
				self.x = int(self.dest_x)
				self.y = int(self.dest_y)
				self.rect.center = (self.x, self.y)
				self.max_move -= int(current_move)
				"""
				for sprite_x in self.game.targets:
					if pygame.sprite.collide_circle(self, sprite_x):
						self.x = temp_x
						self.y = temp_y
						self.rect.center = (self.x, self.y)
						print("Collision!")
						self.max_move -= int(current_move)
						self.dest_x = self.x
						self.dest_y = self.y
				"""
			else:
				self.dest_x = self.x
				self.dest_y = self.y

		else:
			self.dest_x = self.x
			self.dest_y = self.y
			self.rect.center = (self.x, self.y)

		

