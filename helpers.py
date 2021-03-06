import random
import discord
import requests
import sql_db
import asyncio

from lists import responses, nvm, heroes, full_hero_list, strength, agility, intelligence, role1, role2, role3, role4, role5, supps, cores, jungle



class CHECKS:

    def check_same_user(ctx,msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content[:3].upper() != "SB."


class SERVICE:

    def attend():
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
            await ctx.send(f":man_bowing: Current temperature in {(x['name']).capitalize()} is {celsius}??C / {int(current_temperature)}??F. :man_bowing:")
            await ctx.send(f"{weather_emoji} {weather_description.capitalize()} {weather_emoji} and {current_humidity} humidity. If it please you, sir. :man_bowing:")
            print("Weather success.")
        else:
            print("Some other error... check: https://openweathermap.org/faq#error401")
            




class DBSTUFF:

    async def new_conversation(bot, message, greeting):
        creator_id = message.author.id
        await message.channel.send(f"Oh, '{greeting}'. What should I say? No comma's please! (nvm, cancel, etc. to cancel)")
        def check(msg):
            return CHECKS.check_same_user(message, msg)
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            response = str(msg.content)
            if response.upper() in nvm:
                await message.channel.send("Gotcha, no problemo.")
                return
            else:
                sql_db.append_conversation_table(greeting, response, creator_id)
                await message.channel.send(f"Got it! Storing greeting '{greeting}' with response '{response}'.")
        except asyncio.TimeoutError:
            await message.channel.send("I'm so sorry sir, :man_bowing: I have too many other things to take care of I really must get going but do not hesitate to call again I'm so sorry, milord.")



    async def delete(bot, ctx, arg):
        def check(msg):
            return CHECKS.check_same_user(ctx, msg)
        master_id = ctx.guild.owner_id
        user_id = ctx.author.id


        if arg in ["greetings","conversation"]:
            await ctx.send(f"Specify item (or comma separated list of items) from:\n{str(sql_db.fetch_all_greetings())[1:-1]}")
            try:
                msg = await bot.wait_for("message", check=check, timeout=30)
                response = ''
                for word in msg.content.split(","):
                    if sql_db.delete_greeting(word.strip(), user_id, master_id) == 1:
                        response += f"Deleted: {word.strip()}\n"
                    else:
                        response += f"{word.strip()} is not yours to delete!\n"
                await ctx.send(response)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, try again from `sb.deletefrom (table)`.")


        elif arg.upper() in ["DOTA", "POOL"]:
            await ctx.send(f"Specify poolname to delete a pool if it is yours to delete.\nStored pools: {sql_db.get_all_pools()}")
            try:
                msg = await bot.wait_for("message", check=check, timeout=30)
                if msg.content.upper() in nvm:
                    await ctx.send("Gotcha no problem brother.")
                    return
                msg = msg.content.title().split(",")
                response = ''
                for pool in msg:
                    if sql_db.delete_pool(pool.strip(), user_id, master_id) == 1:
                        response += f"Deleted: {pool.strip()}\n"
                    else:
                        response += f"{pool.strip()} is not yours to delete!\n"
                await ctx.send(response)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, try again from `sb.delete (poolname)`.")
        else:   
            await ctx.send("Try `sb.delete greetings` or `sb.delete pool`")
    




class DOTA:


    def dota_help():
        top = "Dota sucks. Use `sb.dota (command)`."
        random = "> `sb.dota random core` \|\| `sb.dota random 3` \|\| `sb.dota random team`"
        hero = "RANDOM: Random team, hero from specified pool, or hero if unspecified.\n\n> `sb.dota earthshaker`"
        pool = "HERO: Gives all stored info on provided hero.\n\n> `sb.dota pool green` \|\| `sb.dota pool list`"
        score = "POOL: Branches into list (all pools), new (make a new pool), -poolname- (see heroes in pool), edit, delete.\n\n> `sb.dota love/hate (hero)` \|\| `sb.dota win/lose (heroes)` \|\| `sb.dota score (hero)`"
        delete = "SCORE: Keeps track of a totally subjective, meaningless score on all the heroes. Can also do `sb.dota top x` or bottom x to see rankings."
        return (f"{top}\n{random}\n{hero}\n{pool}\n{score}\n{delete}")


    def randomdop(ctx, pool):
        if len(pool.strip()) > 6:
            pool = pool[7:]
        stored_pools = sql_db.fetch_query(sql_db.get_pools_query)
        if pool == "RANDOM":
            return random.choice(full_hero_list)     
        elif pool.startswith("STR"):
            return random.choice(strength)
        elif pool.startswith("AGI"):
            return random.choice(agility)
        elif pool.startswith("INT"):
            return random.choice(intelligence)
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
        elif pool.title() in stored_pools:
            pool_id = sql_db.get_pool_id(pool.title())
            hero_ids = sql_db.fetch_query(sql_db.select_heroes_from_pool_query, (pool_id,))
            heroes_in_pool = [sql_db.get_hero_name(hero_id) for hero_id in hero_ids]
            return str(random.choice(heroes_in_pool))[2:-2]
        else:
            return "Couldn't find what to random from!"
        

    def generate_team():
        new_team = []
        seed = random.randint(1,2)
        print(f"Seed: {seed}")
        if seed == 1:

            core_count = random.sample(cores, k=random.randint(1,2))
            print(f"Got cores: {core_count}.")
            supports_no_dupes = supps.copy()
            print(f"Got supports list: {supports_no_dupes}.")
            for core in core_count:
                if core in supports_no_dupes:
                    supports_no_dupes.remove(core)
                    print(f"Removed {core} from the supports list.")
            print(f"Got no dupes supports list: {supports_no_dupes}.")
            support_count = random.sample(supports_no_dupes, k=random.randint(1,3))
            print(f"Got supports: {support_count}")

            remaining_random = 5 - len(core_count) - len(support_count)

            new_team.extend(core_count)
            new_team.extend(support_count)
            while remaining_random > 0:
                pub = random.choice(full_hero_list)
                if pub in new_team:
                    print(f"{pub} was already in {new_team}.")
                else:
                    print(f"{pub} was not in {new_team}, appending.")
                    new_team.append(pub)
                    remaining_random -= 1
            

        else:
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
        
        return " ??? ".join(new_team)
    

    async def dota_db(ctx, bot, arg):
        user_id = str(ctx.author.id)
        arg = arg.upper()
        def check(msg):
            return CHECKS.check_same_user(ctx,msg)

        async def add_delete_heroes(pool_id, poolname, edit_type):
            await ctx.send(f"Give me a hero to {edit_type.lower()}, or a comma separated list of heroes < 50 please (abbreviations like kotl are ok).")
            repeat = True
            while repeat:
                response = ''
                try:
                    msg = await bot.wait_for("message", check=check)
                    if msg.content.upper() in nvm:
                        await ctx.send("Gotcha. All done!")
                        repeat = False
                        return

                    provided_heroes = msg.content.upper().split(',')
                    print(f"provided heroes list: {provided_heroes}")
                    found_heroes = [sql_db.findhero(hero.strip()) for hero in provided_heroes]
                    print(f"found_heroes list: {found_heroes}")

                    await ctx.send("Attempting to add your heroes...")
                    for index, hero in enumerate(found_heroes):
                        if hero == "ERROR":
                            response += f"Couldn't find {provided_heroes[index]}.\n"
                        
                        elif edit_type == "ADD":
                            if hero in sql_db.select_heroes_from_pool(poolname):
                                response += f"{hero} is already in there.\n"
                            else:
                                response += f"Adding {hero} to {poolname}.\n"
                                sql_db.execute_query(sql_db.append_hero_pools_query, {'pool_id':pool_id, 'hero_id':sql_db.get_hero_id(hero)})

                        elif edit_type == "DELETE":
                            if hero not in sql_db.select_heroes_from_pool(poolname):
                                response += f"{hero} isn't in there to delete.\n"
                            else:
                                response += f"Removing {hero} from {poolname}.\n"
                                sql_db.execute_query(sql_db.delete_hero_from_pool_query, {'pool_id':pool_id, 'hero_id':sql_db.get_hero_id(hero)})
                    
                    await ctx.send(response)
                    await ctx.send(f"Any more to {edit_type.lower()}?")
                except:
                    await ctx.send("Duplicate or typo, try again..")

        async def edit_pool(poolname):
            accepted_edits = ["ADD", "DEL", "DELETE", "DELETE POOL"]
            await ctx.send(f"Heroes in {poolname}:\n{sql_db.select_heroes_from_pool(poolname)}\n Want to Add/Delete heroes? Tell me `add` or `delete`. Or `Delete Pool`.")
            try:
                msg = await bot.wait_for("message", check=check)
                if msg.content.upper().strip() in nvm:
                    await ctx.send("Gotcha no problem brother.")
                    return
                if msg.content.upper().strip() in accepted_edits:
                    edit_type = msg.content.upper().strip()
                    if edit_type == "DELETE POOL":
                        await delete_pool(poolname)
                    else:
                        if edit_type == "ADD":
                            await add_delete_heroes(sql_db.get_pool_id(poolname), poolname, "ADD")  
                        else:
                            await add_delete_heroes(sql_db.get_pool_id(poolname), poolname, "DELETE")   
                else:
                    await ctx.send("What?")
                    raise Exception
            except:
                await ctx.send("Try again, probably some issue with your typing you noob. Sorry for the sass, sir.")
                    
        async def delete_pool(poolname):
            await ctx.send(f"Are you sure you want to delete {poolname}? Y/N")
            response = await bot.wait_for("message", check=check)
            if response.content.upper() in nvm:
                await ctx.send("Gotcha no problem brother.")
                return
            elif response.content.upper() in ["YES", "Y"]:
                if sql_db.delete_pool(poolname, user_id, ctx.guild.owner_id) == 1:
                    await ctx.send(f"Deleted: {poolname}.")
                else:
                    await ctx.send(f"{poolname} is not yours to delete!")
            else:
                await ctx.send("That was the easiest instruction ever come on sir.")


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
                        await ctx.send(f"Stored pools for {arg}: {str(sql_db.get_users_pools(sql_db.get_user_id(arg)))}")


                elif arg.startswith('NEW') or arg.startswith('ADD'):
                    await ctx.send(f"What shall we call your pool?")
                    try:
                        msg = await bot.wait_for("message", check=check)
                        if msg.content.upper() in nvm:
                            await ctx.send("Alrighty no worries.")
                            return
                        poolname = msg.content.replace("\"", "").replace("\'","").title()
                        pools = [pool.strip() for pool in sql_db.get_all_pools().split(',')]
                        if poolname in pools:
                            await ctx.send("A pool with that name already exists!")
                            return
                        else:
                            await ctx.send(f"Adding pool {poolname} to the database")
                            sql_db.execute_query(sql_db.append_user_pools_query, (poolname, str(ctx.author.id)))
                            await add_delete_heroes(sql_db.get_pool_id(poolname), poolname, "ADD")
                    except:
                        await ctx.send("Some issue with the pool name.")


                elif arg.startswith('EDIT'):
                    if arg == 'EDIT':
                        await ctx.send(f"Specify poolname to edit a pool. Don't be troll.\nStored pools: {sql_db.get_all_pools()}")
                        try:
                            msg = await bot.wait_for("message", check=check)
                            if msg.content.upper() in nvm:
                                await ctx.send("Gotcha, no problem brother.")
                                return
                            elif msg.content.title() in sql_db.get_all_pools():
                                if msg.content.title() in ["Strength", "Agility", "Intelligence"]:
                                    await ctx.send("Can't edit the defaults, sorry fam.")
                                else:
                                    print(f"Going to edit_pool with {msg.content.title()}")
                                    await edit_pool(msg.content.title())
                            else:
                                await ctx.send("Couldn't find your pool. Try again!")
                        except asyncio.TimeoutError:
                            await ctx.send("Sorry, try again from `sb.delete (poolname)`.")

                    elif len(arg) > 5:
                        arg = arg[5:].title()
                        if arg in sql_db.get_all_pools():
                            if arg in ["Strength", "Agility", "Intelligence"]:
                                await ctx.send("Can't edit the defaults, sorry fam.")
                            else:
                                await edit_pool(arg)
                        else:
                            await ctx.send("Couldn't find your pool. Try again!")
                    
                elif arg.startswith('DELETE'):
                    if len(arg) > 7:
                        try:
                            await delete_pool(arg[7:].title())
                        except:
                            await ctx.send("Couldn't delete pool. Check syntax?")
                    else:
                        try:
                            await ctx.send(f"Which pool are you hoping to delete?\n{sql_db.get_all_pools()}")
                            msg = await bot.wait_for("message", check=check)
                            if msg.content.title() in sql_db.get_all_pools():
                                await delete_pool(arg[7:].title())
                            else:
                                raise Exception
                        except:
                            await ctx.send("Had some issue deleting that pool. Perhaps permissions or a typo.")
                    

                else:
                    if arg.title() in sql_db.get_all_pools():
                        await ctx.send(f"All heroes from {arg.title()}: {sql_db.select_heroes_from_pool(arg.title())}")
                    else:
                        await ctx.send(f"`sb.dota pool list`, `sb.dota pool (poolname)`, `sb.dota pool edit (poolname)`, `sb.dota pool new`.")
            else: 
                await ctx.send("What do you want to do with the pools? sb.dota pool...  list / new / edit / delete / (poolname)")

        #SCORE RELATED FUNCTIONS
        elif arg.startswith('LOVE') or arg.startswith('HATE'):
            plus_or_minus = 'ADD' if arg[:4] == 'LOVE' else 'SUB'
            if len(arg) > 5:
                hero_to_score = arg[5:].split(',')
                try:
                    hero_id_list = [sql_db.get_hero_id(hero = heroes[hero.strip()]) for hero in hero_to_score]
                except:
                    await ctx.send("Probably a typo in there eh?")
                for id in hero_id_list:
                    try:
                        sql_db.change_hero_score(id, plus_or_minus)
                    except:
                        await ctx.send(f"Had some issue finding that {sql_db.get_hero_name(id)} in the db.")
                hero_list = [sql_db.get_hero_name(id)[0] for id in hero_id_list]
                hero_list = ", ".join(hero_list)
                await ctx.send(f"Our feelings towards {hero_list} have been recorded.")
            else:
                await ctx.send(f"Try again and let me know who gets the {plus_or_minus.lower()}. `sb.dota love hoodwink`")

        elif arg.startswith('WIN') or arg.startswith('WON') or arg.startswith('LOS'):
            plus_or_minus = 'ADD' if (arg[:3] == 'WIN' or arg[:3] == 'WON') else 'SUB'
            if len(arg.strip()) > 4:
                hero_to_score = arg[4:].split(',')
                try:
                    hero_id_list = [sql_db.get_hero_id(hero = heroes[hero.strip()]) for hero in hero_to_score]
                except:
                    await ctx.send("Maybe some typo in there, huh?")
                print(f"Got hero_id_list: {hero_id_list}")
                response = ""
                for id in hero_id_list:
                    try:
                        if plus_or_minus == 'ADD':
                            response += f"+1 for {sql_db.get_hero_name(id)[0]} has been recorded.\n"
                            sql_db.change_hero_score(id, plus_or_minus)
                        else:
                            response += f"-1 for {sql_db.get_hero_name(id)[0]} has been recorded.\n"
                            sql_db.change_hero_score(id, plus_or_minus)
                    except:
                        response += f"Had some issue finding {sql_db.get_hero_name(id)} in the db.\n"
                await ctx.send(response)
            else:
                await ctx.send(f"Try again and let me know who you guys won/lost with. comma separated please. `sb.dota win ns, np, hoodwink`")

        elif arg.startswith('SCORE'):
            if arg.strip() == 'SCORES' or 'ALL' in arg[6:11]:
                top = sql_db.get_scores('5', 'TOP')
                bottom = sql_db.get_scores('5','BOTTOM')
                response = "___Top 5:___\n"
                for heroscore in top:
                    response += f"{heroscore[0]}: {heroscore[1]}\n"
                response += "\n___Bottom 5:___\n"
                for heroscore in bottom:
                    response += f"{heroscore[0]}: {heroscore[1]}\n"
                await ctx.send(response)
            elif len(arg.split(' ')) > 1:
                heroes_to_check = arg[5:].strip().split(',')
                hero_id_list = [sql_db.get_hero_id(hero.strip()) for hero in heroes_to_check]
                print(f"Got hero_id_list: {hero_id_list}")
                for id in hero_id_list:
                    try:
                        hero = sql_db.get_hero_name(id)[0]
                        score = sql_db.get_hero_score(hero)
                        await ctx.send(f"{hero}: {score[0]}")
                    except:
                        await ctx.send(f"Had trouble finding {sql_db.get_hero_name(id)[0]}'s score.")
            elif arg == 'SCORE':
                await ctx.send("Whose score are we checking? Try `sb.dota score (heroname)` or `sb.dota (heroname)`.")
                
        elif arg.startswith('TOP') or arg.startswith('BOTTOM'):
            arg = arg.split(' ')
            if len(arg) > 1 and arg[0] in ['TOP', 'BOTTOM']:
                try: 
                    top_or_bottom = arg[0].strip()
                    count = arg[1].strip() if int(arg[1].strip()) <= 10 else '10'
                    scores = sql_db.get_scores(count, top_or_bottom)
                    response = ""
                    for score in scores:
                        response += f"{score[0]}: {score[1]}\n"
                    await ctx.send(response)
                except: 
                    await ctx.send(f"Some issue getting the {top_or_bottom.lower()} scores you requested.")
            else:
                response = ''
                if arg[0] == 'TOP':
                    scores = sql_db.get_scores('5', 'TOP')
                    for score in scores:
                        response += f"{score[0]}: {score[1]}\n"
                elif arg[0] == 'BOTTOM':
                    scores = sql_db.get_scores('5', 'BOTTOM')
                    for score in scores:
                        response += f"{score[0]}: {score[1]}\n"
                else:
                    response += "Some issue with the top/bottom request."
                await ctx.send(response)

        elif arg.startswith('RESET'):
            def check(msg):
                return CHECKS.check_same_user(ctx, msg)
            if ctx.author.id == ctx.guild.owner_id:
                if len(arg.strip()) > 5 and 'ALL' not in arg:
                    try: 
                        hero_to_reset = heroes[arg[5:].strip()]
                        await ctx.send(f"Are you sure you want to reset the score for {hero_to_reset}? Y/N.")
                        try:
                            msg = await bot.wait_for("message", check=check, timeout=30)
                            if msg.content.upper() in ["YES", "Y"]:
                                try:
                                    sql_db.reset_score(hero_to_reset)
                                    await ctx.send("Success!")
                                except:
                                    await ctx.send(f"Failed to reset the score.")
                            else:
                                await ctx.send("Okay no problem bud.")
                                return
                        except asyncio.TimeoutError:
                            await ctx.send("Sorry took too long, I'm gonna hold off on the full reset.")
                    except:
                        await ctx.send("Couldn't find that hero in the database")
                elif arg == "RESET" or arg == "RESET ALL":
                    await ctx.send(f"Are you sure you want to reset all scores stored on the database? Y/N.")
                    try:
                        msg = await bot.wait_for("message", check=check, timeout=30)
                        if msg.content.upper() in ["YES", "Y"]:
                            try:
                                sql_db.reset_all_scores()
                                await ctx.send("Success!")
                            except:
                                await ctx.send(f"Failed to reset all scores.")
                        else:
                            await ctx.send("Okay no problem bud.")
                            return
                    except asyncio.TimeoutError:
                        await ctx.send("Sorry took too long, I'm gonna hold off on the full reset.")
            else:
                await ctx.send("Need permission to reset scores in the database.")

            
        elif arg in heroes:
            hero = heroes[arg]
            await ctx.send(f"Looking up {hero}...")
            await ctx.send(f"In {ctx.message.guild.name}, {hero}'s score is {sql_db.get_hero_score(hero)[0]}.")
        
        else:
            await ctx.send("Sorry, try again with some new dota request.")
       




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
