

#Create and set Window size and FPS constants
TITLE = "40k pygame"
WIDTH = 1024	# 16 * 64 or 32 * 32 or 64 * 16 		Values that are even divisible by 16, 32, or 64 to ensure complete squares with 
HEIGHT = 768	# 16 * 48  or 32 * 24 or 64 * 12			map sizes listed (ex: 16 tiles by 64 tiles).
FPS = 30		#locks the FPS

#define simple color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)	
YELLOW = (255, 255, 0)

TILESIZE = 32 
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#Player settings
PLAYER_SPEED = 300