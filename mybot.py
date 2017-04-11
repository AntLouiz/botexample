import requests
import json
from random import choice

class Bot():
	"""A class to represent a Bot on telegram"""

	def __init__(self, name, token):
		self.name = name
		self.token = token
		self.url = "https://api.telegram.org/bot{}/".format(self.token)
		self.commands = ['/play','hello']

	def get_url(self, url = None, offset=None):
		'''
		 	Make a request on a given url and return a json with the data.
		'''

		params = {'offset':offset} # set the offset(update_id) and timeout to 20s

		if url:
			response = requests.get(url, data=params)
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

		if command == 'hello':
			bot.send_message('hi :D', chat_id)


	def play(self, chat_id, update_id):
		'''
			Play Rock-Paper-Scissors with a bot on telegram.
		'''

		options = ['rock','paper','scissors']
		winner = {
			0: 'Draw !',
			1: 'I win :D',
			2: 'You win... '
		}

		self.send_message("Let's play Rock-Paper-Scissors! Make your move", chat_id)
		update_id += 1

		while True:
			last_update = self.get_last_update(update_id) # catch the last person message

			if last_update:
				person_move = last_update['message']['text']

				if person_move in options:  # if the message in options
					bot_move = choice(options) # the bot will make a move
					self.send_message(bot_move, chat_id) # and send to telegram

					person_index = options.index(person_move)
					bot_index = options.index(bot_move)

					result = (bot_index - person_index - 3) % 3

					self.send_message(winner[result], chat_id)
					break

				else:
					self.send_message("Please insert rock, paper or scissors.", chat_id)
					update_id += 1


bot = Bot('antlouizlabsbot', '352811189:AAFf4qilRrCixf7vGTHb2MfY12fpsFBOOFM')
