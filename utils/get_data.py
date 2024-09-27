from ucimlrepo import fetch_ucirepo

# fetch dataset
statlog_german_credit_data = fetch_ucirepo(id=144)

# data (as pandas dataframes)
X = statlog_german_credit_data.data.features
y = statlog_german_credit_data.data.targets

# save to csv
X.to_csv('data/features.csv', index=False)
y.to_csv('data/targets.csv', index=False)