import pandas as pd

df=pd.read_csv(r"C:\Users\ARSHAN\Desktop\Job-Analyzer\postings.csv")
print("Data Loaded Sucessfully!")
print(f"Total job posting: {len(df)}")
print(df.columns.tolist())