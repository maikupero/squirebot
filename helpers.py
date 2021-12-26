class aoe4:
    def randomciv(civ_id):
        civ = str()
        if civ_id == 1:
            civ = "The Abbasid Dynasty"
            emoji_name = "abbasid"
        elif civ_id == 2:
            civ = "The Chinese"
            emoji_name = "chinese"
        elif civ_id == 3:
            civ = "The Delhi Sultanate"
            emoji_name = "delhi"
        elif civ_id == 4:
            civ = "The French"
            emoji_name = "french"
        elif civ_id == 5:
            civ = "The English"
            emoji_name = "english"
        elif civ_id == 6:
            civ = "The Holy Roman Empire"
            emoji_name = "hre"
        elif civ_id == 7:
            civ = "The Mongols"
            emoji_name = "mongols"
        elif civ_id == 8:
            civ = "The Rus Civilization"
            emoji_name = "rus"

        return (civ, emoji_name)

class dota:
    def dota_help():
        return 0

class server:
    def attend(num):
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
        return response
        