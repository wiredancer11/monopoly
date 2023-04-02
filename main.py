import random


class Property:
	def __init__(self, id, name, price, rent, group):
		self.id = id
		self.name = name
		self.price = price
		self.owner = None
		self.buildings = 0
		self.rent = rent
		self.group = group


	def set_owner(self, owner):
		self.owner = owner
	


class Bank:
	pass

class Player:
	def __init__(self):
		self.properties = []
		self.inJail = False
		self.money = 1500
		self.position = 0
	
	def buy_property(property):
		self.properties.append(property)
		self.money -= property.price
		property.set_owner(self)

class Game:
	pass
