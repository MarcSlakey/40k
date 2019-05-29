import pygame
from pygame.locals import *
import main
import sprite_module
from settings import *
import settings

def intersection(a, b):
	#c = []
	#for target in a:
		#if target in b:
			#c.append(target)
	c = [value for value in b if value in a]
	return c

def get_adjusted_mouse_pos(game):
	return (pygame.mouse.get_pos()[0]-game.screen_topleft_pos[0], pygame.mouse.get_pos()[1]-game.screen_topleft_pos[1])

def model_selection(game):
	for model in game.selectable_models:
		adjusted_model_rect = game.camera.apply(model)
		if adjusted_model_rect.collidepoint(get_adjusted_mouse_pos(game)):
			if game.current_phase == "Shooting Phase" or game.current_phase == "Overwatch":
				if model.in_melee == True:
					print("\nModel is engaged in melee and therefore cannot shoot.")
					return

			elif game.current_phase == "Charge Phase":
				if model.in_melee == True:
					print("\nModel is already engaged in melee and therefore cannot charge.")
					return

			elif game.current_phase == "Fight Phase: Charging Units":
				if model.in_melee == False:
					print("\nModel is not engaged in melee and therefore cannot fight.")
					return

				elif model.unit.charged_this_turn == False:
					print("\nOnly units that charged this turn can fight during this sub-phase.")
					return

			elif game.current_phase == "Fight Phase: Friendly Units":
				if model.in_melee == False:
					print("\nModel is not engaged in melee and therefore cannot fight.")
					return

			elif game.current_phase == "Fight Phase: Enemy Units":
				if model.in_melee == False:
					print("\nModel is not engaged in melee and therefore cannot fight.")
					return

			game.selected_model = model
			game.selected_unit = model.unit
			for model in game.all_models:
				model.color_outline(BLACK)
			game.selected_model.color_outline(WHITE)

			print("\nSelected model: [{}]".format(game.selected_model))
			print("Selected unit: [{}]".format(game.selected_unit.name))
			return

	game.clear_selections()

def multiple_selection(game):
	if len(game.shooting_models) == 0:
		for model in game.selectable_models:
			adjusted_model_rect = game.camera.apply(model)
			if adjusted_model_rect.collidepoint(get_adjusted_mouse_pos(game)):
				if game.current_phase == "Shooting Phase" or game.current_phase == "Overwatch":
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
			adjusted_model_rect = game.camera.apply(model)
			if adjusted_model_rect.collidepoint(get_adjusted_mouse_pos(game)):
				x += 1
				if game.current_phase == "Shooting Phase" or game.current_phase == "Overwatch":
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
			game.shooting_models.clear()
			game.clear_selections()

def multiple_melee_selection(game):
	for model in game.selectable_models:
		adjusted_model_rect = game.camera.apply(model)
		if adjusted_model_rect.collidepoint(get_adjusted_mouse_pos(game)):
			if len(game.fighting_models) == 0:
				game.selected_model = model
				game.selected_unit = model.unit
				game.fighting_models.append(game.selected_model)
				print("\nSelected model: [{}]".format(game.selected_model))
				print("Selected unit: [{}]".format(game.selected_unit.name))
				print("# models selected: {}".format(len(game.fighting_models)))
				game.unit_wide_melee_check(game.selected_model)
				game.selected_unit.melee_unit_targets = game.selected_model.melee_unit_targets
				for target_unit in game.selected_unit.melee_unit_targets:
					for target_model in target_unit.models:
						game.selected_unit.valid_model_targets.append(target_model)
				return

			elif len(game.fighting_models) > 0:
				for fighter in game.fighting_models:
					if model == fighter:
						print("Model already selected for fighting; made it the selected_model.")
						game.selected_model = model
						return

				if model.unit == game.selected_unit:
					game.target_model = None
					game.target_unit = None
					game.selected_model = model
					game.fighting_models.append(model)
					print("\nSelected model: [{}]".format(game.selected_model))
					print("Selected unit: [{}]".format(game.selected_unit.name))
					print("# of models selected: {}".format(len(game.fighting_models)))
					game.selected_unit.melee_unit_targets = intersection(game.selected_unit.melee_unit_targets, game.selected_model.melee_unit_targets)
					game.selected_unit.valid_model_targets.clear()
					for target_unit in game.selected_unit.melee_unit_targets:
						for target_model in target_unit.models:
							game.selected_unit.valid_model_targets.append(target_model)
					return

	game.clear_selections()
	game.clear_melee_lists()
	game.fighting_models.clear()

