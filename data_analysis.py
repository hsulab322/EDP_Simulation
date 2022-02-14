# Import packages
import pandas as pd
import os
import numpy as np
from scipy import stats

n_simulation = 100
path = './simulation_data/initial_chip_equals_to_initial_value'

# Run two types of data
for chip_setting in range(2):
    path = os.listdir('./simulation_data')[chip_setting]
    for type in range(2):
        type_path = os.listdir(f'./simulation_data/{path}')[type]
        n_candidate = len(os.listdir(f'./simulation_data/{path}/{type_path}'))

        for candidate in range(n_candidate):
            # Set up the dataframe before computing data from the first candidate
            if candidate == 0:
                result = pd.DataFrame({
                    'ID':[],
                    'alpha':[],
                    'beta':[],
                    'n_simulation':[],
                    'initial_value':[],
                    'trial_1':[],
                    'trial_2':[],
                    'trial_3':[],
                    'trial_4':[],
                    'trial_5':[],
                    'trial_6':[],
                    'trial_7':[],
                    'trial_8':[],
                    'trial_9':[],
                    'mean':[],
                    'median':[],
                    'mode':[],
                    'Q1':[],
                    'Q3':[]
                })

            # Get alpha & beta from the folder
            player_path = os.listdir(f'./simulation_data/{path}/{type_path}')[candidate]
            id = player_path.split('-')[1][:-6]
            if type_path == 'candidate_criteria':
                id = int(id) + 1
            alpha = player_path.split('-')[2].split('_')[0]
            beta = player_path.split('-')[3]
            n_initial_value = len(os.listdir(f'./simulation_data/{path}/{type_path}/{player_path}'))

            # Respectively compute each initial value
            for i in range(n_initial_value):
                # Read file
                initial_value_path = os.listdir(f'./simulation_data/{path}/{type_path}/{player_path}')[i]
                initial_value = initial_value_path.split('-')[1].split('.')[0]
                data = pd.read_csv(f'./simulation_data/{path}/{type_path}/{player_path}/{initial_value_path}')['Trial']
                data = list(data)

                # Count n_trials
                n_trial_dict = {}
                for i in range(9):
                    n_trial_dict[i+1] = data.count(i+1)

                # Caculate mean, median, mode and quantiles
                mean = np.mean(data)
                median = np.median(data)
                mode = stats.mode(data)[0][0]
                q1 = np.quantile(data, .25)
                q3 = np.quantile(data, .75)

                # Fill in the blank
                result = result.append({
                    'ID':id,
                    'alpha':alpha,
                    'beta':beta,
                    'n_simulation':n_simulation,
                    'initial_value':initial_value,
                    'trial_1':n_trial_dict[1],
                    'trial_2':n_trial_dict[2],
                    'trial_3':n_trial_dict[3],
                    'trial_4':n_trial_dict[4],
                    'trial_5':n_trial_dict[5],
                    'trial_6':n_trial_dict[6],
                    'trial_7':n_trial_dict[7],
                    'trial_8':n_trial_dict[8],
                    'trial_9':n_trial_dict[9],
                    'mean':mean,
                    'median':median,
                    'mode':mode,
                    'Q1':q1,
                    'Q3':q3
                }, ignore_index = True)

        # Store the result after the final candidate
        result_path = f'./data_analysis_result/{path}_{type_path}_analysis_result.csv'
        result.to_csv(result_path, index = False)

        print(f'The analysis of {type_path} is done!')
