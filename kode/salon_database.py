import sqlite3
import datetime

class SalonDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("sekayu.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                telepon TEXT,
                waktu DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS booking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                tanggal TEXT NOT NULL,
                treatment TEXT NOT NULL,
                harga INTEGER NOT NULL,
                waktu_booking DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS treatment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL UNIQUE,
                harga INTEGER NOT NULL
            )
        """)

        self.conn.commit()
        self._init_treatment_data()

    def _init_treatment_data(self):
        treatments = [
            ("Potong Rambut (Boys)", 20000),
            ("Potong Rambut (Girls)", 25000),
            ("Hair Coloring", 350000),
            ("Smoothing", 250000),
            ("Facial", 60000),
            ("Creambath", 60000),
            ("Hair Mask", 70000),
            ("Keratin", 350000),
            ("Cuci Catok", 45000),
            ("Cuci Blow", 45000)
        ]
        
        self.cursor.execute("SELECT COUNT(*) FROM treatment")
        if self.cursor.fetchone()[0] == 0:
            print("Menginisialisasi data treatment...")
            for nama, harga in treatments:
                self.cursor.execute(
                    "INSERT INTO treatment (nama, harga) VALUES (?, ?)",
                    (nama, harga)
                )
            self.conn.commit()

    # ---- QUEUE ----
    def add_queue(self, nama, telepon=""):
        self.cursor.execute(
            "INSERT INTO queue (nama, telepon) VALUES (?, ?)",
            (nama, telepon)
        )
        self.conn.commit()

    def get_queue(self):
        self.cursor.execute("SELECT id, nama, telepon, waktu FROM queue ORDER BY id ASC")
        return self.cursor.fetchall()

    def remove_queue_by_id(self, queue_id):
        self.cursor.execute("DELETE FROM queue WHERE id = ?", (queue_id,))
        self.conn.commit()

    # ---- BOOKING ----
    def add_booking(self, nama, tanggal, treatment, harga, telepon=""):
        self.cursor.execute(
            "INSERT INTO booking (nama, tanggal, treatment, harga) VALUES (?, ?, ?, ?)",
            (nama, tanggal, treatment, harga)
        )
        self.add_queue(nama, telepon)
        self.conn.commit()

    def get_booking(self):
        self.cursor.execute("SELECT id, nama, tanggal, treatment, harga, waktu_booking FROM booking")
        return self.cursor.fetchall()

    # ---- TREATMENT ----
    def get_all_treatments(self):
        self.cursor.execute("SELECT nama, harga FROM treatment ORDER BY harga ASC")
        return self.cursor.fetchall()

    def get_treatment_price(self, treatment_name):
        self.cursor.execute("SELECT harga FROM treatment WHERE nama = ?", (treatment_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None
