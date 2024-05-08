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
        
        Args: none
        
        Side effects: sets attributes of 
            deck: list, deck of cards
            players: list, empty list of player
            river: list, empty list of cards in river
            playing: bool, true while playing
            total_pot: int, money in pot currently 0
            fold: bool, false while not folding
            outcome: str, empty, set when game has outcome
        
        Returns: none
        """
        self.deck = DECK
        self.players = []
        self.river = []
        self.playing=True
        self.total_pot = 0  
        self.challenge = 0
        self.fold = False
        self.outcome = ""
    
    
    def deal(self):
        """Deals first three cards.
        
        Side effects:
            - Distributes three cards each to HumanPlayer and ComputerPlayerEasy 
                or ComputerPlayerHard instances.
            - Removes 3 cards from the deck.
        """
        for n in range(3):
            for player in self.players:
                player.initial_cards.append(self.deck.pop())  
        
    def flop(self):
        """Flips three cards from the deck to the river.
        
        Side effects:
            - Removes 3 cards from the deck.
            - Adds 3 cards to the river
            - Writes to stdout
        """
        self.river.append(self.deck.pop())
        self.river.append(self.deck.pop())
        self.river.append(self.deck.pop())
        str_river = [str(c) for c in self.river]
        print("Community Cards: " + " ".join(str_river))

    def __str__(self):
        """
        Return a string representation of the current game state, listing 
        each player and their cards.

        Returns:
            str: A formatted string where each line contains a player's name 
            followed by a list of their cards. Each player's entry is separated 
            by a newline. The format of each line is 
            'PlayerName: Card1, Card2, ...'.

        Side effects:
            Reads the 'players' attribute of the instance to gather names and 
            cards, but does not modify any data.
        """
        player_cards = []
        for player in self.players:
            cards_str = ', '.join(str(card) for card in player.cards)
            player_cards.append(f'{player.name}: {cards_str}')
        return '\n'.join(player_cards)


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
        print(f"""
              Welcome {args.name}. We are collecting your phone number: 
              {args.phone_number} in case we need to contact you 
              regaurding unsafe gambling behaviour. Please be advised to 
              gamble responsibly""")
        
        print("""\n\n\n
            -------------------Welcome to RoundTable Cards------------------\n 
            First you will be dealt 3 cards, and choose to select 2 of those. 
            Then there will be 2 flops of 3 cards each. Then you will choose
            a final hand of 7 cards from your pocket and the community cards.\n
            Your hand of cards will be assigned a value. Build sets (runs and 
            pairs/3 of a kind) within your hand, and you 
            will be awarded points equal to the face value of the cards in the 
            set times the length of the set. Any cards not in a set will be 
            worth face value, and points from sets and cards will be added to
            get the value for a hand. \n
            You will play against a computuer bot. The computer bot can either 
            easy or hard.
            ====================================================================
            \n\n\n""")

        lev=input("""
            do you want to play easy or hard version: (must type 
            'easy' or 'hard'): """)
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
        if self.fold == False:
            if outcome == "W":
                print(f"Congrats!! You won {pot / 2} dollars with your super poker")

                self.players[0].money+=pot
            elif outcome=="L":
                print(f"You have been beat. Womp womp. You lost {pot / 2} dollars")
                self.players[0].money -=pot/2
            elif outcome == "T":
                print("Wow, there was a tie. That's rare. You will break even")
                self.players[0].money += (pot/2)
        else:
            print(f"You have been beat. Womp womp. You lost {pot / 2} dollars")
            
    def play_again(self):
        play_again=input("Do you want to play again (y or n)").capitalize()
        if play_again=="Y":
            self.playing=True
            print (f"You have {self.players[0].money} left. How much money would you like to add? "
                "Write 0 if none.")
            new_money=int(input("Money to add: "))
            self.players[0].money+=new_money
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
        self.players.pop(1)
        self.outcome = ""        
        self.deck = DECK
        self.river = []
        self.total_pot = 0
        self.players[0].initial_cards = []
        self.players[0].pocket = []
        self.players[0].final_hand = []
        self.fold = False
    
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
            print(f"Congrats! You won with {player_points} points!")
            self.outcome = outcome
        elif player_points < computer_points:
            outcome = "L"
            print(
                f"You lost. Your opponent had "
                f"{computer_points - player_points} points more than you."
                )
            self.outcome = outcome
        else:
            outcome = "T"
            print(f"It's a draw! The pot will be split evenly. Each player has \
                {player_points} points")
            self.outcome = outcome
                        
    def write_info(self, outcome, hrank, crank, human, comp, filename):
        outcome_message = ""
        if outcome == "W":
            outcome_message = f"Congrats! You won ${self.total_pot / 2}."
        elif outcome == "L":
            outcome_message = f"You lost ${self.total_pot / 2}. Better luck next time!"
        elif outcome == "T":
            outcome_message = "It's a tie! You broke even."

        with open(filename, 'a', encoding = "utf-8") as file:
            file.write(f"Money won/lost: {outcome_message} \n")
            file.write(f"Your Points: {hrank} \n")
            file.write(f"Your Final Hand: {human.final_hand} \n")
            file.write(f"Computer Points: {crank} \n")
            file.write(f"Computer Hands: {comp.final_hand} \n")
            file.write(f"Point Difference: {abs(hrank-crank)} \n")
            file.write("\n")

class Player: 
    """
    player class that contains game functions for both players and creates 
    attributes for both player classes
    Attributes:
        money: int, money user inputted, total money available
        initial_cards: str, cards dealt in first round
        pocket: str, cards in player hand
        final_hand: str, cards in players final hand of 7 cards
        gamestate_obj: instance of gamestate obj to update betting and 
        outcome attributes to gamestate
    """
    def __init__(self, gamestate_obj):
        """
        initializer for player class
        args:
            gamestate_obj: instance of gamestate
        side effects: sets attributes for:
            money: int, from gamestate inputted user money
            initial_cards: list, empty
            pocket: list, empty
            final_hand: list, empty
            gamestate_obj: instance of gamestate object 
        returns: none
        """
        self.money=gamestate_obj.money # money for human
        self.initial_cards = []
        self.pocket = []
        self.final_hand = []
        self.gamestate_obj = gamestate_obj
        
    def ranking(self, hand):
        """
        Assigns value to hand
        Args: 
            hand: list of 7 cards as a players's hand 
        Side effects: none
        Returns:int, value of hand
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
   
