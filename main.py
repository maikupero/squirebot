import os
import sql_db
import asyncio

import discord
from discord.ext.commands import Bot as DiscordBot

import helpers
from lists import greetings, conversation

# Env variables
MYTOKEN = os.environ.get('mytoken')
MAPS_API = os.environ.get('maps_api')
# Network & Database connections through psycopg2, postgres, heroku. 
DATABASE_URL = os.environ['DATABASE_URL']

# Initialize bot, intents, and bot prefix.
intents = discord.Intents.default()
bot = DiscordBot(
    command_prefix=["sb.","Sb.","SB.","squirebot."],
    case_insensitive=True,
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# Figure out how to get flexible commands for greetings
@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    # https://stackoverflow.com/questions/62076257/discord-py-bot-event
    await bot.process_commands(ctx)

    if ctx.content.startswith('sb.'):
        print(f"Attempting to handle '{ctx.content[3:]}' command from {ctx.author}")

@bot.command(aliases=greetings)
async def greetings(ctx):
    print(f"Responding to {ctx.content[3:]} with {conversation[ctx.content[3:]]}")
    await ctx.send(conversation[ctx.content[3:]])

### LIL ONES ###
@bot.command()
async def help(ctx, *, arg=None):
    await ctx.send(helpers.service.help(ctx, arg))

@bot.command()
async def attend(ctx):
    await ctx.send(helpers.service.attend())

@bot.command()
async def aoe(ctx, *args):
    if args:
        if args[0] == 'randomciv' or args[0] == 'random':
            await ctx.send(helpers.aoe4.randomciv(ctx))
        else:
            await ctx.send(f'Other AOE commands not ready yet.')
    else:
        await ctx.send(helpers.aoe4.randomciv(ctx))

@bot.command()
async def guess(ctx):
    await helpers.games.guess(ctx, bot)
    
### BIG ONES ###
@bot.command()
async def dota(ctx, *, arg=None):
    if arg == None:
        await ctx.send(helpers.dota.dota_help())
    else:
        conn = sql_db.connect(DATABASE_URL)
        print(f"Handling request: {arg} from {ctx.author} on connection {conn}")
        if arg.startswith("random"):
            await ctx.send(helpers.dota.randomdop(ctx, arg, conn))
        else:
            await helpers.dota.dota_db(ctx, arg, conn)
        conn.close()

@bot.command()     
async def weather(ctx, *, arg=None):
    if arg == None:
        await ctx.send("City, zip code, or coordinates to the thousandth-place precision if you're a nerd.")
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        try:
            location = await bot.wait_for("message", check=check, timeout=30) # 30 seconds to reply
            await helpers.service.weather(ctx, location.content, MAPS_API)
        except asyncio.TimeoutError:
            await ctx.send("I'm so sorry sir, :man_bowing: I have too many other things to take care of I really must get going but do not hesitate to call again I'm so sorry, milord.")
    else:
        await helpers.service.weather(ctx, arg, MAPS_API)

if __name__ == "__main__":
    bot.run(MYTOKEN)