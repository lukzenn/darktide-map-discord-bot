import os
from dotenv import load_dotenv
from base_logger import logger

import discord
from discord import app_commands
from discord.ext import tasks

import mission_manager

# Setup
load_dotenv()
token = os.getenv("TOKEN")


DORKTIDE_MAP_CHANNEL = 1124526082566131753

guilds = []
guilds.append(discord.Object(id=1050951439524044840)) #dorktide
guilds.append(discord.Object(id=589400038120357888)) #LEWDS
guilds.append(discord.Object(id=1075774178344583229)) #kark


class DarktideMapBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        logger.info('Syncing command trees...')
        for guild in guilds:
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        logger.info('Command trees synced')


intents = discord.Intents.default()
client = DarktideMapBot(intents=intents)

@client.tree.command(description = 'Ping the darktide map bot')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Pong!')

@client.tree.command(description = 'Shows any tough Damnation missions on the board right now')
async def tough_right_now(ctx):
    logger.info(f'Current missions requested')
    message = mission_manager.get_current_missions()
    if not message:
        await ctx.response.send_message('No tough missions on the board right now')
    else:
        await ctx.response.send_message(message)


@client.tree.command(description = 'Shows any tough Damnation missions from the last 24 hours')
async def tough_and_recent(ctx,hours_ago:int=24):
    logger.info(f'Missions from last {hours_ago}h requested')
    message = mission_manager.get_recent_missions(hours_ago*3600)
    if not message:
        await ctx.response.send_message('No tough missions found')
    else:
        await ctx.response.send_message(message)



@client.event
async def on_ready():
    logger.info(f"We've logged in as {client.user}")
    #myloop.start()


# TODO Use this loop to do send auto-posts instead of cronjob?
@tasks.loop(seconds=10)
async def myloop():
    channel = client.get_channel(DORKTIDE_MAP_CHANNEL)
    print('Looping!')

# RUN
client.run(token)
