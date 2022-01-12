import os
import sql_db
import asyncio

import discord
from discord.ext.commands import Bot as DiscordBot

from lists import heroes
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
    help_command=None)



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

    if message.content.startswith('sb.'):
        checkingfirst = message.content[3:].split(' ')
        firstword = checkingfirst[0]
        if firstword in sql_db.fetch_all_commands() or message.content[3:].capitalize() in heroes:
            return
        else:
            greeting = message.content[3:53].replace(",", "")
            print(f"Attempting to handle '{greeting}' command from {message.author}")
            if greeting in sql_db.fetch_all_greetings():
                await message.channel.send(str(sql_db.response(greeting))[2:-2])
            else:
                await helpers.DBSTUFF.new_conversation(message, bot, greeting)



### Database Stuff ###
@bot.command()
async def greetings(ctx):
    await ctx.send(f"Current list of greetings: {str(sql_db.fetch_all_greetings())[1:-1]}")
@bot.command()
async def commands(ctx):
    await ctx.send(f"Current list of commands: {str(sql_db.fetch_all_commands())[1:-1]}")
@bot.command()
async def tables(ctx):
    await ctx.send(f"Tables in the database: {str(sql_db.fetch_tables())[1:-1]}")
@bot.command()
async def deletefrom(ctx, *, arg=None):
    await helpers.DBSTUFF.deletefrom(bot, ctx, arg)



### LIL ONES ###
@bot.command()
async def help(ctx, *, arg=None):
    await ctx.send(helpers.SERVICE.help(ctx, arg))

@bot.command()
async def attend(ctx):
    await ctx.send(helpers.SERVICE.attend())

@bot.command(aliases=["randomciv"])
async def aoe(ctx, *, arg=None):
    await helpers.AOE4.randomciv(ctx, arg)

@bot.command()
async def guess(ctx):
    await helpers.GAMES.guess(ctx, bot)
    


### BIG ONES ###
@bot.command(aliases=["dop", "doto", "dotes"])
async def dota(ctx, *, arg=None):
    if arg == None:
        await ctx.send(helpers.DOTA.dota_help())
    else:
        conn = sql_db.connect(DB)
        print(f"Handling request: {arg} from {ctx.author} on connection {conn}")
        if arg.startswith("random"):
            await ctx.send(helpers.DOTA.randomdop(ctx, arg))
        else:
            await helpers.DOTA.dota_db(ctx, arg, conn)
        conn.close()
@bot.command(aliases=heroes)
async def heroinfo(ctx):
    await ctx.send(f"Looking up {ctx.message.content[3:].capitalize()}...")

@bot.command()     
async def weather(ctx, *, arg=None):
    if arg == None:
        await ctx.send("City, zip code, or coordinates to the thousandth-place precision if you're a nerd.")
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        try:
            location = await bot.wait_for("message", check=check, timeout=30) # 30 seconds to reply
            await helpers.SERVICE.weather(ctx, location.content, MAPS_TOKEN)
        except asyncio.TimeoutError:
            await ctx.send("I'm so sorry sir, :man_bowing: I have too many other things to take care of I really must get going but do not hesitate to call again I'm so sorry, milord.")
    else:
        await helpers.SERVICE.weather(ctx, arg, MAPS_TOKEN)

if __name__ == "__main__":
    sql_db.create_conversation_table()
    sql_db.create_command_table()
    sql_db.create_dota_tables()
    bot.run(MYTOKEN)
