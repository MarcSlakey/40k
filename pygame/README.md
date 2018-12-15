Pygame adaptation of the Warhammer 40k tabletop game.

Both python and pygame are required to run this program. Python 2.7 or newer is recommended.
To install python, visit https://www.python.org/downloads/.
To install pygame, use this pip install command in the command line:
python3 -m pip install -U pygame --user

Note: "python3" might be "python" or "py" instead depending on your version of python.

Once both are installed, download this entire folder.
Change directory to the pygame folder and run main.py.

GENERAL CONTROLS:
LMB to click any of the buttons on the bottom part of the screen

MOVE PHASE CONTROLS:
"LMB" on a model (circle) to select it. A model will turn yellow to indicate that it is selected.
"RMB" commands the selected model to move to the clicked location.
"Spacebar" while a model is selected will reset it to its previous position.
Click "Reset Moves" button to achieve the Spacebar effect but for all selectable models.
"Enter/Return" will progress the game to the shooting phase if unit cohesion has been maintained
"Home" will reset to a new game.

SHOOTING PHASE CONTROLS:
"LMB" on a model (circle) to select it. 
	Clicking a second model while one is already selected will attempt to make a group that can shoot at the same time.
"RMB" while a model is selected will target a given model's unit for shooting if that model is in range AND in line of sight of the selected model.
	Valid shooting targets will be highlighted yellow instead of red.
	Once a unit is successfully selected for shooting its models will turn orange.
"MMB" (Middle click mouse) selects an entire squad.
Click "Fire Weapon" while a friendly unit AND a target unit are selected to shoot. If the shots do damage, the game will proceed to a "Wound Allocation" phase.
"Spacebar" while any models are selected will reset clear all selections.
"Enter/Return" will progress the game to the next turn and begin a new movement phase as long as you're not currently allocating wounds.
"Home" will reset to a new game.

WOUND ALLOCATION PHASE CONTROLS:
"LMB" on a model in the currently targetted unit to allocate a single wound to it.
	When all wounds have been allocated, the game will return to the shooting phase.


GAME BASICS:
The white-filled circles are selectable tabletop "models".
The red-filled circles are non-selectable "target models". Game ends when all of these are eliminated.
The large yellow circle that appears on model selection shows remaining move distance. The red one shows the model's shooting range.
The selected model will turn from yellow to green when within 2 squares of a model in its unit to indicate that it is currently maintaining "unit cohesion" (see MOVE PHASE RULES below).
The semi-circle on the top left of the screen will turn green if unit cohesion between the selectable models is established and is red otherwise.

MOVE PHASE RULES:
Selected model is colored either yellow or green depending on unit cohesion.
Each model can only travel a set distance per turn. 
Models cannot pass through each other.
Additionally, models may not be moved within 1" (one tile size) of an enemy model (represented by a red radius around each enemy).
Models that are part of a unit must maintain "unit cohesion." That is, they must end their move phase within 2" of another member of their unit.

SHOOTING PHASE RULES:
Selected model is green, other models in the same unit are cyan. 
Models that have been cumulatively selected for simultaneous shooting have a blue dot on them.
Models can only shoot as a group if they are in the same unit, have the same ballistic skill, use the same weapon, and are shooting at the same target unit.
A model must have line of sight to an enemy and be in range of that enemy in order to shoot it. 
Line of sight is blocked by other enemy models and terrain, but not by friendly models.
Targets in LOS are painted yellow instead of red.
Range is indicated by the thin red radius drawn around a selected model.
Enemies are targeted as unit blocks, not as individuals. 
Individual models are allocated damage once a group of shots have been resolved (been tested for hit, wound, and save)

CURRENTLY IMPLEMENTED:
Movement Phase:
	Basic movement:
		Max move distance
		Collisions
		Unit cohesion checking
Shooting Phase:
	Basic Shooting:
		Multi-shooter selection ("fast dice rolling")
		Range checking
		Group line of sight checking
		Wound allocation
		Model death
Program:
	Basic buttons
	Info text

IN PROGRESS:
Shooting Phase:
	Multiple weapons (selection)

FUTURE WORK:
Movement Phase:
	Special movement:
		Advance moves
		Fall back moves
Shooting Phase:
	Weapon type interactions:
		Rapid fire
		Heavy
		Assault (requires advance moves)
		Rapid fire
		Grenade
		Pistols (requires basic melee phase)
	Terrain/Cover modifiers
	Character targeting ruless
Charge Phase:
	Unit selection (eligibility)
	Targeting and charge declarations
	Overwatch
	Heroic intervention
Fight Phase:
	Pile in move
	Targeting
	Consolidation move
Morale Phase:
General:
	Mortal wounds
	Buff auras
Program:
	Control GUI

Fancy Rules (for the distant future):
	Transports
	Psychic phase
	Reinforcements


CURRENT BUGS:
Models "stick" to walls and other models when they collide.
During shooting phase, can add models to the shooting group even if they have fired all their weapons (although they do not fire again).