import os
import pandas as pd
import json

def get_non_empty_columns(sheet_path):
    # Read the Excel sheet
    df = pd.read_excel(sheet_path)
    
    # Get the non-empty column names
    non_empty_columns = [col for col in df.columns if (not df[col].isnull().all() and col in ['Product Name','Active Substance','Therapeutic Area'] )]
    
    return non_empty_columns

def main():
    # Directory containing the Excel sheets
    dir_path = os.getcwd()
    
    # Dictionary to hold the results
    result = {}
    
    # Iterate through all the files in the directory
    for file_name in os.listdir(dir_path):
        # Check if the file is an Excel file
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            # Full path to the file
            file_path = os.path.join(dir_path, file_name)
            
            # Get the non-empty columns for the sheet
            non_empty_columns = get_non_empty_columns(file_path)
            
            # Add to the result dictionary
            result[file_name] = non_empty_columns
    
    # Convert the result to JSON
    result_json = json.dumps(result, indent=4)
    
    # Print the JSON
    print(result_json)
    
    # Optionally, save the JSON to a file
    with open('result.json', 'w') as json_file, open(os.path.join(dir_path, 'result.json'), 'w') as json_file:
        json_file.write(result_json)

if __name__ == "__main__":
    main()
