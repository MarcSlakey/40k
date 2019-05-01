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
		self.fight_subphase = None
		self.all_sprites = pygame.sprite.Group() 
		self.all_models = pygame.sprite.Group()
		self.selectable_models = pygame.sprite.Group()
		self.targets = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.rays = pygame.sprite.Group()
		self.buttons = []
		self.show_radii = True
		self.selected_model = None
		self.selected_unit = None
		self.shooting_models = []
		self.fighting_models = []
		self.target_model = None
		self.target_unit = None
		self.unallocated_wounds = 0
		self.charging_unit = None
		self.charge_target_unit = None
		self.charge_range = 0
		self.ineligible_fight_units = []

		self.toggle_radii_button = Button(self, "SHOW/HIDE RADII", self.generic_font, self.mediumText, WHITE,  3*WIDTH/4, HEIGHT-3*TILESIZE, 5*TILESIZE, 2*TILESIZE, "center")
		self.reset_all_button = Button(self, "RESET ALL MOVES", self.generic_font, self.mediumText, WHITE,  WIDTH/2, HEIGHT-3*TILESIZE, 5*TILESIZE, 2*TILESIZE, "center")
		self.attack_button = Button(self, "ATTACK", self.generic_font, self.mediumText, WHITE,  WIDTH/2, HEIGHT-3*TILESIZE, 5*TILESIZE, 2*TILESIZE, "center")
		self.charge_button = Button(self, "CONFIRM CHARGE TARGET", self.generic_font, self.mediumText, WHITE,  WIDTH/2, HEIGHT-3*TILESIZE, 5*TILESIZE, 2*TILESIZE, "center")
		self.fight_button = Button(self, "FIGHT WITH THIS UNIT", self.generic_font, self.mediumText, WHITE,  WIDTH/2, HEIGHT-3*TILESIZE, 5*TILESIZE, 2*TILESIZE, "center")

		

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
		self.army2.add_unit(Unit(self, 'Ork Boyz 4'))
		
		self.active_army = self.army1
		self.inactive_army = self.army2

		#Create models and wall sprites from map.txt
		for row, tiles in enumerate(self.map_data):		#enumerate gets the index as well as the value
			for col, tile in enumerate(tiles):
				if tile == '1':
					Wall(self, col, row)

				elif tile == 'M':
					model = create_model_by_name('Initiate', self, col, row)
					self.army1.units[0].add_model(model)
					model.unit = self.army1.units[0]
					model.add_ranged_weapon(create_ranged_weapon_by_name('Test Gun'))
					model.add_melee_weapon(create_melee_weapon_by_name('CCW'))
					model.image = pygame.image.load(path.join(self.img_dir, 'Templar 4.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()

				elif tile == 'N':
					model = create_model_by_name('Initiate', self, col, row)
					self.army1.units[1].add_model(model)
					model.unit = self.army1.units[1]
					model.add_ranged_weapon(create_ranged_weapon_by_name('Test Gun'))
					model.add_melee_weapon(create_melee_weapon_by_name('CCW'))
					model.image = pygame.image.load(path.join(self.img_dir, 'Templar 6.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()

				elif tile == 'P':
					model = create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[0].add_model(model)
					model.unit = self.army2.units[0]
					model.add_ranged_weapon(create_ranged_weapon_by_name('Test Gun'))
					model.add_melee_weapon(create_melee_weapon_by_name('CCW'))
					model.image = pygame.image.load(path.join(self.img_dir, 'Ork Slugga 3.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()

				elif tile == 'A':
					model = create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[1].add_model(model)
					model.unit = self.army2.units[1]
					model.add_ranged_weapon(create_ranged_weapon_by_name('Test Gun'))
					model.add_melee_weapon(create_melee_weapon_by_name('CCW'))
					model.image = pygame.image.load(path.join(self.img_dir, 'Ork Slugga 3.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()

				elif tile == 'G':
					model = create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[2].add_model(model)
					model.unit = self.army2.units[2]
					model.add_ranged_weapon(create_ranged_weapon_by_name('Test Gun'))
					model.add_melee_weapon(create_melee_weapon_by_name('CCW'))
					model.image = pygame.image.load(path.join(self.img_dir, 'Ork Slugga 3.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()

				elif tile == 'K':
					model = create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[3].add_model(model)
					model.unit = self.army2.units[3]
					model.add_ranged_weapon(create_ranged_weapon_by_name('Shoota'))
					model.add_melee_weapon(create_melee_weapon_by_name('CCW'))
					model.image = pygame.image.load(path.join(self.img_dir, 'Ork Slugga 3.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()

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
			self.inactive_army = self.army1

		elif self.active_army == self.army2:
			self.turn_count += 1
			self.active_army = self.army1
			self.inactive_army = self.army2

		self.selectable_models.empty()
		self.targets.empty()

		for unit in self.active_army.units:
			for model in unit.models:
				self.selectable_models.add(model)

		for unit in self.inactive_army.units:
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
		print("\n------Changing phase from [{}] to [{}].------".format(self.previous_phase, new_phase))
		if new_phase == ("Fight Phase: Charging Units" or "Fight Phase: Friendly Units" or "Fight Phase: Enemy Units"):
			self.fight_subphase = new_phase
			print("\n(Fight Subphase is now [{}].)".format(self.fight_subphase))

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

			elif self.current_phase == "Pile In":
				model.pile_in_move = model.pile_in_move_max

			elif self.current_phase == "Consolidate":
				model.consolidate_move = model.consolidate_move_max

	def refresh_moves(self):
		for sprite in self.selectable_models:
			sprite.max_move = sprite.original_max_move
			sprite.charge_move = 0
			sprite.pile_in_move = sprite.pile_in_move_max
			sprite.consolidate_move = sprite.consolidate_move_max
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
			if shot_distance <= self.selected_model.ranged_weapons[0].w_range:
				Ray(self, shooter, target, (shooter.x, shooter.y), (target.x, target.y)).cast()
			#print("{}".format(x))
			#x += 1
		#print("\n")
		#print(shooter.valid_shots)

	def melee_ratio(self, sprite_1, sprite_2):
		ratio = (sprite_1.radius + sprite_2.radius + TILESIZE)/(sprite_1.radius + sprite_2.radius)
		return ratio

	#Populates a given sprite's "enemies_within_melee" and "squadmates_within_melee"
	#Only used by unit_wide_melee_check()
	def direct_melee_check(self, sprite):
		for target_model in self.targets:
			if pygame.sprite.collide_circle_ratio(self.melee_ratio(sprite, target_model))(sprite, target_model):
				sprite.enemies_within_melee.append(target_model)
				sprite.combined_melee.append(target_model)

		for squadmate in sprite.unit.models:
			if squadmate != sprite:
				if pygame.sprite.collide_circle_ratio(self.melee_ratio(sprite, squadmate))(sprite, squadmate):
					sprite.squadmates_within_melee.append(squadmate)

	#Populates a sprite's combined_melee list with the enemies_within_melee of each member of its unit
	#Only used by unit_wide_melee_check()
	def combined_melee_check(self, sprite):
		for squadmate in sprite.squadmates_within_melee:
			for target_model in squadmate.enemies_within_melee:
				sprite.combined_melee.append(target_model)

	#Runs direct_melee_check and combined_melee_check for every member of a selected unit.
	#Should be run when a model in a unit is selected for the first time. If subsequent models are selected from the same unit this does not need to run again.
	#Has to be run because even if only one model is attacking, that model's whole unit must run these melee checks to determine what that model can attack.
	def unit_wide_melee_check(self, sprite):
		print("\nRunning unit-wide melee checks, please wait...")
		for model in sprite.unit.models:
			self.direct_melee_check(model)
		for model in sprite.unit.models:
			self.combined_melee_check(model)
		for model in sprite.unit.models:
			for target_model in model.combined_melee:
				if target_model.unit in model.melee_unit_targets:
					pass
				else:
					model.melee_unit_targets.append(target_model.unit)
					print("Added a unit to a model's melee_unit_targets")
		print("\nMelee checks complete.")

	#Defines whether or not a charge has succeeded based on melee collision
	#	Sets relevant sprite.in_melee flag to True if the charge succeeds
	def charge_success(self):
		for sprite in self.charging_unit.models:
			for target in self.charge_target_unit.models:
				if pygame.sprite.collide_circle_ratio(self.melee_ratio(sprite, target))(sprite, target):
					for model in self.charging_unit.models:
						model.in_melee = True
					for model in self.charge_target_unit.models:
						model.in_melee = True
					self.charging_unit.charged_this_turn = True
					return True
		print("\nNo charging models in melee radius, charge considered a failure.")
		print("Reset moves and then press enter to return to charge phase.")
		return False

	def clear_selections(self):
		#print("\nClearing all selections...")
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

	def clear_melee_lists(self):
		for unit in self.active_army.units:
			unit.melee_unit_targets.clear()
			unit.valid_model_targets.clear()
			for model in unit.models:
				model.enemies_within_melee.clear()
				model.squadmates_within_melee.clear()
				model.combined_melee.clear()
				model.melee_unit_targets.clear()

	def reset_flags(self):
		for model in self.selectable_models:
			model.charged = False
			model.advanced = False
			model.fell_back = False

	def charge_roll(self, unit):
		roll_1 = random.randint(1,6)
		roll_2 = random.randint(1,6)
		roll = roll_1 + roll_2
		print("\nDie rolled; charge distance for [{}] set to {}".format(unit.name, roll))
		self.charge_range = roll*TILESIZE
		for model in unit.models:
			model.charge_move = self.charge_range

	def toggle_radii(self):
		if self.show_radii == True:
			self.show_radii = False
		else:
			self.show_radii = True

	def morale_test(self, unit):
		leadership = self.find_highest_leadership(unit)
		if len(unit.models) > 0 and len(unit.recent_deaths) > 0:
			roll = random.randint(1,6)
			result = roll + len(unit.recent_deaths)
			print("[{}] had {} recent deaths and rolled {}, so highest unit leadership must be {} or higher to pass".format(unit.name, len(unit.recent_deaths), roll, result))
			print("   Highest leadership in unit is {}".format(leadership))
			unit.recent_deaths.clear()
			if result > leadership: 
				unit.morale_losses = result - leadership
				print("\n   [{}] must remove {} models to morale.".format(unit.name, unit.morale_losses))
			else:
				print("\n   [{}] passed the test".format(unit.name))

	def find_highest_leadership(self, unit):
		highest_leadership = 1	#Rules state that leadership can never go below 1, so 1 is the default
		for model in unit.models:
			if model.leadership > highest_leadership:
				highest_leadership = model.leadership
		return highest_leadership

	#Game Loop - Event Handling
	#The bulk of the game logic is defined here. 
	def events(self):
		def model_selection(game):
			for model in game.selectable_models:
				if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
					if self.current_phase == "Shooting Phase" or self.current_phase == "Overwatch":
						if model.in_melee == True:
							print("\nModel is engaged in melee and therefore cannot shoot.")
							return

					elif self.current_phase == "Charge Phase":
						if model.in_melee == True:
							print("\nModel is already engaged in melee and therefore cannot charge.")
							return

					elif self.current_phase == "Fight Phase: Charging Units":
						if model.in_melee == False:
							print("\nModel is not engaged in melee and therefore cannot fight.")
							return

						elif model.unit.charged_this_turn == False:
							print("\nOnly units that charged this turn can fight during this sub-phase.")
							return

					elif self.current_phase == "Fight Phase: Friendly Units":
						if model.in_melee == False:
							print("\nModel is not engaged in melee and therefore cannot fight.")
							return

					elif self.current_phase == "Fight Phase: Enemy Units":
						if model.in_melee == False:
							print("\nModel is not engaged in melee and therefore cannot fight.")
							return

					game.selected_model = model
					game.selected_unit = model.unit

					print("\nSelected model: [{}]".format(game.selected_model))
					print("Selected unit: [{}]".format(game.selected_unit.name))
					return

			self.clear_selections()

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
						print("\nSelected model: [{}]".format(game.selected_model))
						print("Selected unit: [{}]".format(game.selected_unit.name))

			elif len(game.shooting_models) > 0:
				x = 0
				for model in game.selectable_models:
					if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
						x += 1
						if self.current_phase == "Shooting Phase" or self.current_phase == "Overwatch":
							if model.in_melee == True:
								print("\nModel is engaged in melee and cannot shoot.")
								return

						for shooter in game.shooting_models:
							if model == shooter:
								print("Model already selected for shooting; made it the selected_model.")
								game.selected_model = model
								return

						if game.shooting_models[0].unit == model.unit:
							game.selected_model = model
							game.selected_unit = model.unit
							game.shooting_models.append(model)
							print("\nSelected model: [{}]".format(game.selected_model))
							print("Selected unit: [{}]".format(game.selected_unit.name))
							print("# of models selected: {}".format(len(game.shooting_models)))

						else:
							print("\nChosen model not in same unit as currently selected shooting models.")
							print("Please choose a different model or reset shooting models selection with the spacebar.")
							return
				if x == 0:
					self.shooting_models.clear()
					self.clear_selections()

		def multiple_melee_selection(self):
			for model in self.selectable_models:
				if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
					if len(self.fighting_models) == 0:
						self.selected_model = model
						self.selected_unit = model.unit
						self.fighting_models.append(self.selected_model)
						print("\nSelected model: [{}]".format(self.selected_model))
						print("Selected unit: [{}]".format(self.selected_unit.name))
						print("# models selected: {}".format(len(self.fighting_models)))
						self.unit_wide_melee_check(self.selected_model)
						self.selected_unit.melee_unit_targets = self.selected_model.melee_unit_targets
						for target_unit in self.selected_unit.melee_unit_targets:
							for target_model in target_unit.models:
								self.selected_unit.valid_model_targets.append(target_model)
						return

					elif len(self.fighting_models) > 0:
						for fighter in self.fighting_models:
							if model == fighter:
								print("Model already selected for fighting; made it the selected_model.")
								self.selected_model = model
								return

						if model.unit == self.selected_unit:
							self.target_model = None
							self.target_unit = None
							self.selected_model = model
							self.fighting_models.append(model)
							print("\nSelected model: [{}]".format(self.selected_model))
							print("Selected unit: [{}]".format(self.selected_unit.name))
							print("# of models selected: {}".format(len(self.fighting_models)))
							self.selected_unit.melee_unit_targets = intersection(self.selected_unit.melee_unit_targets, self.selected_model.melee_unit_targets)
							self.selected_unit.valid_model_targets.clear()
							for target_unit in self.selected_unit.melee_unit_targets:
								for target_model in target_unit.models:
									self.selected_unit.valid_model_targets.append(target_model)
							return

			self.clear_selections()
			self.clear_melee_lists()
			self.fighting_models.clear()

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

						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						elif self.selected_model == None:
							model_selection(self)

						elif self.selected_model != None:
							self.selected_model = None 	#Defaults to deselecting current model if another model isn't clicked
							model_selection(self)

					elif event.button == 2:	#Middle mouse button
						pass

					elif event.button == 3: #RMB
						if self.selected_model != None:
							if self.selected_model.in_melee != True:
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
							for weapon in model.ranged_weapons:
								weapon.fired = False

				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						elif self.attack_button.mouse_over():
							if len(self.shooting_models) > 0:
								if self.target_unit != None:
									for model in self.shooting_models:
										model.attack_with_ranged_weapon(self.target_unit)
									if self.unallocated_wounds > 0:
										self.change_phase("Wound Allocation")
								else:
									print("\nNo target selected. Select a target to shoot at.")
							else:
								print("\nNo shooting models selected. Select models to shoot with.")

						elif len(self.shooting_models) == 0:
							multiple_selection(self)
							if len(self.shooting_models) > 0:
								self.los_check(self.selected_model)
								self.selected_unit.valid_shots = self.selected_model.valid_shots
									
						elif len(self.shooting_models) > 0:
							multiple_selection(self)
							if len(self.shooting_models) > 0:
								self.los_check(self.selected_model)
								self.selected_unit.valid_shots = intersection(self.selected_unit.valid_shots, self.selected_model.valid_shots)

					elif event.button == 2: #Middle mouse button
						self.shooting_models.clear()
						self.selected_unit = None
						mass_selection(self)
						print("\nRunning LOS checks on entire unit, please wait...")
						if len(self.shooting_models) > 0:
							self.los_check(self.selected_model)
							self.selected_unit.valid_shots = self.selected_model.valid_shots
							for model in self.shooting_models:
								if model != self.selected_model:
									self.los_check(model)
									self.selected_unit.valid_shots = intersection(self.selected_unit.valid_shots, model.valid_shots)
						print("\nLOS checks complete.")

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
						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						else:
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
										self.fighting_models.clear()
										self.target_model = None
										self.target_unit = None

									else:
										return

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
						for unit in self.active_army.units:
							unit.charge_attempt_list.clear()
						self.refresh_moves()
						self.clear_selections()
						self.change_phase("Fight Phase: Charging Units")
						
				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB ; Mouse event.buttom refers to interger values: 1(left), 2(middle), 3(right), 4(scrl up), 5(scrl down)
						if self.reset_all_button.mouse_over():
							for model in self.selectable_models:
								self.reset_moves(model)

						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						if self.charge_button.mouse_over():
							if self.selected_model != None and self.target_model != None:
								for item in self.selected_unit.charge_attempt_list:
									if item == self.target_unit:
										print("\nA charge against this target has already been attempted by the selected unit on this turn.")
										print("Select a different charge target.")
										return
								
								self.selected_unit.charge_attempt_list.append(self.target_unit)
								self.selectable_models.empty()
								self.targets.empty()
								for model in self.selected_unit.models:
									self.targets.add(model)
								for model in self.target_unit.models:
									self.selectable_models.add(model)

								self.charging_unit = self.selected_unit
								self.charge_target_unit = self.target_unit
								self.clear_selections()
								self.target_unit = self.charging_unit
								self.selected_unit = self.charge_target_unit
								print("\nCharge target confirmed. Proceeding to overwatch response.")
								self.change_phase("Overwatch")

							elif self.selected_model == None:
								print("\nNo unit selected. Select a unit to charge with.")

							elif self.target_model == None:
								print("\nNo target selected. Select a charge target.")
								return

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
							for weapon in model.ranged_weapons:
								weapon.fired = False

						self.selectable_models.empty()
						self.targets.empty()
						self.shooting_models.clear()

						for model in self.charging_unit.models:
							self.selectable_models.add(model)

						for unit in self.inactive_army.units:
							for model in unit.models:
								self.targets.add(model)

						self.clear_selections()
						self.clear_valid_shots()
						self.target_unit = self.charge_target_unit
						self.selected_unit = self.charging_unit
						self.charge_roll(self.charging_unit)
						
				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						elif self.attack_button.mouse_over():
							if len(self.shooting_models) > 0:
								if self.target_unit != None:
									for model in self.shooting_models:
										model.attack_with_ranged_weapon(self.target_unit)
									if self.unallocated_wounds > 0:
										self.change_phase("Wound Allocation")
								else:
									print("\nNo target selected. Select a target to shoot at.")
							else:
								print("\nNo shooting models selected. Select models to shoot with.")

						elif len(self.shooting_models) == 0:
							multiple_selection(self)
							if len(self.shooting_models) > 0:
								self.los_check(self.selected_model)
								self.selected_unit.valid_shots = self.selected_model.valid_shots
									
						elif len(self.shooting_models) > 0:
							multiple_selection(self)
							if len(self.shooting_models) > 0:
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
								self.refresh_moves()
								self.clear_selections()
								self.charging_unit = None
								self.charge_target_unit = None
								self.reset_active()
								self.change_phase("Charge Phase")
	
				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB ; Mouse event.buttom refers to interger values: 1(left), 2(middle), 3(right), 4(scrl up), 5(scrl down)
						if self.reset_all_button.mouse_over():
							for model in self.selectable_models:
								self.reset_moves(model)

						elif self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						elif self.selected_model == None:
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

		elif self.current_phase == "Fight Phase: Charging Units":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()

				#Keyboard event handling
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()

					if keys[pygame.K_HOME]:
						g.new()

					elif keys[pygame.K_SPACE]:
						self.clear_selections()

					elif keys[pygame.K_RETURN]:
						self.clear_selections()
						self.reset_active()
						self.change_phase("Fight Phase: Friendly Units")
						

				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						elif self.fight_button.mouse_over():
							if self.selected_model != None and self.selected_unit != None:
								for unit in self.ineligible_fight_units:
									if self.selected_unit == unit:
										print("\nUnit already fought this turn. Select a different unit to fight with.")
										return

								self.selectable_models.empty()
								self.targets.empty()
								for model in self.selected_unit.models:
									self.selectable_models.add(model)

								for unit in self.inactive_army.units:
									for model in unit.models:
										self.targets.add(model)

								self.ineligible_fight_units.append(self.selected_unit)
								self.change_phase("Pile In")

						elif self.selected_model == None:
							model_selection(self)

						elif self.selected_model != None:
							self.selected_model = None
							model_selection(self)								
						
					elif event.button == 2: #Middle mouse button
						pass

					elif event.button == 3:	#RMB
						pass

		elif self.current_phase == "Fight Phase: Friendly Units":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()

				#Keyboard event handling
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()

					if keys[pygame.K_HOME]:
						g.new()

					elif keys[pygame.K_SPACE]:
						self.clear_selections()

					elif keys[pygame.K_RETURN]:
						self.clear_selections()
						for unit in self.inactive_army.units:
							for model in unit.models:
								self.selectable_models.add(model)

						for unit in self.active_army.units:
							for model in unit.models:
								self.targets.add(model)

						self.change_phase("Fight Phase: Enemy Units")
						
				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						elif self.fight_button.mouse_over():
							if self.selected_model != None and self.selected_unit != None:
								for unit in self.ineligible_fight_units:
									if self.selected_unit == unit:
										print("\nUnit already fought this turn. Select a different unit to fight with.")
										return

								self.refresh_moves()
								self.selectable_models.empty()
								self.targets.empty()

								for model in self.selected_unit.models:
									self.selectable_models.add(model)

								for unit in self.inactive_army.units:
									for model in unit.models:
										self.targets.add(model)

								self.ineligible_fight_units.append(self.selected_unit)
								self.change_phase("Pile In")

						elif self.selected_model == None:
							model_selection(self)

						elif self.selected_model != None:
							self.selected_model = None
							model_selection(self)								
						
					elif event.button == 2: #Middle mouse button
						pass

					elif event.button == 3:	#RMB
						pass

		elif self.current_phase == "Fight Phase: Enemy Units":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()

				#Keyboard event handling
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()

					if keys[pygame.K_HOME]:
						g.new()

					elif keys[pygame.K_SPACE]:
						self.clear_selections()

					elif keys[pygame.K_RETURN]:
						self.ineligible_fight_units.clear()
						self.clear_selections()
						for unit in self.active_army.units:
							for model in unit.models:
								model.fought = False

						self.change_phase("Morale Phase")
						for unit in self.army1.units:
							self.morale_test(unit)
						for unit in self.army2.units:
							self.morale_test(unit)
						

				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						elif self.fight_button.mouse_over():
							if self.selected_model != None and self.selected_unit != None:
								for unit in self.ineligible_fight_units:
									if self.selected_unit == unit:
										print("\nUnit already fought this turn. Select a different unit to fight with.")
										return

								self.refresh_moves()
								self.selectable_models.empty()
								self.targets.empty()

								for model in self.selected_unit.models:
									self.selectable_models.add(model)

								for unit in self.active_army.units:
									for model in unit.models:
										self.targets.add(model)

								self.ineligible_fight_units.append(self.selected_unit)
								self.change_phase("Pile In")

						elif self.selected_model == None:
							model_selection(self)

						elif self.selected_model != None:
							self.selected_model = None
							model_selection(self)								
						
					elif event.button == 2: #Middle mouse button
						pass

					elif event.button == 3:	#RMB
						pass

		elif self.current_phase == "Pile In":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()

				#Keyboard event handling
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()

					if keys[pygame.K_HOME]:
						g.new()

					elif keys[pygame.K_SPACE]:
						if self.selected_model != None:
							self.reset_moves(self.selected_model)

					elif keys[pygame.K_RETURN]:
						if self.cohesion_check():
							self.refresh_moves()
							self.clear_selections()
							self.change_phase("Fight Targeting")
						
				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						elif self.reset_all_button.mouse_over():
							for model in self.selectable_models:
								self.reset_moves(model)

						elif self.selected_model == None:
							model_selection(self)

						elif self.selected_model != None:
							self.selected_model = None
							model_selection(self)								
						
					elif event.button == 2: #Middle mouse button
						pass

					elif event.button == 3:	#RMB
						if self.selected_model != None:
							self.selected_model.dest_x = pygame.mouse.get_pos()[0]
							self.selected_model.dest_y = pygame.mouse.get_pos()[1]

		elif self.current_phase == "Fight Targeting":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()

				#Keyboard event handling
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()

					if keys[pygame.K_HOME]:
						g.new()

					elif keys[pygame.K_SPACE]:
						self.clear_melee_lists()
						self.selected_unit.valid_model_targets.clear()
						self.clear_selections()

					elif keys[pygame.K_RETURN]:
						self.change_phase("Consolidate")

				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						elif self.attack_button.mouse_over():
							if len(self.fighting_models) > 0:
								if self.target_unit != None:
									self.clear_melee_lists()
									self.selected_unit.valid_model_targets.clear()
									for model in self.fighting_models:
										if model.fought == False:
											model.fought = True
											model.attack_with_melee_weapon(self.target_unit)
										else:
											print("\nCannot attack; [{}] has no attacks remaining this turn.".format(model.name))
									if self.unallocated_wounds > 0:
										self.change_phase("Wound Allocation")
								else:
									print("\nNo target selected. Select a target to shoot at.")
							else:
								print("\nNo shooting models selected. Select models to shoot with.")

						elif len(self.fighting_models) == 0:
							multiple_melee_selection(self)

						elif len(self.fighting_models) > 0:
							multiple_melee_selection(self)
								
												
					elif event.button == 2: #Middle mouse button
						pass

					elif event.button == 3:	#RMB
						if len(self.fighting_models) > 0 and self.selected_model != None and self.selected_unit != None:
							self.target_model = None
							self.target_unit = None
							#Target selection
							for model in self.targets:
								if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
									if model in self.selected_unit.valid_model_targets:
										self.target_model = model
										self.target_unit = model.unit

		elif self.current_phase == "Consolidate":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()

				#Keyboard event handling
				elif event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()

					if keys[pygame.K_HOME]:
						g.new()

					elif keys[pygame.K_SPACE]:
						if self.selected_model != None:
							self.reset_moves(self.selected_model)

					elif keys[pygame.K_RETURN]:
						if self.cohesion_check():
							self.refresh_moves()
							self.clear_selections()
							self.reset_active()
							self.change_phase(self.fight_subphase)
						
				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						elif self.reset_all_button.mouse_over():
							for model in self.selectable_models:
								self.reset_moves(model)

						elif self.selected_model == None:
							model_selection(self)

						elif self.selected_model != None:
							self.selected_model = None
							model_selection(self)								
						
					elif event.button == 2: #Middle mouse button
						pass

					elif event.button == 3:	#RMB
						if self.selected_model != None:
							self.selected_model.dest_x = pygame.mouse.get_pos()[0]
							self.selected_model.dest_y = pygame.mouse.get_pos()[1]

		elif self.current_phase == "Morale Phase":
			for unit in self.active_army.units:
				if unit.morale_losses > 0:
					self.selected_unit = unit
					self.change_phase("Morale Loss Allocation")

			for unit in self.inactive_army.units:
				if unit.morale_losses > 0:
					self.selected_unit = unit
					self.change_phase("Morale Loss Allocation")

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
						for unit in self.active_army.units:
							if unit.morale_losses > 0:
								print("Cannot proceed to next turn: not all units have undergone morale check")
								return

						for unit in self.inactive_army.units:
							if unit.morale_losses > 0:
								print("Cannot proceed to next turn: not all units have undergone morale check")
								return

						self.change_phase("Movement Phase")
						self.change_active()

				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

					elif event.button == 2: #Middle mouse button
						pass

					elif event.button == 3:	#RMB
						pass

		elif self.current_phase == "Morale Loss Allocation":
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
						pass

				#Mouse event handling
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:	#LMB
						if self.toggle_radii_button.mouse_over():
							self.toggle_radii()

						else:
							for model in self.selected_unit.models:
								if model.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
									model.die()
									print("\nModel being removed as morale loss: ")
									print(model)
									print("This model is part of unit:")
									print(model.unit.name)
									for model in self.selected_unit.models:
										model.update()

									self.selected_unit.morale_losses -= 1
									
									if self.selected_unit.morale_losses <= 0 or len(self.selected_unit.models) == 0:
										if self.selected_unit.morale_losses <= 0:
											print("\nAll morale losses allocated!")
										elif len(self.selected_unit.models) == 0:
											print("\nEntire unit eliminated. No valid morale losses remain.")
											self.selected_unit.morale_losses = 0
										
										self.selected_unit = None
										print("Returning to previous phase")
										self.change_phase("Morale Phase")

								else:
									print("\nChosen model not a valid target, please choose a model in the current unit that needs to allocate morale losses.")

					elif event.button == 2: #Middle mouse button
						pass

					elif event.button == 3:	#RMB
						pass

	#Game Loop - Update
	def update(self):
		self.all_sprites.update()

	#Draws reference grid
	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, BLACK, (x, 0 ), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))

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
	smallText = 17
	mediumText = 20
	largeText = 32

	#Game Loop - Draw
	def draw(self):
		self.screen.fill(LIGHTGREY)	
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

				if self.show_radii == True:
					#Weapon range radius
					pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), int(self.selected_model.ranged_weapons[0].w_range), 1)

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

			self.toggle_radii_button.draw()
			self.toggle_radii_button.fill()

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

				#Targets in LOS
				if self.selected_unit != None:
					if len(self.selected_unit.valid_shots) > 0:
						for model in self.selected_unit.valid_shots:
							pygame.draw.circle(self.screen, YELLOW, model.rect.center, model.radius, 0)

				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, model.rect.center, model.radius, 0)

				if self.show_radii == True:
					#Weapon range radius
					pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), int(self.selected_model.ranged_weapons[0].w_range), 1)
				
			if len(self.shooting_models) > 0:
				for model in self.shooting_models:
					pygame.draw.circle(self.screen, BLUE, model.rect.center, int((model.radius)/2), 0)

			#Buttons
			self.attack_button.draw()
			self.attack_button.fill()

			self.toggle_radii_button.draw()
			self.toggle_radii_button.fill()

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

				#Targets in LOS
				if self.selected_unit != None:
					if len(self.selected_unit.valid_shots) > 0:
						for model in self.selected_unit.valid_shots:
							pygame.draw.circle(self.screen, YELLOW, model.rect.center, model.radius, 0)

				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, model.rect.center, model.radius, 0)

				if self.show_radii == True:
					#Weapon range radius
					pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), int(self.selected_model.ranged_weapons[0].w_range), 1)

			#Buttons
			self.toggle_radii_button.draw()
			self.toggle_radii_button.fill()

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

				#Target unit indicator
				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, model.rect.center, model.radius, 0)

				if self.show_radii == True:
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

			#Draws large semi-circle cohesion indicator
			self.draw_cohesion_indicator()	

			#Buttons
			self.charge_button.draw()
			self.charge_button.fill()

			self.toggle_radii_button.draw()
			self.toggle_radii_button.fill()

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

				#Targets in LOS
				if self.selected_unit != None:
					if len(self.selected_unit.valid_shots) > 0:
						for model in self.selected_unit.valid_shots:
							pygame.draw.circle(self.screen, YELLOW, model.rect.center, model.radius, 0)

				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, model.rect.center, model.radius, 0)

				if self.show_radii == True:
					#Weapon range radius
					pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), int(self.selected_model.ranged_weapons[0].w_range), 1)

			if len(self.shooting_models) > 0:
				for model in self.shooting_models:
					pygame.draw.circle(self.screen, BLUE, model.rect.center, int((model.radius)/2), 0)

			#Buttons
			self.attack_button.draw()
			self.attack_button.fill()

			self.toggle_radii_button.draw()
			self.toggle_radii_button.fill()

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

				if self.show_radii == True:
					#Weapon range radius
					pygame.draw.circle(self.screen, RED, (self.selected_model.x, self.selected_model.y), int(self.selected_model.ranged_weapons[0].w_range), 1)

					#Remaining move radius
					if self.selected_model.charge_move >= 1:
						pygame.draw.circle(self.screen, YELLOW, (self.selected_model.x, self.selected_model.y), int(self.selected_model.charge_move), 1)

					#Melee radius (one inch)
					for sprite in self.targets:
						pygame.draw.circle(self.screen, RED, sprite.rect.center, sprite.true_melee_radius, 1)

					if self.target_unit != None:
						for sprite in self.target_unit.models:
							pygame.draw.circle(self.screen, ORANGE, sprite.rect.center, sprite.true_melee_radius, 1)

					#Cohesion radius (two inches)	
					for sprite in self.selected_model.unit.models:
						if sprite != self.selected_model:
							pygame.draw.circle(self.screen, GREEN, (sprite.x, sprite.y), sprite.true_cohesion_radius, 1)

			#Draws large semi-circle cohesion indicator
			self.draw_cohesion_indicator()	

			#Buttons
			self.reset_all_button.draw()
			self.reset_all_button.fill()

			self.toggle_radii_button.draw()
			self.toggle_radii_button.fill()

			#Controls Info Text	
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: move model|", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: reset selected model's move|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")

		elif self.current_phase in ("Fight Phase: Charging Units", "Fight Phase: Friendly Units", "Fight Phase: Enemy Units"):
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, YELLOW, self.selected_model.rect.center, self.selected_model.radius, 0)
				if self.selected_model.cohesion:
					pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)			

				#Target unit indicator
				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, model.rect.center, model.radius, 0)

			#Draws large semi-circle cohesion indicator
			self.draw_cohesion_indicator()	

			#Buttons
			self.fight_button.draw()
			self.fight_button.fill()

			self.toggle_radii_button.draw()
			self.toggle_radii_button.fill()

			#Controls Info Text	
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: N/A|", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: N/A|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")

		elif self.current_phase == "Pile In":
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, YELLOW, self.selected_model.rect.center, self.selected_model.radius, 0)
				
				if self.selected_model.cohesion:
					pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)

				if self.show_radii == True:
					#Remaining pile in move radius
					if self.selected_model.pile_in_move >= 1:
						pygame.draw.circle(self.screen, YELLOW, (self.selected_model.x, self.selected_model.y), int(self.selected_model.pile_in_move), 1)

					#Melee radius (one inch)
					for sprite in self.targets:
						pygame.draw.circle(self.screen, RED, sprite.rect.center, sprite.true_melee_radius, 1)

					#Melee fight radius (one inch)
					for sprite in self.selected_unit.models:
						if sprite != self.selected_model:
							pygame.draw.circle(self.screen, ORANGE, sprite.rect.center, sprite.true_melee_radius, 1)

					#Cohesion radius (two inches)	
					for sprite in self.selected_model.unit.models:
						if sprite != self.selected_model:
							pygame.draw.circle(self.screen, GREEN, (sprite.x, sprite.y), sprite.true_cohesion_radius, 1)

			#Draws large semi-circle cohesion indicator
			self.draw_cohesion_indicator()	

			#Buttons
			self.reset_all_button.draw()
			self.reset_all_button.fill()

			self.toggle_radii_button.draw()
			self.toggle_radii_button.fill()

			#Controls Info Text	
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: move model|", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: reset selected model's move|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")

		elif self.current_phase == "Fight Targeting":
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			#Model base drawing/coloring
			if self.selected_model != None and self.selected_unit != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)

				if len(self.selected_unit.valid_model_targets) > 0:
					for model in self.selected_unit.valid_model_targets:
						pygame.draw.circle(self.screen, YELLOW, model.rect.center, model.radius, 0)

				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, model.rect.center, model.radius, 0)

				if self.show_radii == True:
					#Melee radius (one inch)
					for sprite in self.targets:
						pygame.draw.circle(self.screen, RED, sprite.rect.center, sprite.true_melee_radius, 1)

					#Melee fight radius (one inch)
					for sprite in self.selected_unit.models:
						if sprite != self.selected_model:
							pygame.draw.circle(self.screen, ORANGE, sprite.rect.center, sprite.true_melee_radius, 1)
				
			if len(self.fighting_models) > 0:
				for model in self.fighting_models:
					pygame.draw.circle(self.screen, BLUE, model.rect.center, int((model.radius)/2), 0)

			#Draws large semi-circle cohesion indicator
			self.draw_cohesion_indicator()	

			#Buttons
			self.toggle_radii_button.draw()
			self.toggle_radii_button.fill()

			self.attack_button.draw()
			self.attack_button.fill()

			#Controls Info Text	
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: select target|", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: deselect all models|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")

		elif self.current_phase == "Consolidate":
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, YELLOW, self.selected_model.rect.center, self.selected_model.radius, 0)
				
				if self.selected_model.cohesion:
					pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)
		
				if self.show_radii == True:
					#Remaining consolidate move radius
					if self.selected_model.consolidate_move >= 1:
						pygame.draw.circle(self.screen, YELLOW, (self.selected_model.x, self.selected_model.y), int(self.selected_model.consolidate_move), 1)

					#Melee radius (one inch)
					for sprite in self.targets:
						pygame.draw.circle(self.screen, RED, sprite.rect.center, sprite.true_melee_radius, 1)

					#Melee fight radius (one inch)
					for sprite in self.selected_unit.models:
						if sprite != self.selected_model:
							pygame.draw.circle(self.screen, ORANGE, sprite.rect.center, sprite.true_melee_radius, 1)

					#Cohesion radius (two inches)	
					for sprite in self.selected_model.unit.models:
						if sprite != self.selected_model:
							pygame.draw.circle(self.screen, GREEN, (sprite.x, sprite.y), sprite.true_cohesion_radius, 1)

			#Draws large semi-circle cohesion indicator
			self.draw_cohesion_indicator()	

			#Buttons
			self.reset_all_button.draw()
			self.reset_all_button.fill()

			self.toggle_radii_button.draw()
			self.toggle_radii_button.fill()

			#Controls Info Text	
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: move model|", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: reset selected model's move|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")

		elif self.current_phase == "Morale Phase":
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, YELLOW, self.selected_model.rect.center, self.selected_model.radius, 0)

			#Buttons

			#Controls Info Text	
			self.draw_text("|LMB: N/A|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: N/A", self.generic_font, self.mediumText, WHITE, 6*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: N/A|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")

		elif self.current_phase == "Morale Loss Allocation":
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, model.rect.center, model.radius, 0)

			#Model base drawing/coloring
			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, GREEN, self.selected_model.rect.center, self.selected_model.radius, 0)

			#Buttons

			#Unallocated wound counter
			if self.selected_unit != None:
				self.draw_text("{} morale losses to allocate.".format(self.selected_unit.morale_losses), self.generic_font, self.largeText, YELLOW, WIDTH/2, HEIGHT - 2*TILESIZE, "center")

			#Controls Info Text
			self.draw_text("|LMB: allocate morale loss to model|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, WIDTH/32, HEIGHT-4*TILESIZE, "w")
			self.draw_text("|RMB: N/A|", self.generic_font, self.mediumText, WHITE, (8*WIDTH/32), HEIGHT-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: N/A|", self.generic_font, self.mediumText, WHITE, 12*WIDTH/32, HEIGHT-5*TILESIZE, "w")
			self.draw_text("|RETURN: N/A|", self.generic_font, self.mediumText, WHITE, 24*WIDTH/32, HEIGHT-5*TILESIZE, "w")

		#General info text
		self.draw_text("Turn #{}: {} {}".format(self.turn_count, self.active_army.name, self.current_phase), self.generic_font, self.largeText, WHITE, WIDTH/2, TILESIZE, "center")
		self.draw_text("|HOME: reset game|", self.generic_font, self.mediumText, WHITE, WIDTH-(TILESIZE*2), TILESIZE, "e")
		fps = int(self.clock.get_fps())
		self.draw_text("FPS: {}".format(fps), self.generic_font, self.mediumText, WHITE, 2*WIDTH/32, TILESIZE, "w")
		self.bullets.draw

		#Side Panel Info (Debug Info)
		self.draw_text("SELECTED MODEL: {}".format(self.selected_model), self.generic_font, self.mediumText, WHITE, WIDTH-(TILESIZE*15), 4*TILESIZE, "w")
		if self.selected_model != None:
			self.draw_text("in_melee: {}".format(self.selected_model.in_melee), self.generic_font, self.smallText, WHITE, WIDTH-(TILESIZE*15), 5*TILESIZE, "w")
			self.draw_text("fought: {}".format(self.selected_model.fought), self.generic_font, self.smallText, WHITE, WIDTH-(TILESIZE*15), 6*TILESIZE, "w")
			self.draw_text("charged: {}".format(self.selected_model.charged), self.generic_font, self.smallText, WHITE, WIDTH-(TILESIZE*15), 7*TILESIZE, "w")
			self.draw_text("advanced: {}".format(self.selected_model.advanced), self.generic_font, self.smallText, WHITE, WIDTH-(TILESIZE*15), 8*TILESIZE, "w")
			self.draw_text("fell_back: {}".format(self.selected_model.fell_back), self.generic_font, self.smallText, WHITE, WIDTH-(TILESIZE*15), 9*TILESIZE, "w")


		if self.selected_unit == None:
			self.draw_text("SELECTED UNIT: {}".format(self.selected_unit), self.generic_font, self.mediumText, WHITE, WIDTH-(TILESIZE*15), 15*TILESIZE, "w")
		if self.selected_unit != None:
			self.draw_text("SELECTED UNIT: {}".format(self.selected_unit), self.generic_font, self.mediumText, WHITE, WIDTH-(TILESIZE*15), 15*TILESIZE, "w")
			if self.current_phase == "Shooting Phase":
				self.draw_text("# of models selected: {}".format(len(self.shooting_models)), self.generic_font, self.smallText, WHITE, WIDTH-(TILESIZE*15), 17*TILESIZE, "w")
			elif self.current_phase == "Fight Targeting":
				self.draw_text("# of models selected: {}".format(len(self.fighting_models)), self.generic_font, self.smallText, WHITE, WIDTH-(TILESIZE*15), 17*TILESIZE, "w")


		self.draw_text("Target Model: {}".format(self.target_model), self.generic_font, self.mediumText, WHITE, WIDTH-(TILESIZE*15), 24*TILESIZE, "w")

		self.draw_text("Target Unit: {}".format(self.target_unit), self.generic_font, self.mediumText, WHITE, WIDTH-(TILESIZE*15), 25*TILESIZE, "w")
		self.draw_text("Target Unit: {}".format(self.target_unit), self.generic_font, self.mediumText, WHITE, WIDTH-(TILESIZE*15), 26*TILESIZE, "w")

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
				if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN:
					waiting = False

g = Game()
g.show_start_screen()

while g.running:
	g.new()
	g.show_game_over_screen()

pygame.quit()