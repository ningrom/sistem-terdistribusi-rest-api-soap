from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Konfigurasi koneksi database
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',  
    'database': 'tugas_api'  
}

# Membuat koneksi database
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Database connected")
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mahasiswa', methods=['GET', 'POST'])
def mahasiswa():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Tambahkan mahasiswa baru
        name = request.form['name']
        nim = request.form['nim']
        prodi = request.form['prodi']
        
        cursor.execute("INSERT INTO mahasiswa (nama, nim, prodi) VALUES (%s, %s, %s)", 
                       (name, nim, prodi))
        conn.commit()

        return redirect(url_for('mahasiswa'))

    # Ambil semua data mahasiswa
    cursor.execute("SELECT * FROM mahasiswa")
    mahasiswa_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('mahasiswa.html', mahasiswa=mahasiswa_data)

@app.route('/mahasiswa/update/<string:nim>', methods=[ 'POST'])
def update_mahasiswa(nim):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil data mahasiswa berdasarkan NIM
    cursor.execute("SELECT * FROM mahasiswa WHERE nim = %s", (nim,))
    mahasiswa = cursor.fetchone()
    if not mahasiswa:
        return "Mahasiswa tidak ditemukan!", 404

    if request.method == 'POST':
        # Update data mahasiswa
        name = request.form['name']
        nim = request.form['nim']
        prodi = request.form['prodi']

        cursor.execute("UPDATE mahasiswa SET nama = %s, nim = %s, prodi = %s WHERE nim = %s",
                       (name, nim, prodi, nim))
        conn.commit()

        return redirect(url_for('mahasiswa'))

    cursor.close()
    conn.close()
    return render_template('update_mahasiswa.html', mahasiswa=mahasiswa)

@app.route('/mahasiswa/delete/<int:nim>', methods=['POST'])
def delete_mahasiswa(nim):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hapus mahasiswa berdasarkan NIM
    cursor.execute("DELETE FROM mahasiswa WHERE nim = %s", (nim,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for('mahasiswa'))

if __name__ == '__main__':
    app.run(debug=True)
