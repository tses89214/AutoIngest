from flask import send_from_directory, render_template, request, jsonify
import time
import os
import csv
from services.validation import validate_schema
from models.dto import DataTransferObject


def index(db_connector, app):
    tables = db_connector.get_table_names()
    selected_table = request.form.get('table_name') or tables[0]
    schema = db_connector.extract_schema(selected_table)
    dto = DataTransferObject({"schema": schema, "tables": tables, "selected_table": selected_table})

    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part', dto=dto)

        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No selected file', dto=dto)

        if file:
            now = int(time.time())
            upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], selected_table)
            os.makedirs(upload_dir, exist_ok=True)
            valid_filename = os.path.join(upload_dir, f"{now}_" +  file.filename)

            try:
                # show preview
                preview = []
                reader = csv.reader(file.stream.read().decode('utf-8').splitlines())
                header = next(reader)
                preview.append(header)
                for i, row in enumerate(reader):
                    if i < 10:
                        preview.append(row)
                    else:
                        break

                # validation
                is_valid, error_message = validate_schema(preview, schema)

                # show error
                if not is_valid:
                    return render_template('index.html', error=error_message, dto=dto, preview=preview)

                # save to valid
                file.save(valid_filename)
                return render_template('index.html', dto=dto, preview=preview, validationResult='Schema validation successful')

            except Exception as e:
                return render_template('index.html', error=str(e), dto=dto)

    return render_template('index.html', dto=dto)

def get_schema(db_connector):
    table_name = request.args.get('table')
    if not table_name:
        return jsonify({'error': 'Table name is required'}), 400

    schema = db_connector.extract_schema(table_name)
    print(schema)
    return jsonify(list(schema.items()))

def send_static(path):
    return send_from_directory('static', path)
