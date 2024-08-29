import pandas as pd
import json
import os

# Define the directory containing the Excel files
directory = '.'  # Current directory

# Initialize a dictionary to store the combined data
combined_data = {}

# Define a mapping of file keys to countries and card types
file_key_mapping = {
    "Germany_MA.xlsx": ("Germany", "MA"),
    "Germany_Reimbursement.xlsx": ("Germany", "Reimbursement"),
    "Europe_MA.xlsx": ("European Union", "MA"),
    "USA_MA.xlsx": ("USA", "MA"),
    "Scotland_MA.xlsx": ("Scotland", "MA"),
    "Scotland_Reimbursement.xlsx": ("Scotland", "Reimbursement"),
    "Australia_MA.xlsx": ("Australia", "MA"),
    "Australia_Reimbursement.xlsx": ("Australia", "Reimbursement"),
    "UK_Reimbursement.xlsx": ("UK", "Reimbursement"),
    "UK_MA.xlsx": ("UK", "MA"),
    "France_MA.xlsx": ("France", "MA"),
    "France_Reimbursement.xlsx": ("France", "Reimbursement"),
    "Spain_MA.xlsx": ("Spain", "MA"),
    "Spain_Reimbursement.xlsx": ("Spain", "Reimbursement"),
    "Sweden_MA.xlsx": ("Sweden", "MA"),
    "Sweden_Reimbursement.xlsx": ("Sweden", "Reimbursement"),
    "Canada_MA.xlsx": ("Canada", "MA"),
    "Canada_Reimbursement.xlsx": ("Canada", "Reimbursement"),
    "South Korea_MA.xlsx": ("South Korea", "MA"),
    "Italy_MA.xlsx": ("Italy", "MA"),
    "Brazil_MA.xlsx": ("Brazil", "MA")
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
                country, card_type = file_key_mapping[file_name]
                if country not in combined_data:
                    combined_data[country] = {}
                if card_type not in combined_data[country]:
                    combined_data[country][card_type] = {
                        'Product Name': [],
                        'Active Substance': [],
                        'Therapeutic Area': []
                    }
                
                combined_data[country][card_type]['Product Name'].extend(df['Product Name'].tolist())
                combined_data[country][card_type]['Active Substance'].extend(df['Active Substance'].tolist())
                combined_data[country][card_type]['Therapeutic Area'].extend(df['Therapeutic Area'].tolist())

# Remove duplicates
for country in combined_data:
    for card_type in combined_data[country]:
        for key in combined_data[country][card_type]:
            combined_data[country][card_type][key] = list(set(combined_data[country][card_type][key]))

# Save the combined data to a JSON file with UTF-8 encoding
with open('combined_data.json', 'w', encoding='utf-8') as f:
    json.dump(combined_data, f, indent=4, ensure_ascii=False)

print("Combined data has been saved to 'combined_data.json'")
