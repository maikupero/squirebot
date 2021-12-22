import discord
import random
import requests
import asyncio

from dota import heroes, pools, teams
from mytoken import mytoken, maps_api

client = discord.Client()

# Google python decorators
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # google coroutines you noob
    if message.content.lower().startswith('sb.'):
        ctx = (message.content)[3:]
        print(f"Attempting to handle '{ctx}' command from {message.author}")

        ### ONE LINERS ###
        if ctx.startswith("hello") or ctx.startswith("hey"):
            await message.channel.send(f"Hey {str(message.author)[:-5]}! How are ya?")
        if ctx.startswith("go"):
            await message.channel.send("No")
        if ctx.startswith("yo") or ctx.startswith("hola"):
            await message.channel.send("sup")
        if ctx.startswith("sup"):
            await message.channel.send("chillin', u?")

        ### LIL ONES ###
        if ctx.startswith('attend'):
            await sb_attend(message)
        if ctx.startswith("help"):
            await sb_help(message)
        if ctx.strip() == ("dota"):
            await dota_help(message)
        if ctx.startswith("randomciv") or message.content[3:].startswith("aoe") or message.content[3:].startswith("civ"):
            await randomciv(message)

        ### BIG ONES ###
        if ctx.startswith("dota") and len(ctx.split(" ")) > 1:
            await dota(message, ctx[5:])

        if ctx.startswith("weather"):
            if len(ctx.split(' ')) > 1:
                await weather(message, ctx[8:])
            else:
                await message.channel.send("City, zip code, or coordinates to the thousandth-place precision if you're a nerd.")
                def check(msg):
                    return msg.author == message.author and msg.channel == message.channel
                try:
                    location = await client.wait_for("message", check=check, timeout=30) # 30 seconds to reply
                    await weather(message, location.content)
                except asyncio.TimeoutError:
                    await message.channel.send("I'm so sorry sir, :man_bowing: I have too many other things to take care of I really must get going but do not hesitate to call again I'm so sorry, milord.")
                except Exception as e:
                    print(e)
    
    # if message.content.startswith(sb.game):
    #     @client.command()
    #     async def command(ctx):
    #         computer = random.randint(1, 10)
    #         await ctx.send('Guess my number')

    #         def check(msg):
    #             return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    #         msg = await client.wait_for("message", check=check)

    #         if int(msg.content) == computer:
    #             await ctx.send("Correct")
    #         else:
    #             await ctx.send(f"Nope it was {computer}")

### LIL ONES ###
async def sb_help(message):
    tags = []
    msg = message.content.split(' ')
    if len(msg) > 1: 
        for tag in range(1, len(msg)):
            if msg[tag].startswith("<"):
                tags.append(msg[tag])
        to_send = ("Someone help ")
        for user in range(len(tags)):
            if user == 0:
                to_send += tags[user]
            else: 
                to_send += (f" and {tags[user]}")
        to_send += "!"
        await message.channel.send(to_send)
    else:
        await message.channel.send(f"I'm here to help, {message.author.name}, sir, if it please you!\n")
    header = ":man_bowing::man_bowing::man_bowing: Command list: `sb.(commandgoeshere)` :man_bowing::man_bowing::man_bowing:"
    hr = "________________________________________"
    help = "`help` (Very wise, sir, figuring this one out already)."
    greet = "`(various greetings)` :wave:"
    attend = "`attend` What does my lord require?"
    weather = "`weather` :white_sun_cloud:"
    dota = f"`dota` {discord.utils.get(message.guild.emojis, name='omni')}"
    aoe = f"`randomciv`/`aoe`/`civ` {discord.utils.get(message.guild.emojis, name='hre')}"
    await message.channel.send(f"{header}\n{hr}\n{help}\n{greet}\n{attend}\n{weather}\n{dota}\n{aoe}")
    
