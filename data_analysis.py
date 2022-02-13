# Import packages
import pandas as pd
import os
import numpy as np
from scipy import stats

n_simulation = 100

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
            'mode':[]
        })

    # Get alpha & beta from the folder
    player_path = os.listdir('./simulation_data')[candidate]
    alpha = player_path.split('_')[1].split('-')[1]
    beta = player_path.split('_')[2].split('-')[1]

    # Respectively compute each initial value
    for i in range(6):
        # Read file
        initial_value_path = os.listdir('./simulation_data/' + player_path)[i]
        initial_value = initial_value_path.split('-')[1].split('.')[0]
        data = pd.read_csv(f'./simulation_data/{player_path}/{initial_value_path}')['Trial']
        data = list(data)

        # Count n_trials
        n_trial_dict = {}
        for i in range(9):
            n_trial_dict[i+1] = data.count(i+1)

        # Compute median and histogram
        mean = np.mean(data)
        median = np.median(data)
        mode = stats.mode(data)[0][0]

        # Fill in the blank
        result = result.append({
            'ID':candidate + 1,
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
            'mode':mode
        }, ignore_index = True)

# Store the result after the final candidate
    path = './data_analysis_result/candidate_selection_criteria_result.csv'
    result.to_csv(path, index = False)

print('done')
