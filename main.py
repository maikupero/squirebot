import os
import sql_db
import random
import asyncio

from discord.ext import commands

import helpers
from lists import random_responses, conversation

# Env variables
MYTOKEN = os.environ.get('mytoken')
MAPS_API = os.environ.get('maps_api')
# Network & Database connections through psycopg2, postgres, heroku. 
DATABASE_URL = os.environ['DATABASE_URL']

bot = commands.Bot(command_prefix='sb.')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

async def on_message(ctx):
    if ctx.author == bot.user:
        return
    # https://stackoverflow.com/questions/62076257/discord-py-bot-event
    await bot.process_commands(ctx)

    if ctx.content.startswith('sb.'):
        msg = ctx.content[3:]
        print(f"Attempting to handle '{msg}' command from {ctx.author}")
        if msg in conversation:
            await ctx.send(conversation[msg])
        else:
            response = random.randint(1,len(random_responses))
            await ctx.send(random_responses[response])

### LIL ONES ###
@bot.command()
async def help(ctx, *args):
    # To test: tagging no one, tagging someone else. 
    await ctx.send(helpers.service.help(ctx, *args))

@bot.command()
async def attend(ctx):
    #To Test: if this gets random response from all the responses in the list.
    await ctx.send(helpers.service.attend())

@bot.command()
async def aoe(ctx, *args):
    #To test: civ and flag are being sent correctly using external helper function.
    if args[0] == 'randomciv' or args[0] == 'random':
        await ctx.send(helpers.aoe4.randomciv(ctx))
    else:
        await ctx.send(f'Other AOE commands not ready yet.')

@bot.command()
async def guess(ctx):
    # To test: if this check works for user and for range.
    await helpers.games.guess(ctx, bot)
    
### BIG ONES ###
@bot.command()
async def dota(ctx, *, arg=None):
    if arg == None:
        await ctx.send(helpers.dota.dota_help)
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
        try:
            location = await bot.wait_for("message", check=helpers.checks.check_same_user, timeout=30) # 30 seconds to reply
            await weather(ctx, location.content)
        except asyncio.TimeoutError:
            await ctx.send("I'm so sorry sir, :man_bowing: I have too many other things to take care of I really must get going but do not hesitate to call again I'm so sorry, milord.")
    else:
        await helpers.services.weather(ctx, arg, MAPS_API)



def main(): 
    bot.run(MYTOKEN)

if __name__ == '__main__':
    main()  