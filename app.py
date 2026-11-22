import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "kunci-rahasia-portofolio-hafiz"

DATA_FILE = "data.json"
ADMIN_USER = "X-NOVA15"
ADMIN_PASS = "Deftones1945"

# Data awal otomatis jika data.json belum ada
DEFAULT_DATA = {
    "profil": {
        "nama": "Muhammad Hafiz Fuadhi",
        "role": "Junior Web Developer",
        "bio": "Mahasiswa S1 Informatika di Universitas Nahdlatul Ulama Yogyakarta (lulusan MA) yang memiliki minat besar di bidang IT, Pengembangan Web, dan Cyber Security.",
        "email": "muhammadhafizfuadhi@gmail.com",
        "github": "X-NOVA15",
        "whatsapp": "6281234567890"
    },
    "skills": [
        {"id": 1, "nama": "Python", "level": "Menengah"},
        {"id": 2, "nama": "Dasar Jaringan Komputer", "level": "Dasar"},
        {"id": 3, "nama": "HTML & CSS", "level": "Dasar"}
    ],
    "proyek": [
        {
            "id": 1,
            "judul": "Kalkulator Sederhana Menggunakan Python",
            "kategori": "Python CLI",
            "deskripsi": "Mengembangkan program kalkulator sederhana menggunakan bahasa pemrograman Python untuk menghitung luas berbagai bangun datar dengan menerapkan rumus matematika dan algoritma pemrograman.",
            "link": "https://github.com/X-NOVA15"
        },
        {
            "id": 2,
            "judul": "Implementasi Algoritma Sorting Menggunakan Python",
            "kategori": "Algoritma",
            "deskripsi": "Membuat program untuk mengurutkan sekumpulan data menggunakan bahasa pemrograman Python dengan menerapkan algoritma pengurutan (sorting).",
            "link": "https://github.com/X-NOVA15"
        },
        {
            "id": 3,
            "judul": "Sistem Laporan Barang Toko Menggunakan Python",
            "kategori": "Struktur Data",
            "deskripsi": "Mengembangkan program pengelolaan data barang toko menggunakan struktur data List dan Dictionary untuk menyimpan, mengelola, dan menampilkan informasi barang.",
            "link": "https://github.com/X-NOVA15"
        },
        {
            "id": 4,
            "judul": "Landing Page Website UMKM DhewokCraft",
            "kategori": "Web Development",
            "deskripsi": "Mengembangkan halaman website (landing page) untuk UMKM DhewokCraft sebagai media informasi dan pengenalan produk serta identitas usaha secara digital.",
            "link": "https://github.com/X-NOVA15"
        }
    ],
    "pendidikan": [
        {"id": 1, "institusi": "Universitas Nahdlatul Ulama Yogyakarta", "jurusan": "S1 Informatika", "tahun": "Mahasiswa Aktif"},
        {"id": 2, "institusi": "Madrasah Aliyah (MA)", "jurusan": "Lulusan Madrasah Aliyah", "tahun": "Lulus"}
    ]
}

# --- FUNGSI BANTUAN JSON (READ & WRITE) ---
def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# --- HALAMAN PUBLIK (READ) ---
# --- HALAMAN PUBLIK (READ) ---
@app.route("/")
def index():
    data = load_data()
    urutan_level = {"Dasar": 1, "Menengah": 2, "Mahir": 3}
    data["skills"] = sorted(
        data["skills"],
        key=lambda s: urutan_level.get(s["level"], 99)
    )
    return render_template("index.html", data=data)

