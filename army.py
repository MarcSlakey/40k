class Army(object):
	"""docstring for Army"""
	def __init__(self):
		self.squads = []

	def add_squad(self, squad):
		self.squads.append(squad)

	def squads_alive(self):
		return [squad for squad in self.squads if squad.alive()]

	def alive(self):
		return len(self.squads_alive()) != 0