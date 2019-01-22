"""40k Pygame Adapation
Please see README.md for details on game rules and controls.
"""

import pygame, random
from pygame.locals import *
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

#Load game graphics

def intersection(a, b):
	#c = []
	#for target in a:
		#if target in b:
			#c.append(target)
	c = [value for value in b if value in a]
	return c

class Game:
	#Initialize program, game window, etc.
	def __init__(self):
		pygame.init() 
		#pygame.mixer.init()
		#flags = FULLSCREEN | DOUBLEBUF | HWSURFACE
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		self.running = True

	def load_data(self):
		self.game_folder = path.dirname(__file__)
		self.img_dir = path.join(self.game_folder, 'img')
		self.map_data = []
		with open(path.join(self.game_folder, 'map.txt'), 'rt') as f:
			for line in f:
				self.map_data.append(line)

		self.spritesheet = Spritesheet(path.join(self.img_dir, 'hyptosis_sprites.png'))

	#Initialize a new game
	def new(self):
		print("\nNEW GAME START\n")
		self.load_data()
		self.turn_count = 1
		#self.phases = ["Movement Phase", "Shooting Phase"]
		self.current_phase = "Movement Phase"
		self.previous_phase = None
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
		self.shooting_models = []
		self.target_model = None
		self.target_unit = None
		self.unallocated_wounds = 0
		self.charging_unit = None
		self.charge_target_unit = None
		self.charge_range = 0

		self.reset_all_button = Button(self, "RESET ALL MOVES", self.generic_font, self.mediumText, WHITE,  WIDTH/2, HEIGHT-3*TILESIZE, 5*TILESIZE, 2*TILESIZE, "center")
		self.attack_button = Button(self, "FIRE WEAPON", self.generic_font, self.mediumText, WHITE,  WIDTH/2, HEIGHT-3*TILESIZE, 5*TILESIZE, 2*TILESIZE, "center")
		self.charge_button = Button(self, "CONFIRM CHARGE TARGET", self.generic_font, self.mediumText, WHITE,  WIDTH/2, HEIGHT-3*TILESIZE, 5*TILESIZE, 2*TILESIZE, "center")

		

		#TEST SPAWNS
		#Bullet(self, create_ranged_weapon_by_name('Bolter'), self.selected_model)
		
		#Initialize army, unit objects
		self.army1 = Army('Black Templars')
		self.army1.add_unit(Unit(self, 'Crusader Squad 1'))
		self.army1.add_unit(Unit(self, 'Crusader Squad 2'))

		self.army2 = Army('Orkz')
		self.army2.add_unit(Unit(self, 'Ork Boyz 1'))
		self.army2.add_unit(Unit(self, 'Ork Boyz 2'))
		self.army2.add_unit(Unit(self, 'Ork Boyz 3'))
		
		self.active_army = self.army1

		#Create walls, enemies from map.txt
		for row, tiles in enumerate(self.map_data):		#enumerate gets the index as well as the value
			for col, tile in enumerate(tiles):
				if tile == '1':
					Wall(self, col, row)

				elif tile == 'M':
					model = create_model_by_name('Initiate', self, col, row)
					self.army1.units[0].add_model(model)
					model.unit = self.army1.units[0]
					model.add_weapon(create_ranged_weapon_by_name('Bolter'))

				elif tile == 'N':
					model = create_model_by_name('Initiate', self, col, row)
					self.army1.units[1].add_model(model)
					model.unit = self.army1.units[1]
					model.add_weapon(create_ranged_weapon_by_name('Bolter'))

				elif tile == 'P':
					model = create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[0].add_model(model)
					model.unit = self.army2.units[0]
					model.add_weapon(create_ranged_weapon_by_name('Shoota'))
					model.image = self.spritesheet.get_image(424, 882, 28, 33)
					model.image.set_colorkey(WHITE)

				elif tile == 'A':
					model = create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[1].add_model(model)
					model.unit = self.army2.units[1]
					model.add_weapon(create_ranged_weapon_by_name('Shoota'))
					model.image = self.spritesheet.get_image(424, 882, 28, 33)
					model.image.set_colorkey(WHITE)

				elif tile == 'G':
					model = create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[2].add_model(model)
					model.unit = self.army2.units[2]
					model.add_weapon(create_ranged_weapon_by_name('Shoota'))
					model.image = self.spritesheet.get_image(424, 882, 28, 33)
					model.image.set_colorkey(WHITE)

		for unit in self.army1.units:
			for model in unit.models:
				self.selectable_models.add(model)

		for unit in self.army2.units:
			for model in unit.models:
				self.targets.add(model)

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

	#Switches active army. Meant to be used at the end of the last phase (morale phase). Turn count incremented here
	#Also checks for whether either of the armies has been destroyed.
	def change_active(self):
		if self.active_army == self.army1:
			self.active_army = self.army2
			active_army = self.army2
			inactive_army = self.army1

		elif self.active_army == self.army2:
			self.turn_count += 1
			self.active_army = self.army1
			active_army = self.army1
			inactive_army = self.army2

		self.selectable_models.empty()
		self.targets.empty()

		for unit in active_army.units:
			for model in unit.models:
				self.selectable_models.add(model)

		for unit in inactive_army.units:
			for model in unit.models:
				self.targets.add(model)

		if len(self.targets) == 0 or len(self.selectable_models) == 0:
			self.playing = False

	#Repopulates the selectable_models and target sprite groups according to current active_army
	def reset_active(self):
		if self.active_army == self.army1:
			active_army = self.army1
			inactive_army = self.army2

		elif self.active_army == self.army2:
			active_army = self.army2
			inactive_army = self.army1

		self.selectable_models.empty()
		self.targets.empty()

		for unit in active_army.units:
			for model in unit.models:
				self.selectable_models.add(model)

		for unit in inactive_army.units:
			for model in unit.models:
				self.targets.add(model)

	def change_phase(self, new_phase):
		self.previous_phase = self.current_phase
		self.current_phase = new_phase
		print("\n------Changing phase from {} to {}.------".format(self.previous_phase, new_phase))

	#Sets sprites back to their starting positions when the spacebar is pressed
	def reset_moves(self, model):
		if model.x != model.original_pos[0] or model.y != model.original_pos[1]:
			#print("\nSprite at ({},{}) resetting to original_pos = ({},{})".format(model.x, model.y, model.original_pos[0], model.original_pos[1]))
			#print("Max_move before reset: {}".format(model.max_move))
			model.x = model.original_pos[0]
			model.y = model.original_pos[1]
			model.dest_x = model.x
			model.dest_y = model.y
			
			if self.current_phase == "Movement Phase":
				model.max_move = model.original_max_move
				#print("Max_move after reset: {}.".format(model.max_move))
				#print("Sprite location after reset: ({},{})".format(model.x, model.y))
			elif self.current_phase == "Charge Move":
				model.charge_move = self.charge_range

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
		else:
			print("\nUnit cohesion violated. Cannot proceed to next phase.")
			print("Move models into cohesion range or reset moves.")
			return False

	def los_check(self, shooter):
		#x = 1
		self.target_model = None
		self.target_unit = None

		for target in self.targets:
			shot_x = self.selected_model.x - target.x
			shot_y = self.selected_model.y - target.y
			shot_distance = find_hypotenuse(shot_x, shot_y)
			if shot_distance <= self.selected_model.weapons[0].w_range:
				Ray(self, shooter, target, (shooter.x, shooter.y), (target.x, target.y)).cast()
			#print("{}".format(x))
			#x += 1
		#print("\n")
		#print(shooter.valid_shots)

	def melee_ratio(self, sprite_1, sprite_2):
		ratio = (sprite_1.radius + sprite_2.radius + TILESIZE)/(sprite_1.radius + sprite_2.radius)
		return ratio

	#Defines whether or not a charge has succeeded based on melee collision
	#	Sets relevant sprite.in_melee flag to True if the charge succeeds
	def charge_success(self):
		for sprite in self.charging_unit.models:
			if sprite.x != sprite.original_pos[0] or sprite.y != sprite.original_pos[1]:
				for target in self.charge_target_unit.models:
					if pygame.sprite.collide_circle_ratio(self.melee_ratio(sprite, target))(sprite, target):
						for model in self.charging_unit.models:
							model.in_melee = True
						for model in self.target_unit.models:
							model.in_melee = True
						return True
				print("No charging models in melee radius, charge considered to be a failure.")
				print("Reset moves and then press enter to return to charge phase.")
				return False
		print("Charging models have not moved. Returning to Charge Phase.")
		return True


	def clear_selections(self):
		self.selected_model = None
		self.selected_unit = None
		self.target_model = None
		self.target_unit = None

	def clear_valid_shots(self):		
		for unit in self.army1.units:
			unit.valid_shots.clear()
			for model in unit.models:
				model.valid_shots.clear()

		for unit in self.army2.units:
			unit.valid_shots.clear()
			for model in unit.models:
				model.valid_shots.clear()


	def reset_flags(self):
		for model in self.selectable_models:
			model.charged = False
			model.advanced = False
			model.fell_back = False

	def charge_roll(self, unit):
		roll_1 = random.randint(1,6)
		roll_2 = random.randint(1,6)
		roll = roll_1 + roll_2
		print("\nDie rolled; charge distance for {} set to {}".format(unit.name, roll))
		self.charge_range = roll*TILESIZE
		for model in unit.models:
			model.charge_move = self.charge_range


	#Game Loop - Event Handling
	def events(self):
		def model_selection(game):
			for model in game.selectable_models:
				if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
					if self.current_phase == "Shooting Phase" or self.current_phase == "Overwatch":
						if model.in_melee == True:
							print("\nModel is engaged in melee and cannot shoot.")
							return

					elif self.current_phase == "Charge Phase":
						if model.in_melee == True:
							print("\nModel is already engaged in melee and cannot charge.")
							return

					game.selected_model = model
					game.selected_unit = model.unit

					print("\nSelected a model:")
					print(game.selected_model)
					print("Selected model's parent unit:")
					print(game.selected_unit.name)

		def multiple_selection(game):
			if len(game.shooting_models) == 0:
				for model in game.selectable_models:
					if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
						if self.current_phase == "Shooting Phase" or self.current_phase == "Overwatch":
							if model.in_melee == True:
								print("\nModel is engaged in melee and cannot shoot.")
								return

						game.selected_model = model
						game.selected_unit = model.unit
						game.shooting_models.append(model)
						print("\nSelected a model:")
						print(game.selected_model)
						print("Selected model's parent unit:")
						print(game.selected_unit.name)
						print("Models selected:")
						print(game.shooting_models)

			elif len(game.shooting_models) > 0:
				for model in game.selectable_models:
					if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
						if self.current_phase == "Shooting Phase" or self.current_phase == "Overwatch":
							if model.in_melee == True:
								print("\nModel is engaged in melee and cannot shoot.")
								return

						for shooter in game.shooting_models:
							if model == shooter:
								print("Model already a shooter; made it the selected_model.")
								game.selected_model = model
								return

						if game.shooting_models[0].unit == model.unit:
							game.selected_model = model
							game.selected_unit = model.unit
							game.shooting_models.append(model)
							print("\nSelected a model:")
							print(game.selected_model)
							print("Selected model's parent unit:")
							print(game.selected_unit.name)
							print("Models selected:")
							print(game.shooting_models)

						else:
							print("Chosen model not in same unit as currently selected shooting models.")
							print("Please choose a different model or reset shooting models selection with the spacebar.")
							return

		def mass_selection(game):
			if len(game.shooting_models) == 0:
				for model in game.selectable_models:
					if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
						if self.current_phase == "Shooting Phase" or self.current_phase == "Overwatch":
							if model.in_melee == True:
								print("\nModel is engaged in melee and cannot shoot.")
								return

						game.selected_model = model
						game.selected_unit = model.unit
						for model in game.selected_unit.models:
							game.shooting_models.append(model)

						print("\nSelected a model:")
						print(game.selected_model)
						print("Selected model's parent unit:")
						print(game.selected_unit.name)
						print("Models selected:")
						print(game.shooting_models)
						
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
							self.clear_selections()
							self.refresh_moves()
							self.change_phase("Shooting Phase")
	
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
						for model in self.shooting_models:
							model.valid_shots.clear()
						self.shooting_models.clear()
						if self.selected_unit != None:
							self.selected_unit.valid_shots.clear()
						self.clear_selections()

					elif keys[pygame.K_RETURN]:
						self.change_phase("Charge Phase")
						self.shooting_models.clear()
						self.clear_selections()
						self.clear_valid_shots()
						for model in self.selectable_models:
							for weapon in model.weapons:
								weapon.fired = False

						

				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if len(self.shooting_models) == 0:
							multiple_selection(self)
							if len(self.shooting_models) > 0:
								self.los_check(self.selected_model)
								self.selected_unit.valid_shots = self.selected_model.valid_shots
									
						elif len(self.shooting_models) > 0:
							#Attack button
							if self.target_unit != None:
								if self.attack_button.mouse_over():
									for model in self.shooting_models:
										model.attack_with_weapon(self.target_unit)
									if self.unallocated_wounds > 0:
										self.change_phase("Wound Allocation")

								else:
									multiple_selection(self)
									self.los_check(self.selected_model)
									self.selected_unit.valid_shots = intersection(self.selected_unit.valid_shots, self.selected_model.valid_shots)

							else:
								multiple_selection(self)
								self.los_check(self.selected_model)
								self.selected_unit.valid_shots = intersection(self.selected_unit.valid_shots, self.selected_model.valid_shots)

					elif event.button == 2: #Middle mouse button
						self.shooting_models.clear()
						self.selected_unit = None
						mass_selection(self)
						if len(self.shooting_models) > 0:
							self.los_check(self.selected_model)
							self.selected_unit.valid_shots = self.selected_model.valid_shots
							for model in self.shooting_models:
								self.los_check(model)
								self.selected_unit.valid_shots = intersection(self.selected_unit.valid_shots, model.valid_shots)

					elif event.button == 3:	#RMB
						if len(self.shooting_models) > 0:
							self.target_model = None
							self.target_unit = None
							#Target selection
							for model in self.targets:
								if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
									if model in self.selected_unit.valid_shots:
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
						for model in self.target_unit.models:
							if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
								model.wounds -= 1
								self.unallocated_wounds -= 1
								print("\nAllocating wound to: ")
								print(model)
								print("This model is part of unit:")
								print(model.unit.name)
								for model in self.target_unit.models:
									model.update()
								if self.unallocated_wounds <= 0 or len(self.target_unit.models) == 0:
									if self.unallocated_wounds <= 0:
										print("\nAll wounds allocated!")
									elif len(self.target_unit.models) == 0:
										print("\nTarget unit eliminated. No valid targets remain.")
									print("Returning to previous phase")
									self.change_phase(self.previous_phase)
									self.unallocated_wounds = 0
									self.selected_model.valid_shots.clear()
									self.selected_model = None
									self.selected_unit = None
									self.shooting_models.clear()
									self.target_model = None
									self.target_unit = None
									
								else:
									print("\nChosen model not a valid target, please select a model in the target unit.")

					elif event.button == 2:	#Middle mouse button
						pass

					elif event.button == 3: #RMB
						pass

		elif self.current_phase == "Charge Phase":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()

				#Keyboard event handling
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()
					if keys[pygame.K_HOME]:
						g.new()

					elif keys[pygame.K_RETURN]:
						self.change_phase("Movement Phase")
						self.clear_selections()
						self.change_active()
	
				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB ; Mouse event.buttom refers to interger values: 1(left), 2(middle), 3(right), 4(scrl up), 5(scrl down)
						if self.reset_all_button.mouse_over():
							for model in self.selectable_models:
								self.reset_moves(model)

						if self.charge_button.mouse_over() and self.selected_model != None and self.target_model != None:
							print("\nCharge target confirmed. Proceeding to overwatch response.")
							self.change_phase("Overwatch")

							self.selectable_models.empty()
							self.targets.empty()
							for model in self.selected_unit.models:
								self.targets.add(model)
							for model in self.target_unit.models:
								self.selectable_models.add(model)

							self.charge_target_unit = self.target_unit
							self.charging_unit = self.selected_unit
							self.clear_selections()
							self.target_unit = self.charging_unit
							self.selected_unit = self.charge_target_unit

						elif self.selected_model == None:
							model_selection(self)

						elif self.selected_model != None:
							self.selected_model = None 	#Defaults to deselecting current model if another model isn't clicked
							self.selected_unit = None
							model_selection(self)

					elif event.button == 2:	#Middle mouse button
						pass

					elif event.button == 3: #RMB
						if self.selected_model != None:
							self.target_model = None
							self.target_unit = None
							charge_x = self.selected_model.x - pygame.mouse.get_pos()[0]
							charge_y = self.selected_model.y - pygame.mouse.get_pos()[1]
							charge_distance = find_hypotenuse(charge_x, charge_y)

							#Target selection
							for model in self.targets:
								if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
									if charge_distance <= 12*TILESIZE:
										self.target_model = model
										self.target_unit = model.unit
									else:
										print("\nAttempted selection outside of max charge range.")
										print("Select a different charge target.")

		elif self.current_phase == "Overwatch":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()

				#Keyboard event handling
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()

					if keys[pygame.K_HOME]:
						g.new()

					elif keys[pygame.K_SPACE]:
						for model in self.shooting_models:
							model.valid_shots.clear()
						self.shooting_models.clear()
						if self.selected_unit != None:
							self.selected_unit.valid_shots.clear()
						self.clear_selections()

					elif keys[pygame.K_RETURN]:
						if len(self.charging_unit.models) == 0:
							self.change_phase("Charge Phase")
							return
						self.change_phase("Charge Move")

						for model in self.selectable_models:
							for weapon in model.weapons:
								weapon.fired = False

						self.selectable_models.empty()
						self.targets.empty()
						self.shooting_models.clear()

						for model in self.charging_unit.models:
							self.selectable_models.add(model)

						self.clear_selections()
						self.clear_valid_shots()
						self.target_unit = self.charge_target_unit
						self.selected_unit = self.charging_unit
						self.charge_roll(self.charging_unit)
						
				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if len(self.shooting_models) == 0:
							multiple_selection(self)
							if len(self.shooting_models) > 0:
								self.los_check(self.selected_model)
								self.selected_unit.valid_shots = self.selected_model.valid_shots
									
						elif len(self.shooting_models) > 0:
							#Attack button
							if self.target_unit != None:
								if self.attack_button.mouse_over():
									for model in self.shooting_models:
										model.attack_with_weapon(self.target_unit)
									if self.unallocated_wounds > 0:
										self.change_phase("Wound Allocation")

								else:
									multiple_selection(self)
									self.los_check(self.selected_model)
									self.selected_unit.valid_shots = intersection(self.selected_unit.valid_shots, self.selected_model.valid_shots)

							else:
								multiple_selection(self)
								self.los_check(self.selected_model)
								self.selected_unit.valid_shots = intersection(self.selected_unit.valid_shots, self.selected_model.valid_shots)

					elif event.button == 2: #Middle mouse button
						self.shooting_models.clear()
						self.selected_unit = None
						mass_selection(self)
						if len(self.shooting_models) > 0:
							self.los_check(self.selected_model)
							self.selected_unit.valid_shots = self.selected_model.valid_shots
							for model in self.shooting_models:
								self.los_check(model)
								self.selected_unit.valid_shots = intersection(self.selected_unit.valid_shots, model.valid_shots)

					elif event.button == 3:	#RMB
						if len(self.shooting_models) > 0:
							self.target_model = None
							self.target_unit = None
							#shot_x = self.selected_model.x - pygame.mouse.get_pos()[0]
							#shot_y = self.selected_model.y - pygame.mouse.get_pos()[1]
							#shot_distance = find_hypotenuse(shot_x, shot_y)

							#Target selection
							for model in self.targets:
								if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
									if model in self.selected_unit.valid_shots:
										self.target_model = model
										self.target_unit = model.unit

		elif self.current_phase == "Charge Move":
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
						if self.charge_success():
							if self.cohesion_check():
								self.change_phase("Charge Phase")
								for model in self.charging_unit.models:
									model.charge_move = 0
								self.clear_selections()
								self.charging_unit = None
								self.charge_target_unit = None
								self.reset_active()
	
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

				
	#Game Loop - Update
	def update(self):
		self.all_sprites.update()

	#Draws reference grid
	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, LIGHTGREY, (x, 0 ), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

	def draw_sprites(self):
		self.all_sprites.draw(self.screen)

		#for sprite in self.selectable_models:
			#pygame.draw.circle(self.screen, WHITE, sprite.rect.center, sprite.radius, 0)

		#for sprite in self.targets:
			#pygame.draw.circle(self.screen, RED, sprite.rect.center, sprite.radius, 0)

	#Total Unit Cohesion Checker
	def draw_cohesion_indicator(self):
		pygame.draw.circle(self.screen, RED, (int(23*WIDTH/32), int(HEIGHT-5*TILESIZE)), 15, 0)	
		unit_cohesions = []
		for sprite in self.selectable_models:
			unit_cohesions.append(sprite.cohesion)
		if all(unit_cohesions):
			pygame.draw.circle(self.screen, GREEN, (int(23*WIDTH/32), int(HEIGHT-5*TILESIZE)), 15, 0)

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
			
		if self.current_phase == "Movement Phase":	
			#Model base drawing/coloring
			if self.selected_unit != None and self.selected_model != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

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

			#Buttons
			self.reset_all_button.draw()
			self.reset_all_button.fill()

			#Controls Info Text	
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: move model|", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: reset selected model's move|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")

		elif self.current_phase == "Shooting Phase":
			#Model base drawing/coloring
			if self.selected_unit != None and self.selected_model != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			#Model base drawing/coloring
			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)

				#Weapon range radius
				pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), int(self.selected_model.weapons[0].w_range), 1)

				#Targets in LOS
				if self.selected_unit != None:
					if len(self.selected_unit.valid_shots) > 0:
						for model in self.selected_unit.valid_shots:
							pygame.draw.circle(self.screen, YELLOW, model.rect.center, model.radius, 0)

				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, model.rect.center, model.radius, 0)

			if len(self.shooting_models) > 0:
				for model in self.shooting_models:
					pygame.draw.circle(self.screen, BLUE, model.rect.center, int((model.radius)/2), 0)

			#Buttons
			self.attack_button.draw()
			self.attack_button.fill()

			#Controls Info Text
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: select entire unit|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: select target|", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: deselect shooters|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")

		elif self.current_phase == "Wound Allocation":
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			#Model base drawing/coloring
			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)

				#Weapon range radius
				pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), int(self.selected_model.weapons[0].w_range), 1)

				#Targets in LOS
				if self.selected_unit != None:
					if len(self.selected_unit.valid_shots) > 0:
						for model in self.selected_unit.valid_shots:
							pygame.draw.circle(self.screen, YELLOW, model.rect.center, model.radius, 0)

				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, model.rect.center, model.radius, 0)

			#Unallocated wound counter
			self.draw_text("{}Wound(s) to allocate!".format(self.unallocated_wounds), self.generic_font, self.largeText, YELLOW, WIDTH/2, HEIGHT - 2*TILESIZE, "center")

			#Controls Info Text
			self.draw_text("|LMB: allocate wound to model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: N/A|", self.generic_font, self.mediumText, WHITE, (8*WIDTH/32), HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: N/A|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: N/A|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")

		elif self.current_phase == "Charge Phase":
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, YELLOW, self.selected_model.rect.center, self.selected_model.radius, 0)
				if self.selected_model.cohesion:
					pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)

				#Remaining charge move radius
				if self.selected_model.charge_move != 0:
					pygame.draw.circle(self.screen, YELLOW, (self.selected_model.x, self.selected_model.y), int(self.charge_range), 1)

				#Max charge move radius
				if self.selected_model.charge_move == 0:
					pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), 12*TILESIZE, 1)

				#Melee radius (one inch)
				for sprite in self.targets:
					pygame.draw.circle(self.screen, RED, sprite.rect.center, sprite.true_melee_radius, 1)

				#Cohesion radius (two inches)	
				for sprite in self.selected_model.unit.models:
					if sprite != self.selected_model:
						pygame.draw.circle(self.screen, GREEN, (sprite.x, sprite.y), sprite.true_cohesion_radius, 1)

				#Target unit indicator
				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, model.rect.center, model.radius, 0)

			#Draws large semi-circle cohesion indicator
			self.draw_cohesion_indicator()	

			#Buttons
			self.charge_button.draw()
			self.charge_button.fill()

			#Controls Info Text	
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: select charge target|", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: N/A|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")

		elif self.current_phase == "Overwatch":
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)

				#Weapon range radius
				pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), int(self.selected_model.weapons[0].w_range), 1)

				#Targets in LOS
				if self.selected_unit != None:
					if len(self.selected_unit.valid_shots) > 0:
						for model in self.selected_unit.valid_shots:
							pygame.draw.circle(self.screen, YELLOW, model.rect.center, model.radius, 0)

				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, model.rect.center, model.radius, 0)

			if len(self.shooting_models) > 0:
				for model in self.shooting_models:
					pygame.draw.circle(self.screen, BLUE, model.rect.center, int((model.radius)/2), 0)

			#Buttons
			self.attack_button.draw()
			self.attack_button.fill()

			#Controls Info Text
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: select entire unit|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: select target|", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: deselect shooters|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")	

		elif self.current_phase == "Charge Move":	
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, YELLOW, self.selected_model.rect.center, self.selected_model.radius, 0)
				if self.selected_model.cohesion:
					pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)

				#Weapon range radius
				pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), int(self.selected_model.weapons[0].w_range), 1)

				#Remaining move radius
				if self.selected_model.charge_move >= 1:
					pygame.draw.circle(self.screen, YELLOW, (self.selected_model.x, self.selected_model.y), int(self.selected_model.charge_move), 1)

				#Melee radius (one inch)
				if self.target_unit != None:
					for sprite in self.target_unit.models:
						pygame.draw.circle(self.screen, RED, sprite.rect.center, sprite.true_melee_radius, 1)

				#Cohesion radius (two inches)	
				for sprite in self.selected_model.unit.models:
					if sprite != self.selected_model:
						pygame.draw.circle(self.screen, GREEN, (sprite.x, sprite.y), sprite.true_cohesion_radius, 1)

			#Draws large semi-circle cohesion indicator
			self.draw_cohesion_indicator()	

			#Buttons
			self.reset_all_button.draw()
			self.reset_all_button.fill()

			#Controls Info Text	
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: move model|", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: reset selected model's move|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")

		#General info text
		self.draw_text("Turn #{}: {} {}".format(self.turn_count, self.active_army.name, self.current_phase), self.generic_font, self.largeText, WHITE, WIDTH/2, TILESIZE, "center")
		self.draw_text("|HOME: reset game|", self.generic_font, self.mediumText, WHITE, WIDTH-(TILESIZE*2), TILESIZE, "e")
		fps = int(self.clock.get_fps())
		self.draw_text("FPS: {}".format(fps), self.generic_font, self.mediumText, WHITE, 2*WIDTH/32, TILESIZE, "w")
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