class HumanPlayer(Player):
    
    
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
        while len(self.pocket) < 2:
            choice = int(input("Choose a card to keep (enter the card number): "))
            if choice in self.initial_cards:
                self.pocket.append(choice)
                self.initial_cards.remove(choice)
                print("You have chosen:", self.pocket)
            else:
                print("Invalid choice, please select from your initial cards.")
        print("Your final hand after choosing initial cards:", self.pocket)   
            
    def bet(self):
        """Makes bet for HumanPlayer.
        
        Side effects:
            - prints to stdout.
            - can change GameState objects outcome.
            - can change GameState objects fold_decision.
            - removes bet amount from HumanPlayer's money.
            - adds bet amount to GameState instances' total_pot.
            - sets GameState's challange to the bet amount.
        """
        print(f"Money left to bet: {self.money}")
        while True:
            try:
                fold_decision = input("Do you want to fold? (Y/N): ").capitalize()
                if fold_decision == "Y":
                    self.gamestate_obj.outcome="L"
                    self.gamestate_obj.fold=True
                    break
                elif fold_decision == "N":
                    break
            except:
                print("Please type in 'Y' or 'N'")
        if fold_decision == "N":
             while True:
                try:
                    bet = int(input("How much would you like to bet? (integers only)"))
                    if 0 <= bet <= self.money:
                        self.money -= bet
                        self.gamestate_obj.total_pot += bet 
                        self.gamestate_obj.challenge = bet
                        break
                except:
                    print(f"Please bet a positive integer or 0 that is less than \
                        your money to bet, {self.money}.")
        else:
            self.final_hand = [0,0,0,0,0,0,0]
            self.gamestate_obj.outcome = "L"
            self.gamestate_obj.fold=True
            
                
    
    def choose_final_cards(self):
        all_cards = self.pocket + self.gamestate_obj.river
        print(f"Here are all the selectable cards: {all_cards}")
        final_hand = []
        while len(final_hand) < 7:
            try:
                pick = int(input("Choose the final cards to add to your hand: "))
                if pick in all_cards:
                    final_hand.append(pick)
                    all_cards.remove(pick)
                    print(f"Your current hand is: {final_hand}")
                else:
                    print("Please select from one of the available cards.")
            except ValueError:
                print("Please enter numbers only.")
        print(f"Here is your final hand: {final_hand}")
        self.final_hand = final_hand
        
