# Import package
from multiprocessing.sharedctypes import Value
import random

class Player:
    # Player's attributes
    def __init__(self, alpha, beta, max_gain = 15000, max_loss = 12000):
        self.__alpha = alpha
        self.__beta = beta
        self.__max_gain = max_gain
        self.__max_loss = max_loss
        self.__current_probability = float()
        self.__current_bet_or_quit = str()
        self.__current_chip = float()
        self.__current_status = str()  # bankrupt or not
        self.__current_incentive = float()
    
    def action(self, game):
        # Bet strategy (unsolved)
        current_lottery = game.show_lottery(self)
        gain = current_lottery[0]
        loss = -1*current_lottery[1]
        if gain > loss:
            self.__current_probability = 1
        else:
            self.__current_probability = 1
        [self.__current_bet_or_quit] = random.choices(['bet', 'quit'], weights = [self.__current_probability, 1-self.__current_probability])
        return self.__current_bet_or_quit  # let True denote "bet"
    
    # Accecc to private properties
    def get_utility_parameters(self):
        return [self.__alpha, self.__beta, self.__max_gain, self.__max_loss]

    def get_current_probability(self):
        return self.__current_probability
    
    def get_current_bet_or_not(self):
        return self.__current_bet_or_quit

    def get_current_chip(self):
        return self.__current_chip
    
    def change_current_chip(self, value):
        self.__current_chip = value
    
    def get_current_status(self):
        return self.__current_status

    def change_current_status(self, string):
        self.__current_status = string
    
    def get_current_incentive(self):
        return self.__current_incentive

    def change_current_incentive(self, value):
        self.__current_incentive = value
