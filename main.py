"""40k Pygame Adapation
Please see README.md for details on game rules and controls.
"""

import pygame
from pygame.locals import *
import sys
import os
from os import path
import random

from settings import *
import settings
import event_handling
import draw_module
import buttons
import sprite_module
import unit_module
import army_module
import data_creation
import ray_casting
import tile_map
import ui


data_creation.get_workbook_data()

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
		#os.environ['SDL_VIDEO_WINDOW_POS'] = str(25) + "," + str(25)
		pygame.init() 
		#pygame.mixer.init()

		#Creates a "video display information object"
		# current_w/h gets width/height of the either the current video mode or the desktop mode depending
		#	on whether it was called before or after pygame.display.set_mode(...)
		#self.displayInfo = pygame.display.Info()
		#self.screen_w = self.displayInfo.current_w
		#self.screen_h = self.displayInfo.current_h



		self.title = "40k pygame"

		#self.screen_w = 1920
		#self.screen_h = 1080	
		self.background_w = 1600
		self.background_h = 800

		#background_w = 1920
		#background_h = 1080

		#	!IMPORTANT!
		#Used in draw_module and in main to define the important screen_topleft_pos
		self.background_x_offset = 50
		self.background_y_offset = 200

		self.screen_w = self.background_w - self.background_x_offset
		self.screen_h = self.background_h - self.background_y_offset

		self.ui_scale = self.background_w/1920



		#	!IMPORTANT!
		#Used to adjust mouse input, raycasting
		self.screen_topleft_pos = (self.background_x_offset/2, self.background_y_offset/3)

		#Fullscreen
		#self.background = pygame.display.set_mode((self.screen_w+self.background_x_offset, self.screen_h+self.background_y_offset), FULLSCREEN)

		#Windowed Borderless
		#os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(0)
		#self.background = pygame.display.set_mode((self.background_w, self.background_h), NOFRAME)

		#Windowed
		os.environ['SDL_VIDEO_WINDOW_POS'] = str(5) + "," + str(30)
		self.background = pygame.display.set_mode((self.background_w, self.background_h), RESIZABLE)

		self.screen = pygame.Surface((self.screen_w, self.screen_h))
		pygame.display.set_caption(self.title)
		self.clock = pygame.time.Clock()
		self.running = True

	def load_data(self):
		self.game_folder = path.dirname(__file__)
		self.img_dir = path.join(self.game_folder, 'img')
		self.map = tile_map.Map(path.join(self.game_folder, 'realistic_map.txt'))

		self.spritesheet = sprite_module.Spritesheet(path.join(self.img_dir, 'hyptosis_sprites.png'))

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
		self.focus = pygame.sprite.Group()
		self.buttons = []
		self.show_radii = True
		self.show_controls = False
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

		buttons.define_buttons(self)
		
		self.camera = tile_map.Camera(self, self.map.width, self.map.height)
		self.camera_focus = sprite_module.Focus(self, self.map.width/2, self.map.height/2, self.map.width, self.map.height)
		
		#Initialize army, unit objects
		self.army1 = army_module.create_army1(self)
		self.army2 = army_module.create_army2(self)
		
		self.active_army = self.army1
		self.inactive_army = self.army2

		#Create models and wall sprites from map.txt
		for row, tiles in enumerate(self.map.data):		#enumerate gets the index as well as the value
			for col, tile in enumerate(tiles):
				if tile == '1':
					sprite_module.Wall(self, col, row)

				elif tile == 'M':
					model = data_creation.create_model_by_name('Initiate', self, col, row)
					self.army1.units[0].add_model(model)
					model.unit = self.army1.units[0]
					model.add_ranged_weapon(data_creation.create_ranged_weapon_by_name('Test Gun'))
					model.add_melee_weapon(data_creation.create_melee_weapon_by_name('CCW'))
					model.image = pygame.image.load(path.join(self.img_dir, 'Templar 4.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()
					model.outline = sprite_module.get_outline(model.image)

				elif tile == 'N':
					model = data_creation.create_model_by_name('Initiate', self, col, row)
					self.army1.units[1].add_model(model)
					model.unit = self.army1.units[1]
					model.add_ranged_weapon(data_creation.create_ranged_weapon_by_name('Test Gun'))
					model.add_melee_weapon(data_creation.create_melee_weapon_by_name('CCW'))
					model.image = pygame.image.load(path.join(self.img_dir, 'Templar 6.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()
					model.outline = sprite_module.get_outline(model.image)

				elif tile == 'Z':
					model = data_creation.create_model_by_name('Dreadnought', self, col, row)
					self.army1.units[2].add_model(model)
					model.unit = self.army1.units[2]
					model.add_ranged_weapon(data_creation.create_ranged_weapon_by_name('Assault Cannon'))
					model.add_melee_weapon(data_creation.create_melee_weapon_by_name('Dreadnought Combat Weapon'))
					model.image = pygame.image.load(path.join(self.img_dir, 'dreadnaught 3.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()
					model.outline = sprite_module.get_outline(model.image)

				elif tile == 'P':
					model = data_creation.create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[0].add_model(model)
					model.unit = self.army2.units[0]
					model.add_ranged_weapon(data_creation.create_ranged_weapon_by_name('Test Gun'))
					model.add_melee_weapon(data_creation.create_melee_weapon_by_name('CCW'))
					model.image = pygame.image.load(path.join(self.img_dir, 'Ork Slugga 3.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()
					model.outline = sprite_module.get_outline(model.image)

				elif tile == 'A':
					model = data_creation.create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[1].add_model(model)
					model.unit = self.army2.units[1]
					model.add_ranged_weapon(data_creation.create_ranged_weapon_by_name('Test Gun'))
					model.add_melee_weapon(data_creation.create_melee_weapon_by_name('CCW'))
					model.image = pygame.image.load(path.join(self.img_dir, 'Ork Slugga 4.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()
					model.outline = sprite_module.get_outline(model.image)

				elif tile == 'G':
					model = data_creation.create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[2].add_model(model)
					model.unit = self.army2.units[2]
					model.add_ranged_weapon(data_creation.create_ranged_weapon_by_name('Test Gun'))
					model.add_melee_weapon(data_creation.create_melee_weapon_by_name('CCW'))
					model.image = pygame.image.load(path.join(self.img_dir, 'Ork Slugga 3.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()
					model.outline = sprite_module.get_outline(model.image)

				elif tile == 'K':
					model = data_creation.create_model_by_name('Ork Boy', self, col, row)
					self.army2.units[3].add_model(model)
					model.unit = self.army2.units[3]
					model.add_ranged_weapon(data_creation.create_ranged_weapon_by_name('Shoota'))
					model.add_melee_weapon(data_creation.create_melee_weapon_by_name('CCW'))
					model.image = pygame.image.load(path.join(self.img_dir, 'Ork Slugga 4.png')).convert()
					model.image.set_colorkey(WHITE)
					model.rect = model.image.get_rect()
					model.outline = sprite_module.get_outline(model.image)

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
		if new_phase in ("Fight Phase: Charging Units", "Fight Phase: Friendly Units", "Fight Phase: Enemy Units"):
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

	#Very slow process
	#Range checking part must be fairly quick, since models with no enemies in range have extremely quick los_checks
	def los_check(self, shooter):
		self.target_model = None
		self.target_unit = None
		x = 0

		for target in self.targets:
			x += 1
			#print("\nCheck #{}: Checking if {} is in range.".format(x, target.name))
			shot_x = self.selected_model.x - target.x
			shot_y = self.selected_model.y - target.y
			shot_distance = sprite_module.find_hypotenuse(shot_x, shot_y)
			if shot_distance <= self.selected_model.ranged_weapons[0].w_range:
				#print("\nStarting ray cast.")
				ray_casting.Ray(self, shooter, target, (shooter.x, shooter.y), (target.x, target.y)).cast()
				#print("\nEnd of ray cast.")


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
		for model in self.all_models:
			model.color_outline(BLACK)

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
		if self.current_phase == "Movement Phase":
			event_handling.movement_phase(self)

		elif self.current_phase == "Shooting Phase":
			event_handling.shooting_phase(self)

		elif self.current_phase == "Wound Allocation":
			event_handling.wound_allocation(self)

		elif self.current_phase == "Charge Phase":
			event_handling.charge_phase(self)

		elif self.current_phase == "Overwatch":
			event_handling.overwatch(self)

		elif self.current_phase == "Charge Move":
			event_handling.charge_move(self)

		elif self.current_phase == "Fight Phase: Charging Units":
			event_handling.fight_phase_charging_units(self)

		elif self.current_phase == "Fight Phase: Friendly Units":
			event_handling.fight_phase_friendly_units(self)

		elif self.current_phase == "Fight Phase: Enemy Units":
			event_handling.fight_phase_enemy_units(self)

		elif self.current_phase == "Pile In":
			event_handling.pile_in(self)

		elif self.current_phase == "Fight Targeting":
			event_handling.fight_targeting(self)

		elif self.current_phase == "Consolidate":
			event_handling.consolidate(self)

		elif self.current_phase == "Morale Phase":
			event_handling.morale_phase(self)

		elif self.current_phase == "Morale Loss Allocation":
			event_handling.morale_loss_allocation(self)

	#Game Loop - Update
	def update(self):
		self.camera.update(self.camera_focus)
		self.all_sprites.update()

	#Draws reference grid
	def draw_grid(self):
		for x in range(0, self.screen_w, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, BLACK, (x, 0), (x, self.screen_h))
		for y in range(0, self.screen_h, TILESIZE):		#draws horizontal lines
			pygame.draw.line(self.screen, BLACK, (0, y), (self.screen_w, y))

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
	#generic_font = pygame.font.match_font('garamondbold')
	#generic_font = pygame.font.match_font('freesansbold')
	#castellar, rod, fangsong, ebrima
	tinyText = 13
	smallText = 17
	mediumText = 20
	largeText = 32

	#Game Loop - Draw
	def draw(self):
		self.background.fill(BLACK)
		self.screen.fill(LIGHTGREY)	
		#self.draw_grid() 

		def text_objects(text, font):
			textSurface = font.render(text, True, WHITE)
			return textSurface, textSurface.get_rect()
		
		#Essential modification (camera.apply) that allows camera movement through changed sprite locations
		#Draws all sprites explicitly.
		for sprite in self.all_sprites:
			if sprite != self.camera_focus:
				self.screen.blit(sprite.image, self.camera.apply(sprite))

		#Draws the outline of all model sprites.
		#for model in self.all_models:
		#	self.screen.blit(model.outline, self.camera.apply(model))
			
		if self.current_phase == "Movement Phase":	
			draw_module.movement_phase(self)

		elif self.current_phase == "Shooting Phase":
			draw_module.shooting_phase(self)
			
		elif self.current_phase == "Wound Allocation":
			draw_module.wound_allocation(self)

		elif self.current_phase == "Charge Phase":
			draw_module.charge_phase(self)

		elif self.current_phase == "Overwatch":
			draw_module.overwatch(self)

		elif self.current_phase == "Charge Move":	
			draw_module.charge_move(self)

		elif self.current_phase in ("Fight Phase: Charging Units", "Fight Phase: Friendly Units", "Fight Phase: Enemy Units"):
			draw_module.fight_phase(self)

		elif self.current_phase == "Pile In":
			draw_module.pile_in(self)

		elif self.current_phase == "Fight Targeting":
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, self.camera.apply(model).center, model.radius, 0)

			#Model base drawing/coloring
			if self.selected_model != None and self.selected_unit != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, GREEN, self.camera.apply(self.selected_model).center, self.selected_model.radius, 0)

				if len(self.selected_unit.valid_model_targets) > 0:
					for model in self.selected_unit.valid_model_targets:
						pygame.draw.circle(self.screen, YELLOW, self.camera.apply(model).center, model.radius, 0)

				if self.target_unit != None:
					for model in self.target_unit.models:
						pygame.draw.circle(self.screen, ORANGE, self.camera.apply(model).center, model.radius, 0)

				if self.show_radii == True:
					#Melee radius (one inch)
					for sprite in self.targets:
						pygame.draw.circle(self.screen, RED, self.camera.apply(sprite).center, sprite.true_melee_radius, 1)

					#Melee fight radius (one inch)
					for sprite in self.selected_unit.models:
						if sprite != self.selected_model:
							pygame.draw.circle(self.screen, ORANGE, self.camera.apply(sprite).center, sprite.true_melee_radius, 1)
				
			if len(self.fighting_models) > 0:
				for model in self.fighting_models:
					pygame.draw.circle(self.screen, BLUE, self.camera.apply(model).center, int((model.radius)/2), 0)

			#Draws large semi-circle cohesion indicator
			draw_module.draw_cohesion_indicator(self)

			#Buttons
			self.toggle_radii_button.draw()
			self.toggle_radii_button.fill()

			self.attack_button.draw()
			self.attack_button.fill()

			#Controls Info Text	
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, self.screen_w/32, self.screen_h-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, self.screen_w/32, self.screen_h-4*TILESIZE, "w")
			self.draw_text("|RMB: select target|", self.generic_font, self.mediumText, WHITE, 6*self.screen_w/32, self.screen_h-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: deselect all models|", self.generic_font, self.mediumText, WHITE, 12*self.screen_w/32, self.screen_h-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*self.screen_w/32, self.screen_h-5*TILESIZE, "w")

		elif self.current_phase == "Consolidate":
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, self.camera.apply(model).center, model.radius, 0)

			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, YELLOW, self.camera.apply(self.selected_model).center, self.selected_model.radius, 0)
				
				if self.selected_model.cohesion:
					pygame.draw.circle(self.screen, GREEN, self.camera.apply(self.selected_model).center, self.selected_model.radius, 0)
		
				if self.show_radii == True:
					#Remaining consolidate move radius
					if self.selected_model.consolidate_move >= 1:
						pygame.draw.circle(self.screen, YELLOW, self.camera.apply(self.selected_model).center, int(self.selected_model.consolidate_move), 1)

					#Melee radius (one inch)
					for sprite in self.targets:
						pygame.draw.circle(self.screen, RED, self.camera.apply(sprite).center, sprite.true_melee_radius, 1)

					#Melee fight radius (one inch)
					for sprite in self.selected_unit.models:
						if sprite != self.selected_model:
							pygame.draw.circle(self.screen, ORANGE, self.camera.apply(sprite).center, sprite.true_melee_radius, 1)

					#Cohesion radius (two inches)	
					for sprite in self.selected_model.unit.models:
						if sprite != self.selected_model:
							pygame.draw.circle(self.screen, GREEN, self.camera.apply(sprite).center, sprite.true_cohesion_radius, 1)

			#Draws large semi-circle cohesion indicator
			draw_module.draw_cohesion_indicator(self)

			#Buttons
			self.reset_all_button.draw()
			self.reset_all_button.fill()

			self.toggle_radii_button.draw()
			self.toggle_radii_button.fill()

			#Controls Info Text	
			self.draw_text("|LMB: select model|", self.generic_font, self.mediumText, WHITE, self.screen_w/32, self.screen_h-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, self.screen_w/32, self.screen_h-4*TILESIZE, "w")
			self.draw_text("|RMB: move model|", self.generic_font, self.mediumText, WHITE, 6*self.screen_w/32, self.screen_h-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: reset selected model's move|", self.generic_font, self.mediumText, WHITE, 12*self.screen_w/32, self.screen_h-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*self.screen_w/32, self.screen_h-5*TILESIZE, "w")

		elif self.current_phase == "Morale Phase":
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, self.camera.apply(model).center, model.radius, 0)

			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, YELLOW, self.camera.apply(self.selected_model).center, self.selected_model.radius, 0)

			#Buttons

			#Controls Info Text	
			self.draw_text("|LMB: N/A|", self.generic_font, self.mediumText, WHITE, self.screen_w/32, self.screen_h-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, self.screen_w/32, self.screen_h-4*TILESIZE, "w")
			self.draw_text("|RMB: N/A", self.generic_font, self.mediumText, WHITE, 6*self.screen_w/32, self.screen_h-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: N/A|", self.generic_font, self.mediumText, WHITE, 12*self.screen_w/32, self.screen_h-5*TILESIZE, "w")
			self.draw_text("|RETURN: progress to next phase|", self.generic_font, self.mediumText, WHITE, 24*self.screen_w/32, self.screen_h-5*TILESIZE, "w")

		elif self.current_phase == "Morale Loss Allocation":
			#Model base drawing/coloring
			if self.selected_unit != None:
				for model in self.selected_unit.models:
					pygame.draw.circle(self.screen, CYAN, self.camera.apply(model).center, model.radius, 0)

			#Model base drawing/coloring
			if self.selected_model != None:
				#Selected model indicator
				pygame.draw.circle(self.screen, GREEN, self.camera.apply(self.selected_model).center, self.selected_model.radius, 0)

			#Buttons

			#Unallocated wound counter
			if self.selected_unit != None:
				self.draw_text("{} morale losses to allocate.".format(self.selected_unit.morale_losses), self.generic_font, self.largeText, YELLOW, self.screen_w/2, self.screen_h - 2*TILESIZE, "center")

			#Controls Info Text
			self.draw_text("|LMB: allocate morale loss to model|", self.generic_font, self.mediumText, WHITE, self.screen_w/32, self.screen_h-5*TILESIZE, "w")
			self.draw_text("|MMB: N/A|", self.generic_font, self.mediumText, WHITE, self.screen_w/32, self.screen_h-4*TILESIZE, "w")
			self.draw_text("|RMB: N/A|", self.generic_font, self.mediumText, WHITE, (8*self.screen_w/32), self.screen_h-5*TILESIZE, "w")
			self.draw_text("|SPACEBAR: N/A|", self.generic_font, self.mediumText, WHITE, 12*self.screen_w/32, self.screen_h-5*TILESIZE, "w")
			self.draw_text("|RETURN: N/A|", self.generic_font, self.mediumText, WHITE, 24*self.screen_w/32, self.screen_h-5*TILESIZE, "w")

		#self.all_models.draw(self.screen)
		#for model in self.all_models:
		#	self.screen.blit(model.outline, model.rect.topleft)
		#pygame.draw.circle(self.screen, YELLOW, (0,0), 25)
		#pygame.draw.circle(self.background, YELLOW, (0,0), 25)

		#Draw the screen on the background; crucial to displaying the actual game
		self.background.blit(self.screen, (self.screen_topleft_pos))

		#Draws things like Turn Name/Counter, FPS, Camera Offset
		draw_module.draw_info_text(self)
		
		pygame.display.update()
		
	def show_start_screen(self):
		self.screen.fill(BLACK)
		self.draw_text("40k Pygame Adaptation", pygame.font.match_font('castellar'), 80, YELLOW, self.screen_w/2, self.screen_h*1/4, "center")
		self.draw_text("Please see the readme/wiki for game rules and", self.generic_font, 40, WHITE, self.screen_w/2, self.screen_h*4/8, "center")
		self.draw_text("look at the command line window for game info.", self.generic_font, 40, WHITE, self.screen_w/2, self.screen_h*5/8, "center")
		self.draw_text("Press any key to start", self.generic_font, 40, WHITE, self.screen_w/2, self.screen_h*7/8, "center")
		self.background.blit(self.screen, (50,50))
		pygame.display.flip()
		self.wait_for_key()

	def show_game_over_screen(self):
		self.screen.fill(BLACK)
		self.draw_text("Victory!", pygame.font.match_font('castellar'), 80, GREEN, self.screen_w/2, self.screen_h*1/4, "center")
		self.draw_text("All targets eliminated", self.generic_font, 40, WHITE, self.screen_w/2, self.screen_h*2/4, "center")
		self.draw_text("Press any key to start a new game", self.generic_font, 40, WHITE, self.screen_w/2, self.screen_h*3/4, "center")
		self.background.blit(self.screen, (50,50))
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
				if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
					waiting = False

if __name__ == "__main__":
	Game().show_start_screen()

	while Game().running:
		Game().new()
		Game().show_game_over_screen()

	pygame.quit()