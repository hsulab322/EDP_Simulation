# Import packages
import pandas as pd
import random
 
class Game:
    # Game's attributes
    def __init__(self, base_value = 200, single_run = None):
        self.__base_value = base_value
        self.__initial_value_list = [self.__base_value + 100*i for i in range(0, 6)]*2
        self.__ratio_list = (0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.1, 1.3, 1.5)
        self.__n_run = len(self.__initial_value_list)
        self.__n_trial = len(self.__ratio_list)
        self.__single_run = single_run
        self.__run_list = list()
        self.__conflict = bool()
        self.__current_run = int()
        self.__current_trial = int()
        self.__current_gain = float()
        self.__current_loss = float()
        self.__current_win_or_lose = str()
        self.__x = pd.DataFrame({  # Store trial data
            'Run':[],
            'Trial':[],
            'Gain':[],
            'Loss':[],
            'Probability':[],
            'Bet_or_quit':[],
            'Win_or_lose':[],
            'Chip':[],
            'Incentive':[]
        })
    
    # Prepare experiment material:
    # Random runs and initial value (make initial gain present randomly)
    def initialization(self):
        # Set run sequence
        sequence_1 = [i for i in range(0, 6)]
        sequence_2 = [i for i in range (6, 12)]
        
        # Shuffle runs when they are randomly presented
        if self.__single_run == None:
            random.shuffle(sequence_1)
            random.shuffle(sequence_2)
            while sequence_1[-1] == sequence_2[0]:
                random.shuffle(sequence_2)
                
            # Combine the two lists
            self.__run_list = sequence_1 + sequence_2

        else:
            self.__run_list = [self.__single_run]
            self.__n_run = 1

    # Start the game
    # Show lottery
    def show_lottery(self, player):
        if self.__current_trial == 0:
            random_run_index = self.__run_list[self.__current_run]
            initial_value = self.__initial_value_list[random_run_index]
            self.__current_gain = initial_value
            self.__current_loss = player.get_loss_outcome(self)
            player.change_current_incentive(None)
            player.change_current_chip(self.__current_gain)  # initial chip: equals to initial value
        else:
            self.__current_gain = round(player.get_current_chip()*0.5 + self.__current_gain)
            self.__current_loss = player.get_loss_outcome(self)
        
        return [self.__current_gain, self.__current_loss]
    
    # Check if the player confront with conflict
    def check_conflict(self):
        gain = self.__current_gain
        loss = self.__current_loss

        if loss == 0:  # Rule 1: loss-outcome equals to 0
            self.__conflict = False
        elif self.__ratio_list[self.__current_trial] == 1 and loss/gain < 1/3:
            # Rule 2: when gain utility and loss utility are the same, the loss-outcome is less than 1/3 of the gain-outcome
            self.__conflict = False
        else:
            self.__conflict = True
        return self.__conflict
    
    # Save the current situation
    def __save_trial(self, player):
        self.__x = self.__x.append({
            'Run':self.__current_run,
            'Trial':self.__current_trial,
            'Gain':self.__current_gain,
            'Loss':self.__current_loss,
            'Probability':player.get_current_probability(),
            'Bet_or_quit':player.get_current_bet_or_not(),
            'Win_or_lose':self.__current_win_or_lose,
            'Chip':player.get_current_chip(),
            'Incentive':player.get_current_incentive()
        }, ignore_index = True)

    # Check if the player is bankrupt
    def __check_bankrupt(self, player):
        if player.get_current_chip() < 0:
            player.change_current_status('bankrupt')
        else:
            player.change_current_status('not_bankrupt')
        return player.get_current_status()

    # Show the next lottery
    def update_lottery(self, player):
        bet_or_not = player.action(self)
        if bet_or_not == 'bet':
            # Win or lose
            self.__current_win_or_lose = random.choice(['win', 'lose'])
            if self.__current_win_or_lose == 'win':
                trial_outcome = self.__current_gain
            else:  # lose
                trial_outcome = self.__current_loss  # self.__current_loss < 0
            
            # Compute chip
            if self.__current_trial == (self.__n_trial - 1):
                player.change_current_incentive(trial_outcome)
                next_step = 'finish current run'
            else:  # It is not the final trial in the current run
                if self.__current_trial == 0:
                    __chip = player.get_current_chip() + trial_outcome
                else:
                    __chip = player.get_current_chip()*0.5 + trial_outcome
                player.change_current_chip(__chip)
                next_step = 'next trial'
            
            # Check if the player is bankrupt
            if self.__check_bankrupt(player) == 'bankrupt':
                next_step = 'bankrupt'
                player.change_current_incentive(trial_outcome)
        else:  # quit
            if self.__current_trial != 0:
                if [self.__x.tail(1)['Win_or_lose']] == 'win':
                    __incentive = self.__x.tail(1)['gain']
                else:  # previous lottery loss
                    __incentive = self.__x.tail(1)['loss']
                player.change_current_incentive(__incentive)
            next_step = 'quit'
        
        self.__save_trial(player)
        if next_step == 'next trial':
            self.__current_trial += 1
        else:
            self.__current_run += 1
            self.__current_trial = 0
    
    # Accecc to private properties
    def get_initial_value_list(self):
        return self.__initial_value_list
        
    def get_ratio_list(self):
        return self.__ratio_list

    def get_n_run(self):
        return self.__n_run
    
    def get_current_run(self):
        return self.__current_run
    
    def get_current_trial(self):
        return self.__current_trial
    
    def get_current_gain(self):
        return self.__current_gain

    def get_result(self):
        return self.__x
    