"""Unit module

"""

import random

class Unit(object):

	"""
	
	Unit objects are stored in a list in Army objects.

	Attributes:
		name (str): unit's name, used solely for output 
		units (Model): list of this unit's Model-class objects

	"""
	
	def __init__(self, name=''):
		"""The constructor for Unit class

		Parameters:
			name (str): unit'ss name, used solely for output 
			units (Unit): list of this unit's Model objects
		"""
		self.name = name
		self.models = []

	def __str__(self):
		pass

	def add_model(self, model):
		"""Adds a Model-class object to the unit's list of models"""
		self.models.append(model)

	def save_against_wound(self, weapon):
		"""Summary."""
		if not self.alive():
			return

		#Wounds models in load order (models loaded first will die first)
		self.models_alive()[0].model_save_against_wound(weapon)

	def models_alive(self):
		"""Returns the number of models alive in the unit"""
		return [model for model in self.models if model.alive()]

	def alive(self):
		"""Returns true as long as at least one model is alive in the given unit."""
		return len(self.models_alive()) != 0