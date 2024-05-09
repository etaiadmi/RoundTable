"Runs RoundTable Cards game."
from random import randint
from argparse import ArgumentParser
import sys
import pandas as pd
import matplotlib.pyplot as plt
DECK = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,
            8,8,8,8,9,9,9,9,10,10,10,10,11,11,11,11,12,12,12,12,
            13,13,13,13]
class PandaData:
    """A class for the simulation of rounds of RoundTable Cards game.

    Attributes:
        sim_player_hand (list of int):  simulated ai player hand
        sim_cpu_hand (list of int):  simulated cpu hand
        sim_result (list of int):  result of simulation
        sim_river (list of int):  simulated community cards
        sim_cpu_final_hand (list of int):  simulated cpu final hand
        sim_player_final_hand (list of int):  simulated ai player final hand 
        sim_deck (list of int): copy of global variable deck list
        """
    def __init__(self):
        """Initilizes a simulated game of roundtables between ai
        Args: 
        sim_player_hand (list of int): see class documentation.
        sim_cpu_hand (list of int): see class documentation.
        sim_result (list of int): see class documentation.
        sim_river (list of int): see class documentation.
        sim_cpu_final_hand (list of int):  see class documentation.
        sim_player_final_hand (list of int):  see class documentation.
        sim_deck (list of int):  see class documentation.
            
        Side effects:
            initlizes all PandaData attributes
        """
        self.sim_player_hand = []
        self.sim_cpu_hand= []
        self.sim_result = []
        self.sim_river = []
        self.sim_cpu_final_hand = []
        self.sim_player_final_hand = []
        self.sim_deck = DECK
        
    def sim_ranking(self, hand):
        """Assigns value to hand.
        Args: 
            hand: list of 7 cards as a players's hand 
        Side effects: none
        Returns:int, value of hand
        """
        #face value 
        value=0
        for card in hand:
            value += int(card)
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
        
    def sim_flop(self):
        """Flips three cards from the simulated deck to the simulated river.
        
        Side effects:
            - Removes 3 cards from the sim_deck.
            - Adds 3 cards to the sim_river
        """
        self.sim_river.append(self.sim_deck.pop())
        self.sim_river.append(self.sim_deck.pop())
        self.sim_river.append(self.sim_deck.pop())

    def sim_shuffle(self):
        """Shuffles the sim_deck.
        
        Side effects:
            - Puts the sim_deck in a random order.
        """
        pre_shuffle = [list() for c in self.sim_deck]
        for n in range(len(self.sim_deck)):
            pre_shuffle[n].append(self.sim_deck[n])
        for c in pre_shuffle:
            c.append(randint(0, 10000))
        post_shuffle = sorted(pre_shuffle, key=lambda x: x[1])
        self.sim_deck = [c[0] for c in post_shuffle]
    
    def sim_deal(self):
        """Deals first three cards.
        
        Side effects:
            - Distributes three cards each to sim_player_ai and sim_cpu 
            instances
            - Removes 3 cards from the sim_deck.
        """
        
        for n in range(3):
            self.sim_player_hand.append(self.sim_deck.pop())  
            self.sim_cpu_hand.append(self.sim_deck.pop())  
        min_card = min(self.sim_player_hand)
        min_cpu_card = min(self.sim_cpu_hand)
        self.sim_player_hand.remove(min_card) 
        self.sim_cpu_hand.remove(min_cpu_card)

    def sim_rd_1(self):
        """ Hard CPU makes a choice on round 1.
        Side effects: 
            - strength is calculated with random integers
            - may append sim_result list with a result
            - may invoke sim_flop()
            - strength is created and updated with an int
        """
        self.sim_cpu_hand.extend([randint(1, 13),randint(1, 13),randint
                                       (1, 13),randint(1, 13),randint(1, 13)])
        strength = self.sim_ranking(self.sim_cpu_hand)
        self.sim_cpu_hand= self.sim_cpu_hand[:-5]
        bluffer = randint(1, 100)
        if bluffer <= 30 or strength >35: 
           self.sim_flop()

        else:
            self.sim_result.append("Fold Round 1")
            
        #round 2
    
    def sim_rd_2(self):
        """Hard CPU makes a choice on round 2.
        Side effects: 
            strength is calculated with random integers
            may append sim_result list with a result
            may invoke sim_flop()
        """
        self.sim_cpu_hand = self.sim_cpu_hand + self.sim_river
        self.sim_cpu_hand.extend([randint(1, 13),randint(1, 13)])
        strength = self.sim_ranking(self.sim_cpu_hand)
        self.sim_cpu_hand= self.sim_cpu_hand[:-5]
        bluffer = randint(1, 100)
        if bluffer <= 30 or strength >=50: 
           self.sim_flop()


        else:
            self.sim_result.append("Fold Round 2")
        
    def sim_rd_3(self):
        """Hard CPU makes a choice on round 3.
        Side effects: 
            - strength is calculated with random integers
            - may append sim_result list with a result
            - may pass
            - strength is created and updated with an int
        """
        bluffer = randint(1, 100)
        self.sim_cpu_hand = self.sim_cpu_hand + self.sim_river
        strength = self.sim_ranking(self.sim_cpu_hand)
        self.sim_cpu_hand= self.sim_cpu_hand[:-5]
        if bluffer <= 20 or strength >=65: 
            pass
        else:
            self.sim_result.append("Fold Round 3")
            
        #sim_cpu choice to pick final hand
    
    def sim_cpu_choose_final(self):
        """simulated cpu chooses final cards
        
        Side effects:
            - sim_cpu_final_hand is updated
            - cpu_choice is appended with a list of cards
            - sim_cpu_final_hand is altered to a 7 digit list
            - ranking is invoked to calculate best hand
        """
        self.sim_cpu_final_hand = self.sim_cpu_hand +self.sim_river
        cpu_choice = []
        sim_cpu_final_hand = self.sim_cpu_final_hand
        for card in range(8):
            sim_cpu_final_hand.pop(card)
            cpu_choice.append([self.sim_ranking(self.sim_cpu_final_hand), card])
            sim_cpu_final_hand = self.sim_river + self.sim_cpu_hand
        cpu_choice = sorted(cpu_choice, reverse=False)
        sim_cpu_final_hand.pop(cpu_choice[0][1])
        self.sim_cpu_final_hand = sim_cpu_final_hand
    
        #sim_player choice to pick final hand
    
    def sim_player_choose_final(self):
        """simulated player ai chooses final cards
        
        Side effects:
            - sim_player_final_hand is updated
            - player_choice is appended with a list of cards
            - sim_player_final hand is altered to a 7 digit list
            - ranking is invoked to calculate best hand

        """
        self.sim_player_final_hand = self.sim_player_hand+self.sim_river
        player_choice = []
        sim_player_final_hand = self.sim_player_final_hand
        for card in range(8):
            sim_player_final_hand.pop(card)
            player_choice.append([self.sim_ranking(self.sim_player_final_hand), card])
            sim_player_final_hand = self.sim_river + self.sim_player_hand
        player_choice = sorted(player_choice, reverse=False)
        self.sim_player_final_hand.pop(player_choice[0][1])
        self.sim_player_final_hand = sim_player_final_hand

        
        #final scores of both sims
    
    def sim_showdown(self):
        """ the final hands of the player ai and cpu instance face off
        Side effects:
            - sim_result may be appened with one of three outcomes (W,L,T)
            - sim_player and sim_cpu final scores are updated
        """
        sim_cpu_final_score = self.sim_ranking(self.sim_cpu_final_hand)
        sim_player_final_score =self.sim_ranking(self.sim_player_final_hand)
        if sim_cpu_final_score>sim_player_final_score:
            self.sim_result.append(f"CPU Won {sim_cpu_final_score}")
        elif sim_cpu_final_score < sim_player_final_score:
            self.sim_result.append(f"CPU Lost {sim_cpu_final_score}")
        elif sim_cpu_final_score == sim_player_final_score:
            self.sim_result.append(f"Tie")
            
        #reset
    def reset(self):
        """resets the simulation results and all attributes in PandaData
        Side effects
            resets the simulation results and all attributes in PandaData
        """
        self.sim_deck = DECK
        self.sim_river = []
        self.sim_player_hand = []
        self.sim_cpu_hand= []
        self.sim_result = []
        self.sim_player_final_hand = []
        self.sim_cpu_final_hand = []
        
    def simulation(self):
        """creates 100 simulations of RoundTable poker between Hard CPU and 
        player ai
        
        Side effects:
            all sim_result is appended to game_results
            
        Returns:
            game_results (list of str): the game results of 100 simulations
        """
        game_results = []
        
        for i in range(100):
            while True:
                self.sim_shuffle()
                self.sim_deal()
                self.sim_rd_1()
                if "Fold Round 1" in self.sim_result:
                    game_results.append(list(self.sim_result))
                    break
                self.sim_rd_2()
                if "Fold Round 2" in self.sim_result:
                    game_results.append(list(self.sim_result))
                    break
                self.sim_rd_3()
                if "Fold Round 3" in self.sim_result:
                    game_results.append(list(self.sim_result))
                    break
                else:
                    self.sim_cpu_choose_final()
                    self.sim_player_choose_final()
                    self.sim_showdown()
                    game_results.append(list(self.sim_result))
                    break
            self.reset()
        print("anyting")
        return game_results
    
    def panda_data_frames(self,game_results):
        """calculates game_results and showcases data on an pyplot and dataframe
        Args:
            game_results (list of str): the game results of 100 simulated games

        Side effects:
            - cpu_won,won_score,cpu_lost,lost_score,ties,fold_rd_1,fold_rd_2,
            fold_rd_3,other_score, other_outcome are all created as empty lists
            - the game_result is stripped and appended to the various lists 
            metioned above.
            - won_score, lost_score, other_scorelists are turned into a single 
            list as str called total_score
            - cpu_won, cpu_lost and other_outcome are appended to a single list 
            called total outcome
            - creates a pyplot based on the list of outcomes
            - prints a dataframe that takes the scores above 100 points and 
            ended in a win for the sim_cpu

        """
        cpu_won = []
        won_score = []
        cpu_lost = []
        lost_score = []
        ties = []
        fold_rd_1 = []
        fold_rd_2 = []
        fold_rd_3 = []
        for result in game_results:
            if "Tie" in result:
                ties.append(result)
            elif "Fold Round 1" in result:
                fold_rd_1.append(result)
            elif "Fold Round 2" in result:
                fold_rd_2.append(result)
            elif "Fold Round 3" in result:
                fold_rd_3.append(result)
        for result in game_results:
            games_won =[string[0:7] for string in result]
            games_lost =[string[0:8] for string in result]
            if "CPU Won" in games_won:
                cpu_won.append(games_won)
                score =[string[8:] for string in result]
                won_score.append(score)
                
            elif "CPU Lost" in games_lost:
                cpu_lost.append(games_lost)
                score =[string[9:] for string in result]
                lost_score.append(score)
        
        other_score = []
        other_outcome = []
        other_outcome = ties +fold_rd_1 +fold_rd_2 +fold_rd_3
        for result in other_outcome:
            other_score.append("0")

        total_score = won_score+lost_score+other_score
        total_outcome = cpu_won +cpu_lost+other_outcome
        
        outcome_counts = {
            "CPU Won": len(cpu_won),
            "CPU Lost": len(cpu_lost),
            "Tie": len(ties),
            "Fold Round 1": len(fold_rd_1),
            "Fold Round 2": len(fold_rd_2),
            "Fold Round 3": len(fold_rd_3),
        }
        
        total_score = won_score + lost_score + other_score
        new_total_score = [int(inner_list[0]) for inner_list in total_score]
        
        total_outcome = cpu_won + cpu_lost + other_outcome

        data = {
            "Score": new_total_score,
            "Outcome": [outcome[0] for outcome in total_outcome]
        }
        
        df = pd.DataFrame(data)
        
        df_filtered = df[(df["Outcome"] == "CPU Won") & (df["Score"] > 100)]
        
        print("this is the amount of hands won by the Hard CPU"
              "with scores above 100 points")
        print(df_filtered)
        
        df = pd.DataFrame(list(outcome_counts.items()), columns=['Outcome',
                                                                 'Frequency'])
        
        df.plot(kind='bar', x='Outcome', y='Frequency', legend=False, color='c',
                alpha=0.7)
        plt.title("Outcome Frequency")
        plt.xlabel("Outcome")
        plt.ylabel("Frequency")
        plt.show()
        
