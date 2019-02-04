import discord
import logging
from random import randint
import datetime


class HoloPearl(discord.Client):
	def __init__(self):
		super().__init__()
		self.bot_token = "NTQwOTc5ODgxMzgzODIxMzIy.DzZFsQ.J8JGiave6VHPw8SReimxnHi3ORg"
		self._logger = logging.getLogger('HoloPearl')
		log_handler = logging.StreamHandler()
		log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
		self._logger.addHandler(log_handler)
		self._logger.setLevel("DEBUG")

	def run(self):
		super().run(self.bot_token)

	def store_suggestion(self, suggestion_message: discord.Message) -> bool:
		write_line = f"{suggestion_message.author} suggested: {suggestion_message.content.lstrip('!suggestion')}\n"
		try:
			with open('suggestions.txt', 'a+') as suggestion_file:
				suggestion_file.write(write_line)
		except IOError as e:
			return False

		return True

	def process_bang_command(self, bang_message: discord.Message) -> str:
		try:
			command_word = bang_message.content.split(' ')[0]

			if command_word == '!help':
				message_to_send = "This is a help message."

			elif command_word == '!suggestion':
				if self.store_suggestion(suggestion_message=bang_message):
					message_to_send = "Thanks! I've logged your suggestion."
				else:
					message_to_send = "Sorry! I couldn't log your suggestion."

			elif command_word == '!japan':
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

	async def process_mention(self, mention_message: discord.Message):
		await mention_message.add_reaction("👀")

	async def on_ready(self):
		self._logger.debug(f"Logged in as {self.user.name}:{self.user.id}")
		self._logger.info(f"{self.user.name} is ready!")

	async def on_message(self, message):
		if message.author == self.user:
			return

		if message.content.startswith('!'):
			message_to_send = self.process_bang_command(message)
			await message.channel.send(message_to_send)
			self._logger.debug(f"Processed command: {message.content}; sent message \"{message_to_send}\"")

		elif self.user in message.mentions:
			await self.process_mention(mention_message=message)
			self._logger.debug(f"Reacted to message: {message.content}")


if __name__ == "__main__":
	client = HoloPearl()
	client.run()
