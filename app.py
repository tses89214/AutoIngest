from flask import Flask
from models.database import DatabaseConnector
import os
from controllers import main

# Database credentials
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=f"{ROOT_PATH}/templates", static_url_path=f'{ROOT_PATH}/static')

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db_connector = DatabaseConnector(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)

@app.route('/', methods=['GET', 'POST'])
def index():
    return main.index(db_connector, app)

@app.route('/get_schema')
def get_schema():
    return main.get_schema(db_connector)

@app.route('/static/<path:path>')
def send_static(path):
    return main.send_static(path)

if __name__ == '__main__':
    with app.app_context():
        db_connector = DatabaseConnector(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
        table_names = db_connector.get_table_names()
        print("Table Names:", table_names)
    app.run(debug=True)