import discord
import logging
from random import randint
import datetime


class HoloPearl(discord.Client):
	def __init__(self):
		super().__init__()
		self.bot_token = "NTQwOTc5ODgxMzgzODIxMzIy.DzZFsQ.J8JGiave6VHPw8SReimxnHi3ORg"
		self._logger = logging.getLogger()
		self._logger.addHandler(logging.StreamHandler())
		self._logger.setLevel("DEBUG")

	def run(self):
		super().run(self.bot_token)

	async def on_ready(self):
		print(f"Logged in as {self.user.name}:{self.user.id}")
		print("The bot is ready!")
		print("------")

	def process_bang_command(self, message: discord.Message) -> str:
		try:
			command_word = message.content.split(' ')[0]

			if command_word == '!help':
				message_to_send = "This is a help message."

			elif command_word == '!suggestion':
				with open('suggestions.txt', 'a+') as suggestions:
					suggestions.write(f"{message.author} suggested: {message.content.lstrip('!suggestion')}\n")
				message_to_send = "Thanks! I've logged your suggestion."

			elif command_word =='!japan':
				future = datetime.date(year=2019, month=3, day=31)
				today = datetime.date.today()
				diff = future - today
				message_to_send = f"{diff.days} days until Japan!"

			elif command_word == '!challenge':
				options = [
					"Do you wish to engage in combat?",
					"You've already made a mistake by challenging me!",
					"Commencing duel.", "Training mode initiated. Level 1. Begin!",
					"Parry! Parry! Thrust!",
					"You've drawn your sword in vain!"
				]
				message_to_send = options[randint(0, len(options) - 1)]
			else:
				message_to_send = f"Sorry, \"{command_word}\" is not a recognized command. Try `!help` for a list of available commands."
		except IndexError as e:
			pass

		except ValueError as e:
			pass

		finally:
			return message_to_send

	async def on_message(self, message):
		if message.author == self.user:
			return

		if message.content.startswith('!'):
			message_to_send = self.process_bang_command(message)
			await message.channel.send(message_to_send)
			self._logger.debug(f"Processed command: {message.content}; sent message \"{message_to_send}\"")


if __name__ == "__main__":
	client = HoloPearl()
	client.run()
