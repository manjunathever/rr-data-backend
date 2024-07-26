import pandas as pd
import json

# Define the file paths and sheet names
files = [
    ('Europe_MA.xlsx', 'Sheet1'),
    ('Australia_Reimbursement.xlsx', 'Sheet1')
]

# Initialize a dictionary to store the combined data
combined_data = {
    'Product Name': [],
    'Active Substance': [],
    'Therapeutic Area': []
}

# Read each file and extract the relevant columns
for file_path, sheet_name in files:
    df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str)
    df = df.fillna('')  # Fill missing values with empty strings
    combined_data['Product Name'].extend(df['Product Name'].tolist())
    combined_data['Active Substance'].extend(df['Active Substance'].tolist())
    combined_data['Therapeutic Area'].extend(df['Therapeutic Area'].tolist())

# Remove duplicates
for key in combined_data:
    combined_data[key] = list(set(combined_data[key]))

# Save the combined data to a JSON file
with open('combined_data.json', 'w') as f:
    json.dump(combined_data, f, indent=4)

print("Combined data has been saved to 'combined_data.json'")