async def sb_attend(message):
    num = random.randint(1,7)
    response = str()
    if num == 1:
        response = "Ready, sir."
    if num == 2:
        response = "As you order, sir."
    if num == 3:
        response = "What can I do for you?"
    if num == 4:
        response = "Work work."
    if num == 5:
        response = "Something need doing?"
    if num == 6:
        response = "How can I help you, sir?"
    if num == 7:
        response = "How can I be of service, my lord?"
    if num == 8:
        response = "$peon"
    await message.channel.send(response)

async def dota_help(message):
    await message.channel.send("Dota sucks. Use `sb.dota (command)`.")
    hr = "________________________________________"
    random = "`random (category)` If no category specified, random hero. Can specify role, attribute, or hero pool."
    pool = "`pool (user)` List of pools. Or list of heroes/pools from specified user/pool."
    team = "`team (team title)` List of teams. Or list of heroes in specified team."
    append = "`append` For adding in heroes/roles/pools."
    await message.channel.send(f"{hr}\n{random}\n{pool}\n{append}")

async def randomciv(message):
    civ_id = random.randint(1,8)
    civ = str()
    if civ_id == 1:
        civ = "The Abbasid Dynasty"
        emoji_name = "abbasid"
    if civ_id == 2:
        civ = "The Chinese"
        emoji_name = "chinese"
    if civ_id == 3:
        civ = "The Delhi Sultanate"
        emoji_name = "delhi"
    if civ_id == 4:
        civ = "The French"
        emoji_name = "french"
    if civ_id == 5:
        civ = "The English"
        emoji_name = "english"
    if civ_id == 6:
        civ = "The Holy Roman Empire"
        emoji_name = "hre"
    if civ_id == 7:
        civ = "The Mongols"
        emoji_name = "mongols"
    if civ_id == 8:
        civ = "The Rus Civilization"
        emoji_name = "rus"

    flag = discord.utils.get(message.guild.emojis, name=emoji_name)
    await message.channel.send(f'{flag} {flag} {flag} {civ} {flag} {flag} {flag}')

### BIG ONES ###
async def dota(message, ctx):
    message.channel.send(f"Handling request: {ctx} from {message.author}")
    if ctx.startswith("random"):
        if ctx == "random":
            num = random.randint(0,(len(heroes)-1))
            await message.channel.send(heroes[num])
        else:
            ctx = ctx[7:]
            if ctx.startswith("str"):
                str_heroes = []
                for hero in heroes:
                    if hero['attribute'].startswith("str"):
                        str_heroes.append(hero['hero'])
                num = random.randint(0,(len(str_heroes)-1))
                result = str_heroes[num]
            if ctx.startswith("agi"):
                agi_heroes = []
                for hero in heroes:
                    if hero['attribute'].startswith("agi"):
                        str_heroes.append(hero['hero'])
                num = random.randint(0,(len(agi_heroes)-1))
                result = agi_heroes[num]
            if ctx.startswith("int"):
                int_heroes = []
                for hero in heroes:
                    if hero['attribute'].startswith("int"):
                        int_heroes.append(hero['hero'])
                num = random.randint(0,(len(agi_heroes)-1))
                result = int_heroes[num]
            if ctx == "core":
                cores = []
                for hero in heroes:
                    if 1 in hero['role'] or 2 in hero['role'] or 3 in hero['role']:
                        cores.append(hero['hero'])
                num = random.randint(0,(len(cores)-1))
                result = cores[num]
            if ctx == "1" or ctx == "carry":
                role1 = []
                for hero in heroes:
                    if 1 in hero['role']:
                        role1.append(hero['hero'])
                num = random.randint(0,(len(role1)-1))
                result = role1[num]
            if ctx == "2" or ctx == "mid":
                role2 = []
                for hero in heroes:
                    if 2 in hero['role']:
                        role2.append(hero['hero'])
                num = random.randint(0,(len(role2)-1))
                result = role2[num]
            if ctx == "3" or ctx == "offlane":
                role3 = []
                for hero in heroes:
                    if 3 in hero['role']:
                        role3.append(hero['hero'])
                num = random.randint(0,(len(role3)-1))
                result = role3[num]
            if ctx == "4" or ctx == "5" or ctx == "support":
                supports = []
                for hero in heroes:
                    if 4 in hero['role'] or 5 in hero['role']:
                        supports.append(hero['hero'])
                num = random.randint(0,(len(supports)-1))
                result = supports[num]
            await message.channel.send(result)
    if ctx.startswith("pool"):
        print('pool')
    if ctx.startswith("team"):
        print('team')
    if ctx.startswith("append"):
        if ctx == "append":
            await message.channel.send("Specify what you'd like to add/edit! Try `sb.dota pool` or `sb.dota team` to see lists.")
        else:
            ctx = ctx[7:]
            if ctx.startswith("hero"):
                sb_prompts = ["Hero name?", "Roles, one at a time please.", "Hero's primary attribute", "Do you hate them?"]
                await message.channel.send(sb_prompts[0])
                def check(msg):
                    return msg.author == message.author and msg.channel == message.channel
                try:
                    location = await client.wait_for("message", check=check, timeout=30) # 30 seconds to reply
                    await weather(message, location.content)
                except asyncio.TimeoutError:
                    await message.channel.send("I'm so sorry sir, :man_bowing: I have too many other things to take care of I really must get going but do not hesitate to call again I'm so sorry, milord.")
            if ctx.startswith("team"):
                await message.channel.send("Team function not ready")
            if ctx.startswith("pool"):
                await message.channel.send("Pool function not ready.")