# --- AUTENTIKASI LOGIN & LOGOUT ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USER and password == ADMIN_PASS:
            session["logged_in"] = True
            flash("Berhasil login ke Dasbor Pengelola!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Username atau Password salah!", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Anda telah keluar dari dasbor.", "info")
    return redirect(url_for("index"))

# --- HALAMAN DASBOR PENGELOLA ---
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        flash("Silakan login terlebih dahulu!", "warning")
        return redirect(url_for("login"))

    data = load_data()
    return render_template("dashboard.html", data=data)

# --- UPDATE PROFIL UTAMA ---
@app.route("/profil/update", methods=["POST"])
def update_profil():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    nama = request.form.get("nama", "").strip()
    role = request.form.get("role", "").strip()
    bio = request.form.get("bio", "").strip()
    email = request.form.get("email", "").strip()
    github = request.form.get("github", "").strip()
    whatsapp = request.form.get("whatsapp", "").strip()

    # Ubah awalan 0 menjadi 62 otomatis agar link wa.me valid
    if whatsapp.startswith("0"):
        whatsapp = "62" + whatsapp[1:]

    if not nama or not role or not bio:
        flash("Nama, Role, dan Bio wajib diisi!", "danger")
        return redirect(url_for("dashboard"))

    data = load_data()
    data["profil"] = {
        "nama": nama,
        "role": role,
        "bio": bio,
        "email": email,
        "github": github,
        "whatsapp": whatsapp
    }
    save_data(data)
    flash("Profil dan kontak berhasil diperbarui!", "success")
    return redirect(url_for("dashboard"))
# --- CRUD PROYEK (CREATE, UPDATE, DELETE) ---
@app.route("/proyek/tambah", methods=["POST"])
def tambah_proyek():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    judul = request.form.get("judul", "").strip()
    kategori = request.form.get("kategori", "").strip()
    deskripsi = request.form.get("deskripsi", "").strip()
    link = request.form.get("link", "").strip() or "#"

    if not judul or not kategori or not deskripsi:
        flash("Judul, Kategori, dan Deskripsi proyek wajib diisi!", "danger")
        return redirect(url_for("dashboard"))

    data = load_data()
    new_id = max([p["id"] for p in data["proyek"]], default=0) + 1
    data["proyek"].append({
        "id": new_id,
        "judul": judul,
        "kategori": kategori,
        "deskripsi": deskripsi,
        "link": link
    })
    save_data(data)
    flash("Proyek baru berhasil ditambahkan!", "success")
    return redirect(url_for("dashboard"))

@app.route("/proyek/edit/<int:item_id>", methods=["POST"])
def edit_proyek(item_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    judul = request.form.get("judul", "").strip()
    kategori = request.form.get("kategori", "").strip()
    deskripsi = request.form.get("deskripsi", "").strip()
    link = request.form.get("link", "").strip() or "#"

    if not judul or not kategori or not deskripsi:
        flash("Field proyek tidak boleh kosong saat diedit!", "danger")
        return redirect(url_for("dashboard"))

    data = load_data()
    for p in data["proyek"]:
        if p["id"] == item_id:
            p["judul"] = judul
            p["kategori"] = kategori
            p["deskripsi"] = deskripsi
            p["link"] = link
            break
    save_data(data)
    flash("Data proyek berhasil diperbarui!", "success")
    return redirect(url_for("dashboard"))

@app.route("/proyek/hapus/<int:item_id>", methods=["POST"])
def hapus_proyek(item_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    data = load_data()
    data["proyek"] = [p for p in data["proyek"] if p["id"] != item_id]
    save_data(data)
    flash("Proyek berhasil dihapus!", "info")
    return redirect(url_for("dashboard"))

# --- CRUD SKILLS (CREATE, UPDATE, DELETE) ---
@app.route("/skill/tambah", methods=["POST"])
def tambah_skill():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    nama = request.form.get("nama", "").strip()
    level = request.form.get("level", "").strip()

    if not nama or not level:
        flash("Nama skill dan tingkat keahlian wajib diisi!", "danger")
        return redirect(url_for("dashboard"))

    data = load_data()
    new_id = max([s["id"] for s in data["skills"]], default=0) + 1
    data["skills"].append({"id": new_id, "nama": nama, "level": level})
    save_data(data)
    flash("Skill berhasil ditambahkan!", "success")
    return redirect(url_for("dashboard"))

@app.route("/skill/edit/<int:item_id>", methods=["POST"])
def edit_skill(item_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    nama = request.form.get("nama", "").strip()
    level = request.form.get("level", "").strip()

    if not nama or not level:
        flash("Nama skill tidak boleh kosong!", "danger")
        return redirect(url_for("dashboard"))

    data = load_data()
    for s in data["skills"]:
        if s["id"] == item_id:
            s["nama"] = nama
            s["level"] = level
            break
    save_data(data)
    flash("Skill berhasil diperbarui!", "success")
    return redirect(url_for("dashboard"))

@app.route("/skill/hapus/<int:item_id>", methods=["POST"])
def hapus_skill(item_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    data = load_data()
    data["skills"] = [s for s in data["skills"] if s["id"] != item_id]
    save_data(data)
    flash("Skill berhasil dihapus!", "info")
    return redirect(url_for("dashboard"))

# --- CRUD PENDIDIKAN (CREATE, UPDATE, DELETE) ---
@app.route("/pendidikan/tambah", methods=["POST"])
def tambah_pendidikan():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    institusi = request.form.get("institusi", "").strip()
    jurusan = request.form.get("jurusan", "").strip()
    tahun = request.form.get("tahun", "").strip()

    if not institusi or not jurusan or not tahun:
        flash("Semua field pendidikan wajib diisi!", "danger")
        return redirect(url_for("dashboard"))

    data = load_data()
    new_id = max([edu["id"] for edu in data["pendidikan"]], default=0) + 1
    data["pendidikan"].append({"id": new_id, "institusi": institusi, "jurusan": jurusan, "tahun": tahun})
    save_data(data)
    flash("Riwayat pendidikan berhasil ditambahkan!", "success")
    return redirect(url_for("dashboard"))

@app.route("/pendidikan/edit/<int:item_id>", methods=["POST"])
def edit_pendidikan(item_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    institusi = request.form.get("institusi", "").strip()
    jurusan = request.form.get("jurusan", "").strip()
    tahun = request.form.get("tahun", "").strip()

    if not institusi or not jurusan or not tahun:
        flash("Field pendidikan tidak boleh kosong!", "danger")
        return redirect(url_for("dashboard"))

    data = load_data()
    for edu in data["pendidikan"]:
        if edu["id"] == item_id:
            edu["institusi"] = institusi
            edu["jurusan"] = jurusan
            edu["tahun"] = tahun
            break
    save_data(data)
    flash("Riwayat pendidikan berhasil diperbarui!", "success")
    return redirect(url_for("dashboard"))

@app.route("/pendidikan/hapus/<int:item_id>", methods=["POST"])
def hapus_pendidikan(item_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    data = load_data()
    data["pendidikan"] = [edu for edu in data["pendidikan"] if edu["id"] != item_id]
    save_data(data)
    flash("Riwayat pendidikan berhasil dihapus!", "info")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)