import requests
import json
import datetime
from random import choice


'''

{"ok":true,
"result":[{"update_id":357677881,
	"message":{
		"message_id":1,
		"from":{"id":218074276,"first_name":"Luiz","last_name":"Rodrigo","username":"AntLouiz"},
		"chat":{
			"id":218074276,
			"first_name":"Luiz",
			"last_name":"Rodrigo",
			"username":"AntLouiz",
			"type":"private"
		 },
		"date":1487621844,
		"text":"/start",
		"entities":[{"type":"bot_command","offset":0,"length":6}]
		}
},

'''


class Bot():
	"""A class to represent a Bot on telegram"""

	def __init__(self, name, token):
		self.name = name
		self.token = token
		self.url = "https://api.telegram.org/bot{}/".format(self.token)
		self.commands = ['/play','/today','hello']

	def get_url(self, url = None, offset=None):
		'''
		 	Make a request on a given url and return a json with the data.
		'''

		params = {'offset':offset, 'timeout':100} # set the offset(update_id) and timeout to 20s
	
		if url:
			response = requests.get(url,data=params) 
		else:
			response = requests.get(self.url)

		data = response.content.decode("utf8") # decode the response to utf8

		return json.loads(data)

	def get_updates(self, offset = None):
		'''
			Get all updates(messages) on the chat.
		'''

		url = self.url+"getUpdates"
		data = self.get_url(url, offset)

		return data

	def get_last_update(self, offset = None):
		'''
			Get the last update on the chat
		'''

		updates = self.get_updates(offset)

		if updates['result']:
			id_last_update = len(updates['result']) -1 # catch the last id on the updates
			last_update = updates['result'][id_last_update] # catch the number of last update
		else:
			return updates['result']

		return last_update

	def send_message(self, message, chat_id):
		'''
			Send a message to a given chat id 
		'''

		url = self.url + 'sendMessage?text={}&chat_id={}/inlineKeyboardButton?text=choose'.format(message, chat_id) # send the message on the url
		self.get_url(url) # make the request to the url with message


	def make_command(self, command, chat_id, update_id):
		'''
			Command the bot with a given command.
		'''

		if command == '/play':
			bot.play(chat_id, update_id)

		if command == '/today':
			bot.today(chat_id)

		if command == 'hello':
			bot.send_message('hi :D', chat_id)


	def play(self, chat_id, update_id):
		'''
			Play Rock-Paper-Scissors with a bot on telegram.
		'''

		options = ['rock','paper','scissors']

		self.send_message("Let's play Rock-Paper-Scissors! Make your move", chat_id)

		while True:
			winner = 0
			last_update = self.get_last_update(update_id) # catch the last person message

			person_move = last_update['message']['text']

			if person_move in options:  # if the message in options
				bot_move = choice(options) # the bot will make a move
				self.send_message(bot_move, chat_id) # and send to telegram

				if person_move == bot_move: # if the person move is equal to the bot move
					self.send_message('Draw! Let\'s try again.', chat_id) # a draw message will be raised
					return 0 # and continue the loop

				if (person_move.lower() == 'rock' and bot_move.lower() == 'paper') or (person_move.lower() == 'paper' and bot_move.lower() == 'rock'):
					if person_move.lower() == 'paper':
						winner = 1
					break
				if (person_move.lower() == 'rock' and bot_move.lower() == 'scissors') or (person_move.lower() == 'scissors' and bot_move.lower() == 'rock'):
					if person_move.lower() == 'rock':
						winner = 1
					break
				else:
					if person_move.lower() == 'scissors':
						winner = 1
					break
			elif person_move != '/play' and person_move not in options:
				self.send_message('You don\'t inserted rock, paper or scissors.', chat_id) # and send to telegram
				return 0

		if winner:
			bot.send_message('You win... --\'', chat_id)
		else:
			bot.send_message('I win! :D', chat_id)

	def today(self, chat_id):
		days = [
			'monday',
			'tuesday',
			'wednesday',
			'thurday',
			'friday',
			'sarturday',
			'sunday'
		]

		today = datetime.date.today()

		message = 'Today ' + today.strftime('%d/%m/%y')

		message += ' is {}.'.format(days[today.weekday()])

		bot.send_message(message, chat_id)


bot = Bot('antlouizlabsbot','352811189:AAFf4qilRrCixf7vGTHb2MfY12fpsFBOOFM')

def main():


	print("Executing the {}.".format(bot.name))

	last_update = bot.get_last_update()
	last_update_id = None

	while True:
		last_update = bot.get_last_update(last_update_id)

		if last_update:
			if not last_update_id:
				last_update_id = last_update['update_id']

			message = last_update['message']['text']
			chat_id = last_update['message']['chat']['id']

			if message.lower() in bot.commands:
				bot.make_command(message, chat_id, last_update_id)
				last_update_id += 1
			else:
				last_update_id += 1

if __name__ == '__main__':
	main()
else:
	exit()