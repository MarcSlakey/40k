import pygame
from settings import *
import event_handling

#This happens once with a new game and is performed again each time the window is resized.
def define_buttons(game):
	game.toggle_radii_button = Button(game, "TOGGLE RADII", BASIC_FONT, TINY_TEXT, WHITE,  game.background_w/2, 62*game.background_h/64, 5*TILESIZE, 2*TILESIZE, "center")
	game.reset_all_button = Button(game, "RESET ALL", BASIC_FONT, TINY_TEXT, WHITE,  game.background_w/2, 58*game.background_h/64, 5*TILESIZE, 2*TILESIZE, "center")
	game.attack_button = Button(game, "ATTACK", BASIC_FONT, TINY_TEXT, WHITE,  game.background_w/2, 58*game.background_h/64, 5*TILESIZE, 2*TILESIZE, "center")
	game.charge_button = Button(game, "CHARGE TARGET", BASIC_FONT, TINY_TEXT, WHITE,  game.background_w/2, 58*game.background_h/64, 5*TILESIZE, 2*TILESIZE, "center")
	game.fight_button = Button(game, "FIGHT", BASIC_FONT, TINY_TEXT, WHITE,  game.background_w/2, 58*game.background_h/64, 5*TILESIZE, 2*TILESIZE, "center")

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
		"""
		This creates a new Surface with the specified text rendered on it. 
		pygame provides no way to directly draw text on an existing Surface: 
		instead you must use Font.render() to create an image (Surface) of the text, then blit this image onto another Surface.
		"""
		self.text_surface = self.font.render(self.text, True, self.color)
		self.text_rect = self.text_surface.get_rect()
		self.game.buttons.append(self)
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

		self.outline = pygame.Rect(self.x, self.y, self.text_rect.width + 10,self.text_rect.height + 10)

	def draw(self):
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

		pygame.draw.rect(self.game.background, WHITE, self.outline, 3)
		self.game.background.blit(self.text_surface, self.text_rect)

	def mouse_over(self):
		pos = pygame.mouse.get_pos()
		if self.outline.collidepoint(pos):
			return True
		return False

	def fill(self):
		#self.game.screen.blit(self.text_surface.fill(GREEN))
		if self.mouse_over():
			self.text_surface.fill(GREEN)
		else:
			self.text_surface = self.font.render(self.text, True, self.color)
			self.draw()

