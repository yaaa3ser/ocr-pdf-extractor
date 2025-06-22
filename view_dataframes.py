import pickle
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Load the pickle file
with open('output/dataframes.txt', 'rb') as f:
    data = pickle.load(f)

claims_df = data['claim_experiences']['claims']
benefits_df = data['claim_experiences']['benefits']

print("Claims DataFrame:")
print(claims_df.info())
print("\nFirst few rows of Claims DataFrame:")
print(claims_df.head(35))
print("\nBenefits DataFrame:")
print(benefits_df.info())
print("\nFirst few rows of Benefits DataFrame:")
print(benefits_df.head(20))