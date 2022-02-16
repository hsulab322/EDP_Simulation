# Import packages
import pandas as pd
import multiprocessing as mp
import os

# Import classes
from player import Player
from game import Game

def whole_experiment(n_simulation):
    for candidate in range(18):
        # Create the game and the player
        alpha = data.iat[candidate, 0]
        beta = data.iat[candidate, 1]
        player = Player(alpha, beta)
        game = Game(exp_type = 0)

        # Initialize the game
        game.initialization()

        # Start the game
        while game.get_current_run < game.get_n_run:
            game.update_lottery(player)

        # Save data
        __result = game.get_result()
        folder_path = f'./simulation_data/player_alpha-{alpha}_beta-{beta}'
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)  # Make directory if the directory is not found
        file_path = folder_path + f'/game-{n_simulation}.csv'
        __result.to_csv(file_path, index = False)

def single_run_experiment(candidate):
    for run_num in range(6):
        run_df = pd.DataFrame({  # Store trial data
            "Simulation":[],
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
        another_run_df = pd.DataFrame({
            'Simulation':[],
            'Trial':[]
        })

        for simulation in range(n_simulation):
            # Create the game and the player
            alpha = round(data.at[candidate, 'alpha'], 3)
            beta = round(data.at[candidate, 'beta'], 3)
            player = Player(alpha, beta)
            if less_initial_chip_amount:
                game = Game(exp_type = 1, single_run = run_num, initial_chip_ratio = 1)
            else:
                game = Game(exp_type = 1, single_run = run_num)
            initial_value = game.get_initial_value_list()[run_num]

            # Initialize the game
            game.initialization()

            # Start the game
            while game.get_current_run() < game.get_n_run():
                game.update_lottery(player)

            # Get the result
            game_result = game.get_result()
            
            # Add how many simulations have been done to this trial's dataframe, and then combine it with the whole run data
            n_index = game_result.shape[0]
            game_result.insert(0, column = 'Simulation', value = [simulation for i in range(n_index)])
            run_df = pd.concat([run_df, game_result], ignore_index = True)

            # Test
            [index_of_last_trial] = game_result.tail(1)['Trial']

            if [game_result.tail(1)['Win_or_lose']] == 'win':
                trial_num = index_of_last_trial
            else:  # Quit the run by running out of chips
                trial_num = index_of_last_trial - 1

            another_run_df = another_run_df.append({
                'Simulation':simulation,
                'Trial':trial_num
            }, ignore_index = True)


        # Save data
        if data_type == 0:
            folder_path = f'./simulation_data/candidate_criteria/player-{candidate}_alpha-{alpha}_beta-{beta}'
        else:
            folder_path = f'./simulation_data/real_subject/player-{subject_list[candidate]}_alpha-{alpha}_beta-{beta}'

        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)  # Make directory if the directory is not found
        file_path = folder_path + f'/initial_value-{initial_value}.csv'
        run_df.to_csv(file_path, index = False)
        another_file_path = f'{folder_path}/previous_format_initial_value-{initial_value}.csv'
        another_run_df.to_csv(another_file_path, index = False)
    print(f'Candidate {candidate} is done!')

# Set up
exp_type_dic = {'whole_experiment':0, 'single_run_experiment':1}
data_type_dic = {'criteria':0, 'real_subject':1}

# Set the experiment type and the data type
exp_type = exp_type_dic['single_run_experiment']  # Choose to simulate the whole experiment, just one run or 
data_type = data_type_dic['real_subject']  # Choose whether the alpha and beta come from real subject or be made up by "candidate_criteria.py"
less_initial_chip_amount = False  # Let true denote that the initial chip in every run is as many as initial gain

# Read candidate data
if data_type == 0:  # Choose "criteria"
    data = pd.read_csv('./resource/candidate_criteria.csv')
else:  # Choose "real_subject"
    data = pd.read_csv('./resource/subject-selecting.csv')
    subject_list = data['subject']

n_simulation = 10
# n_candidate = len(data)
n_candidate = 10

# Run the simulation
if __name__ == '__main__':

    # Mutliprocessing (using different cpu)
    pool = mp.Pool()
    if exp_type == 0:  # Choose "whole_experiment"
        pool.map(whole_experiment, range(n_simulation))
    else:  # Choose "single_run_experiment"
        pool.map(single_run_experiment, range(n_candidate))

    # Inform us when the simulation is done
    print('The simulation is finished')

# # Only for testing
# single_run_experiment(6)