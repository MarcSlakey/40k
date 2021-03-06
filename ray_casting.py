"""
Inspired by the example found here: https://pastebin.com/krFBNK3a

Personal notes: 
Drawing the ray once it collides doesn't seem to change the los_check time.
However, drawing the ray each time it increments quadruples the check time.
Increasing scale_to_length increment amount from 1 to 30 only decreased the check time of a 10 man unit by about 16%.
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
			
			background_shifted_rect_center = (self.adjusted_shooter_rect.center[0] + self.game.screen_topleft_pos[0], self.adjusted_shooter_rect.center[1] + self.game.screen_topleft_pos[1])
			background_shifted_endpoint = (endpoint[0] + self.game.screen_topleft_pos[0], endpoint[1] + self.game.screen_topleft_pos[1])

			#pygame.draw.line(self.game.background, WHITE, background_shifted_rect_center, background_shifted_endpoint)
			#pygame.display.update()

			if self.adjusted_target_rect.collidepoint(endpoint):
				self.shooter.valid_shots.append(self.target)
				#print("\nRay hit intended target with length {}".format(length))
				#print("Ray's end pos: {}".format(endpoint))
				pygame.draw.line(self.game.background, GREEN, background_shifted_rect_center, background_shifted_endpoint)
				pygame.display.update()
				return

			for model in self.game.targets:
				adjusted_model_rect = self.game.camera.apply(model)
				if adjusted_model_rect.collidepoint(endpoint):
					#print("\nRay hit non-target model with length {}".format(length))
					#print("Ray's end pos: {}".format(endpoint))
					pygame.draw.line(self.game.background, ORANGE, background_shifted_rect_center, background_shifted_endpoint)
					pygame.display.update()
					return

			for wall in self.game.walls:
				adjusted_wall_rect = self.game.camera.apply(wall)
				if adjusted_wall_rect.collidepoint(endpoint):
					#print("Ray hit a wall with length {}".format(length))
					#print("Ray's end pos: {}".format(endpoint))
					pygame.draw.line(self.game.background, RED, background_shifted_rect_center, background_shifted_endpoint)
					pygame.display.update()
					return

			x += 1
			#print("Increasing ray length...")
			



