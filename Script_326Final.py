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
            Your hand of cards will be assigned a value. Build sets (run, 2 of 
            a kind, 3 of a kind, full house, flush) within your hand, and you 
            will be awarded points equal to the face value of the cards in the 
            set times the length of the set. Any cards not in a set will be 
            worth face value, and points from sets and cards will be added to
            get teh value for a hand. \n
            You will play against a computuer bot. There are different levels of 
            difficultues for bots: 1 being easiest and 5 being hardest
            ====================================================================
            \n\n\n""")
        self.level=int(input("What level bot would you like to play against: "))
        print ("""You also will bet at the end of each round (after cards are
        dealt then after each card in the river is revealed). How much money
        do you wish to bring to the table (bot will match you)""")
        self.money=int(input("Dollar amount: "))
        print(f"""Game is initializing against level {self.level} bot with a bet
        of ${self.money}, best of luck!""")

class Player: 
    def __init__(self, bet):
        self.cards=[1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,
                    8,8,8,8,9,9,9,9,10,10,10,10,11,11,11,11,12,12,12,12,
                    13,13,13,13]
        self.money = bet
        self.pot=0
    
    def Ranking(hand):
        """
        Assigns value to hand
        Args: 
            hand: list of 7 cards as a players's hand 
        Side effects: none
        Returns: value of hand
        """
        #face value 
        value=0
        for i in hand:
            value += int(i)
        #pairs
        card_counts={}
        for card in hand:
            if card in card_counts:
                card_counts[card]+=1
            else:
                card_counts[card]=1
        for key in card_counts:
            if card_counts[key] > 1:
                value += key * (card_counts[key]-1)
            else:
                pass
        #run 
        set=set(hand)
        for n in set:
            if (n+1) in set:
                if (n+2) in set:
                    if (n+3) in set: 
                        if (n+4) in set: 
                            if (n+5) in set:
                                if (n+6) in set: 
                                    run = ((n) + (n+1) + (n+2) + (n+3) + (n+4)+
                                    (n+5) + (n+6))
                                    pts=run * 7
                                    value += pts
                                    set.remove(n)
                                    set.remove(n+1)
                                    set.remove(n+2)
                                    set.remove(n+3)
                                    set.remove(n+4)
                                    set.remove(n+5)                                
                                else: 
                                    run = ((n) + (n+1) + (n+2) + (n+3) + (n+4)+
                                    (n+5) )
                                    pts=run * 6
                                    value += pts
                                    set.remove(n)
                                    set.remove(n+1)
                                    set.remove(n+2)
                                    set.remove(n+3)
                                    set.remove(n+4)
                            else: 
                                run = ((n) + (n+1) + (n+2) + (n+3) + (n+4))
                                pts=run * 5
                                value += pts
                                set.remove(n)
                                set.remove(n+1)
                                set.remove(n+2)
                                set.remove(n+3)
                                set.remove(n+4)
                        else:
                            run = ((n) + (n+1) + (n+2) + (n+3))
                            pts=run * 4
                            value += pts
                            set.remove(n)
                            set.remove(n+1)
                            set.remove(n+2)
                            set.remove(n+3)
                    else:
                        run = ((n) + (n+1) + (n+2))
                        pts = run*3
                        value += pts
                        set.remove(n)
                        set.remove(n+1)
                        set.remove(n+2)
                else:
                    pass
            else: 
                pass
        return value


        

