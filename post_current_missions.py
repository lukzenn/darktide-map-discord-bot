# Posts current missions to Dorktide, then closes
# To be run every 30 minutes via CronJob

import discord
from dotenv import load_dotenv
import os
import mission_manager

intents = discord.Intents.default()
client = discord.Client(intents=intents)

#TODO: A command for server admins to add their own channels to this list (stored in SQLite)
dorkTideMapChannelId = 1124526082566131753
karkersMapChannelId = 1117124786238279760


# when bot online
@client.event
async def on_ready():
    print('Signed in. Posting auto-message.')
    await client.get_channel(dorkTideMapChannelId).send(message)
    await client.get_channel(karkersMapChannelId).send(message)
    await client.close()
    quit()

message = mission_manager.get_current_missions()
if not message:
    print('no tough missions on the board. aborting auto-post.')
    quit()
else:
    load_dotenv()
    client.run(os.getenv('TOKEN'))
