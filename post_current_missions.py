# Posts current missions to Dorktide, then closes
# To be run every 30 minutes via CronJob

import discord
from dotenv import load_dotenv
import os
import mission_manager

from base_logger import logger

intents = discord.Intents.default()
client = discord.Client(intents=intents)

#TODO: A command for server admins to add their own channels to this list (stored in SQLite)

subscribed_channel_list = []
subscribed_channel_list.append(1124526082566131753) #dorktide
subscribed_channel_list.append(1117124786238279760) #karks
subscribed_channel_list.append(1128840198768296008) #jsat

# when bot online
@client.event
async def on_ready():
    logger.info('Signed in. Posting auto-message.')
    for channel_id in subscribed_channel_list:
        await client.get_channel(channel_id).send(message)
    logger.info('Messages sent. Closing client.')
    await client.close()
    quit()

message = mission_manager.get_current_missions()
if not message:
    logger.info('no tough missions on the board. aborting auto-post.')
    quit()
else:
    load_dotenv()
    client.run(os.getenv('TOKEN'))
