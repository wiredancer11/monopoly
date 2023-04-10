import random
import json

class Card:
	def __init__(self, position, name): 
		self.position = position
		self.name = name	

class Property(Card):
	def __init__(self, position, name, price): 
		super().__init__(position, name)
		self.price = price
		self.owner = None

	def set_owner(self, owner):
		self.owner = owner


class Street(Property):
	def __init__(self, position, name, price, rent, group, housecost):
		super().__init__(position, name, price)
		self.buildings = 0
		self.rent = rent
		self.group = group
		self.househost = housecost


class Utility(Property):
	def __init__(self, position, name, price):
		super().__init__(position, name, price)


class Railroad(Property):
	def __init__(self, position, name, price):
		super().__init__(position, name, price)

class Special(Card):
	def __init__(self, position, name):
		super().__init__(position, name)


class Player:
	def __init__(self, name):
		self.name = name
		self.streets = []
		self.railroads = []
		self.utilities = []
		self.in_jail = False
		self.jail_free = False
		self.money = 1500
		self.position = 0
		self.in_jail = False

	def buy_property(self, property):
		if type(property).__name__ == 'Street':
			self.streets.append(property)
		elif type(property).__name__ == 'Utility':
			self.utilities.append(property)
		elif type(property).__name__ == 'Railroad':
			self.railroads.append(property)
		self.money -= property.price
		property.set_owner(self)

	def action(self, card):
		pass



class Chance:
	def __init__(self, title, action, **kwargs):
		self.title = title
		self.action = action

class Chest:
	def __init__(self, title, action, **kwargs):
		self.title = title
		self.action = action
class Game:
	def __init__(self):
		self.streets = []
		self.railroads = []
		self.utilities = []
		self.special = []
		self.chance_cards = []
		self.chests = []
		self.cards = []
		self.is_finished = False
		with open('src/monopoly.json') as f:
			game_data = json.loads(f.read())
			properties = game_data['properties']
			for card in properties:
				if card['group'].lower() == 'railroad':
					self.railroads.append(Railroad(card['position'], card['name'], card['price']))
				elif card['group'].lower() == 'utilities':
					self.utilities.append(Utility(card['position'], card['name'], card['price']))
				elif card['group'].lower() == 'special':
					self.special.append(Special(card['position'], card['name']))
				else:
					street = Street(card['position'], card['name'], card['price'] ,card['rent'] ,card['group'] ,card['housecost'])
					self.streets.append(street)
			self.cards = self.railroads + self.utilities + self.streets + self.special
			self.cards.sort(key=lambda x: x.position)

			for card in game_data['chance']:
				chance = Chance(
				card['title'],
				card['action'],
				subaction = card.get('subaction'),
				tileid = card.get('tileid'),
				groupid = card.get('groupid'),
				amount = card.get('amount'),
				buildings = card.get('buildings'),
				hotels = card.get('hotels'),
				rentmultiplier = card.get('rentmultiplier'))

				self.chance_cards.append(chance)


			for card in game_data['communitychest']:
				chest = Chest(
				card['title'],
				card['action'],
				subaction = card.get('subaction'),
				tileid = card.get('tileid'),
				amount = card.get('amount'),
				buildings = card.get('buildings'),
				hotels = card.get('hotels'))
				self.chests.append(chest)

		def play():
			players = [Player('Player 1'), Player('Player 2')]
			turn = 0
			while not self.is_finished:
				current_player = players[turn]
				cube_value = random.randint(1, 12)
				current_player.position += cube_value
				current_card = self.cards[current_player.position] 
				current_player.action(current_card)


game = Game()






