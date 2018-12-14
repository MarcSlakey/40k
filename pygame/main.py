"""40k Pygame Adapation
Please see README.md for details on game rules and controls.
"""

import pygame, random
import sys
from os import path
from settings import *
from buttons import *
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
		print("\nNEW GAME START\n")
		self.load_data()
		self.turn_count = 1
		#self.phases = ["Movement Phase", "Shooting Phase"]
		self.current_phase = "Movement Phase"
		self.all_sprites = pygame.sprite.Group() 
		self.all_models = pygame.sprite.Group()
		self.selectable_models = pygame.sprite.Group()
		self.targets = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.rays = pygame.sprite.Group()
		self.buttons = []
		self.selected_model = None
		self.selected_unit = None
		self.target_model = None
		self.target_unit = None
		self.unallocated_wounds = 0

		self.reset_all_button = Button(self, "RESET MOVES", self.generic_font, self.mediumText, WHITE,  WIDTH*3/4, HEIGHT-4*TILESIZE, 5*TILESIZE, 2*TILESIZE, "center")

		self.attack_button = Button(self, "FIRE WEAPON", self.generic_font, self.mediumText, WHITE,  WIDTH*1/4, HEIGHT-4*TILESIZE, 5*TILESIZE, 2*TILESIZE, "center")
		

		#TEST SPAWNS
		#Bullet(self, create_ranged_weapon_by_name('Bolter'), self.selected_model)
		
		#Initialize army, unit objects
		self.army1 = Army('Black Templars')
		self.army1.add_unit(Unit('Crusader Squad 1'))
		self.army1.add_unit(Unit('Crusader Squad 2'))

		self.army2 = Army('Orkz')
		self.army2.add_unit(Unit('Ork Boyz 1'))
		self.army2.add_unit(Unit('Ork Boyz 2'))
		self.army2.add_unit(Unit('Ork Boyz 3'))
		

		#Create walls, enemies from map.txt
		for row, tiles in enumerate(self.map_data):		#enumerate gets the index as well as the value
			for col, tile in enumerate(tiles):
				if tile == '1':
					Wall(self, col, row)

				elif tile == 'M':
					model = create_model_by_name('Initiate', self, col, row)
					self.army1.units[0].add_model(model)
					model.add(self.selectable_models)
					model.unit = self.army1.units[0]
					model.add_weapon(create_ranged_weapon_by_name('Bolter'))

				elif tile == 'N':
					model = create_model_by_name('Initiate', self, col, row)
					self.army1.units[1].add_model(model)
					model.add(self.selectable_models)
					model.unit = self.army1.units[1]
					model.add_weapon(create_ranged_weapon_by_name('Bolter'))

				elif tile == 'P':
					model = create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[0].add_model(model)
					model.add(self.targets)
					model.unit = self.army2.units[0]
					model.add_weapon(create_ranged_weapon_by_name('Shoota'))

				elif tile == 'A':
					model = create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[1].add_model(model)
					model.add(self.targets)
					model.unit = self.army2.units[1]
					model.add_weapon(create_ranged_weapon_by_name('Shoota'))

				elif tile == 'G':
					model = create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[2].add_model(model)
					model.add(self.targets)
					model.unit = self.army2.units[2]
					model.add_weapon(create_ranged_weapon_by_name('Shoota'))

		print(self.army1)
		print(self.army2)

		self.run()

	#Main Game Loop
	def run(self):
		self.playing = True
		while self.playing:
			# Keep loop running at the right speed; defaults unit is milliseconds, converted here to seconds
			dt = self.clock.tick(FPS)/1000
			self.events()			
			self.update()
			self.draw()

	def quit(self):
		print("QUITTING")
		pygame.quit()
		sys.exit()

	#Sets sprites back to their starting positions when the spacebar is pressed
	def reset_moves(self, model):
		if model.x != model.original_pos[0] or model.y != model.original_pos[1]:
			#print("\nSprite at ({},{}) resetting to original_pos = ({},{})".format(model.x, model.y, model.original_pos[0], model.original_pos[1]))
			#print("Max_move before reset: {}".format(model.max_move))
			model.x = model.original_pos[0]
			model.y = model.original_pos[1]
			model.dest_x = model.x
			model.dest_y = model.y
			model.max_move = model.original_max_move
			#print("Max_move after reset: {}.".format(model.max_move))
			#print("Sprite location after reset: ({},{})".format(model.x, model.y))

	def refresh_moves(self):
		for sprite in self.selectable_models:
			sprite.max_move = sprite.original_max_move
			sprite.original_pos = (sprite.x, sprite.y)

	def cohesion_check(self):
		unit_cohesions = []
		for sprite in self.selectable_models:
			unit_cohesions.append(sprite.cohesion)
		if all(unit_cohesions):
			return True

	def los_check(self, shooter):
		#x = 1
		for target in self.targets:
			#self.clock.tick(FPS) 	#not sure whether or not to tick here
			pygame.draw.circle(self.screen, GREEN, target.rect.center, target.radius, 0)
			pygame.display.update()
			Ray(self, shooter, target, (shooter.x, shooter.y), (target.x, target.y)).cast()
			#print("{}".format(x))
			#x += 1
		#print("\n")
		#print(shooter.valid_shots)

	#Game Loop - Event Handling
	def events(self):
		def model_selection(game):
			for model in game.selectable_models:
				if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
					game.selected_model = model
					print("\nSelected a model:")
					print(game.selected_model)
					game.selected_unit = model.unit
					print("Selected model's parent unit:")
					print(game.selected_unit.name)
					
		if self.current_phase == "Movement Phase":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()

				#Keyboard event handling
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()
					if keys[pygame.K_HOME]:
						g.new()

					elif self.selected_model != None and keys[pygame.K_SPACE]:
						self.reset_moves(self.selected_model)

					elif keys[pygame.K_RETURN]:
						if self.cohesion_check():
							self.selected_model = None
							self.selected_unit = None
							self.current_phase = "Shooting Phase"
	
				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB ; Mouse event.buttom refers to interger values: 1(left), 2(middle), 3(right), 4(scrl up), 5(scrl down)
						if self.reset_all_button.mouse_over():
							for model in self.selectable_models:
								self.reset_moves(model)

						if self.selected_model == None:
							model_selection(self)

						elif self.selected_model != None:
							self.selected_model = None 	#Defaults to deselecting current model if another model isn't clicked
							model_selection(self)

					elif event.button == 2:	#Middle mouse button
						pass

					elif event.button == 3: #RMB
						if self.selected_model != None:
							self.selected_model.dest_x = pygame.mouse.get_pos()[0]
							self.selected_model.dest_y = pygame.mouse.get_pos()[1]

		elif self.current_phase == "Shooting Phase":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()

				#Keyboard event handling
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()

					if keys[pygame.K_HOME]:
						g.new()

					elif keys[pygame.K_SPACE]:
						pass

					elif keys[pygame.K_RETURN]:
						self.refresh_moves()
						self.turn_count += 1
						self.current_phase = "Movement Phase"
						self.selected_model = None
						self.selected_unit = None
						self.target_model = None
						self.target_unit = None
						for model in self.selectable_models:
							for weapon in model.weapons:
								weapon.fired = False

				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if self.selected_model == None:
							model_selection(self)
							if self.selected_model != None:
								self.los_check(self.selected_model)
									
						elif self.selected_model != None:
							#Attack button
							if self.target_unit != None:
								if self.attack_button.mouse_over():
									self.selected_model.attack_with_weapon(self.target_unit)
									if self.unallocated_wounds > 0:
										self.current_phase = "Wound Allocation"

								else:
									self.selected_model.valid_shots.clear()
									self.selected_model = None 	#Defaults to deselecting current model if another model isn't clicked
									self.selected_unit = None
									self.target_model = None
									self.target_unit = None
									model_selection(self)
									if self.selected_model != None:
										self.los_check(self.selected_model)
							else:
									self.selected_model.valid_shots.clear()
									self.selected_model = None 	#Defaults to deselecting current model if another model isn't clicked
									self.selected_unit = None
									self.target_model = None
									self.target_unit = None
									model_selection(self)
									if self.selected_model != None:
										self.los_check(self.selected_model)

					elif event.button == 2: #Middle mouse button
						if self.selected_model != None:
							self.los_check(self.selected_model)

					elif event.button == 3:	#RMB
						if self.selected_model != None:
							self.target_model = None
							self.target_unit = None
							shot_x = self.selected_model.x - pygame.mouse.get_pos()[0]
							shot_y = self.selected_model.y - pygame.mouse.get_pos()[1]
							shot_distance = find_hypotenuse(shot_x, shot_y)

							#Target selection
							for model in self.targets:
								if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
									if shot_distance <= self.selected_model.weapons[0].w_range:
										if model in self.selected_model.valid_shots:
											self.target_model = model
											self.target_unit = model.unit

		elif self.current_phase == "Wound Allocation":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()

				#Keyboard event handling
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()
					if keys[pygame.K_HOME]:
						g.new()

					elif keys[pygame.K_RETURN]:
						pass
	
				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB ; Mouse event.buttom refers to interger values: 1(left), 2(middle), 3(right), 4(scrl up), 5(scrl down)
						for model in self.targets:
							if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
								if model in self.target_unit.models:
									model.wounds -= 1
									self.unallocated_wounds -= 1
									print("\nAllocating wound to: ")
									print(model)
									print("This model is part of unit:")
									print(model.unit)
									if self.unallocated_wounds <= 0:
										print("All wounds allocated, returning to shooting phase")
										self.selected_model.valid_shots.clear()
										self.selected_model = None
										self.selected_unit = None
										self.target_model = None
										self.target_unit = None
										self.current_phase = "Shooting Phase"

								else:
									print("Chosen model not a valid target, please select a model in the target unit.")

					elif event.button == 2:	#Middle mouse button
						pass

					elif event.button == 3: #RMB
						pass
				
	#Game Loop - Update
	def update(self):
		self.all_sprites.update()

		if len(self.targets) == 0:
			self.playing = False

	#Draws reference grid
	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, LIGHTGREY, (x, 0 ), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

	def draw_sprites(self):
		self.all_sprites.draw(self.screen)

		for sprite in self.selectable_models:
			pygame.draw.circle(self.screen, WHITE, sprite.rect.center, sprite.radius, 0)

		for sprite in self.targets:
			pygame.draw.circle(self.screen, RED, sprite.rect.center, sprite.radius, 0)

	def draw_buttons(self):
		if self.current_phase == "Movement Phase":
			self.reset_all_button.draw()
			self.reset_all_button.fill()

		elif self.current_phase == "Shooting Phase":
			self.attack_button.draw()
			self.attack_button.fill()


	#Total Unit Cohesion Checker
	def draw_cohesion_indicator(self):
		pygame.draw.circle(self.screen, RED, ((24*WIDTH//32)-15, HEIGHT-TILESIZE), 15, 0)	
		unit_cohesions = []
		for sprite in self.selectable_models:
			unit_cohesions.append(sprite.cohesion)
		if all(unit_cohesions):
			pygame.draw.circle(self.screen, GREEN, ((24*WIDTH//32)-15, HEIGHT-TILESIZE), 15, 0)

	#Text constructor from https://www.youtube.com/watch?v=MJ2GLVA7kaU
	def draw_text(self, text, font_name, size, color, x, y, align="nw"):
		font = pygame.font.Font(font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		if align == "nw":
			text_rect.topleft = (x, y)
		if align == "ne":
			text_rect.topright = (x, y)
		if align == "sw":
			text_rect.bottomleft = (x, y)
		if align == "se":
			text_rect.bottomright = (x, y)
		if align == "n":
			text_rect.midtop = (x, y)
		if align == "s":
			text_rect.midbottom = (x, y)
		if align == "e":
			text_rect.midright = (x, y)
		if align == "w":
			text_rect.midleft = (x, y)
		if align == "center":
			text_rect.center = (x, y)
		self.screen.blit(text_surface, text_rect)

	generic_font = 'freesansbold.ttf'
	mediumText = 20
	largeText = 32

	#Game Loop - Draw
	def draw(self):
		self.screen.fill(BLACK)	
		self.draw_grid()

		def text_objects(text, font):
			textSurface = font.render(text, True, WHITE)
			return textSurface, textSurface.get_rect()
		
		self.draw_sprites()
		self.draw_buttons()
			
		if self.current_phase == "Movement Phase":	
			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, YELLOW, self.selected_model.rect.center, self.selected_model.radius, 0)
				if self.selected_model.cohesion:
					pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)

				#Weapon range radius
				pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), int(self.selected_model.weapons[0].w_range), 1)

				#Remaining move radius
				if self.selected_model.max_move >= 1:
					pygame.draw.circle(self.screen, YELLOW, (self.selected_model.x, self.selected_model.y), int(self.selected_model.max_move), 1)

				#Melee radius (one inch)
				for sprite in self.targets:
					pygame.draw.circle(self.screen, RED, sprite.rect.center, sprite.true_melee_radius, 1)

				#Cohesion radius (two inches)	
				for sprite in self.selected_model.unit.models:
					if sprite != self.selected_model:
						pygame.draw.circle(self.screen, GREEN, (sprite.x, sprite.y), sprite.true_cohesion_radius, 1)

			#Draws large semi-circle cohesion indicator
			self.draw_cohesion_indicator()	

			#Controls Info Text	
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-TILESIZE, "w")
			self.draw_text("|RMB: move model|", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-TILESIZE, "w")
			self.draw_text("|SPACEBAR: reset selected model's move|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-TILESIZE, "w")

		elif self.current_phase == "Shooting Phase":
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)

				#Weapon range radius
				pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), int(self.selected_model.weapons[0].w_range), 1)

				#Targets in LOS
				for model in self.selected_model.valid_shots:
					pygame.draw.circle(self.screen, YELLOW, model.rect.center, model.radius, 0)

				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, model.rect.center, model.radius, 0)

			#Controls Info Text
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-TILESIZE, "w")
			self.draw_text("|RMB: delete target|", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-TILESIZE, "w")
			self.draw_text("|SPACEBAR: N/A|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-TILESIZE, "w")

		elif self.current_phase == "Wound Allocation":
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)

				#Weapon range radius
				pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), int(self.selected_model.weapons[0].w_range), 1)

				#Targets in LOS
				for model in self.selected_model.valid_shots:
					pygame.draw.circle(self.screen, YELLOW, model.rect.center, model.radius, 0)

				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, model.rect.center, model.radius, 0)

			#Unallocated wound counter
			self.draw_text("{}Wound(s) to allocate!".format(self.unallocated_wounds), self.generic_font, self.largeText, YELLOW, WIDTH/2, HEIGHT - 5*TILESIZE, "center")

			#Controls Info Text
			self.draw_text("|LMB: allocate wound to model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-TILESIZE, "w")
			self.draw_text("|RMB: N/A|", self.generic_font, self.mediumText, WHITE, (8*WIDTH/32), HEIGHT-TILESIZE, "w")
			self.draw_text("|SPACEBAR: N/A|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-TILESIZE, "w")
			self.draw_text("|RETURN: N/A|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-TILESIZE, "w")

		#General info text
		self.draw_text("Turn #{}: {}".format(self.turn_count, self.current_phase), self.generic_font, self.largeText, WHITE, WIDTH/2, TILESIZE, "center")
		self.draw_text("|HOME: reset game|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, TILESIZE, "w")

		self.bullets.draw

		pygame.display.update()
		

	def show_start_screen(self):
		self.screen.fill(BLACK)
		self.draw_text("40k Pygame Adaptation", self.generic_font, 120, YELLOW, WIDTH/2, HEIGHT*1/4, "center")
		self.draw_text("Please see the readme for game rules", self.generic_font, 60, WHITE, WIDTH/2, HEIGHT*2/4, "center")
		self.draw_text("Press any key to start...", self.generic_font, 60, WHITE, WIDTH/2, HEIGHT*3/4, "center")
		pygame.display.flip()
		self.wait_for_key()

	def show_game_over_screen(self):
		self.screen.fill(BLACK)
		self.draw_text("Victory!", self.generic_font, 120, GREEN, WIDTH/2, HEIGHT*1/4, "center")
		self.draw_text("All targets eliminated", self.generic_font, 60, WHITE, WIDTH/2, HEIGHT*2/4, "center")
		self.draw_text("Press any key to start a new game", self.generic_font, 60, WHITE, WIDTH/2, HEIGHT*3/4, "center")
		pygame.display.flip()
		self.wait_for_key()

	def wait_for_key(self):
		pygame.event.wait()
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					waiting = False
					self.quit()
				if event.type == pygame.KEYUP:
					waiting = False

g = Game()
g.show_start_screen()
while g.running:
	g.new()
	g.show_game_over_screen()

pygame.quit()