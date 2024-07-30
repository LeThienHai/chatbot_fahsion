import pandas as pd

# Load the Excel file
excel_file = 'products_2.xlsx'

# Load the sheet into a DataFrame
df = pd.read_excel(excel_file)

# Convert the DataFrame to a CSV file
csv_file = 'products_2.csv'
df.to_csv(csv_file, index=False)

print(f"Excel file {excel_file} has been converted to CSV file {csv_file}.")