class ComputerPlayerEasy(Player):
    def cpu_choose_initial_cards(self):
        self.pocket = self.initial_cards
        self.pocket.pop(randint(0,2))

    def cpu_bet(self, round):
        """ easy_cpu makes a percentage bet based on the money it has
        Args: rd1 - the 
            Side effects:
                - Increases the total_pot amount.
                - Changes the amount of money of the computer player
                - If folds then it will call the distribute_pot and give out 
                earnings
            Returns:
                total_pot(int) - updates the total amount of money in the pot 

        """
    
        bet = self.gamestate_obj.challenge
        if bet<= self.money: #call
            self.gamestate_obj.total_pot += bet
            self.money -= bet
            self.gamestate_obj.challenge =0
            print("Computer has called.")
        else:
            self.gamestate_obj.fold=True
            self.gamestate_obj.outcome = "W"
            self.gamestate_obj.challenge =0
            print("Computer has folded. You win!")

    def cpu_choose_final_cards(self):
        final_hand = self.gamestate_obj.river + self.pocket
        cpu_choice = []
        for card in range(8):
            final_hand.pop(card)
            cpu_choice.append([self.ranking(final_hand), card])
            final_hand = self.gamestate_obj.river + self.pocket
        cpu_choice = sorted(cpu_choice, reverse=False)
        final_hand.pop(cpu_choice[0][1])
        self.final_hand = final_hand

