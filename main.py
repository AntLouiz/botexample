from mybot import bot

def main():

	print("Executing the {}.".format(bot.name))
	last_update_id = None

	while True:
		last_update = bot.get_last_update(last_update_id)

		if last_update:
			if not last_update_id:
				last_update_id = last_update['update_id']
				chat_id = last_update['message']['chat']['id']
			try:
				message = last_update['message']['text']

				if message.lower() in bot.commands:
					bot.make_command(message, chat_id, last_update_id)
					last_update_id += 1
				else:
					last_update_id += 1

			except KeyError:
				bot.send_message("Please just insert messages. :D", chat_id)
				last_update_id += 1

if __name__ == '__main__':
	main()
else:
	exit()
