
class Army(object):
	"""docstring for Army"""
	def __init__(self, name):
		self.name = name
		self.squads = []

	#Operator overloading: runs this function on print(Army) or str()
	#Ultimately prints the number of squads alive within the army as well as the units alive within each of those squads
	def __str__(self):
		text = "Army has {} squad(s) left\n".format(len(self.squads_alive()))
		for squad in self.squads_alive():
			text += "  {}".format(squad)
		return text

	def add_squad(self, squad):
		self.squads.append(squad)

	#Returns the number of squads in the army with at least one unit alive
	def squads_alive(self):
		return [squad for squad in self.squads if squad.alive()]

	#Returns true if any squads in the army are alive
	def alive(self):
		return len(self.squads_alive()) != 0

