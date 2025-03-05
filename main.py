from flask import Flask, jsonify, send_from_directory, render_template, request
import pandas as pd
import os

app = Flask(__name__, template_folder='template', static_url_path='/static')

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

SCHEMA = {'name': str, 'age': int, 'city': str}

def validate_schema(df, schema):
    header = df.columns.tolist()
    if len(header) != len(schema):
        return f"Schema does not match: Expected {len(schema)} columns, but got {len(header)} columns"

    for i, col in enumerate(header):
        expected_col_name = list(schema.keys())[i]
        expected_col_type = list(schema.values())[i]
        if col != expected_col_name:
            return f"Schema does not match: Expected column '{expected_col_name}' at position {i+1}, but got '{col}'"

        actual_type = df[col].dtype
        if expected_col_type == int and actual_type != 'int64':
            return f"Schema does not match: Column '{col}' should be of type 'int', but got 'string'"
        elif expected_col_type == str and actual_type != 'object':
            return f"Schema does not match: Column '{col}' should be of type 'str', but got 'string'"
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part', schema=list(SCHEMA.items()))

        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No selected file', schema=list(SCHEMA.items()))

        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            try:
                df = pd.read_csv(filename)
                preview = df.head(10).values.tolist()
                header = df.columns.tolist()
                preview.insert(0, header)

                validation_result = validate_schema(df, SCHEMA)
                if validation_result != True:
                    error_message = validation_result
                    return render_template('index.html', error=error_message, schema=list(SCHEMA.items()), preview=preview)

                return render_template('index.html', preview=preview, schema=list(SCHEMA.items()), validationResult='Schema validation successful')

            except Exception as e:
                return render_template('index.html', error=str(e), schema=list(SCHEMA.items()))

    return render_template('index.html', schema=list(SCHEMA.items()))

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
