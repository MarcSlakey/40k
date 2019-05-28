import pygame
#from pygame.locals import *
from settings import *

def draw_text(game, surface, text, font_name, size, color, x, y, align="nw"):
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
		surface.blit(text_surface, text_rect)

def draw_info_text(game):
	#General info text
	draw_text(game, game.background, "Turn #{}: {} {}".format(game.turn_count, game.active_army.name, game.current_phase), game.generic_font, game.largeText, WHITE, WIDTH/2, 15, "center")
	draw_text(game, game.background, "|HOME: reset game|", game.generic_font, game.mediumText, WHITE, WIDTH-(TILESIZE*2), 15, "e")
	fps = int(game.clock.get_fps())
	draw_text(game, game.background, "FPS: {}".format(fps), game.generic_font, game.mediumText, WHITE, 2*WIDTH/32, 15, "w")
	draw_text(game, game.background, "Camera Offset: {},{}".format(game.camera.cam_rect.x, game.camera.cam_rect.y), game.generic_font, game.mediumText, WHITE, 4*WIDTH/32, 15, "w")	

def draw_controls(game, lmb, mmb, rmb, spacebar, enter):
	#Controls Info Text	
	draw_text(game, game.background, "|LMB: " +str(lmb)+"|", game.generic_font, game.mediumText, WHITE, WIDTH/32, HEIGHT+50, "w")
	draw_text(game, game.background, "|MMB: " +str(mmb)+"|", game.generic_font, game.mediumText, WHITE, WIDTH/32, HEIGHT+80, "w")
	draw_text(game, game.background, "|RMB: " +str(rmb)+"|", game.generic_font, game.mediumText, WHITE, 6*WIDTH/32, HEIGHT+50, "w")
	draw_text(game, game.background, "|SPACEBAR: " +str(spacebar)+"|", game.generic_font, game.mediumText, WHITE, 12*WIDTH/32, HEIGHT+50, "w")
	draw_text(game, game.background, "|RETURN: " +str(enter)+"|", game.generic_font, game.mediumText, WHITE, 24*WIDTH/32, HEIGHT+50, "w")

def draw_selected_model_indicators(game):
	if game.selected_unit != None:
		for model in game.selected_unit.models:
			pygame.draw.circle(game.screen, CYAN, (game.camera.apply(model)).center, model.radius, 0)

	pygame.draw.circle(game.screen, YELLOW, game.camera.apply(game.selected_model).center, game.selected_model.radius, 0)
	if game.selected_model.cohesion:
		pygame.draw.circle(game.screen, GREEN, game.camera.apply(game.selected_model).center, game.selected_model.radius, 0)

def draw_shooting_target_indicators(game):
	#Used in Shooting phase, Wound allocation, Overwatch
	#Targets in LOS
	if game.selected_unit != None:
		if len(game.selected_unit.valid_shots) > 0:
			for model in game.selected_unit.valid_shots:
				pygame.draw.circle(game.screen, YELLOW, game.camera.apply(model).center, model.radius, 0)

def draw_target_unit_indicator(game):
	if game.target_unit != None:
		for model in game.target_unit.models:
			pygame.draw.circle(game.screen, ORANGE, game.camera.apply(model).center, model.radius, 0)

def draw_blue_dot_selections(game, model):
	pygame.draw.circle(game.screen, BLUE, game.camera.apply(model).center, int((model.radius)/2), 0)

