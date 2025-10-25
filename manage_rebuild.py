import os
import shutil
from datetime import datetime
from app import create_app, db

app = create_app()

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")
if os.path.exists(DB_PATH):
    backup_path = f"{DB_PATH}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copyfile(DB_PATH, backup_path)
    print(f"Backup of the database created at {backup_path}")
else:
    print("No existing database found to back up.")

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database rebuilt successfully.")