from salon_database import Database

db = Database()

# Hapus data treatment lama
db.cursor.execute("DELETE FROM treatment")

# Data treatment baru
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

for name, price in treatments:
    db.cursor.execute("INSERT INTO treatment (nama, harga) VALUES (?, ?)", (name, price))

db.conn.commit()
db.conn.close()

print("✔ Data treatment berhasil di-reset & dimasukkan ulang!")
