import pygame
import main
from settings import *


#Basic map class structure from https://www.youtube.com/watch?v=3zV2ewk-IGU&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=40
class Map:
	"""docstring for Map"""
	def __init__(self, filename):
		self.data = []
		with open(filename, 'rt') as f:
			for line in f:
				self.data.append(line.strip())

		self.tilewidth = len(self.data[0])
		self.tileheight = len(self.data)
		self.width = self.tilewidth * TILESIZE
		self.height = self.tileheight * TILESIZE


class Camera:
	"""Tracks the amount the screen drawing needs to be offset and defines functions to apply the offset to sprites.

	Width and height are the size of the map, thus the camera is just a rect that spans the entire map.
	It is critical to understand that the "camera" is an illusion: the screen stays in place, the map itself and all the sprites are drawn at an offset
	The camera is initialized with its top left corner at the natural top left of screen, the coordinates (0,0).
	When the target (the camera_focus sprite) moves, the camera is updated by redefining it as rect with the same size as before but with a new top left corner coordinate.
	Thus the camera x, y (topleft coords) directly correspond to the shift required to match the camera shift
	"""
	def __init__(self, map_width, map_height):
		self.cam_rect = pygame.Rect(0, 0, map_width, map_height)
		self.width = map_width
		self.height	= map_height

	# Determines the necessary shift according to the movement of a target; the target is the camera_focus sprite
	# The camera x, y (topleft coords) directly correspond to the shift required to match the camera shift

	def update(self, target):
		x = -target.rect.x + int(WIDTH / 2)
		y = -target.rect.y + int(HEIGHT / 2)

		# Limit scrolling to map size
		x = min(0, x)	# left
		x = max(-(self.width - WIDTH), x)	# right; if x offset becomes smaller than this value, set it equal to this value instead 

		y = min(0, y)	# top
		y = max(-(self.height - HEIGHT), y)	# bottom

		self.cam_rect = pygame.Rect(x, y, self.width, self.height)

	# Performs the necessary rect position shift to a single entity by returning a shifted rect; looping this over all sprites creates the moving camera effect
	def apply(self, entity):
		return entity.rect.move(self.cam_rect.topleft)