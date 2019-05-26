#Create and set Window size and FPS constants
TITLE = "40k pygame"
#WIDTH = 1920
#HEIGHT = 1080	
WIDTH = 1600
HEIGHT = 850	
FPS = 120		#locks the FPS

CAMERA_SPEED = 20

#define simple color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)	
YELLOW = (255, 255, 0)
ORANGE = (255, 150, 0)


TILESIZE = 25 	#Should always represent 1" in gameplay; for reference: 25.4 mm / inch
				#Standard battlefield size is 4' x 6' (48 tiles x 72 tiles)
				#Recommend a large terrain feature in each 2' x 2' (24 tiles x 24 tiles) section
				#Units are deployed 12" away from the line that divides the two halves of the boards
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