class ComputerPlayerHard(Player):
        
    def cpu_choose_initial_cards(self):
        self.pocket = self.initial_cards
        min_card = min(self.pocket)
        self.pocket.remove(min_card)



    def cpu_bet(self, round):
        """ hard_cpu makes a bet
        
        Args: None
            Side effects:
                - Increases the total_pot amount.
                - Changes the amount of money of the computer player
                - If folds then it will call the distribute_pot and give out 
                earnings
            Returns:
                total_pot(int) - updates the total amount of money in the pot 

        """
        bluffer = randint(1, 100)
        bet = self.gamestate_obj.challenge
        if round == 1:
            self.pocket.extend([randint(1, 13),randint(1, 13),randint
                                       (1, 13),randint(1, 13),randint(1, 13)])
            strength = self.ranking(self.pocket)
            self.pocket= self.pocket[:-5]
        

            if bluffer <= 30: 
                self.gamestate_obj.total_pot += bet
                self.money -= bet
                self.gamestate_obj.challenge =0
                print("Computer has called.") 
            elif strength >35 and bet<= self.money: #call
                self.gamestate_obj.total_pot += bet
                self.money -= bet
                self.gamestate_obj.challenge =0
            else:
                self.gamestate_obj.fold=True
                self.gamestate_obj.outcome = "W"
                self.gamestate_obj.challenge =0
                HumanPlayer.final_hand = 0
                ComputerPlayerHard.final_hand = [0,0,0,0,0,0,0]
                print("Computer has folded. You win!")
        elif round == 2:
            self.pocket.extend([randint(1, 13),randint(1, 13)]+self.gamestate_obj.river)
            strength = self.ranking(self.pocket)
            self.pocket = self.pocket[:-5]
            if bluffer <= 30: 
                self.gamestate_obj.total_pot += bet
                self.money -= bet
                self.gamestate_obj.challenge =0
                print("Computer has called.")
                
            elif strength > 29 and bet<= self.money: #call
                self.gamestate_obj.total_pot += bet
                self.money -= bet
                self.gamestate_obj.challenge =0
            else:
                self.gamestate_obj.fold=True
                self.gamestate_obj.outcome = "W"
                self.gamestate_obj.challenge =0
                HumanPlayer.final_hand = 0
                ComputerPlayerHard.final_hand = [0,0,0,0,0,0,0]
                print("Computer has folded. You win!")
        elif round == 3:
            ComputerPlayerHard.cpu_choose_final_cards
            strength = self.ranking(self.final_hand)
            bluffer = randint(1, 100)
            if bluffer <= 50: 
                self.gamestate_obj.total_pot += bet
                self.money -= bet
                self.gamestate_obj.challenge =0
                print("Computer has called.")
                
            elif strength > 40 and bet>=0: #call
                self.gamestate_obj.total_pot += bet
                self.money -= bet
                self.gamestate_obj.challenge =0
                print("Computer has called.")

            else:
                self.gamestate_obj.fold=True
                self.gamestate_obj.outcome = "W"
                self.gamestate_obj.challenge =0
                HumanPlayer.final_hand = 0
                ComputerPlayerHard.final_hand = [0,0,0,0,0,0,0]
                print("Computer has folded. You win!")

    def cpu_choose_final_cards(self):
        final_hand = self.gamestate_obj.river + self.pocket
        cpu_choice = []
        for card in range(8):
            final_hand.pop(card)
            cpu_choice.append([self.ranking(final_hand), card])
            final_hand = self.gamestate_obj.river + self.pocket
        cpu_choice = sorted(cpu_choice, reverse=False)
        final_hand.pop(cpu_choice[0][1])
        self.final_hand = final_hand
                                                                         
        
def game():
    """
    Runs the game indefinitely, integrating all classes and methods. 
    """
    while True:
        game = GameState()
        game.begin_game()
        human = HumanPlayer(game)
        game.players.append(human)

        while game.playing:
            if game.level == "easy":
                comp = ComputerPlayerEasy(game)
                game.players.append(comp)
            elif game.level == "hard":
                comp = ComputerPlayerHard(game)
                game.players.append(comp)

            game.shuffle()
            game.deal()
            human.choose_initial_cards()
            comp.cpu_choose_initial_cards()
            human.bet()
            if game.fold == False:
                comp.cpu_bet(1)
                if game.fold == False:
                    game.flop()
                    human.bet()
                    if game.fold == False:
                        comp.cpu_bet(2)
                        if game.fold == False:
                            game.flop()
                            human.bet()
                            if game.fold == False:
                                comp.cpu_bet(3)
                                if game.fold == False:
                                    human.choose_final_cards()
                                    comp.cpu_choose_final_cards()
                                    print(comp.final_hand)
                                    hrank = human.ranking(human.final_hand)
                                    crank = comp.ranking(comp.final_hand)
                                    game.point_comparison(hrank, crank)
            game.distribute_pot(game.outcome, game.total_pot)
            hrank = human.ranking(human.final_hand)
            crank = comp.ranking(comp.final_hand)
            game.write_info(game.outcome, hrank, crank, human, comp, "game_results.txt")
            game.play_again()
        


def parse_args(arglist):
    """
    Parse command-line arguments.
    Args:
        arglist (list of str): arguments from the command line.
    Sets arguments of:
        - name: str, player name
        - phone number: str, player's phone number
    Returns:
        arglist: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument("name", type=str,  help="name of player")
    parser.add_argument("phone_number", type=str, help="phone number of player")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    print("Parsing command-line arguments...")
    game()