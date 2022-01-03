import os
import sql_db
import asyncio

import discord
from discord.ext.commands import Bot as DiscordBot

import helpers

# Env variables. # Network & Database connections through psycopg2, postgres, heroku. 
MYTOKEN = os.environ.get('mytoken')
MAPS_TOKEN = os.environ.get('maps_api')
DB = os.environ['DATABASE_URL']

# Initialize bot, intents, and bot prefix, disable default help command.
intents = discord.Intents.default()
bot = DiscordBot(
    command_prefix=["sb.","Sb.","SB.","squirebot."],
    case_insensitive=True,
    intents=intents,
    help_command=None,
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
        if ctx.content[3:] not in sql_db.commands():
            await helpers.service.new_conversation(ctx, bot)

### LIL ONES ###
@bot.command(aliases=(sql_db.greetings()))
async def greet(ctx):
    greeting = ctx.content[3:]
    print(f"Check the greeting: {greeting} to make sure we're getting the right string")
    await ctx.send(sql_db.responses(greeting))

@bot.command()
async def help(ctx, *, arg=None):
    await ctx.send(helpers.service.help(ctx, arg))

@bot.command()
async def attend(ctx):
    await ctx.send(helpers.service.attend())

@bot.command(aliases=["randomciv"])
async def aoe(ctx, *args):   
    await ctx.send(helpers.aoe4.randomciv(ctx))

@bot.command()
async def guess(ctx):
    await helpers.games.guess(ctx, bot)
    
### BIG ONES ###
@bot.command(aliases=["dop", "doto", "dotes"])
async def dota(ctx, *, arg=None):
    if arg == None:
        await ctx.send(helpers.dota.dota_help())
    else:
        conn = sql_db.connect(DB)
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
            await helpers.service.weather(ctx, location.content, MAPS_TOKEN)
        except asyncio.TimeoutError:
            await ctx.send("I'm so sorry sir, :man_bowing: I have too many other things to take care of I really must get going but do not hesitate to call again I'm so sorry, milord.")
    else:
        await helpers.service.weather(ctx, arg, MAPS_TOKEN)

if __name__ == "__main__":
    sql_db.create_conversation_table()
    sql_db.create_command_table()
    bot.run(MYTOKEN)
