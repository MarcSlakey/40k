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
from os import path
from settings import *
from sprites import *
from weapon import *
from unit import Unit
from army import Army
from data_creation import *

get_workbook_data()

class Game:
	#Initialize program, game window, etc.
	def __init__(self):
		pygame.init() 
		#pygame.mixer.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		self.running = True

	def load_data(self):
		game_folder = path.dirname(__file__)
		self.map_data = []
		with open(path.join(game_folder, 'map.txt'), 'rt') as f:
			for line in f:
				self.map_data.append(line)

	#Initialize a new game
	def new(self):
		self.load_data()
		self.turn_count = 1
		self.phases = ["move phase", "shoot_phase"]
		self.current_phase = "move_phase"
		self.all_sprites = pygame.sprite.Group() 
		self.all_models = pygame.sprite.Group()
		self.selectable_models = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()
		self.targets = pygame.sprite.Group()
		self.selected_model = None

		#Create walls, enemies from map.txt
		for row, tiles in enumerate(self.map_data):		#enumerate gets the index as well as the value
			for col, tile in enumerate(tiles):
				if tile == '1':
					Wall(self, col, row)
				elif tile == 'X':
					model = create_model_by_name('Initiate', self, col, row)
					model.add(self.targets)


		self.army1 = Army('Black Templars')
		self.army1.add_unit(Unit('Crusader Unit(1)'))

		for i in range(3):
			x = 4 + i * 2
			model = create_model_by_name('Initiate', self, x, 4)
			#model.add_weapon(create_ranged_weapon_by_name('Bolter'))
			self.army1.units[0].add_model(model)
			model.add(self.selectable_models)
			model.add_weapon(create_ranged_weapon_by_name('Bolter'))

		"""	
		self.model1 = Model(self, "model1", 6, 4, 25//2, YELLOW)	#Spawns a single model sprite at given tile coordinates
		self.model2 = Model(self, "model2", 8, 4, 25//2, YELLOW)
		self.model3 = Model(self, "model3", 10, 4, 25//2, YELLOW)
		self.model1.add(self.selectable_models)
		self.model2.add(self.selectable_models)
		self.model3.add(self.selectable_models)
		"""
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
		if self.selected_model.x != self.selected_model.original_pos[0] or self.selected_model.y != self.selected_model.original_pos[1]:
			print("\nSprite at ({},{}) resetting to original_pos = ({},{})".format(self.selected_model.x, self.selected_model.y, 
																			self.selected_model.original_pos[0], self .selected_model.original_pos[1]))
			print("Max_move before reset: {}".format(self.selected_model.max_move))
			self.selected_model.x = self.selected_model.original_pos[0]
			self.selected_model.y = self.selected_model.original_pos[1]
			self.selected_model.dest_x = self.selected_model.x
			self.selected_model.dest_y = self.selected_model.y
			self.selected_model.max_move = self.selected_model.original_max_move
			print("Max_move after reset: {}.".format(self.selected_model.max_move))
			print("Sprite location after reset: ({},{})".format(self.selected_model.x, self.selected_model.y))

	def refresh_moves(self):
		unit_cohesions = []
		for sprite in self.selectable_models:
			unit_cohesions.append(sprite.cohesion)
		if all(unit_cohesions):
			for sprite in self.selectable_models:
				sprite.max_move = sprite.original_max_move
				sprite.original_pos = (sprite.x, sprite.y)
			self.turn_count += 1	


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
					elif self.selected_model != None and keys[pygame.K_RETURN]:
						self.refresh_moves()

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
							if shot_distance <= self.selected_model.weapons[0].w_range:
								for self.target in self.targets:
									if self.target.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):		#Returns true if the spot clicked is in the target's rect
										self.target.kill()


						elif event.button == 3: #RMB
							self.selected_model.dest_x = pygame.mouse.get_pos()[0]
							self.selected_model.dest_y = pygame.mouse.get_pos()[1]
				
				
	#Game Loop - Update
	def update(self):
		self.all_sprites.update()

	#Draws reference grid
	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, LIGHTGREY, (x, 0 ), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

	#Draws various useful circles: max move, weapon range
	def draw_radii(self):
		thickness = 1
		if self.selected_model.max_move >= thickness:
			pygame.draw.circle(self.screen, YELLOW, (self.selected_model.x, self.selected_model.y), int(self.selected_model.max_move), thickness)

		pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), self.selected_model.weapons[0].w_range, thickness)

	def draw_sprites(self):
		self.all_sprites.draw(self.screen)

	#Total Unit Cohesion Checker
	def draw_cohesion_indicator(self):
		pygame.draw.circle(self.screen, RED, (WIDTH//2, 0), 50, 0)	
		unit_cohesions = []
		for sprite in self.selectable_models:
			unit_cohesions.append(sprite.cohesion)
		if all(unit_cohesions):
			pygame.draw.circle(self.screen, GREEN, (WIDTH//2, 0), 50, 0)

	#Game Loop - Draw
	def draw(self):
		self.screen.fill(BLACK)	
		self.draw_grid()

		def text_objects(text, font):
			textSurface = font.render(text, True, WHITE)
			return textSurface, textSurface.get_rect()
		
		self.draw_sprites()

		#Model base radii
		for sprite in self.selectable_models:
			pygame.draw.circle(self.screen, WHITE, sprite.rect.center, sprite.radius, 0)
		for sprite in self.targets:
			pygame.draw.circle(self.screen, RED, sprite.rect.center, sprite.radius, 0)
		
		#Cohesion radius (two inches)
		#for sprite in self.selectable_models:
		#	pygame.draw.circle(self.screen, GREEN, sprite.rect.center, sprite.true_cohesion_radius, 1)
		
		
		if self.selected_model != None:
			#Selected model indicator
			pygame.draw.circle(self.screen, YELLOW, self.selected_model.rect.center, self.selected_model.radius, 0)
			if self.selected_model.cohesion:
				pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)

			#Melee radius (one inch)
			for sprite in self.targets:
				pygame.draw.circle(self.screen, RED, sprite.rect.center, sprite.true_melee_radius, 1)
			for sprite in self.selectable_models:
				if sprite != self.selected_model:
					pygame.draw.circle(self.screen, GREEN, (sprite.x, sprite.y), sprite.true_cohesion_radius, 1)

		self.draw_cohesion_indicator()

		#Draws useful radii on model selection
		if self.selected_model != None:
			self.draw_radii()	

		#Turn count display text
		largeText = pygame.font.Font('freesansbold.ttf', 32)
		TextSurf, TextRect = text_objects("Turn #{}".format(self.turn_count), largeText)
		TextRect.center = ((WIDTH/8), 14)
		self.screen.blit(TextSurf, TextRect)

		"""
		#Placeholder "Current Phase" Text 
		largeText = pygame.font.Font('freesansbold.ttf', 32)
		TextSurf, TextRect = text_objects("Current phase: {}".format(self.current_phase), largeText)
		TextRect.center = ((WIDTH/2), 16)
		self.screen.blit(TextSurf, TextRect)
		"""

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