def draw_radii(game, weapon_range=False, move_radius=False, enemy_melee_radius=False, cohesion_radius=False, charge_move_radius=False, max_charge_move_radius=False):
	#Weapon range radius
	if weapon_range == True:
		pygame.draw.circle(game.screen, RED, game.camera.apply(game.selected_model).center, int(game.selected_model.ranged_weapons[0].w_range), 1)

	#Remaining move radius
	if move_radius == True:
		if game.selected_model.max_move >= 1:
			pygame.draw.circle(game.screen, YELLOW, game.camera.apply(game.selected_model).center, int(game.selected_model.max_move), 1)

	#Enemy Melee radius (one inch)
	if enemy_melee_radius == True:
		for sprite in game.targets:
			pygame.draw.circle(game.screen, RED, game.camera.apply(sprite).center, sprite.true_melee_radius, 1)

	#Cohesion radius (two inches)
	if cohesion_radius == True:
		for sprite in game.selected_model.unit.models:
			if sprite != game.selected_model:
				pygame.draw.circle(game.screen, GREEN, game.camera.apply(sprite).center, sprite.true_cohesion_radius, 1)

	#Remaining charge move radius
	if charge_move_radius == True:
		if game.selected_model.charge_move != 0:
			pygame.draw.circle(game.screen, YELLOW, game.camera.apply(game.selected_model).center, int(game.charge_range), 1)

	if max_charge_move_radius == True:
		if game.selected_model.charge_move == 0:
			pygame.draw.circle(game.screen, RED, game.camera.apply(game.selected_model).center, 12*TILESIZE, 1)

def movement_phase(game):
	#Model base drawing/coloring
	if game.selected_model != None:
		draw_selected_model_indicators(game)

		if game.show_radii == True:
			draw_radii(game, weapon_range=True, move_radius=True, enemy_melee_radius=True, cohesion_radius=True)

	game.draw_cohesion_indicator()	

	#Buttons
	game.reset_all_button.draw()
	game.reset_all_button.fill()

	game.toggle_radii_button.draw()
	game.toggle_radii_button.fill()

	#Controls Info Text	
	draw_controls(game, lmb="select model", mmb="N/A", rmb="move model", spacebar="reset selected model's move", enter="progress to next phase")

def shooting_phase(game):
	if game.selected_model != None:
		draw_selected_model_indicators(game)
		draw_shooting_target_indicators(game)
		draw_target_unit_indicator(game)
		if game.show_radii == True:
			draw_radii(game, weapon_range=True)
		
	if len(game.shooting_models) > 0:
		for model in game.shooting_models:
			draw_blue_dot_selections(game, model)

	#Buttons
	game.attack_button.draw()
	game.attack_button.fill()

	game.toggle_radii_button.draw()
	game.toggle_radii_button.fill()

	#Controls Info Text
	draw_controls(game, lmb="select model", mmb="select entire unit", rmb="select target", spacebar="deselect shooters", enter="progress to next phase")

def wound_allocation(game):
	if game.selected_model != None:
		draw_selected_model_indicators(game)
		draw_shooting_target_indicators(game)
		draw_target_unit_indicator(game)
		if game.show_radii == True:
			draw_radii(game, weapon_range=True)

	#Buttons
	game.toggle_radii_button.draw()
	game.toggle_radii_button.fill()

	#Unallocated wound counter
	draw_text(game, game.screen, "{}Wound(s) to allocate!".format(game.unallocated_wounds), game.generic_font, game.largeText, YELLOW, WIDTH/2, HEIGHT - 2*TILESIZE, "center")

	#Controls Info Text
	draw_controls(game, lmb="allocate wound", mmb="N/A", rmb="N/A", spacebar="N/A", enter="N/A")

def charge_phase(game):
	if game.selected_model != None:
		draw_selected_model_indicators(game)
		draw_target_unit_indicator(game)

		if game.show_radii == True:
			draw_radii(game, enemy_melee_radius=True, cohesion_radius=True, charge_move_radius=True, max_charge_move_radius=True)

	#Draws large semi-circle cohesion indicator
	game.draw_cohesion_indicator()	

	#Buttons
	game.charge_button.draw()
	game.charge_button.fill()

	game.toggle_radii_button.draw()
	game.toggle_radii_button.fill()

	#Controls Info Text	
	draw_controls(game, lmb="select model", mmb="N/A", rmb="select charge target", spacebar="N/A", enter="progress to next phase")
	