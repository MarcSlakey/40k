This is a repository for various versions of the 40k sim.

TEXT-BASED 40K SHOOTING SIMULATOR

BASIC CONCEPTS:

This simulator creates two armies defined in the body of "shooting_sim.py" and has them take turns shooting at one another until all of one army's models are dead. There is no movement.

To run the text-based simulator, run "python shooting_sim.py" in command line.
Pressing "Enter" at any screen of the sim will make the program proceed to the next screen/step.

Army hierarchy follows tabletop 40k naming conventions: Army-->Units(squads)-->Models(individuals)

The sim will always start with an army report for both armies that displays each unit in each of the two armies, the models in each unit, and their total wounds (health). This screen is repeated at the start of each turn.
The basic turn screen shows a breakdown of each model's shooting attacks for a given turn. 

There are no "morale" losses implemented yet, so outcomes involving low morale units are not reflective of tabletop outcomes.


OPTIONS AND ARMY EDITING":

Editing the options/armies requires adding/subtracting code from "shooting_sim.py".

Armies are defined in the main() function of the "shooting_sim.py" file. 
The name of the armies can be edited there; for example: army1 = Army('Black Templars')

To add units to an army, copy-paste this just under the similar lines in main(): 
	armyX.add_unit(Unit('ABC')) 

The X in armyX is either 1 or 2. This determines which army the unit is going to be added to.
'ABC' is the desired unit(squad) name (this is arbitrary).

Then, copy-paste this into the main() function:
	for i in range(Z):
		model = create_model_by_name('ABC')
		model.add_weapon(create_ranged_weapon_by_name('ABC'))
		armyX.units[Y].add_model(model)

The X in armyX again is either 1 or 2.
The Y in units[Y] is the index of ab item in the list of units; this determines which unit the model will be added to.
For example, if you add another unit to the default 'Black Templars' army just after the 'Crusader Unit(1)', this line would be: 
	army1.units[1].add_model(model)
The Z is the number of models of that given type you want to add to the unit.
'ABC' is NOT arbitrary here; in both cases it is a reference to a specific model or weapon in the Excel file 40k_sim_workbook.xlsx.
Find the model/weapon you want in the Excel file, and use its exact name in this script.


MISCELLANEOUS NOTES:

Models technically shoot one by one, and damage is allocated in order of model creation in the program (that is, models that are initialized first in an army take damage first). For example, in the default Ork army, the "Flash Gitz" will not take damage until all of the "Ork Boyz" are dead. 
This can be used to create realistic target priorities. The main weakness of this structure is that specialized weapons suffer from not being able to pick optimal targets, but as long as the armies are relatively small or homogeneous the outcomes should be reflective of tabletop outcomes. 

A copy of this sim could be used to sim a single small fight phase blob, but would lose accuracy with too many models due to the complex melee targetting rules.

