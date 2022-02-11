import pandas as pd

# Set up
alpha = 0.1
beta = float()
df = pd.DataFrame({
    'alpha':[],
    'beta':[]
})

while alpha < 2.5:
    alpha += 0.05
    alpha = round(alpha, 2)
    for i in range(7):
        beta = round(alpha - 0.15 + 0.05*i, 2)
        if beta != alpha:
            df = df.append({
                'alpha':alpha,
                'beta':beta
            }, ignore_index = True)

df.to_csv('./resource/candidate_criteria.csv', index = False)