def mass_selection(game):
	if len(game.shooting_models) == 0:
		for model in game.selectable_models:
			adjusted_model_rect = game.camera.apply(model)
			if adjusted_model_rect.collidepoint(get_adjusted_mouse_pos(game)):
				if game.current_phase == "Shooting Phase" or game.current_phase == "Overwatch":
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

def core_events(game, keys, mods):
	if keys[pygame.K_F4]:
		if mods & pygame.KMOD_ALT:
			game.quit()

	elif keys[pygame.K_END]:
		game.quit()

	elif keys[pygame.K_HOME]:
		main.Game().show_start_screen()
		main.Game().new()

def movement_phase(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		elif event.type == VIDEORESIZE:
			#pass
			#game.screen = pygame.display.set_mode(event.dict['size'], RESIZABLE)
			game.background_w = event.w
			game.background_h = event.h

			game.screen_w = game.background_w - game.background_x_offset
			game.screen_h = game.background_h - game.background_y_offset

			old_background = game.background
			old_screen = game.screen

			game.background = pygame.display.set_mode((game.background_w, game.background_h), RESIZABLE)
			game.screen = pygame.Surface((game.screen_w, game.screen_h))
			game.camera.update(game.camera_focus)

			#game.background.blit(old_background, (0,0))
			#game.background.blit(old_screen, (game.background_x_offset, game.background_y_offset))

			#del old_background, old_screen

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()
			
			core_events(game, keys, mods)

			if game.selected_model != None and keys[pygame.K_SPACE]:
				game.reset_moves(game.selected_model)

			elif keys[pygame.K_RETURN]:
				if game.cohesion_check():
					game.clear_selections()
					game.refresh_moves()
					game.change_phase("Shooting Phase")

		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB ; Mouse event.buttom refers to interger values: 1(left), 2(middle), 3(right), 4(scrl up), 5(scrl down)
				if game.reset_all_button.mouse_over():
					for model in game.selectable_models:
						game.reset_moves(model)

				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				elif game.selected_model == None:
					model_selection(game)

				elif game.selected_model != None:
					game.selected_model = None 	#Defaults to deselecting current model if another model isn't clicked
					model_selection(game)

			elif event.button == 2:	#Middle mouse button
				pass

			elif event.button == 3: #RMB
				if game.selected_model != None:
					if game.selected_model.in_melee != True:
						game.selected_model.dest_x = get_adjusted_mouse_pos(game)[0] - game.camera.cam_rect.topleft[0]
						game.selected_model.dest_y = get_adjusted_mouse_pos(game)[1] - game.camera.cam_rect.topleft[1]

def shooting_phase(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_SPACE]:
				for model in game.shooting_models:
					model.valid_shots.clear()
				game.shooting_models.clear()
				if game.selected_unit != None:
					game.selected_unit.valid_shots.clear()
				game.clear_selections()

			elif keys[pygame.K_RETURN]:
				game.change_phase("Charge Phase")
				game.shooting_models.clear()
				game.clear_selections()
				game.clear_valid_shots()
				for model in game.selectable_models:
					for weapon in model.ranged_weapons:
						weapon.fired = False

		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB
				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				elif game.attack_button.mouse_over():
					if len(game.shooting_models) > 0:
						if game.target_unit != None:
							for model in game.target_unit.models:
								if model.in_melee == True:
									print('\nCannot shoot at [{}] because it is locked in melee with friendly units.'.format(game.target_unit.name))
									return
							for model in game.shooting_models:
								model.attack_with_ranged_weapon(game.target_unit)
							if game.unallocated_wounds > 0:
								game.change_phase("Wound Allocation")
						else:
							print("\nNo target selected. Select a target to shoot at.")
					else:
						print("\nNo shooting models selected. Select models to shoot with.")

				elif len(game.shooting_models) == 0:
					multiple_selection(game)
					if len(game.shooting_models) > 0:
						game.los_check(game.selected_model)
						game.selected_unit.valid_shots = game.selected_model.valid_shots
							
				elif len(game.shooting_models) > 0:
					multiple_selection(game)
					if len(game.shooting_models) > 0:
						game.los_check(game.selected_model)
						game.selected_unit.valid_shots = intersection(game.selected_unit.valid_shots, game.selected_model.valid_shots)

			elif event.button == 2: #Middle mouse button
				game.shooting_models.clear()
				game.selected_unit = None
				mass_selection(game)
				print("\nRunning LOS checks on entire unit, please wait...")
				if len(game.shooting_models) > 0:
					game.los_check(game.selected_model)
					game.selected_unit.valid_shots = game.selected_model.valid_shots
					for model in game.shooting_models:
						if model != game.selected_model:
							game.los_check(model)
							game.selected_unit.valid_shots = intersection(game.selected_unit.valid_shots, model.valid_shots)
				print("\nLOS checks complete.")

			elif event.button == 3:	#RMB
				if len(game.shooting_models) > 0:
					game.target_model = None
					game.target_unit = None
					#Target selection
					for model in game.targets:
						adjusted_model_rect = game.camera.apply(model)
						if adjusted_model_rect.collidepoint(get_adjusted_mouse_pos(game)):
							if model in game.selected_unit.valid_shots:
								game.target_model = model
								game.target_unit = model.unit

def wound_allocation(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_RETURN]:
				pass

		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB ; Mouse event.buttom refers to interger values: 1(left), 2(middle), 3(right), 4(scrl up), 5(scrl down)
				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				else:
					for model in game.target_unit.models:
						adjusted_model_rect = game.camera.apply(model)
						if adjusted_model_rect.collidepoint(get_adjusted_mouse_pos(game)):
							model.wounds -= 1
							game.unallocated_wounds -= 1
							print("\nAllocating wound to: ")
							print(model)
							print("This model is part of unit:")
							print(model.unit.name)
							for model in game.target_unit.models:
								model.update()

							if game.unallocated_wounds <= 0 or len(game.target_unit.models) == 0:
								if game.unallocated_wounds <= 0:
									print("\nAll wounds allocated!")
								elif len(game.target_unit.models) == 0:
									print("\nTarget unit eliminated. No valid targets remain.")
								print("Returning to previous phase")
								game.change_phase(game.previous_phase)
								game.unallocated_wounds = 0
								game.selected_model.valid_shots.clear()
								game.selected_model = None
								game.selected_unit = None
								game.shooting_models.clear()
								game.fighting_models.clear()
								game.target_model = None
								game.target_unit = None

							else:
								return

					print("\nChosen model not a valid target, please select a model in the target unit.")

			elif event.button == 2:	#Middle mouse button
				pass

			elif event.button == 3: #RMB
				pas

def charge_phase(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_RETURN]:
				for unit in game.active_army.units:
					unit.charge_attempt_list.clear()
				game.refresh_moves()
				game.clear_selections()
				game.change_phase("Fight Phase: Charging Units")
				
		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB ; Mouse event.buttom refers to interger values: 1(left), 2(middle), 3(right), 4(scrl up), 5(scrl down)
				if game.reset_all_button.mouse_over():
					for model in game.selectable_models:
						game.reset_moves(model)

				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				if game.charge_button.mouse_over():
					if game.selected_model != None and game.target_model != None:
						for item in game.selected_unit.charge_attempt_list:
							if item == game.target_unit:
								print("\nA charge against this target has already been attempted by the selected unit on this turn.")
								print("Select a different charge target.")
								return
						
						game.selected_unit.charge_attempt_list.append(game.target_unit)
						game.selectable_models.empty()
						game.targets.empty()
						for model in game.selected_unit.models:
							game.targets.add(model)
						for model in game.target_unit.models:
							game.selectable_models.add(model)

						game.charging_unit = game.selected_unit
						game.charge_target_unit = game.target_unit
						game.clear_selections()
						game.target_unit = game.charging_unit
						game.selected_unit = game.charge_target_unit
						print("\nCharge target confirmed. Proceeding to overwatch response.")
						game.change_phase("Overwatch")

					elif game.selected_model == None:
						print("\nNo unit selected. Select a unit to charge with.")

					elif game.target_model == None:
						print("\nNo target selected. Select a charge target.")
						return

				elif game.selected_model == None:
					model_selection(game)

				elif game.selected_model != None:
					game.selected_model = None 	#Defaults to deselecting current model if another model isn't clicked
					game.selected_unit = None
					model_selection(game)

			elif event.button == 2:	#Middle mouse button
				pass

			elif event.button == 3: #RMB
				if game.selected_model != None:
					game.target_model = None
					game.target_unit = None

					#Target selection
					adjusted_model_rect = game.camera.apply(game.selected_model)
					for model in game.targets:
						adjusted_target_rect = game.camera.apply(model)
						if adjusted_target_rect.collidepoint(get_adjusted_mouse_pos(game)):
							charge_x = adjusted_model_rect.center[0] - adjusted_target_rect.center[0]
							charge_y = adjusted_model_rect.center[1] - adjusted_target_rect.center[1]
							charge_distance = sprite_module.find_hypotenuse(charge_x, charge_y)

							if charge_distance <= 12*TILESIZE:
								game.target_model = model
								game.target_unit = model.unit
								print("\nSelected {}.".format(game.target_model))
							else:
								print("\nAttempted selection outside of max charge range.")
								print("Select a different charge target.")

def overwatch(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_SPACE]:
				for model in game.shooting_models:
					model.valid_shots.clear()
				game.shooting_models.clear()
				if game.selected_unit != None:
					game.selected_unit.valid_shots.clear()
				game.clear_selections()

			elif keys[pygame.K_RETURN]:
				if len(game.charging_unit.models) == 0:
					game.change_phase("Charge Phase")
					return
				game.change_phase("Charge Move")

				for model in game.selectable_models:
					for weapon in model.ranged_weapons:
						weapon.fired = False

				game.selectable_models.empty()
				game.targets.empty()
				game.shooting_models.clear()

				for model in game.charging_unit.models:
					game.selectable_models.add(model)

				for unit in game.inactive_army.units:
					for model in unit.models:
						game.targets.add(model)

				game.clear_selections()
				game.clear_valid_shots()
				game.target_unit = game.charge_target_unit
				game.selected_unit = game.charging_unit
				game.charge_roll(game.charging_unit)
				
		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB
				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				elif game.attack_button.mouse_over():
					if len(game.shooting_models) > 0:
						if game.target_unit != None:
							for model in game.shooting_models:
								model.attack_with_ranged_weapon(game.target_unit)
							if game.unallocated_wounds > 0:
								game.change_phase("Wound Allocation")
						else:
							print("\nNo target selected. Select a target to shoot at.")
					else:
						print("\nNo shooting models selected. Select models to shoot with.")

				elif len(game.shooting_models) == 0:
					multiple_selection(game)
					if len(game.shooting_models) > 0:
						game.los_check(game.selected_model)
						game.selected_unit.valid_shots = game.selected_model.valid_shots
							
				elif len(game.shooting_models) > 0:
					multiple_selection(game)
					if len(game.shooting_models) > 0:
						game.los_check(game.selected_model)
						game.selected_unit.valid_shots = intersection(game.selected_unit.valid_shots, game.selected_model.valid_shots)

			elif event.button == 2: #Middle mouse button
				game.shooting_models.clear()
				game.selected_unit = None
				mass_selection(game)
				if len(game.shooting_models) > 0:
					game.los_check(game.selected_model)
					game.selected_unit.valid_shots = game.selected_model.valid_shots
					for model in game.shooting_models:
						game.los_check(model)
						game.selected_unit.valid_shots = intersection(game.selected_unit.valid_shots, model.valid_shots)

			elif event.button == 3:	#RMB
				if len(game.shooting_models) > 0:
					game.target_model = None
					game.target_unit = None
					#shot_x = game.selected_model.x - pygame.mouse.get_pos()[0]
					#shot_y = game.selected_model.y - pygame.mouse.get_pos()[1]
					#shot_distance = sprite_module.find_hypotenuse(shot_x, shot_y)

					#Target selection
					for model in game.targets:
						adjusted_model_rect = game.camera.apply(model)
						if adjusted_model_rect.collidepoint(get_adjusted_mouse_pos(game)):
							if model in game.selected_unit.valid_shots:
								game.target_model = model
								game.target_unit = model.unit

def charge_move(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if game.selected_model != None and keys[pygame.K_SPACE]:
				game.reset_moves(game.selected_model)

			elif keys[pygame.K_RETURN]:
				if game.charge_success():
					if game.cohesion_check():
						game.refresh_moves()
						game.clear_selections()
						game.charging_unit = None
						game.charge_target_unit = None
						game.reset_active()
						game.change_phase("Charge Phase")

		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB ; Mouse event.buttom refers to interger values: 1(left), 2(middle), 3(right), 4(scrl up), 5(scrl down)
				if game.reset_all_button.mouse_over():
					for model in game.selectable_models:
						game.reset_moves(model)

				elif game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				elif game.selected_model == None:
					model_selection(game)

				elif game.selected_model != None:
					game.selected_model = None 	#Defaults to deselecting current model if another model isn't clicked
					model_selection(game)

			elif event.button == 2:	#Middle mouse button
				pass

			elif event.button == 3: #RMB
				if game.selected_model != None:
					game.selected_model.dest_x = get_adjusted_mouse_pos(game)[0] - game.camera.cam_rect.topleft[0]
					game.selected_model.dest_y = get_adjusted_mouse_pos(game)[1] - game.camera.cam_rect.topleft[1]

def fight_phase_charging_units(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_SPACE]:
				game.clear_selections()

			elif keys[pygame.K_RETURN]:
				game.clear_selections()
				game.reset_active()
				game.change_phase("Fight Phase: Friendly Units")
				

		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB
				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				elif game.fight_button.mouse_over():
					if game.selected_model != None and game.selected_unit != None:
						for unit in game.ineligible_fight_units:
							if game.selected_unit == unit:
								print("\nUnit already fought this turn. Select a different unit to fight with.")
								return

						game.selectable_models.empty()
						game.targets.empty()
						for model in game.selected_unit.models:
							game.selectable_models.add(model)

						for unit in game.inactive_army.units:
							for model in unit.models:
								game.targets.add(model)

						game.ineligible_fight_units.append(game.selected_unit)
						game.change_phase("Pile In")

				elif game.selected_model == None:
					model_selection(game)

				elif game.selected_model != None:
					game.selected_model = None
					model_selection(game)								
				
			elif event.button == 2: #Middle mouse button
				pass

			elif event.button == 3:	#RMB
				pass

def fight_phase_charging_units(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_SPACE]:
				game.clear_selections()

			elif keys[pygame.K_RETURN]:
				game.clear_selections()
				game.reset_active()
				game.change_phase("Fight Phase: Friendly Units")
				

		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB
				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				elif game.fight_button.mouse_over():
					if game.selected_model != None and game.selected_unit != None:
						for unit in game.ineligible_fight_units:
							if game.selected_unit == unit:
								print("\nUnit already fought this turn. Select a different unit to fight with.")
								return

						game.selectable_models.empty()
						game.targets.empty()
						for model in game.selected_unit.models:
							game.selectable_models.add(model)

						for unit in game.inactive_army.units:
							for model in unit.models:
								game.targets.add(model)

						game.ineligible_fight_units.append(game.selected_unit)
						game.change_phase("Pile In")

				elif game.selected_model == None:
					model_selection(game)

				elif game.selected_model != None:
					game.selected_model = None
					model_selection(game)								
				
			elif event.button == 2: #Middle mouse button
				pass

			elif event.button == 3:	#RMB
				pass

def fight_phase_friendly_units(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_SPACE]:
				game.clear_selections()

			elif keys[pygame.K_RETURN]:
				if mods & pygame.KMOD_SHIFT:
					game.ineligible_fight_units.clear()
					game.clear_selections()
					for unit in game.active_army.units:
						for model in unit.models:
							model.fought = False

					for unit in game.inactive_army.units:
						for model in unit.models:
							model.fought = False

					game.change_phase("Morale Phase")
					for unit in game.army1.units:
						game.morale_test(unit)
					for unit in game.army2.units:
						game.morale_test(unit)

				else:
					game.clear_selections()
					game.selectable_models.empty()
					game.targets.empty()
					for unit in game.inactive_army.units:
						for model in unit.models:
							game.selectable_models.add(model)

					for unit in game.active_army.units:
						for model in unit.models:
							game.targets.add(model)

					game.change_phase("Fight Phase: Enemy Units")
				
		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB
				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				elif game.fight_button.mouse_over():
					if game.selected_model != None and game.selected_unit != None:
						for unit in game.ineligible_fight_units:
							if game.selected_unit == unit:
								print("\nUnit already fought this turn. Select a different unit to fight with.")
								return

						game.refresh_moves()
						game.selectable_models.empty()
						game.targets.empty()

						for model in game.selected_unit.models:
							game.selectable_models.add(model)

						for unit in game.inactive_army.units:
							for model in unit.models:
								game.targets.add(model)

						game.ineligible_fight_units.append(game.selected_unit)
						game.change_phase("Pile In")

				elif game.selected_model == None:
					model_selection(game)

				elif game.selected_model != None:
					game.selected_model = None
					model_selection(game)								
				
			elif event.button == 2: #Middle mouse button
				pass

			elif event.button == 3:	#RMB
				pass

def fight_phase_enemy_units(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_SPACE]:
				game.clear_selections()

			elif keys[pygame.K_RETURN]:
				if mods & pygame.KMOD_SHIFT:
					game.ineligible_fight_units.clear()
					game.clear_selections()
					for unit in game.active_army.units:
						for model in unit.models:
							model.fought = False

					for unit in game.inactive_army.units:
						for model in unit.models:
							model.fought = False

					game.change_phase("Morale Phase")
					for unit in game.army1.units:
						game.morale_test(unit)
					for unit in game.army2.units:
						game.morale_test(unit)

				else:
					game.clear_selections()
					game.selectable_models.empty()
					game.targets.empty()
					for unit in game.active_army.units:
						for model in unit.models:
							game.selectable_models.add(model)

					for unit in game.inactive_army.units:
						for model in unit.models:
							game.targets.add(model)

					game.change_phase("Fight Phase: Friendly Units")

		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB
				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				elif game.fight_button.mouse_over():
					if game.selected_model != None and game.selected_unit != None:
						for unit in game.ineligible_fight_units:
							if game.selected_unit == unit:
								print("\nUnit already fought this turn. Select a different unit to fight with.")
								return

						game.refresh_moves()
						game.selectable_models.empty()
						game.targets.empty()

						for model in game.selected_unit.models:
							game.selectable_models.add(model)

						for unit in game.active_army.units:
							for model in unit.models:
								game.targets.add(model)

						game.ineligible_fight_units.append(game.selected_unit)
						game.change_phase("Pile In")

				elif game.selected_model == None:
					model_selection(game)

				elif game.selected_model != None:
					game.selected_model = None
					model_selection(game)								
				
			elif event.button == 2: #Middle mouse button
				pass

			elif event.button == 3:	#RMB
				pass

def pile_in(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_SPACE]:
				if game.selected_model != None:
					game.reset_moves(game.selected_model)

			elif keys[pygame.K_RETURN]:
				if game.cohesion_check():
					game.refresh_moves()
					game.clear_selections()
					game.change_phase("Fight Targeting")
				
		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB
				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				elif game.reset_all_button.mouse_over():
					for model in game.selectable_models:
						game.reset_moves(model)

				elif game.selected_model == None:
					model_selection(game)

				elif game.selected_model != None:
					game.selected_model = None
					model_selection(game)								
				
			elif event.button == 2: #Middle mouse button
				pass

			elif event.button == 3:	#RMB
				if game.selected_model != None:
					game.selected_model.dest_x = get_adjusted_mouse_pos(game)[0] - game.camera.cam_rect.topleft[0]
					game.selected_model.dest_y = get_adjusted_mouse_pos(game)[1] - game.camera.cam_rect.topleft[1]

def fight_targeting(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_SPACE]:
				game.clear_melee_lists()
				game.selected_unit.valid_model_targets.clear()
				game.clear_selections()

			elif keys[pygame.K_RETURN]:
				game.change_phase("Consolidate")

		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB
				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				elif game.attack_button.mouse_over():
					if len(game.fighting_models) > 0:
						if game.target_unit != None:
							game.clear_melee_lists()
							game.selected_unit.valid_model_targets.clear()
							for model in game.fighting_models:
								if model.fought == False:
									model.fought = True
									model.attack_with_melee_weapon(game.target_unit)
								else:
									print("\nCannot attack; [{}] has no attacks remaining this turn.".format(model.name))
							if game.unallocated_wounds > 0:
								game.change_phase("Wound Allocation")
						else:
							print("\nNo target selected. Select a target to shoot at.")
					else:
						print("\nNo shooting models selected. Select models to shoot with.")

				elif len(game.fighting_models) == 0:
					multiple_melee_selection(game)

				elif len(game.fighting_models) > 0:
					multiple_melee_selection(game)
						
										
			elif event.button == 2: #Middle mouse button
				pass

			elif event.button == 3:	#RMB
				if len(game.fighting_models) > 0 and game.selected_model != None and game.selected_unit != None:
					game.target_model = None
					game.target_unit = None
					#Target selection
					for model in game.targets:
						adjusted_model_rect = game.camera.apply(model)
						if adjusted_model_rect.collidepoint(get_adjusted_mouse_pos(game)):
							if model in game.selected_unit.valid_model_targets:
								game.target_model = model
								game.target_unit = model.unit

def consolidate(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_SPACE]:
				if game.selected_model != None:
					game.reset_moves(game.selected_model)

			elif keys[pygame.K_RETURN]:
				if game.cohesion_check():
					if game.fight_subphase == "Fight Phase: Charging Units":
						game.reset_active()
					game.refresh_moves()
					game.clear_selections()
					game.change_phase(game.fight_subphase)
				
		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB
				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				elif game.reset_all_button.mouse_over():
					for model in game.selectable_models:
						game.reset_moves(model)

				elif game.selected_model == None:
					model_selection(game)

				elif game.selected_model != None:
					game.selected_model = None
					model_selection(game)								
				
			elif event.button == 2: #Middle mouse button
				pass

			elif event.button == 3:	#RMB
				if game.selected_model != None:
					game.selected_model.dest_x = get_adjusted_mouse_pos(game)[0] - game.camera.cam_rect.topleft[0]
					game.selected_model.dest_y = get_adjusted_mouse_pos(game)[1] - game.camera.cam_rect.topleft[1]

def morale_phase(game):
	for unit in game.active_army.units:
		if unit.morale_losses > 0:
			game.selected_unit = unit
			game.change_phase("Morale Loss Allocation")

	for unit in game.inactive_army.units:
		if unit.morale_losses > 0:
			game.selected_unit = unit
			game.change_phase("Morale Loss Allocation")

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_SPACE]:
				pass

			elif keys[pygame.K_RETURN]:
				for unit in game.active_army.units:
					if unit.morale_losses > 0:
						print("Cannot proceed to next turn: not all units have undergone morale check")
						return

				for unit in game.inactive_army.units:
					if unit.morale_losses > 0:
						print("Cannot proceed to next turn: not all units have undergone morale check")
						return

				game.change_phase("Movement Phase")
				game.change_active()

		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB
				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

			elif event.button == 2: #Middle mouse button
				pass

			elif event.button == 3:	#RMB
				pass

def morale_loss_allocation(game):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.quit()

		#Keyboard event handling
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			mods = pygame.key.get_mods()

			core_events(game, keys, mods)

			if keys[pygame.K_SPACE]:
				pass

			elif keys[pygame.K_RETURN]:
				pass

		#Mouse event handling
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:	#LMB
				if game.toggle_radii_button.mouse_over():
					game.toggle_radii()

				else:
					for model in game.selected_unit.models:
						adjusted_model_rect = game.camera.apply(model)
						if adjusted_model_rect.collidepoint(get_adjusted_mouse_pos(game)):
							model.die()
							print("\nModel being removed as morale loss: ")
							print(model)
							print("This model is part of unit:")
							print(model.unit.name)
							for model in game.selected_unit.models:
								model.update()

							game.selected_unit.morale_losses -= 1
							
							if game.selected_unit.morale_losses <= 0 or len(game.selected_unit.models) == 0:
								if game.selected_unit.morale_losses <= 0:
									print("\nAll morale losses allocated!")
								elif len(game.selected_unit.models) == 0:
									print("\nEntire unit eliminated. No valid morale losses remain.")
									game.selected_unit.morale_losses = 0
								
								game.selected_unit = None
								print("Returning to previous phase")
								game.change_phase("Morale Phase")

						else:
							print("\nChosen model not a valid target, please choose a model in the current unit that needs to allocate morale losses.")

			elif event.button == 2: #Middle mouse button
				pass

			elif event.button == 3:	#RMB
				pass