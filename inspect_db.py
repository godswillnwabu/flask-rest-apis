import sqlite3
from pprint import pprint

# Path to the SQLite database file
DB_PATH = "instance/data.db"

# Connect to the SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()



# Retrieve the list of tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
pprint(tables)


# Retrieve and print the schema for each table
for table_name in tables:
    table_name = table_name[0]
    print(f"\nSchema for table '{table_name}':")
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    for column in columns:
        print(column)
        

conn.close()
print("\nDatabase inspection completed.")
