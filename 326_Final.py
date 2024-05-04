"Runs RoundTable Cards game."
from random import randint
from argparse import ArgumentParser
import sys

DECK = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,
            8,8,8,8,9,9,9,9,10,10,10,10,11,11,11,11,12,12,12,12,
            13,13,13,13]

class GameState:
    def __init__(self):
        """Initializes a GameState object.
        
        Side effects:
            Initializes attribute deck.
        """
        self.deck = DECK
        self.players = []
        self.river = []
        self.playing=True

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
        print(f"""Welcome {args.name}. We are collecting your phone number: 
              {args.phone_numer} in case we need to contact you 
              regaurding unsafe gambling behaviour. Please be advised to 
              gamble responsibly""")
        
        print("""\n\n\n
            -------------------Welcome to RoundTable Cards------------------\n 
            You will build a hand of 7 cards, choosing to keep 2 of 3 cards 
            initially dealt, then choosing 5 of the 6 cards in the river. \n
            Your hand of cards will be assigned a value. Build sets (run, 2 of 
            a kind, 3 of a kind, full house, flush) within your hand, and you 
            will be awarded points equal to the face value of the cards in the 
            set times the length of the set. Any cards not in a set will be 
            worth face value, and points from sets and cards will be added to
            get the value for a hand. \n
            You will play against a computuer bot. There are different levels of 
            difficultues for bots: 1 being easiest and 5 being hardest
            ====================================================================
            \n\n\n""")
        lev=input("""do you want to play easy or hard version: (must type 
                  'easy' or 'hard')""")
        if lev in ["easy", "hard"]:
            self.level=lev
        else:
            print("""You were unable to type the level correctly so you should 
                  probably just play the easy level""")
            self.level="easy"
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
            c.append(randint(0, 10000))
        post_shuffle = sorted(pre_shuffle, key=lambda x: x[1])
        self.deck = [c[0] for c in post_shuffle]

    def distribute_pot(self,outcome, pot):
        if outcome == "W":
            print (f"Congrats!! You won {pot} dollars with your super poker 
                   skills.")
            self.money+=pot
        elif outcome=="L":
            print(f"You have been beat. Womp womp. You lost {pot} dollars")
            self.money -=pot
        elif outcome == "T":
            print("Wow, there was a tie. That's rare. You will break even")
            self.money += (pot/2)
    
    def play_again(self):
        play_again=input("Do you want to play again (y or n)").capitalize
        if play_again=="Y":
            self.playing=True
            print (f"You have {self.money} left. How much money would you like 
                   to add. (write 0 if none)")
            new_money=input("Money to add: ")
            self.money+=new_money
            the_level =input("Do you want computer level easy or hard?")
            if the_level in ["easy", "hard"]:
                self.level = the_level
            else:
                print ("""You were unable to correctly type easy or hard so 
                       you probably should play the easy game""")
                self.level = "easy"
        else:
            print("Thanks for playing!!")
            self.playing=False


class Player: 
    def __init__(self, gamestate_obj):
        self.money=gamestate_obj.money # money for human
        self.deck=gamestate_obj.shuffle()
        self.total_pot = 0 #money bet in pot, combo of both players
        self.initial_cards = []
        self.fold=False
        self.river= []
        self.final_hand = []
        self.outcome=""

    def rd1(self):
        """Deals first three cards.
        
        Side effects:
            Distributes three cards each to HumanPlayer and ComputerPlayer 
            instances
        """
        self.initial_cards.append(self.deck.pop())
        self.initial_cards.append(self.deck.pop())
        self.initial_cards.append(self.deck.pop())
   
    def rd2(self):
        """Flips three cards from the deck to the river
        
        Side effects:
            Takes a card from the deck and adds it to the river.
        """
        self.river.append(self.deck.pop())
        self.river.append(self.deck.pop())
        self.river.append(self.deck.pop())
        print(self.river)

        
    def rd3(self):
        """Flips threes cards from the deck to the river.
        
        Side effects:
            Takes 3 cards from deck and adds it to the river.
        """
        self.river.append(self.deck.pop())
        self.river.append(self.deck.pop())
        self.river.append(self.deck.pop())
        print(self.river)

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
                f"{computer_points - player_points} points"
                f"more than you."), outcome
        else:
            outcome = "T"
            return (f"It's a draw! The pot will be split evenly. Each player has "
                f"{player_points} points"), outcome
   
class HumanPlayer(Player):
    def choose_rd1(self): 
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
        card1=input("first card")
        card2=input("second card")
        cards=[card1,card2]
        if cards in self.initial_cards:
            self.final=[]
            self.final+=cards
    def bet(self):
            print("Money left to bet: " + self.money)
            while True:
                fold_decision = input("Do you want to fold? (Y/N): ").capitalize()
                if fold_decision == "Y":
                    super().outcome="L"
                    super().fold=True
                    break
                elif fold_decision == "N":
                    break
                print("Please type in 'Y' or 'N'")
            while True:
                bet = int(input("How much would you like to bet? (integers only)"))
                if 0 <= bet <= self.money:
                    break
                else:
                    print(f"Please bet a positive integer or 0 that is less than \
                        your money to bet, {self.money}.")
            self.money -= bet
            super().total_pot += bet
    
    def river(self): 
        print("Choose 5 cards from: " + super().river)
        card3=input("third card choice")
        card4=input("4 card choice")
        card5=input("5 card choice")
        card6=input("6 card choice")
        card7=input("7 card choice")
        #add cards to self.final if valid
        
class ComputerPlayerEasy(Player):
    """Prompts computer player to choose the two highest cards

        Side effects: 
                - Changes the hand of the computer player 
                - Modifies the `initial_cards` list by removing the chosen cards.
                - Modifies the `final_hand` list by adding the chosen cards.
    """
    def cpu_choose_initial_cards(self):
        while len(self.final_hand) <2:
            choice = min(self.initial_cards)
            if choice in self.initial_cards:
                self.final_hand.append(choice)
                self.initial_cards.remove(choice)
            else:
                print("CPU_initial card error")

    def cpu_bet(self,bet):
        """ cpu makes a percentage bet based on the money it has
        Args: None
            Side effects:
                - Increases the total_pot amount.
                - Changes the amount of money of the computer player
                - If folds then it will call the distribute_pot and give out 
                earnings
            Returns:
                total_pot(int) - updates the total amount of money in the pot 

        """
        if self.money< gamestate_obj.bet:
            bet = self.money  # all in 
            self.money -= bet
            self.total_pot += bet
            print(f"CPU (Easy) has bet ${bet}")
            

        elif self.money >= gamestate_obj.bet: #call
            bet = gamestate_obj.bet
            self.money -= bet
            self.total_pot = bet
            print(f"CPU (Easy) has bet ${bet}")
            
             
        else:
            outcome = 'W'
            return gamestate_obj.distribute_pot(outcome) #should trigger method 
                                                     #outcome W for human player
class ComputerPlayerHard(Player):
    
    def cpu_choose_initial_cards(self):
        while len(self.final_hand) <2:
            choice = min(self.initial_cards)
            if choice in self.initial_cards:
                self.final_hand.append(choice)
                self.initial_cards.remove(choice)
            else:
                print("CPU_initial card error")

    def cpu_bet(self,bet):
        """ cpu makes a bet
        Args: None
            Side effects:
                - Increases the total_pot amount.
                - Changes the amount of money of the computer player
                - If folds then it will call the distribute_pot and give out 
                earnings
            Returns:
                total_pot(int) - updates the total amount of money in the pot 

        """
        strength = Player.Ranking(self.hand)
        bluffer = randint(1, 100)
        if bluffer <= 10:
            bet = self.money 
            self.money -=bet
            self.total_pot += bet
            print(f"CPU (Hard) has bet ${bet}")
            return bet

        elif strength >35 and self.money >= bet:
            self.money -=bet
            self.total_pot += bet
            print(f"CPU (Hard) has bet ${bet}")
            return bet
            
        elif strength > 50 and self.money >0:
            bet = self.money
            self.money -=bet
            self.total_pot += bet
            print(f"CPU (Hard) has bet ${bet}")
            return bet

        else:
            outcome = 'W'
            return gamestate_obj.distribute_pot(outcome) #should trigger method 
                                                     #outcome W for human player
        
def game():
    game=GameState
    game.begin_game()
    while game.playing ==True:
        play=Player(game)
        human=HumanPlayer(game)
        if game.level=="easy":
            comp=ComputerPlayerEasy(game)
        elif game.level== "hard":
            comp=ComputerPlayerHard(game)
        while play.fold==False:
            human.rd1()
            human.choose_rd1()
            rd1_bet=human.bet_rd1()
            #comp choose iniital card (rd1_bet)
            play.rd2()
            rd2_bet=human.rd2_bet()
            #comp rd2 bet
            play.rd3()
            rd3_bet=human.rd3_bet()
            #comp rd3 bet
            human.river()
            #comp choose cards
            hrank=play.ranking(human.final)
            crank=play.ranking(comp.final)
            outcome=play.point_comparison(hrank,crank)
        game.distribute_pot(outcome, play.total_pot)
        game.end()


def parse_args(arglist):
    """ Parse command-line arguments.
    Args:
        arglist (list of str): arguments from the command line.
    Arguments:
        - name: player name
        - phone number: player's phone number
    Returns:
        namespace: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument("name", type=str,  help="name of player")
    parser.add_argument("phone_number", type=str, help="phone number of player")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
