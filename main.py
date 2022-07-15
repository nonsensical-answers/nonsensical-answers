from transformers import pipeline, set_seed
from dotenv import load_dotenv
import rustrict
import disnake
import random
import os

generator = pipeline("text-generation", model="gpt2")

load_dotenv()

reaction_failed_message = "😐"
reaction_inappropriate_message = "🤬"

class BotClient(disnake.Client):
	async def on_ready(self):
		print(f"Logged in as {self.user} (ID: {self.user.id})")

		for guild in self.guilds:
			print("Server name:", guild.name)
		
		await self.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening, name="the inevitable confusion"))

		print("Waiting for questions...")

	async def on_message(self, message):
		if message.author.id == self.user.id:
			return

		if message.content.lower().endswith("?") or message.content.lower().startswith("why ") or message.content.lower().startswith("does ") or message.content.lower().startswith("when ") or message.content.lower().startswith("can ") or message.content.lower().startswith("will ") or message.content.lower().startswith("who ") or message.content.lower().startswith("have ") or message.content.lower().startswith("how ") or message.content.lower().startswith("what ") or message.content.lower().endswith("when"):
			line = "=" * 50
			print(f"{line}\n{message.author} ({message.guild.name}, #{message.channel.name}): \"{message.content}\"\n{line}")

			if "general" in message.channel.name.lower():
				await message.reply("I noticed that the channel you asked that question in contains the text \"general\".\nUnfortunately, I can't answer questions in the general channel.\n**If you are asking me a question, please send it in a different channel.**")
				return
			
			gpt2_seed = random.randint(0, 999999999)
			gpt2_max_length = 100

			print("GPT2 seed:", gpt2_seed)

			set_seed(gpt2_seed)

			author_name = message.author.name
			question_text = message.content

			prompt = f"Answer {author_name}'s Question: \"{question_text}\""

			try:
				await message.channel.trigger_typing()
			except:
				print("The bot does not have permission to send messages in this channel.")
				return

			output = generator(prompt, max_length=gpt2_max_length, num_return_sequences=1)[0]["generated_text"].replace(prompt, "").strip()

			if output == "":
				await message.add_reaction(reaction_failed_message)
				return
			elif "god" in output.lower() or "http://" in output.lower() or "https://" in output.lower():
				line = "-" * 50
				print(f"{line}\n{output}\n{line}")
				
				await message.add_reaction(reaction_failed_message)
				return
			else:
				line = "-" * 50
				print(f"{line}\n{output}\n{line}")

				if rustrict.is_inappropriate(output):
					await message.add_reaction(reaction_inappropriate_message)
					return
				
				await message.reply(output)
				return

intents = disnake.Intents.default()
intents.message_content = True

client = BotClient(intents=intents)
client.run(os.environ["BOT_TOKEN"])