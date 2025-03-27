import discord
from discord.ext import commands

import python_weather

### --- --- --- ###

description = "A bot that tells the weather"
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix='/',
    description=description,
    intents=intents
)

### --- --- --- ###

# Default config
LOCATION = "Chicago, IL"
UNIT = "Imperial" # CURRENTLY CANNOT CHANGE -> TBD
LOCALE = 'ENGLISH'

### --- --- --- ###

# Events
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print("-------")

### --- --- --- ###

# Commands
# Displays settings
@bot.tree.command(name = "settings", description = "View weather settings")
async def settings(interaction):
    await interaction.response.send_message("**Settings:**"
             f"\n```Location: {LOCATION}"
             f"\nUnits: {UNIT}"
             f"\nLocale: {LOCALE.capitalize()}```")

# Changes location
@bot.tree.command(name = "setlocation", description = "Sets the location of the weather")
async def setlocation(interaction, location: str):
    global LOCATION
    LOCATION = location
    await interaction.response.send_message(f"**Changed location to:** {LOCATION}")

@bot.tree.command(name = "temp", description = "Shows the current temperature")
async def temp(interaction):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(LOCATION)
    await interaction.response.send_message(f"{weather.temperature}F in {LOCATION}")

### --- --- --- ###

# Running the bot
with open('token', 'r') as file:
    token = file.readline().strip()
bot.run(token)