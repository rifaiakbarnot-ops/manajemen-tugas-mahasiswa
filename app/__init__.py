import os
from flask import Flask, request
from dotenv import load_dotenv
from sqlalchemy import text
from app.extensions import db

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Memuat model agar dikenali SQLAlchemy
    from app.models import Tugas

    @app.route("/", methods=["GET"])
    def index():
        return {
            "status": "success",
            "message": "Selamat datang di API Flask & Supabase!"
        }, 200

    @app.route("/db-check", methods=["GET"])
    def check_db():
        try:
            db.session.execute(text("SELECT 1"))
            return {
                "status": "success",
                "database": "Terhubung ke Supabase!"
            }, 200
        except Exception:
            db.session.rollback()
            return {"error": "Koneksi database gagal"}, 500

    # GET semua tugas
    @app.route("/tugas", methods=["GET"])
    def get_tugas():
        tugas_list = Tugas.query.order_by(Tugas.tugas_id).all()
        return {
            "data": [
                {
                    "tugas_id": t.tugas_id,
                    "mahasiswa_id": t.mahasiswa_id,
                    "mata_kuliah_id": t.mata_kuliah_id,
                    "status_id": t.status_id,
                    "prioritas_id": t.prioritas_id,
                    "judul": t.judul,
                    "deskripsi": t.deskripsi,
                    "deadline": t.deadline.isoformat(),
                    "tanggal_dibuat": (
                        t.tanggal_dibuat.isoformat()
                        if t.tanggal_dibuat else None
                    ),
                    "link_tugas": t.link_tugas,
                    "lokasi_pengumpulan": t.lokasi_pengumpulan
                }
                for t in tugas_list
            ]
        }, 200

    # GET satu tugas
    @app.route("/tugas/<int:tugas_id>", methods=["GET"])
    def get_satu_tugas(tugas_id):
        t = db.session.get(Tugas, tugas_id)

        if t is None:
            return {"error": "Tugas tidak ditemukan"}, 404

        return {
            "data": {
                "tugas_id": t.tugas_id,
                "mahasiswa_id": t.mahasiswa_id,
                "mata_kuliah_id": t.mata_kuliah_id,
                "status_id": t.status_id,
                "prioritas_id": t.prioritas_id,
                "judul": t.judul,
                "deskripsi": t.deskripsi,
                "deadline": t.deadline.isoformat(),
                "tanggal_dibuat": (
                    t.tanggal_dibuat.isoformat()
                    if t.tanggal_dibuat else None
                ),
                "link_tugas": t.link_tugas,
                "lokasi_pengumpulan": t.lokasi_pengumpulan
            }
        }, 200

    # POST tugas baru
    @app.route("/tugas", methods=["POST"])
    def tambah_tugas():
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return {"error": "Request body harus berupa JSON"}, 400

        required = [
            "mahasiswa_id", "mata_kuliah_id", "status_id",
            "prioritas_id", "judul", "deadline"
        ]

        missing = [
            field for field in required
            if field not in data or data[field] is None or data[field] == ""
        ]

        if missing:
            return {
                "error": "Field wajib belum diisi",
                "fields": missing
            }, 400

        from datetime import datetime

        try:
            deadline = datetime.fromisoformat(data["deadline"])
            tugas = Tugas(
                mahasiswa_id=data["mahasiswa_id"],
                mata_kuliah_id=data["mata_kuliah_id"],
                status_id=data["status_id"],
                prioritas_id=data["prioritas_id"],
                judul=data["judul"],
                deskripsi=data.get("deskripsi"),
                deadline=deadline,
                link_tugas=data.get("link_tugas"),
                lokasi_pengumpulan=data.get("lokasi_pengumpulan")
            )

            db.session.add(tugas)
            db.session.commit()

            return {
                "message": "Tugas berhasil ditambahkan",
                "tugas_id": tugas.tugas_id,
                "judul": tugas.judul
            }, 201

        except ValueError:
            db.session.rollback()
            return {
                "error": "Format deadline tidak valid. Gunakan YYYY-MM-DDTHH:MM:SS"
            }, 400
        except Exception:
            db.session.rollback()
            return {
                "error": "Gagal menambahkan tugas. Periksa ID relasi dan data."
            }, 400

    # PUT/PATCH memperbarui tugas
    @app.route("/tugas/<int:tugas_id>", methods=["PUT", "PATCH"])
    def ubah_tugas(tugas_id):
        t = db.session.get(Tugas, tugas_id)

        if t is None:
            return {"error": "Tugas tidak ditemukan"}, 404

        data = request.get_json(silent=True)

        if not isinstance(data, dict) or not data:
            return {"error": "Request body JSON tidak boleh kosong"}, 400

        allowed = [
            "mahasiswa_id", "mata_kuliah_id", "status_id",
            "prioritas_id", "judul", "deskripsi", "deadline",
            "link_tugas", "lokasi_pengumpulan"
        ]

        if request.method == "PUT":
            required = [
                "mahasiswa_id", "mata_kuliah_id", "status_id",
                "prioritas_id", "judul", "deadline"
            ]
            missing = [
                f for f in required if f not in data or data[f] in (None, "")]
            if missing:
                return {
                    "error": "PUT membutuhkan semua field wajib",
                    "fields": missing
                }, 400

        try:
            from datetime import datetime

            for field in allowed:
                if field in data:
                    value = data[field]
                    if field == "deadline":
                        value = datetime.fromisoformat(value)
                    setattr(t, field, value)

            db.session.commit()
            return {
                "message": "Tugas berhasil diperbarui",
                "tugas_id": t.tugas_id
            }, 200

        except ValueError:
            db.session.rollback()
            return {"error": "Format deadline tidak valid"}, 400
        except Exception:
            db.session.rollback()
            return {"error": "Gagal memperbarui tugas. Periksa data dan ID relasi."}, 400

    # DELETE tugas
    @app.route("/tugas/<int:tugas_id>", methods=["DELETE"])
    def hapus_tugas(tugas_id):
        t = db.session.get(Tugas, tugas_id)

        if t is None:
            return {"error": "Tugas tidak ditemukan"}, 404

        try:
            db.session.delete(t)
            db.session.commit()
            return {
                "message": "Tugas berhasil dihapus",
                "tugas_id": tugas_id
            }, 200
        except Exception:
            db.session.rollback()
            return {"error": "Gagal menghapus tugas"}, 400

    return app
