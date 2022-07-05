from transformers import pipeline, set_seed
from dotenv import load_dotenv
import disnake
import random
import os

generator = pipeline("text-generation", model="gpt2")

load_dotenv()

class BotClient(disnake.Client):
	async def on_ready(self):
		print(f"Logged in as {self.user} (ID: {self.user.id})")

	async def on_message(self, message):
		if message.author.id == self.user.id:
			return

		if message.content.startswith("how ") or message.content.startswith("what "):
			set_seed(random.randint(0, 999999999))

			author_name = message.author.name
			question_text = message.content

			prompt = f"Answer {author_name}'s Question: \"{question_text}\""

			output = generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"].replace(prompt, "")

			await message.reply(output)
			return
		
		print(message.author, message.content)

client = BotClient()
client.run(os.environ["BOT_TOKEN"])