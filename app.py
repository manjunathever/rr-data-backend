from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import os
import logging
# import matplotlib
# matplotlib.use('Agg')  # Use a non-GUI backend
# import matplotlib.pyplot as plt
# import io
# import base64
# import numpy as np
# from waitress import serve
from collections import OrderedDict

# app = Flask(__name__)
app = Flask(__name__, static_folder="../client/build", static_url_path="/")
app.json.sort_keys = False
CORS(app, resources={r"/*": {"origins": "https://rr-data-frontend.vercel.app"}})  # Allow CORS for all origins on all routes

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# # Set default font family for Matplotlib
# matplotlib.rcParams['font.family'] = 'Arial'

# Function to load data from Excel file
def load_data(file_path):
    path = os.getcwd()
    if file_path == '1':
        file_path = 'data/Germany_MA.xlsx'
    elif file_path == '2':
        file_path = 'data/Germany_Reimbursement.xlsx'
    elif file_path == '3':
        file_path = 'data/Europe_MA.xlsx'
    elif file_path == '4':
        file_path = 'data/USA_MA.xlsx'
    elif file_path == '5':
        file_path = 'data/Scotland_MA.xlsx'
    elif file_path == '6':
        file_path = 'data/Scotland_Reimbursement.xlsx'
    elif file_path == '7':
        file_path = 'data/Australia_MA.xlsx'
    elif file_path == '8':
        file_path = 'data/Australia_Reimbursement.xlsx'
    elif file_path == "9":
        file_path = 'data/UK_Reimbursement.xlsx'
    else:
        file_path = 'data/UK_MA.xlsx'
    file_path = os.path.join(path, file_path)
    df = pd.read_excel(file_path)
    df['Date of decision'] = pd.to_datetime(df['Date of decision'], dayfirst=True, errors='coerce')
    return df

# Function to filter data based on criteria
def filter_data(df, column_name, search_term, start_date, end_date):
    logging.debug(f"Start date: {start_date}, End date: {end_date}, Column: {column_name}, Term: {search_term}")

    if start_date and end_date:
        start_date = pd.to_datetime(start_date, errors='coerce')
        end_date = pd.to_datetime(end_date, errors='coerce')
        df = df[(df['Date of decision'] >= start_date) & (df['Date of decision'] <= end_date)]
    elif start_date:
        start_date = pd.to_datetime(start_date, errors='coerce')
        df = df[df['Date of decision'] >= start_date]
    elif end_date:
        end_date = pd.to_datetime(end_date, errors='coerce')
        df = df[df['Date of decision'] <= end_date]

    if column_name and search_term:
        df = df[df[column_name].astype(str).str.contains(search_term, case=False, na=False)]

    logging.debug(f"Filtered data: {df.head()}")

    # df = df.drop(columns=['Date of decision'])
    df = df.dropna(axis=1, how='all')  # Remove columns with all missing values
    df = df.where(pd.notnull(df), None)  # Replace NaN with None

    result = [OrderedDict(zip(df.columns, row)) for row in df.values]

    
    # # Determine the status column
    # st = ''
    # if "Market Authorization Status" in df.columns:
    #     st = "Market Authorization Status"
    # elif "Reimbursement Status" in df.columns:
    #     st = "Reimbursement Status"
    
    # # no viz if no status column
    # if st:
    #     color_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    #     grouped_counts = df[st].value_counts()
    #     status_color_map = dict(zip(grouped_counts.index, color_list))

    #     #donut chart
    #     fig, ax = plt.subplots(figsize=(4,3))
    #     wedges, texts, autotexts = ax.pie(grouped_counts.values, labels=grouped_counts.index,
    #                                     autopct=lambda pct: f'{int(round(pct / 100 * sum(grouped_counts.values)))}',
    #                                     startangle=120, colors=[status_color_map.get(status, 'gray') for status in grouped_counts.index],
    #                                     wedgeprops={'edgecolor': 'white'})
    #     ax.axis('equal')
    #     centre_circle = plt.Circle((0, 0), 0.70, color='white')
    #     ax.add_artist(centre_circle)
            
    #     plt.setp(texts, size=10)
    #     plt.setp(autotexts, size=10)

    #     # Adjust title position and add padding
    #     fig.subplots_adjust(top=0.85)
    #     ax.set_title('Number of Decisions', fontsize=16, weight='bold', pad=20)
    #     ax.legend(fontsize=10, loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=1)
            
    #     # Save the donut chart to a bytes buffer
    #     donut_buf = io.BytesIO()
    #     plt.savefig(donut_buf, format='png', bbox_inches='tight')
    #     donut_buf.seek(0)
    #     donut_chart = base64.b64encode(donut_buf.getvalue()).decode('utf-8')
    #     plt.tight_layout()
    #     plt.close(fig)

    #     # Generate the bar chart
    #     op=''
    #     if "Therapeutic Area" in df.columns and not df["Therapeutic Area"].isnull().all():
    #         op = "Therapeutic Area"
    #     elif "Manufacturer" in df.columns and not df["Manufacturer"].isnull().all():
    #         op = "Manufacturer"
    #     #no bar chart if either columns are absent
    #     if op:
    #         top_areas = df[op].value_counts().head(5).index.tolist()
    #         nested_dict = {}

    #         for area in top_areas:
    #             subset_df = df[df[op] == area]
    #             status_counts = subset_df[st].value_counts().to_dict()
    #             nested_dict[area] = status_counts

    #         therapeutic_areas = list(nested_dict.keys())
    #         therapeutic_areas_sorted = sorted(therapeutic_areas, key=lambda area: sum(nested_dict[area].values()), reverse=False)
                
    #         fig, ax = plt.subplots(figsize=(4,3))
    #         bar_width = 0.25
    #         bar_positions = np.arange(len(therapeutic_areas_sorted))

    #         for i, status in enumerate(grouped_counts.index):
    #             counts_sorted = [nested_dict[area].get(status, 0) for area in therapeutic_areas_sorted]
    #             bars = ax.barh(bar_positions - bar_width / 2 + i * bar_width, counts_sorted, height=bar_width, label=status, color=status_color_map.get(status, 'gray'))
    #             for bar, value in zip(bars, counts_sorted):
    #                 ax.annotate(f'{value}', xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2), 
    #                             xytext=(5, 0), textcoords='offset points',
    #                             ha='left', va='center', fontsize=10)

    #         ax.set_yticks(bar_positions)
    #         ax.set_yticklabels(therapeutic_areas_sorted, fontsize=10)
    #         ax.legend(fontsize=10, loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=1)
    #         ax.tick_params(axis='x', which='major', labelsize=10, length=3)
    #         ax.set_xlabel('Count', fontsize=10)
                
    #         # Adjust title position and add padding
    #         fig.subplots_adjust(top=0.9)
    #         ax.set_title("Top 5 "+op+" by Status", fontsize=16, weight='bold', pad=20,loc="left")
    #         ax.set_aspect('auto')
    #         # Save the bar chart to a bytes buffer
    #         bar_buf = io.BytesIO()
    #         plt.savefig(bar_buf, format='png', bbox_inches='tight')
    #         bar_buf.seek(0)
    #         bar_chart = base64.b64encode(bar_buf.getvalue()).decode('utf-8')
    #         plt.close(fig)
    #         legend=ax.legend()
    #         num_legends=len(legend.get_texts())
    #         if num_legends>9:
    #             bar_chart=None
    #             donut_chart=None
    #     else: 
    #         bar_chart=None
    # else:
    #     donut_chart=None
    #     bar_chart=None

    donut_chart=None
    bar_chart=None

    return {
        'results': result,
        'visualization1': donut_chart,
        'visualization2': bar_chart
   }

