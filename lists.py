recognized_commands = ["hi","help","weather","aoe","dota","dotes","dop","doto","guess","attend"]

random_responses = ["Read any good books lately?","Let's play some dota","Wha?","Not sure about that","You are like friend if mine who look for fight in early game and create space for the team, but sadly my friend play the carry role.","Say peacock and no one bats an eye... say poopcock and society goes wild","and in the end, after long time the match ended, u realized that she is a girl, a beautiful girl like u have been dreaming of all this time. what would u do? what do u say?"]

conversation = {
    "hey": "hi hi",
    "yo": "hola",
    "sup": "chillin', u?",
    "whatup": "yooo",
    "hi": "hi!",
    "hola": "what up",
    "aloha": "what's goin' on?",
    "whats up": "sup",
    "go": "No",
    "no": "yes",
    "hello": "Hey! How are ya?",
    "stop": "u stop"
}
#DB Functionality so if command is not recognized, can ask for what to say and add an element to this dict.
    
heroes = ["Legion Commander","Omniknight","Phoenix","Sven","Timbersaw","Tiny","Treant Protector","Tusk","Abaddon","Axe","Chaos Knight","Doom","Lifestealer","Lycan","Magnus","Night Stalker","Pudge","Sand King","Slardar","Spirit Breaker","Undying","Tidehunter","Anti-Mage","Wraith King","Drow Ranger","Bounty Hunter","Gyrocopter","Ember Spirit","Lone Druid","Juggernaut","Mirana","Luna","Naga Siren","Morphling","Riki","Phantom Lancer","Templar Assassin","Sniper","Ursa","Troll Warlord","Bloodseeker","Vengeful Spirit","Clinkz","Broodmother","Medusa","Faceless Void","Nyx Assassin","Meepo","Razor","Phantom Assassin","Slark","Shadow Fiend","Terrorblade","Spectre","Viper","Venomancer","Chen","Weaver","Disruptor","Crystal Maiden","Jakiro","Enchantress","Lina","Keeper of the Light","Ogre Magi","Nature's Prophet","Puck","Oracle","Shadow Shaman","Rubick","Skywrath Mage","Silencer","Techies","Storm Spirit","Windranger","Tinker","Ancient Apparition","Zeus","Batrider","Bane","Dazzle","Dark Seer","Enigma","Death Prophet","Leshrac","Invoker","Lion","Lich","Outworld Devourer","Necrophos","Queen of Pain","Pugna","Visage","Shadow Demon","Winter Wyvern","Warlock","Witch Doctor"]
stre = ["Legion Commander","Omniknight","Phoenix","Sven","Timbersaw","Tiny","Treant Protector","Tusk","Abaddon","Axe","Chaos Knight","Doom","Lifestealer","Lycan","Magnus","Night Stalker","Pudge","Sand King","Slardar","Spirit Breaker","Undying","Tidehunter","Wraith King"]
agil = ["Anti-Mage","Drow Ranger","Bounty Hunter","Gyrocopter","Ember Spirit","Lone Druid","Juggernaut","Mirana","Luna","Naga Siren","Morphling","Riki","Phantom Lancer","Templar Assassin","Sniper","Ursa","Troll Warlord","Bloodseeker","Vengeful Spirit","Clinkz","Broodmother","Medusa","Faceless Void","Nyx Assassin","Meepo","Razor","Phantom Assassin","Slark","Shadow Fiend","Terrorblade","Spectre","Viper","Venomancer","Weaver"]
inte = ["Chen","Disruptor","Crystal Maiden","Jakiro","Enchantress","Lina","Keeper of the Light","Ogre Magi","Nature's Prophet","Puck","Oracle","Shadow Shaman","Rubick","Skywrath Mage","Silencer","Techies","Storm Spirit","Windranger","Tinker","Ancient Apparition","Zeus","Batrider","Bane","Dazzle","Dark Seer","Enigma","Death Prophet","Leshrac","Invoker","Lion","Lich","Outworld Devourer","Necrophos","Queen of Pain","Pugna","Visage","Shadow Demon","Winter Wyvern","Warlock","Witch Doctor"]
role1 = ["Legion Commander","Sven","Tiny","Chaos Knight","Lifestealer","Lycan","Wraith King","Anti-Mage","Drow Ranger","Gyrocopter","Lone Druid","Juggernaut","Luna","Naga Siren","Morphling","Riki","Phantom Lancer","Templar Assassin","Sniper","Ursa","Troll Warlord","Clinkz","Medusa","Faceless Void","Phantom Assassin","Slark","Terrorblade","Spectre","Weaver",]
role2 = ["Tiny","Magnus","Night Stalker","Ember Spirit","Lone Druid","Morphling","Riki","Templar Assassin","Sniper","Bloodseeker","Broodmother","Medusa","Meepo","Razor","Shadow Fiend","Viper","Lina","Puck","Rubick","Silencer","Storm Spirit","Windranger","Tinker","Zeus","Batrider","Death Prophet","Leshrac","Invoker","Outworld Devourer","Necrophos","Queen of Pain","Pugna","Visage"]
role3 = ["Legion Commander","Omniknight","Phoenix","Timbersaw","Tiny","Axe","Chaos Knight","Doom","Lycan","Magnus","Night Stalker","Pudge","Sand King","Slardar","Spirit Breaker","Undying","Tidehunter","Bounty Hunter","Lone Druid","Mirana","Riki","Ursa","Vengeful Spirit","Clinkz","Broodmother","Faceless Void","Nyx Assassin","Razor","Viper","Venomancer","Weaver","Enchantress","Nature's Prophet","Puck""Silencer","Batrider","Dark Seer","Enigma","Outworld Devourer","Necrophos","Pugna"]
role4 = ["Omniknight","Phoenix","Tiny","Treant Protector","Tusk","Abaddon","Night Stalker","Pudge","Sand King","Spirit Breaker","Undying","Bounty Hunter","Mirana","Vengeful Spirit","Nyx Assassin","Venomancer","Jakiro","Enchantress","Lina","Keeper of the Light","Nature's Prophet","Shadow Shaman","Rubick","Skywrath Mage","Silencer","Windranger","Enigma","Invoker","Pugna","Winter Wyvern"]
role5 = ["Abaddon","Undying","Chen","Disruptor","Crystal Maiden","Jakiro","Keeper of the Light","Ogre Magi","Oracle","Shadow Shaman","Rubick","Skywrath Mage","Silencer","Ancient Apparition","Bane","Dazzle","Lion","Lich","Shadow Demon","Winter Wyvern","Warlock","Witch Doctor"]
supps = ["Omniknight","Phoenix","Tiny","Treant Protector","Tusk","Abaddon","Night Stalker","Pudge","Sand King","Spirit Breaker","Undying","Bounty Hunter","Mirana","Sniper","Vengeful Spirit","Nyx Assassin","Venomancer","Weaver","Chen","Disruptor","Crystal Maiden","Jakiro","Enchantress","Lina","Keeper of the Light","Ogre Magi","Nature's Prophet","Oracle","Shadow Shaman","Rubick","Silencer","Windranger","Ancient Apparition","Bane","Dazzle","Enigma","Invoker","Lion","Lich","Pugna","Visage","Shadow Demon","Winter Wyvern","Warlock","Witch Doctor"]
cores = ["Legion Commander","Sven","Tiny","Chaos Knight","Lifestealer","Lycan","Wraith King","Anti-Mage","Drow Ranger","Gyrocopter","Lone Druid","Juggernaut","Luna","Naga Siren","Morphling","Riki","Phantom Lancer","Templar Assassin","Sniper","Ursa","Troll Warlord","Clinkz","Medusa","Faceless Void","Phantom Assassin","Slark","Terrorblade","Spectre","Weaver","Tiny","Magnus","Night Stalker","Ember Spirit","Lone Druid","Morphling","Riki","Templar Assassin","Sniper","Bloodseeker","Broodmother","Medusa","Meepo","Razor","Shadow Fiend","Viper","Lina","Puck","Rubick","Silencer","Storm Spirit","Windranger","Tinker","Zeus","Batrider","Death Prophet","Leshrac","Invoker","Outworld Devourer","Necrophos","Queen of Pain","Pugna","Visage","Legion Commander","Omniknight","Phoenix","Timbersaw","Tiny","Axe","Chaos Knight","Doom","Lycan","Magnus","Night Stalker","Pudge","Sand King","Slardar","Spirit Breaker","Undying","Tidehunter","Bounty Hunter","Lone Druid","Mirana","Riki","Ursa","Vengeful Spirit","Clinkz","Broodmother","Faceless Void","Nyx Assassin","Razor","Viper","Venomancer","Weaver","Enchantress","Nature's Prophet","Puck""Silencer","Batrider","Dark Seer","Enigma","Outworld Devourer","Necrophos","Pugna"]
jungle = ["Nature's Prophet","Legion Commander","Batrider","Axe","Lifestealer","Chaos Knight","Lycan","Enchantress","Chen","Mirana","Crystal Maiden","Sand King","Sniper","Play with your team you nerd"]