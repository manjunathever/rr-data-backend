from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from data_loading import load_data, load_clinical_trials_data
from data_filtering import filter_data, filter_clinical_trials
from visualization import create_donut_chart, create_bar_chart

app = Flask(__name__, static_folder="../client/build", static_url_path="/")
app.json.sort_keys = False
CORS(app, resources={r"/*": {"origins": "https://rr-data-frontend.vercel.app"}})

logging.basicConfig(level=logging.DEBUG)

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
        return jsonify([])

    try:
        df = load_data(file_path)
        results = filter_data(df, column_name, search_term, start_date, end_date)
        visualization1 = None
        visualization2 = None

        if "Market Authorization Status" in df.columns:
            st = "Market Authorization Status"
        elif "Reimbursement Status" in df.columns:
            st = "Reimbursement Status"
        else:
            st = None

        if st:
            grouped_counts = df[st].value_counts()
            visualization1 = create_donut_chart(grouped_counts)

            if "Therapeutic Area" in df.columns:
                op = "Therapeutic Area"
            elif "Manufacturer" in df.columns:
                op = "Manufacturer"
            else:
                op = None

            if op:
                visualization2 = create_bar_chart(df, st, op, grouped_counts)

        return jsonify({
            'results': results,
            'visualization1': visualization1,
            'visualization2': visualization2
        })
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
        return jsonify([])

    try:
        df = load_data(file_path)
        if query and column_name in df.columns:
            results = df[df[column_name].astype(str).str.contains(query, case=False, na=False)]
            suggestions = results[column_name].dropna().unique().tolist()
            return jsonify(suggestions[:10])
        return jsonify([])
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

mode = 'dev'

if __name__ == "__main__":
    if mode == 'dev':
        app.run(debug=True)
