Pygame adaptation of the Warhammer 40k tabletop game.

Python and pygame are required to run this program. Python 2.7 or newer is recommended.
To install python, visit https://www.python.org/downloads/.
To install pygame, use this pip install command in the command line:
python3 -m pip install -U pygame --user

Note: "python3" might be "python" or "py" instead depending on your version of python.

Once both are installed, change directory to the pygame folder and run main.py.
"main.py", "settings.py", and "sprites.py" must all be in the same folder.

MOVE PHASE CONTROLS:
"LMB" on a model (circle) to select it. A model will turn yellow to indicate that it is selected.
"RMB" commands the selected model to move to the clicked location.
"Spacebar" while a model is selected will reset it to its previous position.
"Enter/Return" will progress the game to the shooting phase if unit cohesion has been maintained
"Home" will reset to a new game.

SHOOTING PHASE CONTROLS:
"LMB" on a model (circle) to select it. A model will turn yellow to indicate that it is selected. 
	When a model is selected, the game will check that model's line of sight against enemies.
"RMB" while a model is selected will shoot a bullet at the moused-over target model if that model is in range AND in line of sight of the selected model.
	Valid shooting targets will be highlighted yellow instead of red.
"Enter/Return" will progress the game to the next turn and begin a new movement phase.
"Home" will reset to a new game.

GAME BASICS:
The white-filled circles are selectable tabletop "models".
The red-filled circles are non-selectable "target models". Game ends when all of these are eliminated.
The large yellow circle that appears on model selection shows remaining move distance. The red one shows the model's shooting range.
The selected model will turn from yellow to green when within 2 squares of a model in its unit to indicate that it is currently maintaining "unit cohesion" (see MOVE PHASE RULES below).
The semi-circle on the top left of the screen will turn green if unit cohesion between the selectable models is established and is red otherwise.

MOVE PHASE RULES:
Each model can only travel a set distance per turn. 
Models cannot pass through each other.
Additionally, models may not be moved within 1" (one tile size) of an enemy model (represented by a red radius around each enemy).
Models that are part of a unit must maintain "unit cohesion." That is, they must end their move phase within 2" of another member of their unit.

SHOOTING PHASE RULES:
A model must have line of sight to an enemy and be in range of that enemy in order to shoot it. 
Range is indicated by the thin red radius drawn around a selected model.
Line of sight is blocked by other enemy models and terrain, but not by friendly models.
Targets in LOS are painted yellow instead of red.

CURRENTLY IMPLEMENTED:
Movement Phase

IN PROGRESS:
Shooting Phase

FUTURE WORK:
Psychic Phase
Charge Phase
Fight Phase
Morale Phase


CURRENT BUGS:
Game crashes if a bullet is fired at an already dead target.