
import pandas as pd

# Load data
df = pd.read_csv('sample_sales_data.csv')

# Display basic info
print("First few rows of the dataset:")
print(df.head())

# Total revenue
print("Total revenue generated:", df['Revenue'].sum())
