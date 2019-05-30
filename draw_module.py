import pygame
#from pygame.locals import *
from settings import *

def scale_text(game, font_size):
	return int(game.ui_scale * font_size)

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
	fps = int(game.clock.get_fps())
	draw_text(game, game.background, "FPS: {}".format(fps), game.generic_font,  scale_text(game, game.mediumText), WHITE, 2*game.background_w/32, 15, "w")
	draw_text(game, game.background, "Camera Offset: {},{}".format(game.camera.cam_rect.x, game.camera.cam_rect.y), game.generic_font,  scale_text(game, game.mediumText), WHITE, 4*game.background_w/32, 15, "w")
	draw_text(game, game.background, "Camera Dimensions: {},{}".format(game.camera.width, game.camera.height), game.generic_font,  scale_text(game, game.mediumText), WHITE, 4*game.background_w/32, 40, "w")
	draw_text(game, game.background, "Turn #{}: {} {}".format(game.turn_count, game.active_army.name, game.current_phase), game.generic_font, scale_text(game, game.largeText), WHITE, game.background_w/2, 15, "center")
	draw_text(game, game.background, "Background Size: {},{}".format(game.background_w, game.background_h), game.generic_font,  scale_text(game, game.mediumText), WHITE, 45*game.background_w/64, 15, "w")
	draw_text(game, game.background, "Screen Size: {},{}".format(game.screen_w, game.screen_h), game.generic_font,  scale_text(game, game.mediumText), WHITE, 45*game.background_w/64, 40, "w")
	draw_text(game, game.background, "|HOME: reset game|", game.generic_font,  scale_text(game, game.mediumText), WHITE, game.background_w-50, 15, "e")

def draw_controls(game, lmb="N/A", mmb="N/A", rmb="N/A", spacebar="N/A", enter="N/A", shift_enter="N/A"):
	#Controls Info Text	
	draw_text(game, game.background, "|LMB: "+str(lmb)+"|", game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w/128, game.background_h-100, "w")
	draw_text(game, game.background, "|MMB: "+str(mmb)+"|", game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w/128, game.background_h-60, "w")
	draw_text(game, game.background, "|RMB: "+str(rmb)+"|", game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w/128, game.background_h-80, "w")
	draw_text(game, game.background, "|HOME: reset game|", game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w/128, game.background_h-40, "w")
	draw_text(game, game.background, "|END: close game|", game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w/128, game.background_h-20, "w")
	
	draw_text(game, game.background, "|SPACEBAR: "+str(spacebar)+"|", game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*15/128, game.background_h-100, "w")
	draw_text(game, game.background, "|RETURN: "+str(enter)+"|", game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*15/128, game.background_h-80, "w")
	draw_text(game, game.background, "|SHIFT+RETURN: "+str(shift_enter)+"|", game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*15/128, game.background_h-60, "w")
	draw_text(game, game.background, "|ARROW KEYS: move camera|", game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*15/128, game.background_h-40, "w")

def draw_debug_info(game):
	#Model Stats
	x_align = 20
	x_align2 = 23
	draw_text(game, game.background, "|MODEL: {}|".format(game.selected_model), game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*(x_align-1)/64, game.background_h-100, "w")
	if game.selected_model != None:
		draw_text(game, game.background, "M:  {}".format(game.selected_model.original_max_move/TILESIZE), game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*x_align/64, game.background_h-80, "e")
		draw_text(game, game.background, "Ld: {}".format(game.selected_model.leadership), game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*x_align2/64, game.background_h-80, "e")
		draw_text(game, game.background, "WS: {}".format(game.selected_model.weapon_skill), game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*x_align/64, game.background_h-65, "e")
		draw_text(game, game.background, "BS: {}".format(game.selected_model.ballistic_skill), game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*x_align2/64, game.background_h-65, "e")
		draw_text(game, game.background, "S: {}".format(game.selected_model.strength), game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*x_align/64, game.background_h-50, "e")
		draw_text(game, game.background, "T: {}".format(game.selected_model.toughness), game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*x_align2/64, game.background_h-50, "e")
		draw_text(game, game.background, "Sv: {}".format(game.selected_model.save), game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*x_align/64, game.background_h-35, "e")
		draw_text(game, game.background, "Inv: {}".format(game.selected_model.invulnerable), game.generic_font, scale_text(game, game.smallText), WHITE, game.background_w*x_align2/64, game.background_h-35, "e")

	#Side Panel Info (Debug Info)
	x_align = 34
	draw_text(game, game.background, "|SELECTED MODEL: {}|".format(game.selected_model), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-100, "w")
	if game.selected_model != None:
		draw_text(game, game.background, "in_melee: {}".format(game.selected_model.in_melee), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-80, "w")
		draw_text(game, game.background, "fought: {}".format(game.selected_model.fought), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-65, "w")
		draw_text(game, game.background, "charged: {}".format(game.selected_model.unit.charged_this_turn), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-50, "w")
		draw_text(game, game.background, "advanced: {}".format(game.selected_model.advanced), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-35, "w")
		draw_text(game, game.background, "fell_back: {}".format(game.selected_model.fell_back), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-20, "w")

	x_align = 41
	if game.selected_unit == None:
		draw_text(game, game.background, "|SELECTED UNIT: None|", game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-100, "w")
	if game.selected_unit != None:
		draw_text(game, game.background, "|SELECTED UNIT|: {}".format(game.selected_unit.name), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-100, "w")
		draw_text(game, game.background, "# of recent deaths: {}".format(len(game.selected_unit.recent_deaths)), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-80, "w")
		draw_text(game, game.background, "# of shooters selected: {}".format(len(game.shooting_models)), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-65, "w")
		draw_text(game, game.background, "# of fighters selected: {}".format(len(game.fighting_models)), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-50, "w")

	x_align = 50
	draw_text(game, game.background, "|Target Model: {}|".format(game.target_model), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-100, "w")

	x_align = 57
	if game.target_unit == None:
		draw_text(game, game.background, "|Target Unit: None|", game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-100, "w")
	if game.target_unit != None:
		draw_text(game, game.background, "|Target Unit: {}|".format(game.target_unit.name), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-100, "w")
		draw_text(game, game.background, "# of recent deaths: {}".format(len(game.target_unit.recent_deaths)), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-80, "w")
	#draw_text(game, game.background, "Target Unit: {}".format(game.target_unit), game.generic_font, scale_text(game, game.tinyText), WHITE, game.background_w*x_align/64, game.background_h-50, "w")

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

