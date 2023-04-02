import random
import json


class Property:
	def __init__(self, id, name, price, rent, group, housecost):
		self.id = id
		self.name = name
		self.price = price
		self.owner = None
		self.buildings = 0
		self.rent = rent
		self.group = group
		self.househost = househost


	def set_owner(self, owner):
		self.owner = owner
	



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


class Chance:
	def __init__(self, action, amount):
		self.action = action
		self.amount = amount

class Chest:
	def __init__(self, action, amount):
		pass	

class Game:
	def __init__(self):
		streets = []
		with open('src/monopoly.json') as f:
			game_data = json.loads(f.read()).items()
			for key, value in game_data['properties']:
				street = Street(value[)
			
			
			
	
