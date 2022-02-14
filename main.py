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
        game = Game()

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
        run_df = pd.DataFrame({
            'Simulation':[],
            'Trial':[],
        })
        df_append_index = 0

        for index in range(n_simulation):
            # Create the game and the player
            alpha = round(data.at[candidate, 'alpha'], 3)
            beta = round(data.at[candidate, 'beta'], 3)
            player = Player(alpha, beta)
            game = Game(single_run = run_num)
            initial_value = game.get_initial_value_list()[run_num]
            game_break = False

            # Initialize the game
            game.initialization()

            # Start the game
            while game.get_current_run() < game.get_n_run():
                game.update_lottery(player)
                if not game.check_conflict(player):
                    game_break = True
                    break

            # Get the result
            if not game_break:
                game_result = game.get_result()
                [index_of_last_trial] = game_result.tail(1)['Trial']

                if [game_result.tail(1)['Win_or_lose']] == 'win':
                    trial_num = index_of_last_trial
                else:  # Quit the run by running out of chips
                    trial_num = index_of_last_trial - 1
                trial_num += 1  # Make the number more intuitive (start from 1 instead of 0)

                run_df = run_df.append({
                    'Simulation':index + 1,
                    'Trial':trial_num
                }, ignore_index = True)
                df_append_index += 1

        # Save data
        if df_append_index == 0:
            continue

        if data_type == data_type_list[0]:
            folder_path = f'./simulation_data/candidate_criteria/player-{candidate}_alpha-{alpha}_beta-{beta}'
        else:
            folder_path = f'./simulation_data/real_subject/player-{subject_list[candidate]}_alpha-{alpha}_beta-{beta}'

        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)  # Make directory if the directory is not found
        file_path = folder_path + f'/initial_value-{initial_value}.csv'
        run_df.to_csv(file_path, index = False)
    print(f'Candidate {candidate} is done!')

# Set up
task_type_list = ['whole_experiment', 'single_run_experiment']
data_type_list = ['criteria', 'real_subject']

# Set the experiment type and the data type
task_type = task_type_list[1]  # Choose to simulate the whole experiment or just one run
data_type = data_type_list[1]  # Choose whether the alpha and beta come from real subject or be made up by "candidate_criteria.py"

# Read candidate data
if data_type == data_type_list[0]:  # Choose "criteria"
    data = pd.read_csv('./resource/candidate_criteria.csv')
else:  # Choose "real_subject"
    data = pd.read_csv('./resource/subject-selecting.csv')
    subject_list = data['subject']

n_simulation = 100
n_candidate = len(data)

# Run the simulation
if __name__ == '__main__':

    # Mutliprocessing (using different cpu)
    pool = mp.Pool()
    if task_type == task_type_list[0]:  # Choose "whole_experiment"
        pool.map(whole_experiment, range(n_simulation))
    else:  # Choose "single_run_experiment"
        pool.map(single_run_experiment, range(n_candidate))

    # Inform us when the simulation is done
    print('The simulation is finished')
