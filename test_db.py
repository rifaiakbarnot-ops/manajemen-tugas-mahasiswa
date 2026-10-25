
import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    print("ERROR: DATABASE_URL tidak ditemukan di file .env")
else:
    try:
        with psycopg.connect(database_url, connect_timeout=10) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                result = cur.fetchone()

                if result is not None:
                    print("BERHASIL! Terhubung ke Supabase PostgreSQL.")
                    print("Hasil tes:", result[0])
                else:
                    print("Koneksi berhasil, tetapi hasil query kosong.")

    except Exception as e:
        print("Koneksi gagal.")
        print("Jenis error:", type(e).__name__)
        print("Detail:", str(e).splitlines()[0])
