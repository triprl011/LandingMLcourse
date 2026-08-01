from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

# Файл для хранения заявок (в реальном проекте лучше использовать SQLite/Postgres)
LEADS_FILE = 'leads.json'

# Инициализация файла с лидами
if not os.path.exists(LEADS_FILE):
    with open(LEADS_FILE, 'w') as f:
        json.dump([], f)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit_lead', methods=['POST'])
def submit_lead():
    """Сохраняет email и имя пользователя в JSON-файл"""
    data = request.json
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()

    if not email or '@' not in email:
        return jsonify({'status': 'error', 'message': 'Введите корректный email'}), 400

    # Загружаем существующие лиды
    with open(LEADS_FILE, 'r') as f:
        leads = json.load(f)

    # Добавляем нового лида
    leads.append({
        'name': name,
        'email': email,
        'timestamp': datetime.now().isoformat()
    })

    # Сохраняем обратно
    with open(LEADS_FILE, 'w') as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    return jsonify({'status': 'success', 'message': 'Спасибо! Менеджер Настя свяжется с вами.'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)