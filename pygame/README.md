Pygame adaptation of Warhammer 40k tabletop game.

Python and pygame are required to run this program. Python 2.7 or newer is recommended.
To install python, visit https://www.python.org/downloads/.
To install pygame, use this pip install command in the command line:
python3 -m pip install -U pygame --user

Note: "python3" might be "python" or "py" instead depending on your version of python.

Once both are installed, change directory to the pygame folder and run main.py.
"main.py", "settings.py", and "sprites.py" must all be in the same folder.

Controls:
LMB on a model (circle) to select it. A model will turn yellow to indicate that it is selected.
RMB commands the selected model to move the clicked location.
Spacebar while a model is selected will reset it to its original position.
Middle click while a model is selected will delete a target model if that model is in range.

Game basics:
The white-filled circles on the left of the screen are selectable tabletop "models".
The white-filled circles on the right are non-selectable "target models".
The large yellow circle that appears on model selection shows remaining move distance. The red one shows the model's shooting range.
The selected model will turn from yellow to green when within 2 squares of a model in its unit to indicate that it is currently maintaining "unit cohesion" (see MOVE PHASE RULES below).
The large red semi-circle on the top of the screen will turn green if unit cohesion between the selectable models is established.
Only the "move phase" is implemented. Rudimentary shooting is lumped into this phase.

MOVE PHASE RULES:
Each model can only travel a set distance. 
Models cannot pass through each other.
Additionally, models may not be moved within 1" (one tile size) of an enemy model.
Models that are part of a unit must maintain "unit cohesion." That is, they must end their move phase within 2" of another member of their unit.


CURRENTLY IMPLEMENTED:
Move phase
Rudimentary shooting 

FUTURE WORK:
Psychic Phase
Shooting Phase
Charge Phase
Fight Phase
Morale Phase
