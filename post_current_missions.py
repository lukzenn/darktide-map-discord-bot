# Posts current missions to Dorktide, then closes
# To be run every 30 minutes via CronJob

import discord
from dotenv import load_dotenv
import os
import mission_manager

intents = discord.Intents.default()
client = discord.Client(intents=intents)

dorkTideMapChannelId = 1124526082566131753


# when bot online
@client.event
async def on_ready():
    message = mission_manager.get_current_missions()
    print('Posting auto-message')
    await client.get_channel(dorkTideMapChannelId).send(message)
    await client.close()


load_dotenv()
client.run(os.getenv('TOKEN'))
