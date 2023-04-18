import random
import json
import pygame
import time

JAIL_POSITION = 10
FREE_PARKING_POSITION = 20
GO_TO_JAIL_POSITION = 30
RAILROADS_POSITIONS= [5, 15, 25, 35]
UTILITIES_POSITIONS = [12, 28]
COLORS = {'red': (237, 27, 36), 'brown': (149, 84, 54), 'yellow': (254, 242, 0), 'pink': (217, 58, 150), 'orange': (248, 147, 29), 'darkgreen': (31, 178, 90), 'lightblue': (170, 224, 250), 'darkblue': (0, 114, 187)}

class Card:
	def __init__(self, position, name, id):
		self.position = position - 1
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
	def __init__(self, position, name, id, price, rent, group, housecost, multiplied_rent):
		super().__init__(position, name, id, price)
		self.buildings = 0
		self.rent = rent
		self.group = group
		self.househost = housecost
		self.multiplied_rent = multiplied_rent


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
		return f"{self.name} bought {property.name} for {property.price} and has {self.money}$ left"

	def pay_other_player(self, other_player, amount):
		self.money -= amount
		other_player.money += amount
		print(f"{self.name} paid {other_player.name} {amount}$ and now has {self.money}$ left")
		return f"{self.name} paid {other_player.name} {amount}$ and now has {self.money}$ left"

	def go_to_card(self, card):
		self.position = card.position
		return self.action(card)

	def throw_dice(self):
		if random.randint(1, 6) == random.randint(1, 6):
			return True
		return False

	def cross_start(self):
		self.money += 200
		print(f'{self.name} started a new lap and gets 200$ from the Bank')
		return f'{self.name} started a new lap and gets 200$ from the Bank'

	def pay_tax(self, amount):
		self.money -= 200
		print(f'{self.name} paid {amount}$ in taxes')
		return f'{self.name} paid {amount}$ in taxes'


	def leave_jail(self):
		if self.jail_free:
			self.jail_free = False
			self.in_jail = False
			print(f'{self.name} uses Get out of jail card')
			return f'{self.name} uses Get out of jail card'
		elif self.money >= 50:
			self.money -= 50
			self.in_jail = False
			print(f'{self.name} pays fine and gets out of jail')
			return f'{self.name} pays fine and gets out of jail'
		else:
			if self.throw_dice():
				self.in_jail = False
				print(f'{self.name} gets lucky and gets out of jail')
				return f'{self.name} gets lucky and gets out of jail'
		print(f"{self.name} couldn't get out of jail")
		return f"{self.name} couldn't get out of jail"


	def action(self, card, dice_value=None):
		card_type = type(card).__name__
		message = ''
		if type(card).__bases__[0].__name__ == 'Property':
			if card.owner is None:
				if self.money >= card.price:
					return self.buy_property(card)
				else:
					print(f"{self.name} can't afford {card.name}")
					message += f"{self.name} can't afford {card.name}\n"
			elif card.owner is not self:
				if type(card).__name__ == 'Utility':
					if len(card.owner.utilities) == 1:
						rent = self.game.dice_value * 4
					else:
						rent = self.game.dice_value * 10
				elif type(card).__name__== 'Railroad':
					rent = len(card.owner.railroads) * 25
				else:
					if card.buildings > 0:
						rent = card.multiplied_rent[card.buildings - 1]
					else:
						rent = card.rent * (1 + int(card.owner.check_color_monopoly(card.group)))

				message += self.pay_other_player(card.owner, rent) + '\n'
			else:
				print(f"{self.name} has landed on his own card: {card.name}")
				message += f"{self.name} has landed on his own card: {card.name}\n"

				

		elif card_type == 'Special':
			id = card.id
			if id == 'incometax':
				message += self.pay_tax(200) + '\n'
			elif id == 'jail':
				if self.in_jail:
					message += self.leave_jail()+ '\n'
				else:
					print(f'{self.name} is just visiting the jail')
					message += f'{self.name} is just visiting the jail'+ '\n'
			elif id == 'chance' or id == 'communitychest':
				effect = random.choice(game.chance_cards + game.chests)
				message += self.get_effect(effect)+ '\n'
			elif id == 'freeparking':
				print(f'{self.name} is resting in a free parking')
				message += f'{self.name} is resting in a free parking'+ '\n'
			elif id == 'gotojail':
				self.position = JAIL_POSITION
				self.in_jail = True
				print(f'{self.name} commits a crime and goes to jail')
				message += f'{self.name} commits a crime and goes to jail'+ '\n'
			elif id == 'luxurytax':
				message += self.pay_tax(100)+ '\n'
			elif id == 'go':
				print(f"{self.name} has just landed on the go square")
				message += f"{self.name} has just landed on the go square"+ '\n'


		for color in COLORS.keys():
			if self.check_color_monopoly(color):
				potential_house_street = sorted(filter(lambda x: x.group == color, game.streets), key=lambda x: x.buildings)[0]
				if self.money - potential_house_street.househost > 200 and potential_house_street.buildings < 4:
					self.money -= potential_house_street.househost
					potential_house_street.buildings += 1 
					print(f"{self.name} bought a house on {potential_house_street.name}")
					message += f"{self.name} bought a house on {potential_house_street.name}\n"
		return message

	def check_color_monopoly(self, color):
		if set(filter(lambda x: x.group == color, self.streets)) == set(filter(lambda x: x.group == color, game.streets)):
			return True
		return False


	def get_effect(self, card):
		if card.action == 'move':
			id = card.tileid
			new_card = self.game.get_card_by_id(id)
			return card.title + '\n' + self.go_to_card(new_card)

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
		elif card.action == 'propertycharges':
			buildings = 0
			for street in self.streets:
				buildings += street.buildings
			self.money -= buildings * card.buildings
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
			return card.title + '\n' + self.go_to_card(nearest_card)
		print(self.name + ': ' + card.title)
		return self.name + ': ' + card.title







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
		pygame.font.init()
		print(pygame.font.get_fonts())
		self.font = pygame.font.SysFont('Arial', 15)
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
					street = Street(card['position'], card['name'], card['id'], card['price'] ,card['rent'] ,card['group'] ,card['housecost'], card['multipliedrent'])
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

		pygame.init()
		self.screen_w = 1920
		self.screen_h = 1080
		self.screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
		self.screen.fill((255, 255, 255))
		self.field_w = 950
		self.field_h = 950
		self.field_image= pygame.transform.scale(pygame.image.load('src/field.jpg'), (self.field_w, self.field_h))
		self.dice_sides = ['src/dice1.png', 'src/dice2.png', 'src/dice3.png', 'src/dice4.png','src/dice5.png','src/dice6.png']
		self.players_pictures = [pygame.transform.scale(pygame.image.load('src/battleship.png'), (80, 80)),
		pygame.transform.scale(pygame.image.load('src/car.png'), (80, 80))]

	def play(self):
		self.players = [Player('Player 1', game), Player('Player 2', game)]
		self.players[0].buy_property(self.cards[1])
		self.players[0].buy_property(self.cards[3])

		turn = 0
		self.draw_players()
		self.screen.blit(self.field_image, ((self.screen_w - self.field_w) // 2, 10))
		pygame.display.flip()
		#time.sleep(5)
		input()
		while not self.is_finished:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.is_finished = True
			self.screen.fill((255, 255, 255))
			dice1, dice2 = (random.randint(1, 6), random.randint(1, 6))
			self.dice_value = dice1 + dice2

			current_player = self.players[turn]
			message = ''
			if current_player.in_jail:
				new_position = current_player.position
			else:
				new_position = (current_player.position + self.dice_value) % 40
				if current_player.position + self.dice_value > 40:
					current_player.money += 200
					message += f'{current_player.name} crossed the Go tile and gets 200$ from the Bank'
			current_card = self.cards[new_position]
			message = message + '\n' + current_player.go_to_card(current_card)
			turn  = (turn + 1) % 2
			if current_player.money < 0:
				message += self.declare_winner(self.players[turn])
			self.draw_dices(dice1, dice2)
			self.show_stats()
			self.screen.blit(self.field_image, ((self.screen_w - self.field_w) // 2, 10))
			pygame.display.update()
			#time.sleep(2)
			input()
			
			self.field_image= pygame.transform.scale(pygame.image.load('src/field.jpg'), (self.field_w, self.field_h))
			self.draw_dices(dice1, dice2)
			self.draw_players()
			self.show_stats()
			self.show_message(message)
			self.screen.blit(self.field_image, ((self.screen_w - self.field_w) // 2, 10))
			
			pygame.display.flip()
			#time.sleep(5)
			input()


	def declare_winner(self, player):
		self.is_finished = True
		print(f'Game over. {player.name} is victorious!')
		return f'Game over. {player.name} is victorious!'


	def draw_dices(self, dice1, dice2):
		dice_file1, dice_file2 = self.dice_sides[dice1 - 1], self.dice_sides[dice2 - 1]
		dice_image1, dice_image2 = (pygame.transform.scale(pygame.image.load(dice_file1), (50, 50)),
				pygame.transform.scale(pygame.image.load(dice_file2), (50, 50)))
		self.field_image.blit(dice_image1, (460, 700))
		self.field_image.blit(dice_image2, (560, 700))


	def show_message(self, message):
		self.message_box = pygame.Surface((500, 100))	
		self.message_box.fill((220, 220, 220, 0.3))
		messages = message.split('\n')
		next_string_coords_y = 5
		for message in messages:
			self.message_box.blit(self.font.render((message), True, (0, 0, 0)), (5, next_string_coords_y))
			next_string_coords_y += 20
		self.field_image.blit(self.message_box, (180, 600))
	

	def show_stats(self):
		
		for i in range(len(self.players)):
			player = self.players[i]
			stats_player = pygame.Surface((400, 1000))
			stats_player.fill((255, 255, 255))
			stats_player.blit(self.font.render((player.name), True, (0, 0, 0)), (5,5))
			stats_player.blit(self.font.render(('Balance: ' + str(player.money) + '$'), True, (0, 0, 0)), (5, 25))
			if player.in_jail:
				jail_message = 'In jail'
			else:
				jail_message = ''
			stats_player.blit(self.font.render((jail_message), True, (255, 0, 0)), (5,45))
			stats_player.blit(self.font.render(('Posessions'), True, (0, 0, 0)), (5, 65))
			next_string_coords_y = 85
			streets_color_sorted = sorted(player.streets, key=lambda x: x.group)
			for j in range(3):
				property_type_list =[streets_color_sorted, player.railroads, player.utilities][j] 
				property_type_name = ['Streets', 'Railroads', 'Utilities'][j]
				stats_player.blit(self.font.render((property_type_name + ':'), True, (0, 0, 0)), (15, next_string_coords_y))
				next_string_coords_y += 20
				for k in range(len(property_type_list)):
					property = property_type_list[k]
					if property_type_name == 'Streets':
						pygame.draw.rect(stats_player, COLORS.get(property.group), pygame.Rect(5, next_string_coords_y, 10, 10) )
						if property.buildings > 0:
							stats_player.blit(self.font.render((str(property.buildings) + 'H'), True, (0, 0, 0)), (270, next_string_coords_y))
					stats_player.blit(self.font.render((property.name), True, (0, 0, 0)), (25, next_string_coords_y))
					next_string_coords_y += 20
				next_string_coords_y += 20



			self.screen.blit(stats_player, (5 + ( 600 + self.field_w) * i , 5))
			print(5 + ( 400 + self.field_w) * i )


	def draw_players(self):
		tile_w = tile_h = self.field_w * 0.08
		big_tile_w = self.field_h * 0.13
		for i in range(2):
			
			player = self.players[i]
			position = player.position 
			print(position)
			if position // 10 == 0:
				coords_x = self.field_w - big_tile_w  - tile_w * (position  % 10)
				coords_y = 800
			elif position // 10 == 1:
				coords_x = 50
				coords_y = self.field_h - big_tile_w - tile_h * (position   % 10)
			elif position // 10 == 2:
				coords_x = big_tile_w + tile_w * (position   % 10) - 80
				coords_y = 50
			elif position // 10 == 3:
				coords_x = self.field_w - 120
				coords_y = big_tile_w + tile_h * (position % 10) - 80
			self.field_image.blit(self.players_pictures[i], (coords_x, coords_y))




	def get_streets_by_color(self, color):
		streets = []
		for street in self.streets:
			if street.group == color:
				streets.append(street)
		return streets



	def get_card_by_id(self, id):
		for card in self.cards:
			if card.id == id:
				return card



game = Game()
game.play()





