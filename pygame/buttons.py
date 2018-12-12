import pygame
from settings import *

class Button(object):
	""" Basic button constructor class
	
	"""

	def __init__(self, game, text, font_name, size, color, x, y, width, height, align="nw"):
		self.game = game
		self.text = text
		self.font_name = font_name
		self.size = size
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.align  = align
		self.font = pygame.font.Font(font_name, size)
		self.text_surface = self.font.render(text, True, color)
		self.text_rect = self.text_surface.get_rect()
		#self.game.buttons.append(self)
		if align == "nw":
			self.text_rect.topleft = (self.x, self.y)
		if align == "ne":
			self.text_rect.topright = (self.x, self.y)
		if align == "sw":
			self.text_rect.bottomleft = (self.x, self.y)
		if align == "se":
			self.text_rect.bottomright = (self.x, self.y)
		if align == "n":
			self.text_rect.midtop = (self.x, self.y)
		if align == "s":
			self.text_rect.midbottom = (self.x, self.y)
		if align == "e":
			self.text_rect.midright = (self.x, self.y)
		if align == "w":
			self.text_rect.midleft = (self.x, self.y)
		if align == "center":
			self.text_rect.center = (self.x, self.y)



	def draw(self):
		self.outline = pygame.Rect(self.x, self.y, self.text_rect.width + 10,self.text_rect.height + 10)
		if self.align == "nw":
			self.outline.topleft = (self.x, self.y)
		if self.align == "ne":
			self.outline.topright = (self.x, self.y)
		if self.align == "sw":
			self.outline.bottomleft = (self.x, self.y)
		if self.align == "se":
			self.outline.bottomright = (self.x, self.y)
		if self.align == "n":
			self.outline.midtop = (self.x, self.y)
		if self.align == "s":
			self.outline.midbottom = (self.x, self.y)
		if self.align == "e":
			self.outline.midright = (self.x, self.y)
		if self.align == "w":
			self.outline.midleft = (self.x, self.y)
		if self.align == "center":
			self.outline.center = (self.x, self.y)

		pygame.draw.rect(self.game.screen, WHITE, self.outline, 3)
		self.game.screen.blit(self.text_surface, self.text_rect)

	def mouse_over(self):
		pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
		if self.outline.collidepoint(pos):
			return True
		return False

		