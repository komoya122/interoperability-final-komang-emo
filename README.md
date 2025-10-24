# 🏫 Campus Event Registration API

**UTS Interoperabilitas – Komang Emo**

Proyek ini merupakan implementasi sistem **pendaftaran acara kampus (Campus Event Registration System)** menggunakan **FastAPI** dan **SQLite**.  
Sistem ini memungkinkan admin membuat dan mengelola acara, serta peserta untuk mendaftar ke acara yang tersedia.

---

## 🚀 Fitur Utama

✅ REST API berbasis **FastAPI**  
✅ CRUD Data Event (Create, Read, Update, Delete)  
✅ Registrasi peserta ke acara  
✅ Autentikasi token sederhana untuk admin  
✅ Database **SQLite** via SQLAlchemy ORM  
✅ Dokumentasi otomatis via Swagger UI (`/docs`)  
✅ Dapat diakses dari **frontend HTML** atau **Postman**

---

## 🧩 Struktur Proyek

interoperability-final-komang-emo/
├─ Backend/
│ ├─ init.py
│ ├─ main.py
│ ├─ models.py
│ ├─ schemas.py
│ ├─ database.py
│ └─ create_db.sql
└─ frontend/
└─ index.html

---

## ⚙️ Instalasi dan Menjalankan Server

### 1️⃣ Clone repository

```bash
git clone https://github.com/<username>/interoperability-final-komang-emo.git
cd interoperability-final-komang-emo/Backend
```

### 2️⃣ Buat virtual environment dan install dependency

```bash
python -m venv .venv
# Aktifkan environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

```bash
# Install dependency
pip install fastapi uvicorn sqlalchemy pydantic email-validator python-multipart
```

### 3️⃣ Jalankan server FastAPI

Masuk ke direktori utama proyek:

```bash
cd .. #Direktori utama
uvicorn Backend.main:app --reload
```

### 🧠 Dokumentasi API

Swagger UI otomatis tersedia di:
👉 http://127.0.0.1:8000/docs

### 🔐 Autentikasi Admin

Untuk menambah, mengedit, dan menghapus event, API membutuhkan header:

```pgsql
x-admin-token: secret-admin-token
```

### 🧪 Contoh Pengujian API (Postman)

1️⃣ GET /events

Deskripsi: Ambil semua data event
Method: GET
URL: http://127.0.0.1:8000/events

2️⃣ POST /events

Deskripsi: Tambah event baru (hanya admin)
Method: POST
Headers:

```pgsql
x-admin-token: secret-admin-token
Content-Type: application/json
```

Body(JSON):

```json
{
  "title": "Workshop AI",
  "date": "2025-11-01",
  "location": "Lab Computer Vision",
  "quota": 30
}
```

3️⃣ POST /register

Deskripsi: Daftar sebagai peserta event
Method: POST
Body (JSON):

```json
{
  "name": "Komang Emo",
  "email": "komang@example.com",
  "event_id": 1
}
```

4️⃣ GET /participants

Deskripsi: Ambil semua peserta terdaftar
Method: GET
URL: http://127.0.0.1:8000/participants

5️⃣ DELETE /events/{id}

Deskripsi: Hapus event berdasarkan ID (hanya admin)
Headers:

```pgsql
x-admin-token: secret-admin-token
```

### 💻 Frontend (index.html)

File frontend sederhana (frontend/index.html) dapat digunakan untuk:

- Menampilkan daftar event

- Mengisi form pendaftaran peserta

- Mengirim data ke endpoint /register

- Frontend ini menggunakan Fetch API untuk komunikasi dengan backend FastAPI.

### 🧰 Teknologi yang Digunakan

| Komponen          | Teknologi        |
| ----------------- | ---------------- |
| Backend Framework | FastAPI          |
| Database          | SQLite           |
| ORM               | SQLAlchemy       |
| Data Validation   | Pydantic         |
| Frontend          | HTML + Fetch API |
| Testing           | Postman          |

### 📸 Dokumentasi Tambahan

Screenshot Swagger UI (/docs)
![Swagger UI](<Media/swagger(ui).png>)
Screenshot Postman pengujian API
![Swagger UI](<Media/swagger(ui).png>)
Screenshot tampilan frontend (opsional)
![Swagger UI](<Media/swagger(ui).png>)
