"""40k Pygame

Three Sprites are spawned, two named model1 and model2, and the other named target.

Left clicking a sprite selects it, left clicking empty space deselects it. 
	Selecting a model causes three circles to be drawn: yellow for move distance, red for weapon range, and green to highlight the selected sprite.
Right click moves the model to the clicked location if it within the remaining move distance.
Space resets the selected model to its original position and restores its max move distance.
Middle click will attempt to delete the target. If the model selected is within shooting range of target, the target will be killed.
"""

import pygame
import random
from settings import *
from sprites import *


class Game:
	def __init__(self):
		#Initialize program, game window, etc.
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
			self.events()		#Meat of the program
			self.update()
			self.draw()

	#Sets sprites back to their starting positions when the spacebar is pressed
	def reset_moves(self):
		keys = pygame.key.get_pressed()
		if self.selected_model != None and keys[pygame.K_SPACE]:
			if self.selected_model.x != self.selected_model.original_pos[0] and self.selected_model.y != self.selected_model.original_pos[1]:
				print("\nSprite at ({},{}) reset to original_pos = ({},{})".format(self.selected_model.x, self.selected_model.y, 
																				self.selected_model.original_pos[0], self .selected_model.original_pos[1]))
				#sloppy fix to move-reset bug; sometimes space needed to be pressed several times to reset the model's position
				while self.selected_model.x != self.selected_model.original_pos[0] or self.selected_model.y != self.selected_model.original_pos[1]:
					self.selected_model.x = self.selected_model.original_pos[0]
					self.selected_model.y = self.selected_model.original_pos[1]
					self.selected_model.max_move = self.selected_model.original_max_move

	def events(self):
		#Game Loop - Event Handling
		for event in pygame.event.get():	#event.get() returns a list of all events currently in the queue and also removes all these events from the queue
			if event.type == pygame.QUIT:
				if self.playing:
					self.playing = False
				self.running = False

			elif event.type == pygame.KEYDOWN:
				self.reset_moves()


			elif event.type == pygame.MOUSEBUTTONUP:
				if self.selected_model == None:
					if event.button == 1:		#mouse event.buttom refers to interger values: 1(left), 2(middle), 3(right), 4(scrl up), 5(scrl down)
						for self.model in self.model_sprites:
							if self.model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
								self.selected_model = self.model

				elif self.selected_model != None:
					if event.button == 1:	
						for self.model in self.model_sprites:
							if self.model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
								self.selected_model = self.model
							else:	#commenting these 2 lines out allows selection of new sprite while one is selected; ideally want that as well as deselection functionality
								self.selected_model = None

					elif event.button == 2:
						shot_x = self.selected_model.x - pygame.mouse.get_pos()[0]
						shot_y = self.selected_model.y - pygame.mouse.get_pos()[1]
						shot_distance = find_hypotenuse(shot_x, shot_y)
						if shot_distance <= self.selected_model.weapon_range:
							if self.target.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):		#Returns true if the spot clicked is in the target's rect
								self.target.kill()

					elif event.button == 3:
						self.selected_model.dest_x = pygame.mouse.get_pos()[0]
						self.selected_model.dest_y = pygame.mouse.get_pos()[1]
				

	def update(self):
		#Game Loop - Update
		self.all_sprites.update()

	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, LIGHTGREY, (x, 0 ), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

	def draw_radii(self):
		pygame.draw.circle(self.screen, YELLOW, (self.selected_model.x, self.selected_model.y), self.selected_model.max_move, 1)		#Draw surface, color, location, radius, width
		pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), self.selected_model.weapon_range, 1)
		pygame.draw.circle(self.screen, GREEN, (self.selected_model.x, self.selected_model.y), 32, 1)


	def draw(self):
		#Game Loop - Draw
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