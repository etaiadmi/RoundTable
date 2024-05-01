#Code for 4/12 checkin 

#Dan

from random import randint

class GameState:
    def __init__(self):
        """Initializes a GameState object.
        
        Side effects:
            Initializes attribute deck.
        """
        self.deck = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,
            8,8,8,8,9,9,9,9,10,10,10,10,11,11,11,11,12,12,12,12,
            13,13,13,13]
        self.players = [human, computer]
        self.river = []

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
        
    def shuffle(self):
        """Shuffles the deck.
        
        Side effects:
            Puts the deck in a random order.
        """
        pre_shuffle = [list() for c in self.deck]
        for n in range(len(self.deck)):
            pre_shuffle[n].append(self.deck[n])
        for c in pre_shuffle:
            c.append(randint(0, 1000))
        post_shuffle = sorted(pre_shuffle, key=lambda x: x[1])
        self.deck = [c[0] for c in post_shuffle]
        
    def deal(self):
        """Deals first three cards.
        
        Side effects:
            Distributes three cards each to HumanPlayer and ComputerPlayer 
            instances
        """
        for player in self.players:
            player.initial_cards.append(self.deck.pop())
            player.initial_cards.append(self.deck.pop())
            player.initial_cards.append(self.deck.pop())
            
    def flip(self):
        """Flips one card from the deck to the river
        
        Side effects:
            Takes a card from the deck and adds it to the river.
        """
        self.river.append(self.deck.pop())
        
    def flop(self):
        """Flips threes cards from the deck to the river.
        
        Side effects:
            Takes 3 cards from deck and adds it to the river.
        """
        self.river.append(self.deck.pop())
        self.river.append(self.deck.pop())
        self.river.append(self.deck.pop())
        
    def point_comparison(self, player_points, computer_points):
        """Comapres the point values of the player and computer and determines who
        won.
        
        Args:
            player_points (int): The points of the player's hand.
            computer_points (int): The points of the computer's hand.
        
        Returns:
            tuple: 
                A string message which describes the outcome 
                of the game, which can either be a win, loss, or tie.
            
                A string containing a single character which represents one of the
                three outcomes for the game('W', 'L', 'T') 
        """
        outcome = ""
        if player_points > computer_points:
            outcome = "W"
            return f"Congrats! You won with {player_points} points!", outcome
        elif player_points < computer_points:
            outcome = "L"
            return ("You lost. Your opponent had "
                f"{computer_points - player_points} "
                f"more than you."), outcome
        else:
            outcome = "T"
            return (f"It's a draw! The pot will be split evenly. Each player has "
                f"{player_points} points"), outcome

    def distribute_pot(self,outcome):
        """ Distributes the pot to the winner
        Args:
            outcome(str): The outcome result string from the 
            point_comprehenstion method
        Side effects:
            The money of the player may increase if they win
        Returns:
            self.money(int): The money of the player after the distribution 
            of the pot. 
        """
        final_result = outcome[1]  
        if final_result == 'W':
            print(f"You won ${self.total_pot}!")
            self.money += self.total_pot  
        elif final_result == 'L':
            print("You lost!")
        elif final_result == 'T':
            print(f"It's a chop! You won ${self.total_pot/2}!")
            self.money += self.total_pot / 2  
        return self.money
    
class Player:
    def __init__(self, gamestate_obj):
        self.money=gamestate_obj.money
        self.cards=gamestate_obj.shuffle()
        self.total_pot = 0
        self.initial_cards = []
        self.final_hand = []

    def choose_initial_cards(self): #this is HumanPlayer
        """
        Prompts the player to choose two cards to keep from their initially dealt three cards.

        This method displays the three initially dealt cards to the player and requests input to
        select two of these cards to keep for their hand. The chosen cards are moved from the
        `initial_cards` list to the `final_hand` list. This process continues until the player has
        successfully chosen two cards. If the player attempts to choose a card not among their
        initial cards, they are prompted to make a valid selection.

        Side Effects:
            - Modifies the `initial_cards` list by removing the chosen cards.
            - Modifies the `final_hand` list by adding the chosen cards.
            - Prints messages to stdout to show the cards available for selection, prompt the
              player for their choice, and confirm the chosen cards.

        Returns:
            None
        """
        print("Your initial cards are:", self.initial_cards)
        while len(self.final_hand) < 2:
            choice = int(input("Choose a card to keep (enter the card number): "))
            if choice in self.initial_cards:
                self.final_hand.append(choice)
                self.initial_cards.remove(choice)
                print("You have chosen:", self.final_hand)
            else:
                print("Invalid choice, please select from your initial cards.")
        print("Your final hand after choosing initial cards:", self.final_hand)
        
    def Ranking(self, hand):
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
        set=sorted(hand, key=lambda x: x+1, reverse=False)
        for n in set:
            if (n+1) in set:
                if (n+2) in set:
                    if (n+3) in set: 
                        if (n+4) in set: 
                            if (n+5) in set:
                                if (n+6) in set: 
                                    run = ((n) + (n+1) + (n+2) + (n+3) + (n+4)+
                                    (n+5) + (n+6))
                                    pts=run * 6
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
                                    pts=run * 5
                                    value += pts
                                    set.remove(n)
                                    set.remove(n+1)
                                    set.remove(n+2)
                                    set.remove(n+3)
                                    set.remove(n+4)
                            else: 
                                run = ((n) + (n+1) + (n+2) + (n+3) + (n+4))
                                pts=run * 4
                                value += pts
                                set.remove(n)
                                set.remove(n+1)
                                set.remove(n+2)
                                set.remove(n+3)
                                set.remove(n+4)
                        else:
                            run = ((n) + (n+1) + (n+2) + (n+3))
                            pts=run * 3
                            value += pts
                            set.remove(n)
                            set.remove(n+1)
                            set.remove(n+2)
                            set.remove(n+3)
                    else:
                        run = ((n) + (n+1) + (n+2))
                        pts = run*2
                        value += pts
                        set.remove(n)
                        set.remove(n+1)
                        set.remove(n+2)
                else:
                    pass
            else: 
                pass
        return value
    
    def player_bet(self):
        """ 
        Player option to bet with their money 
        Args: None
        Side effects:
            - Increases the total_pot amount.
            - Prints a message to the console of how much they bet or if they 
            cannot bet the amount due to the bet being to high or a negative 
            number
        Returns:
            total_pot(int) - updates the total amount of money in the pot 
        """
        bet = int(input("Bet amount:"))
        if 0 < bet <= self.money:
            self.money -= bet
            self.total_pot += bet  
            print(f"Player has bet ${bet}")
            return self.total_pot # Return updated total_pot
        elif bet < 0:
            print("You must bet a positive whole number")#add redo try later
        else:
            print("You don't have enough money to bet that amount") 
            # add redo try later

class HumanPlayer (Player):

def game():
    """Plays 1 round of RoundTable Cards.
    """
    
    gamestate.begin_game()
    gamestate.shuffle()
    gamestate.deal()
    human.choose_initial_cards()
    computer.choose_inital_cards()
    human.player_bet()
    


def main():
    """Runs as many RoundTable Cards games as wanted.
    """
    gamestate = GameState
    human = HumanPlayer
    computer = ComputerPlayer
    while 1 != 0:
        break