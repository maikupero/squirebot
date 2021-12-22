import random

class randomciv:
    
    def number_gen():
        number = random.randint(1,8)
        return number

    def civ(num):
        civ = str()
        if num == 1:
            civ = "The Abbasid Dynasty."
        if num == 2:
            civ = "The Chinese."
        if num == 3:
            civ = "The Delhi Sultanate."
        if num == 4:
            civ = "The French."
        if num == 5:
            civ = "The English."
        if num == 6:
            civ = "The Holy Roman Empire."
        if num == 7:
            civ = "The Mongols."
        if num == 8:
            civ = "The Rus Civilization."
        return civ

    def flag(num):
        emoji_name = str()
        if num == 1:
            emoji_name = "abbasid"
        if num == 2:
            emoji_name = "chinese"
        if num == 3:
            emoji_name = "delhi"
        if num == 4:
            emoji_name = "french"
        if num == 5:
            emoji_name = "english"
        if num == 6:
            emoji_name = "hre"
        if num == 7:
            emoji_name = "mongols"
        if num == 8:
            emoji_name = "rus"
        return emoji_name

    def main():
        civ_id = number_gen()
        civ = civ(civ_id)
        flag = flag(civ_id)




