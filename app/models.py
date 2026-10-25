from app.extensions import db


class Mahasiswa(db.Model):
    __tablename__ = "mahasiswa"

    mahasiswa_id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))


class MataKuliah(db.Model):
    __tablename__ = "mata_kuliah"

    matkul_id = db.Column(db.Integer, primary_key=True)
    kode_matkul = db.Column(db.String(20), unique=True, nullable=False)
    nama_matkul = db.Column(db.String(100), nullable=False)
    sks = db.Column(db.Integer, nullable=False)


class StatusTugas(db.Model):
    __tablename__ = "status_tugas"

    status_id = db.Column(db.Integer, primary_key=True)
    nama_status = db.Column(db.String(50), unique=True, nullable=False)


class Prioritas(db.Model):
    __tablename__ = "prioritas"

    prioritas_id = db.Column(db.Integer, primary_key=True)
    nama_prioritas = db.Column(db.String(30), unique=True, nullable=False)


class Tugas(db.Model):
    __tablename__ = "tugas"

    tugas_id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(
        db.Integer, db.ForeignKey("mahasiswa.mahasiswa_id"), nullable=False
    )
    mata_kuliah_id = db.Column(
        db.Integer, db.ForeignKey("mata_kuliah.matkul_id"), nullable=False
    )
    status_id = db.Column(
        db.Integer, db.ForeignKey("status_tugas.status_id"), nullable=False
    )
    prioritas_id = db.Column(
        db.Integer, db.ForeignKey("prioritas.prioritas_id"), nullable=False
    )
    judul = db.Column(db.String(200), nullable=False)
    deskripsi = db.Column(db.Text)
    deadline = db.Column(db.DateTime, nullable=False)
    tanggal_dibuat = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
    link_tugas = db.Column(db.String(500))
    lokasi_pengumpulan = db.Column(db.String(500))
