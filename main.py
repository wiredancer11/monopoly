import random
import json
import time

JAIL_POSITION = 11
FREE_PARKING_POSITION = 21
GO_TO_JAIL_POSITION = 31
RAILROADS_POSITIONS= [6, 16, 26, 36]
UTILITIES_POSITIONS = [13, 29]

class Card:
	def __init__(self, position, name, id): 
		self.position = position
		self.name = name	
		self.id = id

class Property(Card):
	def __init__(self, position, name, id, price): 
		super().__init__(position, name, id)
		self.price = price
		self.owner = None

	def set_owner(self, owner):
		self.owner = owner


class Street(Property):
	def __init__(self, position, name, id, price, rent, group, housecost):
		super().__init__(position, name, id, price)
		self.buildings = 0
		self.rent = rent
		self.group = group
		self.househost = housecost


class Utility(Property):
	def __init__(self, position, name, id, price):
		super().__init__(position, name, id, price)


class Railroad(Property):
	def __init__(self, position, name, id, price):
		super().__init__(position, name, id, price)

class Special(Card):
	def __init__(self, position, name, id):
		super().__init__(position, name, id)


class Player:
	def __init__(self, name, game):
		self.name = name
		self.game = game
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
		print(f"{self.name} bought {property.name} for {property.price} and has {self.money}$ left")

	def pay_other_player(self, other_player, amount):
		self.money -= amount 
		other_player.money += amount
		print(f"{self.name} paid {other_player.name} {amount}$ and now has {self.money}$ left")

	def go_to_card(self, card):
		print(card)
		self.position = card.position
		self.action(card)

	def throw_dice(self):
		if random.randint(1, 6) == random.randint(1, 6):
			return True
		return False
	
	def cross_start(self):
		self.money += 200
		print(f'{self.name} started a new lap and gets 200$ from the Bank')

	def pay_tax(self, amount):
		self.money -= 200
		print(f'{self.name} paid {amount}$ in taxes')


	def leave_jail(self):
		if self.jail_free:
			self.jail_free = False
			self.in_jail = False 
			print(f'{self.name} uses Get out of jail card')
		elif self.money >= 50:
			self.money -= 50
			self.in_jail = False
			print(f'{self.name} pays fine and gets out of jail')
		else:
			if self.throw_dice():
				self.in_jail = False
				print(f'{self.name} gets lucky and gets out of jail')

	def action(self, card, dice_value=None):
		card_type = type(card).__name__
		if type(card).__bases__[0].__name__ == 'Property':
			if card.owner is None:
				if self.money >= card.price:
					self.buy_property(card)
				else:
					print(f"{self.name} can't afford {card.name}")
			else:
				if type(card).__name__ == 'Utility':
					if len(card.owner.utilities) == 1:
						rent = self.game.dice_value * 4
					else:
						rent = self.game.dice_value * 10
				elif type(card).__name__== 'Railroad':
					rent = len(card.owner.railroads) * 25
				else:
					rent = card.rent
				self.pay_other_player(card.owner, rent) 
		
		elif card_type == 'Special':
			id = card.id
			if id == 'incometax':
				self.pay_tax(200)
			elif id == 'jail':
				if self.in_jail:
					self.leave_jail()
				else:
					print(f'{self.name} is just visiting the jail')
			elif id == 'chance' or id == 'communitychest':
				effect = random.choice(game.chance_cards + game.chests)
				self.get_effect(effect)
			elif id == 'freeparking':
				print(f'{self.name} is resting in a free parking')
			elif id == 'gotojail':
				self.position == 11
				self.in_jail = True
			elif id == 'luxurytax':
				self.pay_tax(100)
				
	def get_effect(self, card):
		print(self.name + ': ' + card.title)
		if card.action == 'move':
			id = card.tileid
			new_card = self.game.get_card_by_id(id)
			self.go_to_card(new_card)
		
		elif card.action == 'addfunds':
			self.money += card.amount
		elif card.action == 'addfundsfromplayers':
			for player in self.game.players:
				player.money -= card.amount
				self.money += card.amount
		elif card.action == 'jail':
			if card.subaction == 'goto':
				self.in_jail = True
				self.position = JAIL_POSITION
			elif card.subaction == 'getout':
				self.jail_free = True
		elif card.action == 'removefunds':
			self.money -= card.amount
		elif card.action == 'removefundstoplayers':
			for player in self.game.players:
				player.money += card.amount
				self.money -= card.amount
		elif card.action == 'removefunds':
			self.money -= card.amount
		elif card.action == 'movenearest':
			nearest_distance = 100
			nearest_card = None
			if card.groupid == 'utility':
				positions = UTILITIES_POSITIONS
			elif card.groupid == 'railroad':
				positions = RAILROADS_POSITIONS
			for card_position in positions:
				distance = abs(self.position - card_position)
				if distance < nearest_distance:
					nearest_distance = distance
					nearest_card = self.game.cards[card_position]
			self.go_to_card(nearest_card)







class Chance:
	def __init__(self, title, action, **kwargs):
		self.title = title
		self.action = action
		self.subaction = kwargs['subaction']
		self.tileid = kwargs['tileid']
		self.groupid = kwargs['groupid']
		self.amount = kwargs['amount']
		self.buildings = kwargs['buildings']
		self.hotels = kwargs['hotels']


class Chest:
	def __init__(self, title, action, **kwargs):
		self.title = title
		self.action = action
		self.subaction = kwargs['subaction']
		self.tileid = kwargs['tileid']
		self.amount = kwargs['amount']
		self.buildings = kwargs['buildings']
		self.hotels = kwargs['hotels']


class Game:
	def __init__(self):
		self.streets = []
		self.railroads = []
		self.utilities = []
		self.special = []
		self.chance_cards = []
		self.chests = []
		self.cards = []
		self.players = []
		self.is_finished = False
		self.dice_value = None
		with open('src/monopoly.json') as f:
			game_data = json.loads(f.read())
			properties = game_data['properties']
			for card in properties:
				if card['group'].lower() == 'railroad':
					self.railroads.append(Railroad(card['position'], card['name'], card['id'], card['price']))
				elif card['group'].lower() == 'utilities':
					self.utilities.append(Utility(card['position'], card['name'], card['id'],card['price']))
				elif card['group'].lower() == 'special':
					self.special.append(Special(card['position'], card['name'], card['id']))
				else:
					street = Street(card['position'], card['name'], card['id'], card['price'] ,card['rent'] ,card['group'] ,card['housecost'])
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

	def play(self):
		self.players = [Player('Player 1', game), Player('Player 2', game)]
		turn = 0
		while not self.is_finished:
			current_player = self.players[turn]
			self.dice_value = random.randint(1, 12)
			new_position = (current_player.position + self.dice_value - 1) % 40  
			print(new_position)
			current_card = self.cards[new_position] 
			current_player.go_to_card(current_card)
			turn  = (turn + 1) % 2
			if current_player.money < 0:
				self.declare_winner(self.players[turn])

	def declare_winner(self, player):
		self.is_finished = True
		print(f'Game over. {player.name} is victorious!')

	
	def get_card_by_id(self, id):
		for card in self.cards:
			if card.id == id:
				return card



game = Game()
game.play()





