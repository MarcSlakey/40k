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
	def __init__(self, game, x, y, color):
		self.groups = [game.all_sprites]	#Sets the list of groups that contain this sprite
		pygame.sprite.Sprite.__init__(self, self.groups)			#always needed for basic sprite functionality
		self.image = pygame.Surface((TILESIZE, TILESIZE))			#makes the image the same size as the tiles
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.vx, self.vy = (0, 0)
		self.x = x * TILESIZE		#spawn x coordinate; allows initializing with a tile number which is then converted to pixels
		self.y = y * TILESIZE 		#spawn y coordinate
		self.pos = self.x, self.y
		self.original_pos = (self.x, self.y)
		self.dest_x = 0
		self.dest_y = 0
		self.shot_dest_x = 0
		self.shot_dest_y = 0
		self.weapon_range = 500
		self.max_move = 320
		self.original_max_move = (self.max_move)


		print("\nSprite created. at {},{}. original_pos = ({},{})".format(self.x, self.y, self.original_pos[0], self .original_pos[1]))	

	def update(self):
		delta_x = self.x - self.dest_x
		delta_y = self.y - self.dest_y
		current_move = find_hypotenuse(delta_x, delta_y)
		
		if current_move <= self.max_move:
			if self.dest_x != 0 and self.dest_y != 0:
				if self.max_move > 0:
					self.x = int(self.dest_x)
					self.y = int(self.dest_y)
					self.rect.center = (self.x, self.y)

					self.max_move -= int(current_move)

					self.dest_x = 0
					self.dest_y = 0

				else:
					self.dest_x = self.x
					self.dest_y = self.y

		elif current_move > self.max_move:
			self.dest_x = self.x
			self.dest_y = self.y