def draw_radii(game, weapon_range=False, move_radius=False, enemy_melee_radius=False, target_melee_radius=False, cohesion_radius=False, charge_move_radius=False, max_charge_move_radius=False):
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

	#Target melee radius
	if target_melee_radius == True:
		if game.target_unit != None:
			for sprite in game.target_unit.models:
				pygame.draw.circle(game.screen, ORANGE, game.camera.apply(sprite).center, sprite.true_melee_radius, 1)

	#Cohesion radius (two inches)
	if cohesion_radius == True:
		for sprite in game.selected_model.unit.models:
			if sprite != game.selected_model:
				pygame.draw.circle(game.screen, GREEN, game.camera.apply(sprite).center, sprite.true_cohesion_radius, 1)

	#Remaining charge move radius
	if charge_move_radius == True:
		if game.selected_model.charge_move > 1:
			pygame.draw.circle(game.screen, YELLOW, game.camera.apply(game.selected_model).center, int(game.selected_model.charge_move), 1)

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
	draw_debug_info(game)
	draw_controls(game, lmb="select model", mmb="N/A", rmb="move model", spacebar="reset move", enter="progress to next phase")

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
	draw_debug_info(game)
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
	draw_text(game, game.screen, "{}Wound(s) to allocate!".format(game.unallocated_wounds), game.generic_font, game.largeText, YELLOW, game.screen_w/2, game.screen_h - 2*TILESIZE, "center")

	#Controls Info Text
	draw_debug_info(game)
	draw_controls(game, lmb="allocate wound", mmb="N/A", rmb="N/A", spacebar="N/A", enter="N/A")

def charge_phase(game):
	if game.selected_model != None:
		draw_selected_model_indicators(game)
		draw_target_unit_indicator(game)

		if game.show_radii == True:
			draw_radii(game, enemy_melee_radius=True, cohesion_radius=True, max_charge_move_radius=True)

	#Draws circle cohesion indicator
	game.draw_cohesion_indicator()	

	#Buttons
	game.charge_button.draw()
	game.charge_button.fill()

	game.toggle_radii_button.draw()
	game.toggle_radii_button.fill()

	#Controls Info Text	
	draw_debug_info(game)
	draw_controls(game, lmb="select model", mmb="N/A", rmb="select target", spacebar="N/A", enter="progress to next phase")

def overwatch(game):
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
	draw_debug_info(game)
	draw_controls(game, lmb="select model", mmb="select entire unit", rmb="select target", spacebar="deselect shooters", enter="progress to next phase") 

def charge_move(game):
	if game.selected_model != None:
		draw_selected_model_indicators(game)
		if game.show_radii == True:
			draw_radii(game, weapon_range=True, cohesion_radius=True, charge_move_radius=True, enemy_melee_radius=True)

	#Draws circle cohesion indicator
	game.draw_cohesion_indicator()	

	#Buttons
	game.reset_all_button.draw()
	game.reset_all_button.fill()

	game.toggle_radii_button.draw()
	game.toggle_radii_button.fill()

	#Controls Info Text	
	draw_debug_info(game)
	draw_controls(game, lmb="select model", mmb="N/A", rmb="move model", spacebar="reset move", enter="progress to next phase") 


def fight_phase(game):
	if game.selected_model != None:
		draw_selected_model_indicators(game)
		draw_target_unit_indicator(game)

	#Draws large semi-circle cohesion indicator
	game.draw_cohesion_indicator()	

	#Buttons
	game.fight_button.draw()
	game.fight_button.fill()

	game.toggle_radii_button.draw()
	game.toggle_radii_button.fill()

	#Controls Info Text	
	draw_debug_info(game)
	draw_controls(game, lmb="select model", mmb="N/A", rmb="N/A", spacebar="N/A", enter="next Fight sub-phase", shift_enter="end Fight Phase")

