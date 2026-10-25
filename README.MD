## Entity Relationship Diagram (ERD)

ERD berikut menggambarkan relasi antara lima tabel dalam
sistem Manajemen Tugas Mahasiswa.

![ERD Manajemen Tugas Mahasiswa](erd.webp)

# Manajemen Tugas Mahasiswa

REST API untuk mengelola tugas mahasiswa, mulai dari melihat daftar tugas, menambahkan tugas, memperbarui informasi tugas, hingga menghapus tugas.

## Informasi Proyek

- **Bahasa pemrograman:** Python
- **Framework:** Flask
- **ORM:** Flask-SQLAlchemy
- **Database:** PostgreSQL (Supabase)
- **Deployment:** Vercel
- **Format komunikasi:** JSON

### Link Proyek

- **GitHub Repository:** https://github.com/rifaiakbarnot-ops/manajemen-tugas-mahasiswa
- **Live API:** https://manajemen-tugas-mahasiswa-git-main-rifaiakbarnot-ops.vercel.app/

## Entity Relationship Diagram (ERD)

ERD menggambarkan hubungan antara lima tabel dalam database Manajemen Tugas Mahasiswa.

![ERD Manajemen Tugas Mahasiswa](erd.webp)

### Struktur Database

Database terdiri dari lima tabel:

1. **mahasiswa** — menyimpan data mahasiswa.
2. **mata_kuliah** — menyimpan data mata kuliah.
3. **status_tugas** — menyimpan daftar status tugas.
4. **prioritas** — menyimpan tingkat prioritas tugas.
5. **tugas** — menyimpan informasi tugas dan menghubungkannya dengan mahasiswa, mata kuliah, status, dan prioritas.

Tabel `tugas` memiliki primary key `tugas_id` dan foreign key `mahasiswa_id`, `mata_kuliah_id`, `status_id`, serta `prioritas_id`.

## Deployment

API dapat diakses melalui:

**Base URL**

https://manajemen-tugas-mahasiswa-git-main-rifaiakbarnot-ops.vercel.app/

Database menggunakan PostgreSQL pada Supabase. Konfigurasi koneksi database disimpan melalui environment variable `DATABASE_URL` di Vercel.

## Dokumentasi Endpoint

Semua endpoint mengembalikan respons dalam format JSON.

| Method | Endpoint            | Fungsi                                                    | Status sukses |
| ------ | ------------------- | --------------------------------------------------------- | ------------- |
| GET    | `/`                 | Informasi API                                             | 200           |
| GET    | `/db-check`         | Memeriksa koneksi database                                | 200           |
| GET    | `/tugas`            | Mendapatkan semua tugas                                   | 200           |
| GET    | `/tugas/<tugas_id>` | Mendapatkan satu tugas                                    | 200           |
| POST   | `/tugas`            | Menambahkan tugas                                         | 201           |
| PUT    | `/tugas/<tugas_id>` | Memperbarui seluruh field wajib dan field yang disertakan | 200           |
| PATCH  | `/tugas/<tugas_id>` | Memperbarui field tertentu                                | 200           |
| DELETE | `/tugas/<tugas_id>` | Menghapus tugas                                           | 200           |

### 1. GET — Semua Tugas

**Request**

`GET /tugas`

**Contoh response**

```json
{
  "data": [
    {
      "tugas_id": 1,
      "mahasiswa_id": 1,
      "mata_kuliah_id": 1,
      "status_id": 1,
      "prioritas_id": 3,
      "judul": "Latihan Soal Kalkulus I",
      "deskripsi": "Mengerjakan latihan soal untuk persiapan UTS.",
      "deadline": "2026-10-30T12:00:00",
      "tanggal_dibuat": "2026-10-25T13:05:22.747778",
      "link_tugas": null,
      "lokasi_pengumpulan": "Kertas Folio"
    }
  ]
}
```

Response aktual dapat berisi lebih dari satu data tugas.

### 2. GET — Satu Tugas

**Request**

`GET /tugas/1`

**Contoh response**

```json
{
  "data": {
    "tugas_id": 1,
    "mahasiswa_id": 1,
    "mata_kuliah_id": 1,
    "status_id": 1,
    "prioritas_id": 3,
    "judul": "Latihan Soal Kalkulus I",
    "deskripsi": "Mengerjakan latihan soal untuk persiapan UTS.",
    "deadline": "2026-10-30T12:00:00",
    "tanggal_dibuat": "2026-10-25T13:05:22.747778",
    "link_tugas": null,
    "lokasi_pengumpulan": "Kertas Folio"
  }
}
```

Jika tugas tidak ditemukan, API mengembalikan status `404 Not Found`.

### 3. POST — Menambahkan Tugas

**Request**

`POST /tugas`

Header:

`Content-Type: application/json`

**Request body**