async def weather(message, location):
    api_key = maps_api
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    city_name = location
    measure = "&units=imperial"

    # Complete url address, converted for your convenience.
    if len(city_name.replace(" ", "").split(',')) == 2:
        coords = city_name.replace(" ", "").split(',')
        complete_url = base_url + "lat=" + coords[0] + "&lon=" + coords[1] + "&appid=" + api_key + measure
    else:
        try:
            int(city_name)
            complete_url = base_url + "zip=" + str(city_name) + "&appid=" + api_key + measure
        except:
            complete_url = base_url + "q=" + city_name + "&appid=" + api_key + measure

    # Get method of requests module
    response = requests.get(complete_url)
    print(f"Looking up request {response} for location {city_name}.")
    x = response.json()
    
    if x['cod'] == 401:
        print("Provided API Key didn't work.")
    elif x['cod'] == 404:
        print("City Not Found.")
    elif x['cod'] == 429:
        print("Too many calls for your free plan.")
    elif x['cod'] == 200:
        main = x['main']
        current_temperature = main['temp']
        celsius = int((current_temperature - 32) * .5556)
        current_humidity = main['humidity']
        weather_description = x['weather'][0]['description']
        if "rain" in weather_description:
            weather_emoji = ":cloud_rain:"
        elif "cloud" in weather_description:
            weather_emoji = ":white_sun_cloud:"
        elif "clear" in weather_description:
            weather_emoji = ":sunny:"
        elif "snow" in weather_description or "sleet" in weather_description: 
            weather_emoji = ":cloud_snow:"
        elif "storm" in weather_description or "thunder" in weather_description:
            weather_emoji = ":thunder_cloud_rain:"
        elif "tornado" in weather_description:
            weather_emoji = ":cloud_tornado:"
        else:
            weather_emoji = ":fire:"
        await message.channel.send(f":man_bowing: Current temperature in {(x['name']).capitalize()} is {celsius}°C / {int(current_temperature)}°F. :man_bowing:")
        await message.channel.send(f"{weather_emoji} {weather_description.capitalize()} {weather_emoji} and {current_humidity} humidity. If it please you, sir. :man_bowing:")
        print("Weather success.")
    else:
        print("Some other error... check: https://openweathermap.org/faq#error401")


def main(): 
    client.run(mytoken)

if __name__ == '__main__':
    main()