def load_clinical_trials_data():
    path = os.getcwd()
    file_path = 'data/Clinical_Trials.xlsx'
    file_path = os.path.join(path, file_path)
    df = pd.read_excel(file_path)
    # df['StartDate'] = pd.to_datetime(df['Start Date'], errors='coerce')
    return df

# Function to filter clinical trials data based on criteria
def filter_clinical_trials(df, column_name, search_term):
    if column_name and search_term:
        df = df[df[column_name].astype(str).str.contains(search_term, case=False, na=False)]
    df = df.dropna(axis=1, how='all')  # Remove columns with all missing values
    df = df.where(pd.notnull(df), None)  # Replace NaN with None
    result = [OrderedDict(zip(df.columns, row)) for row in df.values]
    return result

# Route to handle POST requests for data filtering
@app.route('/filter', methods=['OPTIONS', 'POST'])
def filter_data_route():

    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return '', 200, headers
    
    data = request.get_json()
    file_path = data.get('file_path')
    column_name = data.get('column_name', '')
    search_term = data.get('search_term', '')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not file_path:
        return jsonify([])  # Return an empty list if no file path is provided

    try:
        df = load_data(file_path)
        results = filter_data(df, column_name, search_term, start_date, end_date)
        return jsonify(results)
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/get_columns', methods=['POST'])
def get_columns():
    data = request.get_json()
    file_path = data.get('file_path')

    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400

    try:
        df = load_data(file_path)
        non_empty_columns = df.dropna(axis=1, how='all').columns.tolist()
        return jsonify({'columns': non_empty_columns})
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/clinical/', methods=['POST'])
def filter_clinical_trials_route():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return '', 200, headers

    data = request.get_json()
    column_name = data.get('column_name', '')
    search_term = data.get('search_term', '')

    try:
        df = load_clinical_trials_data()
        results = filter_clinical_trials(df, column_name, search_term)
        return jsonify(results)
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/autosuggest', methods=['GET'])
def autosuggest():
    query = request.args.get('query', '')
    column_name = request.args.get('column_name', 'Product Name')
    file_path = request.args.get('file_path', '')

    if not file_path:
        return jsonify([])  # Return an empty list if no file path is provided

    try:
        df = load_data(file_path)
        if query and column_name in df.columns:
            results = df[df[column_name].astype(str).str.contains(query, case=False, na=False)]
            suggestions = results[column_name].dropna().unique().tolist()
            return jsonify(suggestions[:10])  # Return only the top 10 suggestions
        return jsonify([])
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500



mode = 'dev'

if __name__ == "__main__":
    if mode == 'dev':
        app.run(debug=True)
    # elif mode == 'prod':
    #     serve(app,host="0.0.0.0",port=5000,threads=7)