```json
{
  "mahasiswa_id": 1,
  "mata_kuliah_id": 1,
  "status_id": 1,
  "prioritas_id": 2,
  "judul": "Tes API Vercel",
  "deskripsi": "Data untuk pengujian endpoint POST",
  "deadline": "2026-11-05T23:59:00",
  "link_tugas": null,
  "lokasi_pengumpulan": "Pengujian API"
}
```

**Contoh response — `201 Created`**

```json
{
  "judul": "Tes API Vercel",
  "message": "Tugas berhasil ditambahkan",
  "tugas_id": 6
}
```

ID yang diberikan database dapat berbeda pada pengujian berikutnya.

### 4. PUT — Memperbarui Tugas

**Request**

`PUT /tugas/6`

**Request body**

```json
{
  "mahasiswa_id": 1,
  "mata_kuliah_id": 1,
  "status_id": 2,
  "prioritas_id": 2,
  "judul": "Tes API Vercel - Diperbarui",
  "deskripsi": "Pengujian PUT berhasil",
  "deadline": "2026-11-06T23:59:00",
  "link_tugas": null,
  "lokasi_pengumpulan": "Pengujian API"
}
```

**Contoh response — `200 OK`**

```json
{
  "message": "Tugas berhasil diperbarui",
  "tugas_id": 6
}
```

PUT membutuhkan semua field wajib. Gunakan ID tugas yang benar-benar tersedia ketika melakukan pengujian.

### 5. PATCH — Memperbarui Sebagian Data

**Request**

`PATCH /tugas/1`

**Request body**

```json
{
  "judul": "Latihan Kalkulus I - Revisi"
}
```

**Contoh response — `200 OK`**

```json
{
  "message": "Tugas berhasil diperbarui",
  "tugas_id": 1
}
```

Contoh ini mengubah judul tugas nomor 1. Gunakan data uji jika tidak ingin mengubah data utama.

### 6. DELETE — Menghapus Tugas

**Request**

`DELETE /tugas/6`

**Contoh response — `200 OK`**

```json
{
  "message": "Tugas berhasil dihapus",
  "tugas_id": 6
}
```

Jika ID tugas tidak ditemukan, API mengembalikan status `404 Not Found`.

## Penanganan Error

API menggunakan status HTTP untuk menunjukkan hasil permintaan.

| Status | Keterangan                         |
| ------ | ---------------------------------- |
| 200    | Permintaan berhasil                |
| 201    | Data berhasil dibuat               |
| 400    | Request atau data tidak valid      |
| 404    | Data tugas tidak ditemukan         |
| 500    | Pemeriksaan koneksi database gagal |

Contoh response error:

```json
{
  "error": "Tugas tidak ditemukan"
}
```

## Cara Menjalankan Secara Lokal

### 1. Clone repository

```bash
git clone https://github.com/rifaiakbarnot-ops/manajemen-tugas-mahasiswa.git
cd manajemen-tugas-mahasiswa
```

### 2. Buat virtual environment

```bash
python -m venv .venv
```

Aktifkan di Git Bash pada Windows:

```bash
source .venv/Scripts/activate
```

### 3. Instal dependensi

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi environment variable

Buat file `.env` di direktori utama proyek:

```env
DATABASE_URL=URL_KONEKSI_POSTGRESQL_KAMU
```

Ganti nilai contoh dengan connection string PostgreSQL milikmu. Jangan mengunggah file `.env` ke GitHub atau membagikan kredensial database.

### 5. Jalankan aplikasi

```bash
python -m flask --app run.py run
```

Aplikasi lokal dapat diakses melalui:

`http://127.0.0.1:5000`

Periksa koneksi database di:

`http://127.0.0.1:5000/db-check`

## Pengujian API

Pengujian dilakukan menggunakan Thunder Client pada URL deployment Vercel.

| Pengujian                          | Hasil                                  |
| ---------------------------------- | -------------------------------------- |
| GET `/tugas`                       | Berhasil menampilkan daftar tugas      |
| GET `/tugas/1`                     | Berhasil menampilkan satu tugas        |
| POST `/tugas`                      | Berhasil menambahkan tugas, status 201 |
| PUT `/tugas/6`                     | Berhasil memperbarui tugas, status 200 |
| DELETE `/tugas/6`                  | Berhasil menghapus tugas, status 200   |
| GET `/tugas/6` setelah penghapusan | Mengembalikan 404 Not Found            |

Screenshot hasil pengujian dilampirkan sebagai bukti pengujian API.

## Keamanan

- Kredensial database disimpan melalui environment variable.
- File `.env` dikecualikan dari Git menggunakan `.gitignore`.
- Request untuk menambahkan dan memperbarui data divalidasi.
- API mengembalikan status HTTP dan pesan error yang sesuai.

## Penutup

Proyek ini dibuat sebagai implementasi REST API menggunakan Flask dan PostgreSQL untuk mengelola tugas mahasiswa. Aplikasi mendukung operasi CRUD, menggunakan relasi antartabel, serta di-deploy agar dapat diakses melalui internet.
