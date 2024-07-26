import pandas as pd
import json
import os

# Define the directory containing the Excel files
directory = '.'  # Current directory

# Initialize a dictionary to store the combined data
combined_data = {
    'Product Name': [],
    'Active Substance': [],
    'Therapeutic Area': []
}

# List all Excel files in the directory
for file_name in os.listdir(directory):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(directory, file_name)
        
        # Read all sheet names in the Excel file
        xls = pd.ExcelFile(file_path)
        for sheet_name in xls.sheet_names:
            # Read the sheet into a DataFrame with all columns as strings
            df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str)
            df = df.fillna('')  # Fill missing values with empty strings
            
            if 'Product Name' in df.columns and 'Active Substance' in df.columns and 'Therapeutic Area' in df.columns:
                combined_data['Product Name'].extend(df['Product Name'].tolist())
                combined_data['Active Substance'].extend(df['Active Substance'].tolist())
                combined_data['Therapeutic Area'].extend(df['Therapeutic Area'].tolist())

# Remove duplicates
for key in combined_data:
    combined_data[key] = list(set(combined_data[key]))

# Save the combined data to a JSON file with UTF-8 encoding
with open('combined_data.json', 'w', encoding='utf-8') as f:
    json.dump(combined_data, f, indent=4, ensure_ascii=False)

print("Combined data has been saved to 'combined_data.json'")
