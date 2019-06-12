import pygame
from settings import *



class SelectionBox(object):
	"""docstring for SelectionBox"""
	def __init__(self, game, x, y):
		self.game = game
		self.x = x - game.screen_topleft_pos[0]
		self.y = y - game.screen_topleft_pos[1]
		self.rect = pygame.Rect(x, y, 1, 1)

	def get_adjusted_mouse_pos(self, game):
		return (pygame.mouse.get_pos()[0]-game.screen_topleft_pos[0], pygame.mouse.get_pos()[1]-game.screen_topleft_pos[1])

	def update(self):
		adjusted_pos = self.get_adjusted_mouse_pos(self.game)
		endpointx = adjusted_pos[0]
		endpointy = adjusted_pos[1]

		width = endpointx - self.x
		height = endpointy - self.y

		if (width < 0) and (height < 0):
			topleftx = endpointx
			toplefty = endpointy
			width = abs(width)
			height = abs(height)
			self.rect = pygame.Rect(topleftx, toplefty, width, height)

		elif width < 0:
			topleftx = endpointx
			toplefty = self.y
			width = abs(width)
			height = abs(height)
			self.rect = pygame.Rect(topleftx, toplefty, width, height)

		elif height < 0:
			topleftx = self.x
			toplefty = endpointy
			width = abs(width)
			height = abs(height)
			self.rect = pygame.Rect(topleftx, toplefty, width, height)

		else:
			self.rect = pygame.Rect(self.x, self.y, width, height) 

	def draw(self):
		pygame.draw.rect(self.game.screen, YELLOW, self.rect, 1)

	def finish(self):
		for model in self.game.selectable_models:
			adjusted_model_rect = self.game.camera.apply(model)
			if adjusted_model_rect.colliderect(self.rect):
				self.game.selected_model = model
				self.game.selected_unit = model.unit

		self.game.selection_box = None
		del self
		
		
		