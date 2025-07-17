import json
import os
from datetime import datetime

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_transaction(amount, description, date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    data = load_data()
    data.append({
        "amount": amount,
        "description": description,
        "date": date
    })
    save_data(data)

def get_summary(period="week"):
    # Placeholder - sẽ tùy chỉnh theo yêu cầu bạn
    return {
        "income": 1000000,
        "expense": 450000,
        "transactions": []
    }
