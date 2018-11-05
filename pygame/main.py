"""40k Pygame

Four Sprites are spawned, three controllable models named model1, model2, and model3, and one non-controllable model named target.

Left clicking a controllable model selects it, left clicking empty space deselects it. 
	Selecting a model causes three circles to be drawn: yellow for move distance, red for weapon range, and green to highlight the selected sprite.
Right click moves the selected model to the clicked location if it is within the model's remaining move distance.
Space resets the selected model to its original position and restores its max move distance.
Middle click while hovering the mouse over the target model will delete it if the currently selected model is within shooting range.
"""

import pygame
import random
from settings import *
from sprites import *


class Game:
	#Initialize program, game window, etc.
	def __init__(self):
		pygame.init()				#Always needed 
		pygame.mixer.init()			#Always needed if you want any sound
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()		#Creates a new Clock object that can be used to track an amount of time.
		self.running = True						#		Provides several functions to help control a game's framerate.

	#Initialize a new game
	def new(self):
		self.all_sprites = pygame.sprite.Group() 	#All-inclusive group of sprites, simplifies updating and drawing
		self.model_sprites = pygame.sprite.Group()

		self.model1 = Model(self, 10, 10, YELLOW)			#Spawns a single model sprite at given tile coordinates
		self.model2 = Model(self, 10, 12, YELLOW)
		self.model3 = Model(self, 10, 14, YELLOW)
		self.model1.add(self.model_sprites)
		self.model2.add(self.model_sprites)
		self.model3.add(self.model_sprites)

		self.target = Model(self, 30, 20, RED)

		self.selected_model = None
		self.run()

	#Main Game Loop
	def run(self):
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)	#Update the clock. Should be called once per "frame" (game loop?)
			self.events()				#Meat of the program
			self.update()
			self.draw()

	#Sets sprites back to their starting positions when the spacebar is pressed
	def reset_moves(self):
		keys = pygame.key.get_pressed()
		if self.selected_model != None and keys[pygame.K_SPACE]:
			if self.selected_model.x != self.selected_model.original_pos[0] and self.selected_model.y != self.selected_model.original_pos[1]:
				self.selected_model.x = self.selected_model.original_pos[0]
				self.selected_model.y = self.selected_model.original_pos[1]
				self.selected_model.max_move = self.selected_model.original_max_move
				print("\nSprite at ({},{}) reset to original_pos = ({},{})".format(self.selected_model.x, self.selected_model.y, 
																				self.selected_model.original_pos[0], self .selected_model.original_pos[1]))
				print("\nMax move reset to {}".format(self.selected_model.original_max_move))

	#Game Loop - Event Handling
	def events(self):
		for event in pygame.event.get():	#event.get() returns a list of all events currently in the queue and also removes all these events from the queue
			if event.type == pygame.QUIT:
				if self.playing:
					self.playing = False
				self.running = False

			#Keyboard event handling
			elif event.type == pygame.KEYDOWN:
				self.reset_moves()

			#Mouse event handling
			elif event.type == pygame.MOUSEBUTTONUP:
				#If a model is not selected, LMB selects a model.
				if self.selected_model == None:
					if event.button == 1:	#Mouse event.buttom refers to interger values: 1(left), 2(middle), 3(right), 4(scrl up), 5(scrl down)
						for self.model in self.model_sprites:
							if self.model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
								self.selected_model = self.model

				#If a model is selected, LMB deselects it, RMB moves it, and Middle mouse button shoots.
				elif self.selected_model != None:
					if event.button == 1:	#LMB
						for self.model in self.model_sprites:
							#This line doesn't work (not sure why); should allow selecting a different sprite while one is already selected
							if self.model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
								self.selected_model = self.model
							#Commenting this else out allows selection of new sprite while one is selected, but removes deselection
							else:	
								self.selected_model = None

					elif event.button == 2:	#Middle mouse button
						shot_x = self.selected_model.x - pygame.mouse.get_pos()[0]
						shot_y = self.selected_model.y - pygame.mouse.get_pos()[1]
						shot_distance = find_hypotenuse(shot_x, shot_y)
						if shot_distance <= self.selected_model.weapon_range:
							if self.target.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):		#Returns true if the spot clicked is in the target's rect
								self.target.kill()

					elif event.button == 3: #RMB
						self.selected_model.dest_x = pygame.mouse.get_pos()[0]
						self.selected_model.dest_y = pygame.mouse.get_pos()[1]
				
	#Game Loop - Update
	def update(self):
		self.all_sprites.update()

	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, LIGHTGREY, (x, 0 ), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

	#Draws various useful circles: max move, weapon range, and a selection indicator
	def draw_radii(self):
		pygame.draw.circle(self.screen, YELLOW, (self.selected_model.x, self.selected_model.y), self.selected_model.max_move, 1)		#Draw surface, color, location, radius, width
		pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), self.selected_model.weapon_range, 1)
		pygame.draw.circle(self.screen, GREEN, (self.selected_model.x, self.selected_model.y), 32, 1)

	#Game Loop - Draw
	def draw(self):
		self.screen.fill(BLACK)
		self.draw_grid()
		if self.selected_model != None:
			self.draw_radii()
		self.all_sprites.draw(self.screen)		#Draw every sprite in the group all_sprites
		pygame.display.flip()	#*AFTER* drawing everything, flip the display

	def show_start_screen(self):
		pass

	def show_go_screen(self):
		pass

g = Game()
g.show_start_screen()

while g.running:		#self.running always starts as True on Game __init__
	g.new()
	g.show_go_screen()

pygame.quit()