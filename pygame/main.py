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
		pygame.init() 
		pygame.mixer.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		self.running = True

	#Initialize a new game
	def new(self):
		self.phases = ["move phase", "shoot_phase"]
		self.current_phase = "move_phase"
		self.all_sprites = pygame.sprite.Group() 	
		self.selectable_models = pygame.sprite.Group()
		self.targets = pygame.sprite.Group()
		self.selected_model = None

		self.model1 = Model(self, 10, 10, TILESIZE//2, YELLOW)	#Spawns a single model sprite at given tile coordinates
		self.model2 = Model(self, 10, 12, TILESIZE//2, YELLOW)
		self.model3 = Model(self, 10, 14, TILESIZE//2, YELLOW)
		self.model1.add(self.selectable_models)
		self.model2.add(self.selectable_models)
		self.model3.add(self.selectable_models)

		self.target1 = Model(self, 15, 16, TILESIZE//2, RED)
		self.target2 = Model(self, 15, 14, TILESIZE//2, RED)
		self.target3 = Model(self, 15, 12, TILESIZE//2, RED)
		self.target4 = Model(self, 15, 10, TILESIZE//2, RED)
		self.target1.add(self.targets)
		self.target2.add(self.targets)
		self.target3.add(self.targets)
		self.target4.add(self.targets)

		self.run()

	#Main Game Loop
	def run(self):
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()			
			self.update()
			self.draw()

	#Sets sprites back to their starting positions when the spacebar is pressed
	def reset_moves(self):
		if self.selected_model.x != self.selected_model.original_pos[0] and self.selected_model.y != self.selected_model.original_pos[1]:
			print("\nSprite at ({},{}) reseting to original_pos = ({},{})".format(self.selected_model.x, self.selected_model.y, 
																			self.selected_model.original_pos[0], self .selected_model.original_pos[1]))
			print("Max_move before reset: {}".format(self.selected_model.max_move))
			self.selected_model.x = self.selected_model.original_pos[0]
			self.selected_model.y = self.selected_model.original_pos[1]
			self.selected_model.dest_x = self.selected_model.x
			self.selected_model.dest_y = self.selected_model.y
			self.selected_model.max_move = self.selected_model.original_max_move
			print("Max_move after reset: {}.".format(self.selected_model.max_move))
			print("Sprite location after reset: ({},{})".format(self.selected_model.x, self.selected_model.y))

	#Game Loop - Event Handling
	def events(self):
		if self.current_phase == "move_phase":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					if self.playing:
						self.playing = False
					self.running = False

				#Keyboard event handling
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()
					if self.selected_model != None and keys[pygame.K_SPACE]:
						self.reset_moves()

				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					#If a model is not selected, LMB selects a model.
					if self.selected_model == None:
						if event.button == 1:	#Mouse event.buttom refers to interger values: 1(left), 2(middle), 3(right), 4(scrl up), 5(scrl down)
							for self.model in self.selectable_models:
								if self.model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
									self.selected_model = self.model

					#If a model is selected, LMB deselects it, RMB moves it, and Middle mouse button shoots.
					elif self.selected_model != None:
						if event.button == 1:	#LMB
							self.selected_model = None 	#Defaults to deselecting current model if another model isn't clicked
							for self.model in self.selectable_models:
								if self.model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
									self.selected_model = self.model
								

						elif event.button == 2:	#Middle mouse button
							shot_x = self.selected_model.x - pygame.mouse.get_pos()[0]
							shot_y = self.selected_model.y - pygame.mouse.get_pos()[1]
							shot_distance = find_hypotenuse(shot_x, shot_y)
							if shot_distance <= self.selected_model.weapon_range:
								for self.target in self.targets:
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
		pygame.draw.circle(self.screen, GREEN, (self.selected_model.x, self.selected_model.y), 25, 3)

	#Game Loop - Draw
	def draw(self):
		self.screen.fill(BLACK)	
		self.draw_grid()

		def text_objects(text, font):
			textSurface = font.render(text, True, WHITE)
			return textSurface, textSurface.get_rect()

		largeText = pygame.font.Font('freesansbold.ttf', 32)
		TextSurf, TextRect = text_objects("Current phase: {}".format(self.current_phase), largeText)
		TextRect.center = ((WIDTH/2), 16)
		self.screen.blit(TextSurf, TextRect)

		self.all_sprites.draw(self.screen)
		for sprite in self.all_sprites:
			pygame.draw.circle(self.screen, LIGHTGREY, sprite.rect.center, sprite.radius)
		if self.selected_model != None:
			self.draw_radii()
			
		pygame.display.update()
		

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