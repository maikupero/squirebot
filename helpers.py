import random
import discord
import requests
import sql_db
import asyncio

from lists import heroes, stre, agil, inte, role1, role2, role3, role4, role5, supps, cores, jungle
#CAPITALIZE CLASS NAMES PEP STYLE GUIDES

class checks:
    def check_same_user(ctx,msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

class service:
    async def new_conversation(ctx, bot):
        greeting = ctx.content[3:]
        await ctx.send(f"Oh! I don't know '{greeting}' yet. How should I respond?")
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            response = str(msg.content)
            sql_db.append_command_table(greeting)
            sql_db.append_conversation_table(greeting, response)
        except asyncio.TimeoutError:
            await ctx.send("I'm so sorry sir, :man_bowing: I have too many other things to take care of I really must get going but do not hesitate to call again I'm so sorry, milord.")

    def attend():
        responses = ["Ready, sir.", "As you order, sir.", "What can I do for you?", "Work work.", 
        "Something need doing?", "How can I help you, sir?", "How can I be of service, my lord?"]
        return random.choice(responses)

    def help(ctx, *args):
        if args[0]:
            tag = f"I'm here to help {args[0]}, sir, if it please you!"
        else:
            tag = f"I'm here to help, {ctx.author.name}, sir, if it please you!"
        header = ":man_bowing::man_bowing::man_bowing: Command list: `sb.(commandgoeshere)` :man_bowing::man_bowing::man_bowing:"
        hr = "________________________________________"
        help = "`help` (Very wise, sir, figuring this one out already)."
        greet = "`(various greetings)` :wave:"
        attend = "`attend` What does my lord require?"
        guess = "`guess` Game with your boi."
        weather = "`weather` :white_sun_cloud:"
        dota = f"`dota` {discord.utils.get(ctx.guild.emojis, name='omni')}"
        aoe = f"`randomciv`/`aoe`/`civ` {discord.utils.get(ctx.guild.emojis, name='hre')}"
        return f"{tag}\n{header}\n{hr}\n{help}\n{greet}\n{attend}\n{guess}\n{weather}\n{dota}\n{aoe}"

    async def weather(ctx, location, api):
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        city_name = location
        measure = "&units=imperial"

        # Complete url address, converted for your convenience.
        if len(city_name.replace(" ", "").split(',')) == 2:
            coords = city_name.replace(" ", "").split(',')
            print(f"CITY NAME HERE: {city_name}, {city_name[0]}, {city_name[1]}")
            complete_url = base_url + "lat=" + coords[0] + "&lon=" + coords[1] + "&appid=" + api + measure
        else:
            try:
                int(city_name)
                complete_url = base_url + "zip=" + str(city_name) + "&appid=" + api + measure
            except:
                complete_url = base_url + "q=" + city_name + "&appid=" + api + measure

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
            elif "mist" in weather_description:
                weather_emoji = ":fog:"
            else:
                weather_emoji = ":fire:"
            await ctx.send(f":man_bowing: Current temperature in {(x['name']).capitalize()} is {celsius}°C / {int(current_temperature)}°F. :man_bowing:")
            await ctx.send(f"{weather_emoji} {weather_description.capitalize()} {weather_emoji} and {current_humidity} humidity. If it please you, sir. :man_bowing:")
            print("Weather success.")
        else:
            print("Some other error... check: https://openweathermap.org/faq#error401")
            


class aoe4:
    def randomciv(ctx):
        num = random.randint(0,7)
        civs = ["The Abbasid Dynasty","The Chinese","The Delhi Sultanate","The French","The English","The Holy Roman Empire","The Mongols","The Rus Civilization"]
        flags = ["abbasid","chinese","delhi","french","english","hre","mongols","rus"]
        civ = civs[num]
        flag = discord.utils.get(ctx.guild.emojis, name=flags[num])
        return f'{flag} {flag} {flag} {civ} {flag} {flag} {flag}'

class dota:
    def dota_help():
        top = "Dota sucks. Use `sb.dota (command)`."
        hr = "___________________Command List_____________________"
        random = "random () : If unspecified suggests a random hero to play.\n Otherwise, can specify team, attribute, role, pool, theme.\n // `sb.dota random core` • `sb.dota random 3` • `sb.dota random team` //"
        hero = "hero_name : Gives all stored info on provided hero\n // `sb.dota hero earthshaker` //"
        append = "append (): Begins dialogue towards adding a new pool, hero, or hero info to the DB.\n // `sb.dota append` //"
        return (f"{top}\n{hr}\n```{random}\n{hero}\n{append}```")

    def randomdop(ctx, pool, conn):
        if len(pool.strip()) > 6:
            pool = pool[7:]
        if pool == "random":
            return random.choice(heroes)     
        elif pool.startswith("str"):
            return random.choice(stre)
        elif pool.startswith("agi"):
            return random.choice(agil)
        elif pool.startswith("int"):
            return random.choice(inte)
        elif pool == "core":
            return random.choice(cores)
        elif pool == "1" or pool == "carry":
            return random.choice(role1)
        elif pool == "2":
            return random.choice(role2)
        elif pool == "3":
            return random.choice(role3)
        elif pool.startswith("sup") or pool == "4" or pool == "5":
            return random.choice(supps)
        elif pool.startswith("jung"):
            return random.choice(jungle)
        elif pool == "team":
            return dota.generate_team()
        
    def generate_team():
        new_team = []
        seed = random.randint(1,2)
        if seed == 1:
            core_count = random.sample(cores, k=random.randint(1,3))
            support_count = random.sample(supps, k=random.randint(1,2))
            remaining_random = 5 - len(core_count) - len(support_count)

            new_team.extend(core_count)
            for i in range(remaining_random):
                pub = random.choice(heroes)
                while pub in core_count or pub in support_count: pub = random.choice(heroes)
                new_team.append(pub)
            new_team.extend(support_count)
        else:
            print(f"seed {seed}")
            pub = random.choice(role1)
            while pub in new_team: pub = random.choice(role1)
            new_team.append(pub)
            while pub in new_team: pub = random.choice(role2)
            new_team.append(pub)
            while pub in new_team: pub = random.choice(role3)
            new_team.append(pub)
            while pub in new_team: pub = random.choice(role4)
            new_team.append(pub)
            while pub in new_team: pub = random.choice(role5)
            new_team.append(pub)
        
        return " • ".join(new_team)
    
    async def dota_db(ctx, arg, conn):
        cur = conn.cursor()
        if arg.startswith('pool'):
            cmd = arg[5:]
            cur.execute("SELECT * FROM test;")
        elif arg.startswith("team"):
            cmd = arg[5:]
            cur.execute("SELECT * FROM test;")
        elif arg.startswith("append"):
            if arg == "append":
                await ctx.send("Specify what you'd like to add/edit! Try `sb.dota pool (name)` to see lists.")
            else:
                db_command = arg[7:]
                if db_command == "pool":
                    # If table doesn't exist, create it. send a success message.
                    cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
                    # if table does exist, send a failure message.
        cur.close()
       

class games:
    async def guess(ctx, bot):
        num = random.randint(1, 10)
        await ctx.send('Guess a number 1-10')
        
        def guess_check(msg):
            return checks.check_same_user(ctx, msg) and int(msg.content) in range(1, 11)
        msg = await bot.wait_for("message", check=guess_check)
    
        if int(msg.content) == num:
            await ctx.send("Correct")
        else:
            await ctx.send(f"Nope it was {num}")
