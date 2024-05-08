import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog

def veritabani_olustur():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def kullanici_kayit(username, password):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    except sqlite3.IntegrityError:
        return False
    conn.commit()
    conn.close()
    return True

def check_user(username, password):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result and result[0] == password

def sifreyi_guncelle(username, new_password):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
    conn.commit()
    conn.close()

def dosya_oku(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def jaccard_benzerligi(text1, text2):
    set1 = set(text1.split())
    set2 = set(text2.split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0

def basit_esleme(text1, text2):
    words1 = text1.split()
    words2 = text2.split()
    matches = sum(1 for word in words1 if word in words2)
    total = len(words1) + len(words2)
    return (2 * matches) / total if total else 0

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Login ekrani')
        self.geometry('300x200')
        self.widget_olustur()

    def widget_olustur(self):
        self.username_label = tk.Label(self, text="Kullanıcı Adı:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        self.password_label = tk.Label(self, text="Sifre:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Giris", command=self.login)
        self.login_button.pack()
        self.register_button = tk.Button(self, text="Register", command=self.register)
        self.register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if check_user(username, password):
            messagebox.showinfo("Giris bilgisi", "Giris basarili")
            self.destroy()  # Destroy the login window
            main_app = MainWindow(username)  # Open the main application window
            main_app.mainloop()
        else:
            messagebox.showerror("Giris bilgisi", "gecersiz kullanıcı adı veya sifre")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if kullanici_kayit(username, password):
            messagebox.showinfo("kayit bilgisi", "basariyla kayit olundu")
        else:
            messagebox.showerror("Register Info", "boyle bir kullanıcı var")

class MainWindow(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title('proje')
        self.geometry('400x300')
        self.widget_olustur()

    def widget_olustur(self):
        menu = tk.Menu(self)
        self.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Karşılaştır", menu=file_menu)
        file_menu.add_command(label="Jaccard Algoritması", command=self.jaccard_karsilastir)
        file_menu.add_command(label="Basit Eşleşme", command=self.basit_esleme_karsilastir)

        settings_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="İşlemler", menu=settings_menu)
        password_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="Şifre", menu=password_menu)
        password_menu.add_command(label="Değiştir", command=self.sifreyi_degistir)

        menu.add_command(label="Çıkış", command=self.quit)

    def jaccard_karsilastir(self):
        self.textleri_karsilastir(jaccard_benzerligi)

    def basit_esleme_karsilastir(self):
        self.textleri_karsilastir(basit_esleme)

    def textleri_karsilastir(self, algorithm):
        file1 = filedialog.askopenfilename(title="Birinci metin dosyasını seçiniz", filetypes=[("Text files", "*.txt")])
        file2 = filedialog.askopenfilename(title="İkinci metin dosyasını seçiniz", filetypes=[("Text files", "*.txt")])
        if file1 and file2:
            text1 = dosya_oku(file1)
            text2 = dosya_oku(file2)
            similarity = algorithm(text1, text2)
            messagebox.showinfo("Karşılaştırma Sonucu", f"Benzerlik Oranı: {similarity:.2f}")

    def sifreyi_degistir(self):
        new_password = simpledialog.askstring("Yeni Şifre", "Yeni şifrenizi giriniz:", show='*')
        if new_password:
            sifreyi_guncelle(self.username, new_password)
            messagebox.showinfo("Şifre Güncelleme", "Şifreniz başarıyla güncellendi.")
        else:
            messagebox.showerror("Şifre Güncelleme", "Şifre güncellenemedi.")


if __name__ == "__main__":
    veritabani_olustur()  
    app = LoginWindow()  
    app.mainloop()  