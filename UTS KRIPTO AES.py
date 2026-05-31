import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def beri_padding(data):
    jumlah_pad = 16 - (len(data) % 16)
    return data + bytes([jumlah_pad] * jumlah_pad)

def hapus_padding(data):
    jumlah_pad = data[-1]
    return data[:-jumlah_pad]

def proses_enkripsi():
    path_file = entry_file.get().strip()
    password = entry_password.get()
    
    if not path_file or path_file == "Pilih file atau ketik lokasi file..." or not password or password == "Masukkan kata sandi Anda":
        messagebox.showwarning("Peringatan", "File dan Kata Sandi tidak boleh kosong!")
        return

    try:
        kunci = SHA256.new(password.encode()).digest()
        cipher = AES.new(kunci, AES.MODE_CBC)
        iv = cipher.iv
        
        with open(path_file, 'rb') as f:
            data_asli = f.read()
            
        data_terpad = beri_padding(data_asli)
        data_rahasia = cipher.encrypt(data_terpad)
        
        with open(path_file + ".enc", 'wb') as f:
            f.write(iv)
            f.write(data_rahasia)
            
        messagebox.showinfo("Sukses", "File BERHASIL dienkripsi!")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

def proses_dekripsi():
    path_file = entry_file.get().strip()
    password = entry_password.get()
    
    if not path_file or path_file == "Pilih file atau ketik lokasi file..." or not password or password == "Masukkan kata sandi Anda":
        messagebox.showwarning("Peringatan", "File dan Kata Sandi tidak boleh kosong!")
        return

    try:
        kunci = SHA256.new(password.encode()).digest()
        
        with open(path_file, 'rb') as f:
            iv = f.read(16)
            data_rahasia = f.read()
            
        cipher = AES.new(kunci, AES.MODE_CBC, iv=iv)
        data_terdekripsi = cipher.decrypt(data_rahasia)
        data_asli = hapus_padding(data_terdekripsi)
        
        nama_file_baru = path_file.replace(".enc", "")
        nama, ekstensi = os.path.splitext(nama_file_baru)
        file_output = f"{nama}_restored{ekstensi}"
        
        with open(file_output, 'wb') as f:
            f.write(data_asli)
            
        messagebox.showinfo("Sukses", "File BERHASIL didekripsi!")
    except Exception:
        messagebox.showerror("Gagal", "Kata sandi salah atau file rusak!")

def unggah_file():
    nama_file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if nama_file:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, nama_file)
        entry_file.config(fg="#111111")

def hapus_placeholder_file(event):
    if entry_file.get() == "Pilih file atau ketik lokasi file...":
        entry_file.delete(0, tk.END)
        entry_file.config(fg="#111111")

def hapus_placeholder_pass(event):
    if entry_password.get() == "Masukkan kata sandi Anda":
        entry_password.delete(0, tk.END)
        entry_password.config(show="*", fg="#111111")

root = tk.Tk()
root.title("Aplikasi Enkripsi AES")
root.geometry("600x520")
root.configure(bg="#F4EFEA")

card = tk.Canvas(root, bg="#F4EFEA", highlightthickness=0)
card.pack(fill="both", expand=True, padx=40, pady=30)

card.create_rounded_rectangle = lambda x1, y1, x2, y2, r, **kwargs: card.create_polygon(
    x1+r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y2-r, x2, y2, x2-r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y1+r, x1, y1, 
    smooth=True, **kwargs
)
card.create_rounded_rectangle(10, 10, 510, 450, 30, fill="white")

lbl_judul = tk.Label(root, text="Aplikasi Enkripsi AES", font=("Poppins", 18, "bold"), bg="white", fg="#111111")
card.create_window(260, 50, window=lbl_judul)

lbl_pilih = tk.Label(root, text="Pilih File", font=("Poppins", 11, "bold"), bg="white", fg="#222222")
card.create_window(70, 110, window=lbl_pilih)

entry_file = tk.Entry(root, font=("Poppins", 11), bg="#F8F9FA", fg="#A0A0A0", bd=1, relief="solid", width=30)
entry_file.insert(0, "Pilih file atau ketik lokasi file...")
entry_file.bind("<FocusIn>", hapus_placeholder_file)
card.create_window(195, 145, window=entry_file, height=38)

btn_upload = tk.Button(root, text="📤 Upload File", font=("Poppins", 10, "bold"), bg="#E1E3E6", fg="#111111", bd=0, cursor="hand2", command=unggah_file, width=12)
card.create_window(410, 145, window=btn_upload, height=38)

lbl_sandi = tk.Label(root, text="Kata Sandi", font=("Poppins", 11, "bold"), bg="white", fg="#222222")
card.create_window(77, 210, window=lbl_sandi)

entry_password = tk.Entry(root, font=("Poppins", 11), bg="#F8F9FA", fg="#A0A0A0", bd=1, relief="solid", width=44)
entry_password.insert(0, "Masukkan kata sandi Anda")
entry_password.bind("<FocusIn>", hapus_placeholder_pass)
card.create_window(260, 245, window=entry_password, height=38)

btn_enkrip = tk.Button(root, text="🔒 Enkripsi File", font=("Poppins", 11, "bold"), bg="#721C24", fg="white", bd=0, cursor="hand2", command=proses_enkripsi, width=19)
card.create_window(145, 340, window=btn_enkrip, height=45)

btn_dekrip = tk.Button(root, text="🔓 Dekripsi File", font=("Poppins", 11, "bold"), bg="#00B074", fg="white", bd=0, cursor="hand2", command=proses_dekripsi, width=19)
card.create_window(375, 340, window=btn_dekrip, height=45)

lbl_footer = tk.Label(root, text="Mendukung format: .txt saja", font=("Poppins", 9), bg="white", fg="#A0A0A0")
card.create_window(260, 410, window=lbl_footer)

root.mainloop()