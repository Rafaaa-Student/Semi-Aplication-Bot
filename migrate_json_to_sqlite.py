import json
import os
from database import init_db, add_book

# Path ke file JSON lama
JSON_FILE = "database_buku_log.json"
BACKUP_FILE = "database_buku_log.json.backup"

def migrate():
    """Migrasi data buku dari JSON ke SQLite"""
    
    # Inisialisasi database SQLite
    print("🔄 Menginisialisasi database SQLite...")
    init_db()
    
    # Cek apakah file JSON ada
    if not os.path.exists(JSON_FILE):
        print(f"⚠️ File {JSON_FILE} tidak ditemukan. Tidak ada data untuk dimigrasi.")
        return
    
    # Load data dari JSON
    print(f"📖 Membaca data dari {JSON_FILE}...")
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            data_buku = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ Error: File {JSON_FILE} tidak valid atau kosong.")
            return
    
    if not data_buku:
        print("⚠️ File JSON kosong. Tidak ada data untuk dimigrasi.")
        return
    
    # Backup file JSON lama
    print(f"💾 Membuat backup ke {BACKUP_FILE}...")
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(data_buku, f, indent=4, ensure_ascii=False)
    
    # Migrasi data ke SQLite
    print(f"🚀 Memulai migrasi {len(data_buku)} buku ke SQLite...")
    berhasil = 0
    gagal = 0
    
    for buku in data_buku:
        try:
            judul = buku.get("judul", "")
            harga = buku.get("harga", "N/A")
            deskripsi = buku.get("deskripsi", "N/A")
            url = buku.get("url", "")
            
            if judul:  # Pastikan judul tidak kosong
                add_book(judul, harga, deskripsi, url)
                berhasil += 1
            else:
                gagal += 1
        except Exception as e:
            print(f"❌ Error migrasi buku: {e}")
            gagal += 1
    
    print(f"\n✅ Migrasi selesai!")
    print(f"   Berhasil: {berhasil} buku")
    print(f"   Gagal: {gagal} buku")
    print(f"\n📝 File JSON lama telah di-backup ke: {BACKUP_FILE}")
    print(f"   Anda dapat menghapus {JSON_FILE} jika sudah yakin migrasi berhasil.")

if __name__ == "__main__":
    migrate()
