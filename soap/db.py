import sqlite3

DATABASE_FILE = "database.db"
SQL_FILE = "tugas_api.sql"

# Eksekusi file SQL untuk inisialisasi database
def initialize_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    with open(SQL_FILE, "r") as f:
        sql_script = f.read()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    print("Database berhasil diinisialisasi dari file SQL.")

if __name__ == "__main__":
    initialize_database()
