#########################################<br>
################## squirebot ###############<br>
#########################################<br>
--- Discord Bot for TheBoys. 

Born on Dec. 16, 2021, launched and living on the internet one week later,<br>
Squirebot is here to attend to your every need before you go into battle.

<hr><center>####USAGE</center><hr>

Start any command message with sb.

        sb.
            help : 
                Essentially returns this list of commands to you on discord.
            greet : 
                Accepts and returns various greetings.
            attend : 
                Takes care of your every need.
            guess : 
                Simple guessing game to play with your bot.
            aoe /civ/randomciv :
                Suggests a random civ to play in Age of Empires 4, complete with custom flag emoji.
        
            weather () : If unspecified, prompts the user to send a location - city name, zip code, or coordinates.
                location : 
                    i.e. sb.weather Tokyo
                    
            dota () :    If unspecified, sends a help menu for dota functionality.
            -   pool () :    If unspecified lists the hero pools saved into the bot's database.
                    poolname : Can be specified to list the heroes within one pool.
                        // sb.dota pool // Lists all global pools and user-specific pools.
            -   hero hero_name :  
                    Gives all stored info on provided hero
                        // .sb.dota hero earthshaker // Lists all characteristics and stats stored on Earthshaker.
            -   append (): If unspecified sends a help menu for how to append more info to the database.
                    hero : Guidance to append info to an existing hero or add a new one.
                    pool : Guidance to add heroes to an existing pool or create a new one.
                    team : Guidance to add a hero to an existing team or create a new one.
                        // sb.dota append team // Assists you in adding a new team of heroes to the database.
            -   random () : If unspecified suggests a random hero to play.
                    hero: 
                        pool_name : Suggests a random hero from specified user's pool if pool exists in DB.
                        attribute : Included as pools 
                    team : Suggests a random team
                        // sb.dota random hero green // Suggests random hero that is green.
    
<hr>####ROADMAP<hr>

    Build a database to store user info, preferences, user-created dota hero pools, stats, etc.
    Clean up main.py and separate functions - shouldn't all be under one @client.event.