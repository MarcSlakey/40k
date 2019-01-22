Pygame adaptation of the 8th Edition of the Warhammer 40k tabletop game.

Both python and pygame are required to run this program. Python 2.7 or newer is recommended.
To install python, visit https://www.python.org/downloads/.
To install pygame, use this pip install command in the command line:
python3 -m pip install -U pygame --user

Note: "python3" might be "python" or "py" instead depending on your version of python.

Once both are installed, download this entire folder.
Change directory to the pygame folder and run main.py.

Detailed rules for game mechanics that have been implemented are listed below.
Basic controls are shown in a rudimentary UI in-game, but detailed controls are listed further down.
They attempt to match the rules in the included 8e Battle Primer PDF as closely as possible.
See that PDF in the pygame folder (40k\pygame\"8e Battle Primer (Basic Rules)") for the best explanation of the core rules.

GAME BASICS:
This is a turn based game in which two armies take turns until one of them is destroyed.
Each army's turn consists of 6 sequential main phases: Movement, Psychic, Shooting, Charge, Fight, Morale.
	Note: Psychic, Fight, and Morale have not been implemented yet.
The game ends when all models in a given army are destroyed.

MOVEMENT PHASE RULES:
Each model can only travel a set distance per turn: the yellow radius that appears on model selection shows remaining move distance.
Models cannot pass through each other.
Additionally, models may not be moved within 1" (one tile size) of an enemy model (represented by a red radius around each enemy).
Models that are part of a unit must maintain "unit cohesion." That is, they must end their move phase within 2" of another member of their unit.
The selected model will turn from yellow to green when within 2 squares of a model in its unit to indicate that it is currently maintaining "unit cohesion."
The semi-circle near the RETURN tooltip on the bottom right will turn green if unit cohesion between the selectable models is established and is red otherwise.

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

CHARGE PHASE RULES:
Selected model is green, other models in the same unit are cyan.
Maximum charge range is indicated by the thin red radius. An enemy unit can only be chosen as a charge target if it is within this range.
Only one unit can charge at a time, and that unit can only choose one charge target at a time. 
Pressing the "Confirm Charge Target" button progresses the game to the Overwatch phase, in which each model in the target unit can fire overwatch.
Overwatch works exactly the same as the shooting phase, with the exception that the overwatch models can only shoot at the unit charging them, and their shots have exactly 1/6 chance to hit (ballistic skill and all other hit mechanics are ignored entirely).
Pressing enter during Overwatch progresses to the Charge Move. The charging models are assigned a random charged distance value from 2-12 inches (2D6).
At least one model from the charging unit must establish melee collision (1 inch) with their target, otherwise the charge is considered a failure and no model may move.
Pressing enter in either case (successful or failed charge) returns the game to the Charge Phase where other friendly units may attempt charges as well.

GENERAL CONTROLS:
LMB to click any of the buttons on the bottom middle part of the screen.

MOVEMENT PHASE CONTROLS:
"LMB" on a model to select it. A model will turn green to indicate that it is selected.
	Clicking empty space will deselect the model/unit.
"RMB" commands the selected model to move to the clicked location.
"Spacebar" while a model is selected will reset it to its previous position.
Click "Reset Moves" button to achieve the Spacebar effect but for all selectable models.
"Enter/Return" will progress the game to the shooting phase if unit cohesion has been maintained
"Home" will reset the entire game.

SHOOTING PHASE CONTROLS:
"LMB" on a friendly model to select it. 
	Clicking a second friendly model while one is already selected will attempt to make a group that can shoot at the same time.
"RMB" while a friendly model is selected will target a given model's unit for shooting if that model is in range AND in line of sight of the selected model.
	Valid shooting targets will be highlighted yellow instead of orange.
	Once a unit is successfully selected for shooting its models will turn orange.
"MMB" (Middle click mouse) selects an entire friendly squad.
Click "Fire Weapon" while a friendly unit AND a target unit are selected to shoot. If the shots do damage, the game will proceed to a "Wound Allocation" phase.
"Spacebar" while any models are selected will reset clear all selections.
"Enter/Return" will progress the game to the next turn and begin a new movement phase as long as you're not currently allocating wounds.
"Home" will reset the entire game.

WOUND ALLOCATION CONTROLS:
"LMB" on a model in the currently targetted unit to allocate a single wound to it.
	When all wounds have been allocated, the game will return to the shooting phase.

CHARGE PHASE CONTROLS:
"LMB" on a friendly model to select it.
	Clicking empty space will deselect the model/unit.
"RMB" while a friendly model is selected will target an enemy model's unit for charging if that model is within the max range (12 inches).
	Once a unit is successfully selected for charging its models will turn orange.
Click "Confirm Charge Target" while a friendly unit AND a target unit are selected. The game will proceed to a "Overwatch."
"Enter/Return" will progress the game to the next turn and begin a new movement phase as long as you're not currently allocating wounds.
"Home" will reset the entire game.

OVERWATCH CONTROLS:
See "Shooting Phase" controls above.

CHARGE MOVE CONTROLS:
See "Movement Phase" controls above.



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
Charge Phase:
	Unit selection (eligibility)
	Overwatch
Program:
	Basic buttons
	Info text
Optimization:
	Lock/unlock screen around multiple draw() calls

IN PROGRESS:
Charge Phase:
	Targeting and charge declarations
	

FUTURE WORK:
Movement Phase:
	Special movement:
		Advance moves
		Fall back moves
Shooting Phase:
	Weapon type interactions:
		Multiple weapons (selection)
		Rapid fire
		Heavy
		Assault (requires advance moves)
		Rapid fire
		Grenade
		Pistols (requires basic melee phase)
	Terrain/Cover modifiers
	Character targeting ruless
Charge Phase:
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
	Dirty rect animation

Fancy Rules (for the distant future):
	Transports
	Psychic phase
	Reinforcements


CURRENT BUGS:

High Priority:


Low Priority:
LOS checks are currently very slow, especially when doing multi-shooter LOS checks.
Models can maintain coherency by simply being next to one of their unit models; thus a pair can break away from the rest of the unit. This is because I've implemented the RAW; a more historically accurate and honest interpretation of the coherency rules would check for a "chain" of coherency.
Models "stick" to walls and other models when they collide; although this is workable, it feels terrible and should be improved by pathfinding.
There is no way to collide the circular model bases with rectangular terrain. Need to write custom collision code for this interaction.
During shooting phase, can "add" models to the shooting group even if they have fired all their weapons (although they do not fire again).
During the charge phase, a unit can attempt to charge the same unit after having failed a charge against it.
During the charge phase, charging units can violate the melee radius of enemies that are not its charge target.