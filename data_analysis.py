# Import packages
import pandas as pd
import os
import numpy as np
from scipy import stats

# Set how many simulations, data type and initial chip setting
n_simulation = 100
data_type_dic = {0:"candidate_criteria", 1:"real_subject"}
chip_setting_dic = {0:"more_initial_chip", 1:"less_initial_chip"}

# Run two types of data
for chip_setting in range(1):
    for data_type in range(1, 2):
        simulation_data_path = f'./simulation_data/consider_maximum/{chip_setting_dic[chip_setting]}'
        n_candidate = len(os.listdir(simulation_data_path))

        for candidate in range(n_candidate):
            # Set up the dataframe before computing data from the first candidate
            if candidate == 0:
                result = pd.DataFrame({
                    'ID':[],
                    'alpha':[],
                    'beta':[],
                    'alpha - beta':[],
                    'max_gain':[],
                    'max_loss':[],
                    'n_simulation':[],
                    'initial_value':[],
                    'trial_0':[],
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
                    'Q3':[],
                    'lottery_6_num':[],
                    'lottery_6_mean_difference':[],
                    'lottery_8_num':[],
                    'lottery_8_mean_difference':[]
                })

            # Get alpha & beta from the folder
            player_path = os.listdir(simulation_data_path)[candidate]
            id = player_path.split('-')[1][:-6]
            if data_type == 0:
                id = int(id) + 1
            alpha = player_path.split('-')[2].split('_')[0]
            beta = player_path.split('-')[3].split('_')[0]
            max_gain = player_path.split('-')[4].split('_')[0]
            max_loss = player_path.split('-')[5]
            n_initial_value = len(os.listdir(f'{simulation_data_path}/{player_path}'))

            # Respectively compute each initial value
            for i in range(n_initial_value):
                # Read file
                initial_value_path = os.listdir(f'{simulation_data_path}/{player_path}')[i]
                initial_value = initial_value_path.split('-')[1].split('.')[0]
                exp_data = pd.read_csv(f'{simulation_data_path}/{player_path}/{initial_value_path}')
                current_initial_value_list = []
                lottery_6_num = lottery_8_num = 0
                lottery_6_mean_difference = lottery_8_mean_difference = 0

                # Compute mean difference between gain-outcome and loss-outcome at lottery 6 & 8
                for lottery_index in [5, 7]:
                    lottery = exp_data[exp_data["Trial"] == lottery_index]
                    lottery_num = len(lottery)
                    lottery.index = range(lottery_num)
                    lottery_diff_list = []
                    for trial_index in range(lottery_num):
                        gain = float(lottery.at[trial_index, "Gain_outcome"])
                        loss = float(lottery.at[trial_index, "Loss_outcome"])
                        lottery_diff_list.append(abs(gain + loss))
                    lottery_mean_difference = np.mean(lottery_diff_list)
                    if lottery_index == 5:
                        lottery_6_num = int(lottery_num)
                        lottery_6_mean_difference = lottery_mean_difference
                    else:
                        lottery_8_num = int(lottery_num)
                        lottery_8_mean_difference = lottery_mean_difference

                # Find out how many trials can players play
                for simulation_num in range(n_simulation):
                    run_data = exp_data[exp_data['Simulation'] == simulation_num]
                    if [run_data.tail(1)['Win_or_lose']] == 'win':
                        n_trial = run_data.shape[0]
                    else:
                        n_trial = run_data.shape[0] - 1
                    current_initial_value_list.append(n_trial)

                # Raise error message if the number of rows does not equal to n_simulation
                if len(current_initial_value_list) != n_simulation:
                    assert False, "The number of rows doesn't match the number of simulations "

                # Count n_trials
                n_trial_dict = {}
                for i in range(10):
                    n_trial_dict[i] = current_initial_value_list.count(i)

                # Caculate mean, median, mode and quantiles
                mean = np.mean(current_initial_value_list)
                median = np.median(current_initial_value_list)
                mode = stats.mode(current_initial_value_list)[0][0]
                q1 = np.quantile(current_initial_value_list, .25)
                q3 = np.quantile(current_initial_value_list, .75)

                # Fill in the blank
                current_player_df = pd.DataFrame({
                    'ID':[id],
                    'alpha':[alpha],
                    'beta':[beta],
                    'alpha - beta':[round(float(alpha) - float(beta), 3)],
                    'max_gain':[max_gain],
                    'max_loss':[max_loss],
                    'n_simulation':[n_simulation],
                    'initial_value':[initial_value],
                    'trial_0':[n_trial_dict[0]],
                    'trial_1':[n_trial_dict[1]],
                    'trial_2':[n_trial_dict[2]],
                    'trial_3':[n_trial_dict[3]],
                    'trial_4':[n_trial_dict[4]],
                    'trial_5':[n_trial_dict[5]],
                    'trial_6':[n_trial_dict[6]],
                    'trial_7':[n_trial_dict[7]],
                    'trial_8':[n_trial_dict[8]],
                    'trial_9':[n_trial_dict[9]],
                    'mean':[mean],
                    'median':[median],
                    'mode':[mode],
                    'Q1':[q1],
                    'Q3':[q3],
                    'lottery_6_num':[lottery_6_num],
                    'lottery_6_mean_difference':[lottery_6_mean_difference],
                    'lottery_8_num':[lottery_8_num],
                    'lottery_8_mean_difference':[lottery_8_mean_difference]
                })
                result = pd.concat([result, current_player_df], ignore_index = True)

        # Store the result after the final candidate
        result_path = f'./data_analysis_result/{data_type_dic[data_type]}_{chip_setting_dic[chip_setting]}_analysis_result_new.csv'
        result.to_csv(result_path, index = False)

        print(f'The analysis of {data_type_dic[data_type]}*{chip_setting_dic[chip_setting]} is done!')
