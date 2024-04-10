#Code for 4/12 checkin 

#Dan
class GameState:
    def __init__(self):
        pass

    def begin_game(self):
        """
        To initilize game explaining rules and determining user inputted 
        bot difficulty and bet money amount. 
        Args: none
        Side Effects: 
            sets attributes of 
                level: int, difficulty of bot
                money: int, money player has, bot will match
            prints messages explaining game to sd out
        Returns: none
        """
        print("""\n\n\n
            -------------------Welcome to RoundTable Cards------------------\n 
            You will build a hand of 7 cards, choosing to keep 2 of 3 cards 
            initially dealt, then choosing 5 of the 6 cards in the river. \n
            Your hand of  cards will be assigned a value. Build sets (run, 2 of 
            a kind, 3 of a kind, full house, flush) within your hand, and you 
            will be awarded points equal to the face value of the cards in the 
            set times the length of the set. Flushes will be considered for 5+ 
            cards. 
            All other sets can be 2+ cards. Any cards not in a set will have 
            their 
            face values added to the total points. \n
            You will play against a computuer bot. There are different levels of 
            difficultues for bots: 1 being easiest and 5 being hardest
            ====================================================================
            """)
        self.level=int(input("What level bot would you like to play against: "))
        print ("""You also will bet at the end of each round (after cards are
        dealt then after each card in the river is revealed). How much money
        do you wish to bring to the table (bot will match you)""")
        self.money=int(input("Dollar amount: "))
        print(f"""Game is initializing against level {self.level} bot with a bet
        of ${self.money}, best of luck!""")
        
x=GameState()
x.begin_game()
