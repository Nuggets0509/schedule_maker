from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory
from jinja2 import TemplateNotFound

app = Flask(__name__, static_folder='static')

# In-memory app state so the app does not depend on local JSON files.
APP_STATE = {
    'start_time': [],
    'Total_Time': [],
    'Days': [],
}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/second')
def second():
    try:
        return render_template('mainform.html')
    except TemplateNotFound:
        return jsonify({'error': 'mainform.html not found'}), 404


@app.route('/elements/<path:filename>')
def elements(filename):
    elements_dir = Path(app.root_path) / 'elements'
    return send_from_directory(elements_dir, filename)


@app.route('/save_form_data', methods=['POST'])
def save_form_data():
    payload = request.get_json(silent=True) or {}

    start_time = str(payload.get('start_time', '')).strip()
    total_hours = str(payload.get('total_hours', '')).strip()
    days = payload.get('days', [])

    if isinstance(days, str):
        days = [day.strip() for day in days.split(',') if day.strip()]
    elif isinstance(days, list):
        days = [str(day).strip() for day in days if str(day).strip()]
    else:
        days = []

    if not start_time or not total_hours or not days:
        return jsonify({'error': 'start_time, total_hours, and days are required'}), 400

    APP_STATE.update({
        'start_time': [start_time],
        'Total_Time': [total_hours],
        'Days': days,
    })

    return jsonify({'message': 'Form data saved successfully', 'data': APP_STATE}), 200


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/state')
def state():
    return jsonify(APP_STATE)


if __name__ == '__main__':
    app.run(debug=True)
