# Import packages
import pandas as pd
import random
 
class Game:
    # Game's attributes
    def __init__(self, base_value = 200, initial_chip_ratio = 2, exp_type = 0, single_run = 0):
        self.__base_value = base_value
        self.__initial_value_list = [self.__base_value + 100*i for i in range(0, 6)]*2
        self.__ratio_list = (0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.1, 1.3, 1.5)
        self.__n_run = len(self.__initial_value_list)
        self.__n_trial = len(self.__ratio_list)
        self.__exp_type = exp_type
        self.__single_run = single_run
        self.__run_list = list()
        self.__conflict = bool()
        self.__current_run = int()
        self.__current_trial = int()
        self.__current_gain_utility = float()
        self.__current_loss_utility = float()
        self.__current_gain_outcome = float()
        self.__current_loss_outcome = float()
        self.__initial_chip_ratio = initial_chip_ratio
        self.__current_win_or_lose = str()
        self.__x = pd.DataFrame({  # Store trial data
            'Run':[],
            'Trial':[],
            'Gain_outcome':[],
            'Loss_outcome':[],
            'Gain_utility':[],
            'Loss_utility':[],
            'Probability':[],
            'Conflict_or_not':[],
            'Bet_or_quit':[],
            'Win_or_lose':[],
            'Chip':[],
            'Incentive':[],
        })

    # Prepare experiment material:
    # Random runs and initial value (make initial gain present randomly)
    def initialization(self):
        # Set run sequence
        sequence_1 = [i for i in range(0, 6)]
        sequence_2 = [i for i in range (6, 12)]
        
        # When the experiment type is "whole experiment", shuffle runs when they are randomly presented
        if self.__exp_type == 0:
            random.shuffle(sequence_1)
            random.shuffle(sequence_2)
            while sequence_1[-1] == sequence_2[0]:
                random.shuffle(sequence_2)
                
            # Combine the two lists
            self.__run_list = sequence_1 + sequence_2
        # When the experiment type is "single run", only undergo the specific run
        elif self.__exp_type == 1:
            self.__run_list = [self.__single_run]
            self.__n_run = 1

    # Compute loss outcome
    def __compute_loss_outcome(self, player):
        __player_attributes_list = player.get_utility_parameters()
        __ratio = self.__ratio_list[self.__current_trial]
        self.__current_gain_utility = (self.__current_gain_outcome / __player_attributes_list[2])**__player_attributes_list[0]
        self.__current_loss_utility = self.__current_gain_utility * __ratio
        __loss_outcome = round(-1 * __player_attributes_list[3] * self.__current_loss_utility **(1/__player_attributes_list[1]))
        return __loss_outcome

    # Start the game
    # Show lottery
    def show_lottery(self, player):
        if self.__current_trial == 0:
            __random_run_index = self.__run_list[self.__current_run]
            __initial_value = self.__initial_value_list[__random_run_index]
            self.__current_gain_outcome = __initial_value
            self.__current_loss_outcome = self.__compute_loss_outcome(player)
            player.change_current_incentive(None)
            player.change_current_chip(self.__current_gain_outcome*self.__initial_chip_ratio)  # initial chip: equals to initial value
        else:
            self.__current_gain_outcome = round(player.get_current_chip()*0.5 + self.__current_gain_outcome)
            self.__current_loss_outcome = self.__compute_loss_outcome(player)

        # See if the lottery induce conflict
        self.__check_conflict(player)
        
        return [self.__current_gain_outcome, self.__current_loss_outcome]
    
    # Check if the player confront with conflict
    def __check_conflict(self, player):
        gain = self.__current_gain_outcome
        loss = abs(self.__current_loss_outcome)  # Make the loss outcome > 0, which is easier to compute
        '''
        Rule 1: If the player is bankrupt, it is meaningless to know if a player feels conflict.
        Rule 2: When loss outcome euqals to 0, it means a player can easily choose to bet without conflict.
        Rule 3: When gain utility and loss utility are the same, and loss outcome is less than 1/3 of the 
            gain outcome, it means a player cannot feel conflict according to our definition or assumption.
        '''
        if player.get_current_chip() <= 0:
            self.__conflict = 'Meaningless'
        elif loss == 0:
            self.__conflict = 'Not_conflict'
        elif self.__ratio_list[self.__current_trial] == 1 and loss/gain < 1/3:
            self.__conflict = 'Not-conflict'
        else:
            self.__conflict = 'Conflict'
    
    # Save the current situation
    def __save_trial(self, player):
        __current_trial_info = pd.DataFrame({
            'Run':[self.__current_run],
            'Trial':[self.__current_trial],
            'Gain_outcome':[self.__current_gain_outcome],
            'Loss_outcome':[self.__current_loss_outcome],
            'Gain_utility':[self.__current_gain_utility],
            'Loss_utility':[self.__current_loss_utility],
            'Probability':[player.get_current_probability()],
            'Conflict_or_not':[self.__conflict],
            'Bet_or_quit':[player.get_current_bet_or_not()],
            'Win_or_lose':[self.__current_win_or_lose],
            'Chip':[player.get_current_chip()],
            'Incentive':[player.get_current_incentive()]
        })
        self.__x = pd.concat([self.__x, __current_trial_info], ignore_index = True)

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
                trial_outcome = self.__current_gain_outcome
            else:  # lose
                trial_outcome = self.__current_loss_outcome  # self.__current_loss_outcome < 0
            
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
        
        # Save the current trial after computing the chip
        self.__save_trial(player)
        if next_step == 'next trial':
            self.__current_trial += 1
        else:
            self.__current_run += 1
            self.__current_trial = 0
    
    # Accecc to private properties
    def get_initial_value_list(self):
        return self.__initial_value_list
        
    def get_n_run(self):
        return self.__n_run
    
    def get_current_run(self):
        return self.__current_run
    
    def get_result(self):
        return self.__x
    