class GameState:
    """A class to facilitate part of RoundTable Cards game.
    
    Attributes:
        deck: list of int, deck of cards
        players: list of HumanPlayer and ComputerPlayerEasy or 
            ComputerPlayerHard, players of game
        river: list of int, community cards
        playing: bool, true while playing
        total_pot: int, money in pot
        fold: bool, false while not folding
        outcome: str, empty, set when game has outcome
    """
    def __init__(self):
        """Initializes a GameState object.
        
        Args: none
        
        Side effects: sets attributes of 
            - deck: list, deck of cards
            - players: list, empty list of player
            - river: list, empty list of cards in river
            - playing: bool, true while playing
            - total_pot: int, money in pot currently 0
            - fold: bool, false while not folding
            - outcome: str, empty, set when game has outcome
        
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
        
    def __str__(self):
        """
        Provides a string representation of the current game state.

        This method returns a string that summarizes the game state, including 
        the number of players, the number of cards remaining in the deck, the 
        cards in the river, the total pot size, and the active status of the 
        game. It is particularly useful for debugging or providing quick 
        insights into the game's status during runtime.

        Args:
            None

        Returns:
            str: A string summarizing the current state of the game.
        """
        return (f"GameState: {len(self.players)} players, "
                f"Deck has {len(self.deck)} cards remaining, "
                f"River has {len(self.river)} cards: {self.river}, "
                f"Total pot: ${self.total_pot}, "
                f"Game {'is' if self.playing else 'is not'} active.")

    
    
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


    def begin_game(self):
        """
        To initilize game explaining rules and determining user inputted 
        bot difficulty and bet money amount. 
        Args: none
        Side Effects: 
            sets attributes of 
                level: int, difficulty of bot
                stats: str, players prompt to view simulation 
                money: int, money player has, bot will match
            prints messages explaining game to sd out
            prints messages showing the results of the simulation between the ai
            and prints a bar graph
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
        stats=input("""
            would you like to see a simulation of the Hard CPU vs Easy CPU with
            data analysis?: """)
        if stats in ["yes"]:
            simulation_instance = PandaData()
            game_results = simulation_instance.simulation()  # Run the simulation
            simulation_instance.panda_data_frames(game_results)
        else:
            print("""
            Thats fine, less work for me """)

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
        while True:
            try:
                self.money=int(input("Dollar amount: "))
                if self.money >= 0:
                    print(f"Game is initializing against level {self.level} "
                        f"bot with a bet of ${self.money}, best of luck!")
                    break
                else:
                    print("Please input an integer that is 0 or greater.")
            except:
                print("Please input an integer that is 0 or greater.")
        
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
        """distributes pot to player instances 
        Args:
            outcome(str): outcome of round (W,L,T)
            pot(int): total int of pot from human player and bot cpu
        
        Side effects:
            - may set self.fold to false
            - changes the money of either the cpu or human player based on the 
            outcome
            - print statements to console depending on outcome
        """
        if outcome == "W":
            print(f"Congrats!! You won {pot / 2} dollars with your super poker")
            self.players[0].money+=pot
        elif outcome=="L":
            if self.fold == False:
                print(f"You have been beat. Womp womp. You lost {pot / 2} dollars")
                self.players[0].money -=pot/2
            else:
                print(f"You have been beat. Womp womp. You lost {pot / 2} dollars")
        elif outcome == "T":
            print("Wow, there was a tie. That's rare. You will break even")
            self.players[0].money += (pot/2)
                
    def play_again(self):
        """Allows user to play again
        Side effects:
            - prompts user if they want to play again with user input
            - may increase humanplayer self.money depending on input
            - print to console various questions
            - may end script if user chooses to 
            - may reset all class attributes to initial values
            - changes ComputerPlayer to Hard or Easy 
        """
        play_again=input("Do you want to play again (y or n)").capitalize()
        if play_again=="Y":
            self.playing=True
            while True:
                try:
                    print (f"You have {self.players[0].money} left. How much money would you like to add? "
                        "Write 0 if none.")
                    new_money=int(input("Money to add: "))
                    if new_money >= 0:
                        break
                    else:
                        print("Please input an integer that is 0 or greater.")
                except:
                    print("Please insert an integer that is 0 or greater.")
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
        """Comapres the point values of the player and computer and determines 
        who won.
        
        Args:
            player_points (int): The points of the player's hand.
            computer_points (int): The points of the computer's hand.
            
        Side effects:
            prints information to stdout regarding point difference.
            updates the outcome attribute to "W", "L", or "T" based on outcome.
            
        Returns:
            None
        """
        outcome = ""
        if player_points > computer_points:
            outcome = "W"
            print(f"Congrats! You won with {player_points} points!")
            self.outcome = outcome
        elif player_points < computer_points:
            outcome = "L"
            print(f"You lost. Your opponent had " \
                  f"{computer_points - player_points} points more than you.")
            self.outcome = outcome
        else:
            outcome = "T"
            print(f"It's a draw! The pot will be split evenly. Each player " \
                  f"has {player_points} points")
            self.outcome = outcome
                        
    def write_info(self, outcome, hrank, crank, human, comp, filename):
        """Writes end game information to a file.
        
        Args:
            outcome (str): The outcome of the game.
            hrank (int): The player's hand rank value.
            crank (int): The computer's hand rank value.
            human (HumanPlayer): HumanPlayer object which represents a human.
            comp (ComputerPlayer): An easy or hard ComputerPlayerobject.
            filename (str): The name of the text file.
            
        Side effects:
            - Writes a variety of end game information to a text file.
            - prevents cheating by writing computer hands as empty or 0 if they 
            fold
            
        Returns:
            None
        """
        
        outcome_message = ""
        if outcome == "W":
            outcome_message = f"Congrats! You won ${self.total_pot / 2}."
        elif outcome == "L":
            outcome_message = f"You lost ${self.total_pot / 2}."
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
        initial_cards: list of int, cards dealt in first round
        pocket: list of int, cards in player hand
        final_hand: list of int, cards in players final hand of 7 cards
        gamestate_obj: instance of GameState to update betting and 
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
    """A class that facilitates the human players interaction with the
    RoundTable Cards game.
    
    Attributes:
        money: int, money user inputted, total money available
        initial_cards: list of int, cards dealt in first round
        pocket: list of int, cards in player hand
        final_hand: list of int, cards in players final hand of 7 cards
        gamestate_obj: instance of GameState to update betting and 
        outcome attributes to gamestate
    """
    
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
            print("You have chosen:", self.pocket) if choice in self.initial_cards and not self.pocket.append(choice) and not self.initial_cards.remove(choice) else print("Invalid choice, please select from your initial cards.")
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
        """Allows the user to pick their final hand comprised of 7 cards.
        
        Args:
            None
        
        Side effects:
            updates the final_card attribute to the list of cards the player 
            picked.
            prints final_hand information to stdout.
        
        Returns:
            None
        """
        all_cards = self.pocket + self.gamestate_obj.river
        print(f"Here are all the selectable cards: {all_cards}")
        final_hand = []
        while len(final_hand) < 7:
            try:
                prompt = "Choose the final cards to add to your hand: "
                pick = int(input(prompt))
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
    """Easy CPU opponent
    Attributes: 
        money: int, money user inputted, total money available
        initial_cards: list of int, cards dealt in first round
        pocket: list of int, cards in cpu hand
        final_hand: list of int, cards in cpu final hand of 7 cards
        gamestate_obj: instance of GameState to update betting and 
        outcome attributes to gamestate
    """
    def cpu_choose_initial_cards(self):
        """computer chooses cards
        Side effects:
            - changes the value of self.pocket to self,intial cards(list of int)
            - pops a random card from self.pocket
        """
        self.pocket = self.initial_cards
        self.pocket.pop(randint(0,2))

    def cpu_bet(self, round):
        """ easy_cpu makes a choice
        Args: 
            round (int): the current round 
        Side effects:
            - may print fold or call 
            - removes computers money based on bet from user
            - may change self.gamestate_obj.change outcome to "W"
            - may change self.gamestate_obj.fold. to True
            - adds money to total_pot based on bet
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
        """cpu chooses their final hand
        Side effects:
            - changes final hand to a list of 7 cards (int)
            - takes in all cards on river and in hand to choose best 7 cards
            - activates ranking method 
            - self.final_hand is appended list of 7 cards (int)
        """
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
    """Hard CPU opponent
    Attributes: 
        money: int, money user inputted, total money available
        initial_cards: list of int, cards dealt in first round
        pocket: list of int, cards in cpu hand
        final_hand: list of int, cards in cpu final hand of 7 cards
        gamestate_obj: instance of GameState to update betting and 
        outcome attributes to gamestate
    """
        
    def cpu_choose_initial_cards(self):
        """computer chooses cards
        Side effects:
            - changes the value of self.pocket to self,intial cards(list of int)
            - min card is the lowest card in self.pocket
            - pops a lowest card value from self.pocket
        """
        self.pocket = self.initial_cards
        min_card = min(self.pocket)
        self.pocket.remove(min_card)



    def cpu_bet(self, round):
        """ Hard cpu makes a choice
        Args: 
            round (int): the current round 
        Side effects:
            - may print fold or call 
            - removes computers money based on bet from user
            - may change self.gamestate_obj.change outcome to "W"
            - may change self.gamestate_obj.fold. to True
            - adds money to total_pot based on bet
            - changes the level of strength from creating random integer
            values that predict the flop 
            - alters self.pocket and reverts changes after strength calculations
            - computer may bluff if bluffer is within range of random int
            
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
            elif strength >25 and bet>=0: #call
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
                
            elif strength >=45 and bet>=0: #call
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
                
            elif strength >= 65 and bet>=0: #call
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
        """cpu chooses their final hand
        Side effects:
            - changes final hand to a list of 7 cards (int)
            - takes in all cards on river and in hand to choose best 7 cards
            - activates ranking method 
            - self.final_hand is appended list of 7 cards (int)
        """
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
    
    Side effects:
        - creates instances of PandaData, GameState, HumanPlayer, and ComputerPlayerEasy or
            ComputerPlayerHard. 
        - writes to stdout.
        - see also GameState.begin_game()
        - see also GameState.shuffle()
        - see also GameState.deal()
        - see also HumanPlayer.choose_initial_cards()
        - see also ComputerPlayerEasy.choose_initial_cards()
        - see also ComputerPlayerHard.choose_initial_cards()
        - see also HumanPlayer.bet()
        - see also Player.ranking()
        - see also GameState.point_comparison()
        - see also GameState.distribute_pot()
        --see also GameState.write_info()
        - see also GameState.play_again()
        - see also PandaData.panda_data_frames()
    """
    
    game=GameState()
    game.begin_game()
    human=HumanPlayer(game)
    game.players.append(human)
    while game.playing == True:
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
            hrank = human.ranking(human.final_hand)#update hrank for write info
            crank = comp.ranking(comp.final_hand)#update hrank for write info
            game.write_info(game.outcome, hrank, crank, human, comp, "game_results.txt")
            game.play_again()
    print("Bye-Bye")   


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