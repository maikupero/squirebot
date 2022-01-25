#########################################<br>
################# **squirebot** ################<br>
#########################################<br>
*Discord Bot for TheBoys.*
    *-Though made portable so you can have it too.*

Born on Dec. 16, 2021, launched and living on the internet one week later,<br>
and (mostly) complete exactly one month after that.<br>

Squirebot is here to attend to your every need before you go into battle.

<hr><h1>USAGE</h1>

Start any command message with sb.<br>
Bail out of anything with the usual forms of refusal (no, nope, etc.).

        sb.
            help : Essentially returns this list of commands to you on discord.
                // sb.help // 

            (various greetings) : Stores command-response pairs - if unknown, asks for a response.
                // sb.hey // 

            attend : Takes care of your every need.
                // sb.attend // 

            delete (greeting/pool) : Permission restrictive assistance in deleting greetings / dota hero pools stored in the database.
                // sb.delete pool green //

            weather (location) : If unspecified, prompts the user to send a location - city name, zip code, or coordinates.
                // sb.weather Tokyo // Gives you the current weather in Tokyo complete with emoji.
                    
            guess : Simple guessing game to play with your bot.
                // sb.guess // 

            aoe/randomciv : Suggests a (or x number of) random civ to play in Age of Empires 4, complete with custom flag emoji.
                // sb.randomciv 3 // 
        
            *** Dota Database Functionality ***
            dota (see below) : If unspecified, sends a help menu for dota functionality.

            -   pool () :    If unspecified lists the hero pools saved into the bot's database.
                    list : Lists out all the pools stored in the DB
                    me/username : Lists out pools linked to specified user.
                    poolname : Can be specified to list the heroes within one pool.
                        // sb.dota pool agility //
                    new/add : Prompts the user to create a new hero pool.
                    edit () : Prompts the user for a pool if unspecified, begins the edit process.
                        // sb.dota pool new   ->   green   ->   treant, necro //
                        // sb.dota pool edit green  ->   add   ->   viper //

            -   hero hero_name :  
                    Gives all stored info on provided hero
                        // sb.dota hero earthshaker //

            -   scores : Pulls up the top 5 and bottom 5 heroes by score in the database. Totally subjective and for fun.
                top/bottom x : Specify number of heroes to pull from for ranking.
                        // sb.dota top 10 //
                score (hero) : Retrieves the score of specified hero.
                love/hate (hero) : Send a specific hero +1 or -1 when they're on your mind.
                        // sb.dota hate techies //
                win/loss (heroes) : Give a list of heroes you just won with or lost with.
                        // sb.dota win hoodwink, naga siren, undying, lich, sb //

            -   random () : If unspecified suggests a random hero to play.
                    attribute/role : Random heroes from defaults like core, support, 2, strength.
                    pool_name : Suggests a random hero from specified pool in the DB.
                        // sb.dota random hero my_pool //
                    team : Suggests a random team, (usually) viable for real Dota 2 victories.
                        // sb.dota random team //
    
<hr><h1>ROADMAP</h1>

    • Implement opendota API functionality to pull up hero info and more.
    • Automatically update hero scores on win/loss for users in the discord.
    • Add other games, trivia etc, keep scores among users.