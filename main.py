# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os

import discord
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv

import mission_manager

load_dotenv()
token = os.getenv("TOKEN")
DORKTIDE_MAP_CHANNEL = 1124526082566131753
DORKTIDE_GUILD = discord.Object(id=1050951439524044840)
LEWDS_GUILD = discord.Object(id=589400038120357888)

class DarktideMapBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        print('Syncing command trees...')
        self.tree.copy_global_to(guild=DORKTIDE_GUILD)
        await self.tree.sync(guild=DORKTIDE_GUILD)
        self.tree.copy_global_to(guild=LEWDS_GUILD)
        await self.tree.sync(guild=LEWDS_GUILD)
        print('Command trees synced')


intents = discord.Intents.default()
client = DarktideMapBot(intents=intents)


@client.tree.command(description = 'Ping the darktide map bot')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Pong!')

@client.tree.command(description = 'Shows any tough Damnation missions on the board right now')
async def tough_right_now(ctx):
    print(f'Current missions requested')
    mission_manager.update_missions()
    message = ''
    missions = mission_manager.get_current_missions()
    for mission in missions:
        message = message + '\n' + mission_manager.format_mission_for_discord(mission)
    await ctx.response.send_message(message)
    print(f'responded with {len(missions)} current missions')

@client.tree.command(description = 'Shows any tough Damnation missions from the last 24 hours')
async def tough_right_now(ctx):
    print(f'Missions from last 24h requested')
    mission_manager.update_missions()
    message = ''
    missions = mission_manager.get_recent_missions(3600*24)
    for mission in missions:
        message = message + '\n' + mission_manager.format_mission_for_discord(mission)
    await ctx.response.send_message(message)
    print(f'responded with {len(missions)} missions')


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    #myloop.start()


@tasks.loop(seconds=10)
async def myloop():
    channel = client.get_channel(DORKTIDE_MAP_CHANNEL)
    print('Looping!')


client.run(token)
