
<?php
header("Content-Type: application/json; charset=UTF-8");

// Konfigurasi database
$host = "localhost";
$username = "root";
$password = "";
$database = "tugas_api";

// Membuat koneksi
$conn = new mysqli($host, $username, $password, $database);

// Cek koneksi
if ($conn->connect_error) {
    die(json_encode(["error" => "Connection failed: " . $conn->connect_error]));
}

//Handler POST (Create)
if ($_SERVER['REQUEST_METHOD']== 'POST'){
    $database = json_decode(file_get_contents('php://input'), true);

    if(isset($database['nama']) && isset($database['nim']) && isset ($database['prodi'])) {
        $nama = $database['nama'];
        $nim = $database['nim'];
        $prodi = $database['prodi'];

        $query = "INSERT INTO mahasiswa (nama, nim, prodi) VALUES ('$nama', '$nim', '$prodi')";
        
        if ($conn->query($query) === TRUE) {
            echo json_encode(["message" => "Mahasiswa berhasil ditambahkan"]);
        } else {
            echo json_encode(["error" => "Error: " . $conn->error]);
        }
    } else {
        echo json_encode(["error" => "Data tidak lengkap"]);
    }
    exit;
}

//Handler PUT (Update)
if ($_SERVER['REQUEST_METHOD'] == 'PUT') {
    $database = json_decode(file_get_contents('php://input'), true);

    if (isset($database['id'], $database['nama'], $database['nim'], $database['prodi'])) {
        $id = $database['id'];
        $nama = $database['nama'];
        $nim = $database['nim'];
        $prodi = $database['prodi'];

        // Periksa apakah ID ada di database
        $checkQuery = "SELECT * FROM mahasiswa WHERE id=$id";
        $result = $conn->query($checkQuery);

        if ($result->num_rows > 0) {
            // Jika ID ditemukan, lakukan update
            $query = "UPDATE mahasiswa SET nama='$nama', nim='$nim', prodi='$prodi' WHERE id=$id";
            if ($conn->query($query) === TRUE) {
                echo json_encode(["message" => "Mahasiswa berhasil diperbarui"]);
            } else {
                echo json_encode(["error" => "Error: " . $conn->error]);
            }
        } else {
            echo json_encode(["error" => "Mahasiswa dengan ID $id tidak ditemukan"]);
        }
    } else {
        echo json_encode(["error" => "Data tidak lengkap"]);
    }
}


// Handler Delete
if ($_SERVER['REQUEST_METHOD'] == 'DELETE') {
    $database = json_decode(file_get_contents('php://input'), true);

    // Pastikan ID diberikan dalam body request
    if (isset($database['id'])) {
        $id = $database['id']; 
        
        if ($id != "") {
            $query = "DELETE FROM mahasiswa WHERE id=$id";
            if ($conn->query($query) === TRUE) {
                echo json_encode(["message" => "Mahasiswa berhasil dihapus"]);
            } else {
                echo json_encode(["message" => "Error: " . $conn->error]);
            }
        } else {
            echo json_encode(["error" => "ID tidak valid"]);
        }
    } else {
        echo json_encode(["error" => "ID tidak diberikan"]);
    }
}


// Handler GET (REad)
if ($_SERVER['REQUEST_METHOD'] == 'GET'){
    
    // Array untuk menampung data
    $response = [
        "mahasiswa" => [],
        "matkul" => []
    ];

    // Query data tabel `mahasiswa`
    $sql_mahasiswa = "SELECT * FROM mahasiswa";
    $result_mahasiswa = $conn->query($sql_mahasiswa);

    if ($result_mahasiswa->num_rows > 0) {
        while ($row = $result_mahasiswa->fetch_assoc()) {
            $response["mahasiswa"][] = $row;
        }
    }

    // Query data tabel `matkul`
    $sql_matkul = "SELECT * FROM matkul";
    $result_matkul = $conn->query($sql_matkul);

    if ($result_matkul->num_rows > 0) {
        while ($row = $result_matkul->fetch_assoc()) {
            $response["matkul"][] = $row;
        }
    }

    // Output data dalam format JSON
    echo json_encode($response, JSON_PRETTY_PRINT);
}
// Tutup koneksi
$conn->close();
?>
