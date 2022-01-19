import random
import discord
import requests
import sql_db
import asyncio

from lists import nvm, heroes, full_hero_list, stre, agil, inte, role1, role2, role3, role4, role5, supps, cores, jungle

class CHECKS:
    def check_same_user(ctx,msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

class DBSTUFF:
    async def new_conversation(message, bot, greeting):
        creator_id = message.author.id
        await message.channel.send(f"Oh, '{greeting}'. What should I say? No comma's please! (nvm, cancel, etc. to cancel)")
        def check(msg):
            return msg.author == message.author and msg.channel == message.channel
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            response = str(msg.content)
            if response.lower() in nvm:
                await message.channel.send("No problemo.")
                return
            else:
                sql_db.append_conversation_table(greeting, response, creator_id)
                await message.channel.send(f"Got it! Storing greeting '{greeting}' with response '{response}'.")
        except asyncio.TimeoutError:
            await message.channel.send("I'm so sorry sir, :man_bowing: I have too many other things to take care of I really must get going but do not hesitate to call again I'm so sorry, milord.")

    async def deletefrom(bot, ctx, arg):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        master_id = ctx.guild.owner_id
        user_id = ctx.author.id

        if arg in ["greetings","conversation"]:
            await ctx.send(f"Specify item (or comma separated list of items) from:\n{str(sql_db.fetch_all_greetings())[1:-1]}")
            try:
                msg = await bot.wait_for("message", check=check, timeout=30)
                for word in msg.content.split(","):
                    if sql_db.delete_greeting(word.strip(), user_id, master_id) == 1:
                        await ctx.send(f"Deleted: {word.strip()}")
                    else:
                        await ctx.send(f"{word.strip()} is not yours to delete!")
            except asyncio.TimeoutError:
                await ctx.send("Sorry, try again from `sb.deletefrom (table)`.")
        else:   
            await ctx.send("Try `sb.deletefrom greetings` or `sb.deletefrom commands`")
    
class SERVICE:
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
        attend = "`attend` What does my lord require?"
        guess = "`guess` Game with your boi."
        weather = "`weather` :white_sun_cloud:"
        dbstuff = "`sb.greetings` Lists all stored phrases. sb.deletefrom greetings to remove ones you made."
        dota = f"`dota` {discord.utils.get(ctx.guild.emojis, name='omni')}"
        aoe = f"`randomciv`/`aoe`/`civ` {discord.utils.get(ctx.guild.emojis, name='hre')}"
        return f"{tag}\n{header}\n{hr}\n{help}\n{attend}\n{guess}\n{weather}\n{dbstuff}\n{dota}\n{aoe}"

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
            


class AOE4:
    async def randomciv(ctx, arg):
        if arg:
            if int(arg) > 0 and int(arg) < 9:
                civcount = int(arg)
        else: 
            civcount = 1
        for i in range(civcount):
            num = random.randint(0,7)
            civs = ["The Abbasid Dynasty","The Chinese","The Delhi Sultanate","The French","The English","The Holy Roman Empire","The Mongols","The Rus Civilization"]
            flags = ["abbasid","chinese","delhi","french","english","hre","mongols","rus"]
            civ = civs[num]
            flag = discord.utils.get(ctx.guild.emojis, name=flags[num])
            await ctx.send(f'{flag} {flag} {flag} {civ} {flag} {flag} {flag}')

class DOTA:
    def dota_help():
        top = "Dota sucks. Use `sb.dota (command)`."
        hr = "___________________Command List_____________________"
        random = "random () : If unspecified suggests a random hero to play. Otherwise, can specify team or pool.\n// `sb.dota random core` • `sb.dota random 3` • `sb.dota random team` //"
        hero = "hero_name : Gives all stored info on provided hero. If two words, use abbreviation.\n// `sb.dota hero earthshaker` //"
        append = "append () : Begins dialogue towards adding a new pool to the DB.\n// `sb.dota append` //"
        return (f"{top}\n{hr}\n```{random}\n{hero}\n{append}```")

    def randomdop(ctx, pool):
        if len(pool.strip()) > 6:
            pool = pool[7:]
        if pool == "RANDOM":
            return random.choice(full_hero_list)     
        elif pool.startswith("STR"):
            return random.choice(stre)
        elif pool.startswith("AGI"):
            return random.choice(agil)
        elif pool.startswith("INT"):
            return random.choice(inte)
        elif pool == "CORE":
            return random.choice(cores)
        elif pool == "1" or pool == "CARRY":
            return random.choice(role1)
        elif pool == "2":
            return random.choice(role2)
        elif pool == "3":
            return random.choice(role3)
        elif pool.startswith("SUP") or pool == "4" or pool == "5":
            return random.choice(supps)
        elif pool.startswith("JUNG"):
            return random.choice(jungle)
        elif pool == "TEAM":
            return DOTA.generate_team()
        
    def generate_team():
        new_team = []
        seed = random.randint(1,2)
        if seed == 1:
            core_count = random.sample(cores, k=random.randint(1,2))
            support_count = random.sample(supps, k=random.randint(1,3))
            remaining_random = 5 - len(core_count) - len(support_count)

            new_team.extend(core_count)
            for i in range(remaining_random):
                pub = random.choice(heroes)
                while pub in core_count or pub in support_count: pub = random.choice(full_hero_list)
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
    
    async def dota_db(ctx, bot, arg):
        user_id = str(ctx.author.id)
        arg = arg.upper()

        if arg.startswith("RANDOM"):
            await ctx.send(DOTA.randomdop(ctx, arg))

        elif arg.startswith('POOL'):
            if len(arg) > 5:
                arg = arg[5:].strip()
                if arg == 'LIST':
                    await ctx.send(f"Here are all the pools we have stored, sir (Case Insensitive):\n{sql_db.get_all_pools()}.")
                elif arg in sql_db.get_users() or arg == "ME":
                    if arg == "ME":
                        await ctx.send(f"Your stored pools: {str(sql_db.get_users_pools(user_id))}")
                else:
                    await ctx.send(f"{arg.title()} heroes: {sql_db.select_heroes_from_pool(arg.title())}.")
            else:
                await ctx.send(f"`sb.dota pool list/poolname` for all the pools, or `sb.dota pool (poolname)` to look it up.")

        elif arg.startswith('NEW'):
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            
            async def add_heroes(ctx, pool_id, poolname):
                await ctx.send(f"Give me a hero to add to the pool, or a comma separated list of heroes (abbreviations like kotl are ok).")
                addmore = True
                while addmore:
                    try:
                        msg = await bot.wait_for("message", check=check)
                        if msg.content in nvm:
                            await ctx.send("Gotcha. All done!")
                            addmore = False
                            return
                        heroes_to_add = msg.content.upper().split(',')
                        heroes_to_add = [sql_db.findhero(hero.strip()) for hero in heroes_to_add]
                        for hero in heroes_to_add:
                            if hero == "ERROR":
                                raise Exception
                            elif hero in sql_db.select_heroes_from_pool(poolname):
                                raise Exception
                            else:
                                await ctx.send(f"Adding {hero} to {poolname}.")
                                sql_db.execute_query(sql_db.append_hero_pools_query, (pool_id, (sql_db.get_hero_id(hero))))
                        await ctx.send("Any more to add?")
                    except:
                        await ctx.send("Duplicate or typo, try again..")
                
            if len(arg) > 4:
                arg = arg[4:].strip()
                print(f"Trying to handle dota new {arg}")
                if arg not in ['STRENGTH','AGILITY','INTELLIGENCE','POOL','HERO']:
                    print("in here now")
                    try:
                        await add_heroes(ctx, sql_db.get_pool_id(arg.title()), arg.title())
                    except:
                        ctx.send("Double check pool name.")

                elif arg == 'POOL':
                    await ctx.send(f"What shall we call your pool?")
                    try:
                        msg = await bot.wait_for("message", check=check)
                        poolname = msg.content.title()
                        pools = [pool.strip() for pool in sql_db.get_all_pools().split(',')]
                        print(f"poolname: {poolname}, stored pools: {pools}")
                        if poolname in pools:
                            await ctx.send("A pool with that name already exists!")
                            return
                        else:
                            await ctx.send(f"Adding pool {poolname} to the database")
                            sql_db.execute_query(sql_db.append_user_pools_query, (poolname, str(ctx.author.id)))
                            await add_heroes(ctx, sql_db.get_pool_id(poolname), poolname)
                    except:
                        await ctx.send("Some issue with the pool name.")

                elif arg == 'hero':
                    await ctx.send("No need to add new heroes as there are no new heroes yet. Message gaben.")
                    
            else: 
                await ctx.send("Specify what you'd like to add / add to! Try `sb.dota new pool` to make a new one.")

        elif arg in heroes:
            await ctx.send(f"Looking up {heroes[arg]}...")
        
        else:
            await ctx.send("Sorry, try again with some new dota request.")
       
class GAMES:
    async def guess(ctx, bot):
        num = random.randint(1, 10)
        await ctx.send('Guess a number 1-10')
        
        def guess_check(msg):
            return CHECKS.check_same_user(ctx, msg) and int(msg.content) in range(1, 11)
        msg = await bot.wait_for("message", check=guess_check)
    
        if int(msg.content) == num:
            await ctx.send("Correct")
        else:
            await ctx.send(f"Nope it was {num}")
