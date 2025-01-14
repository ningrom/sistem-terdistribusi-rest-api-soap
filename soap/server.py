from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import mysql.connector

# Koneksi database
DATABASE_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',  
    'database': 'tugas_api'
}

class MahasiswaService(ServiceBase):
    # Create Operation: Adds a new record to the mahasiswa table
    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def create(ctx, nama, nim, prodi):
        print("Request Context:", ctx.in_object)
        print(f"Received Create Request: nama={nama}, nim={nim}, prodi={prodi}")
        """Add a new mahasiswa record to the database."""
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO mahasiswa (nama, nim, prodi) VALUES (%s, %s, %s)', (nama, nim, prodi))
            conn.commit()
            # print("Insert successful")
            if cursor.rowcount == 0:
                return "Insert failed. Please check your input."
        except mysql.connector.IntegrityError as e:
            print(f"Database error: {e}")
            return "NIM already exists. Please use a different NIM."
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            conn.close()
        return "Mahasiswa record created successfully"

    # Read Operation: Retrieves a mahasiswa record by NIM
    @rpc(Unicode, _returns=Unicode)
    def read(ctx, nim):
        """Retrieve a mahasiswa record by NIM from the database."""
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM mahasiswa WHERE nim = %s', (nim,))
        record = cursor.fetchone()
        conn.close()
        if record:
            return f"Nama: {record[0]}, NIM: {record[1]}, Prodi: {record[2]}"
        return "Mahasiswa record not found"

    # Read All Operation: Retrieves all mahasiswa records
    @rpc(_returns=Unicode)
    def readAll(ctx):
        """Retrieve all mahasiswa records from the database."""
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM mahasiswa')
        records = cursor.fetchall()
        conn.close()
        if records:
            return "\n".join([f"Nama: {r[0]}, NIM: {r[1]}, Prodi: {r[2]}" for r in records])
        return "No mahasiswa records found."

    # Update Operation: Updates a mahasiswa record by NIM
    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def update(ctx, nim, nama, prodi):
        """Update a mahasiswa record by NIM in the database."""
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM mahasiswa WHERE nim = %s', (nim,))
        record = cursor.fetchone()
        if not record:
            conn.close()
            return "Mahasiswa record not found"
        cursor.execute('UPDATE mahasiswa SET nama = %s, prodi = %s WHERE nim = %s', (nama, prodi, nim))
        conn.commit()
        conn.close()
        return "Mahasiswa record updated successfully"

    # Delete Operation: Deletes a mahasiswa record by NIM
    @rpc(Unicode, _returns=Unicode)
    def delete(ctx, nim):
        """Delete a mahasiswa record by NIM from the database."""
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM mahasiswa WHERE nim = %s', (nim,))
        record = cursor.fetchone()
        if not record:
            conn.close()
            return "Mahasiswa record not found"
        cursor.execute('DELETE FROM mahasiswa WHERE nim = %s', (nim,))
        conn.commit()
        conn.close()
        return "Mahasiswa record deleted successfully"

# Setting up the SOAP application
application = Application([MahasiswaService],
    tns='spyne.examples.mysql.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, WsgiApplication(application))
    print("SOAP server is running on http://127.0.0.1:8000")
    server.serve_forever()
