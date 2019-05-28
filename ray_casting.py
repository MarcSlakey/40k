"""
Inspired by the example found here: https://pastebin.com/krFBNK3a
"""

import pygame
import main
from math import *
from settings import *

vec = pygame.math.Vector2

class Ray(object):
	"""docstring for Ray"""
	def __init__(self, game, shooter, target, shooter_pos, target_pos):
		self.game = game
		self.shooter_pos = shooter_pos
		self.target_pos = target_pos
		self.shooter = shooter
		self.target = target

		self.adjusted_shooter_rect = game.camera.apply(self.shooter)
		self.adjusted_target_rect = game.camera.apply(self.target)

		self.pos_vec = vec(self.adjusted_shooter_rect.center)
		self.target_vec = vec(self.adjusted_target_rect.center)

		#print("Shooter's position vector: ({}, {})".format(self.pos_vec[0], self.pos_vec[1]))
		#print("Target vector: ({}, {})".format(self.target_vec[0], self.target_vec[1]))

	#Casts a single ray from the shooter towards the target.
	def cast(self):
		ray = self.target_vec - self.pos_vec
		length = int(ray.length())

		for x in range(length):
			ray.scale_to_length(x+1)
			endpoint = self.pos_vec + ray
			
			if self.adjusted_target_rect.collidepoint(endpoint):
				self.shooter.valid_shots.append(self.target)
				#print("\nRay hit intended target with length {}".format(length))
				#print("Ray's end pos: {}".format(endpoint))
				pygame.draw.line(self.game.background, GREEN, self.adjusted_shooter_rect.center, endpoint)
				pygame.display.update()
				return

			for model in self.game.targets:
				adjusted_model_rect = self.game.camera.apply(model)
				if adjusted_model_rect.collidepoint(endpoint):
					#print("\nRay hit non-target model with length {}".format(length))
					#print("Ray's end pos: {}".format(endpoint))
					pygame.draw.line(self.game.background, ORANGE, self.adjusted_shooter_rect.center, endpoint)
					pygame.display.update()
					return

			for wall in self.game.walls:
				adjusted_wall_rect = self.game.camera.apply(wall)
				if adjusted_wall_rect.collidepoint(endpoint):
					#print("Ray hit a wall with length {}".format(length))
					#print("Ray's end pos: {}".format(endpoint))
					pygame.draw.line(self.game.background, RED, self.adjusted_shooter_rect.center, endpoint)
					pygame.display.update()
					return

			x += 1
			#print("Increasing ray length...")
			



