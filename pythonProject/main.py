import tkinter as tk
import pyautogui
from PIL import ImageGrab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Pencereyi oluştur
root = tk.Tk()
root.title("Fare Tıklama ve Ekran Resmi Alma Uygulaması")

# Fare konumu güncelleyen fonksiyon
def guncelle_fare_konumu():
    fare_konumu = pyautogui.position()
    fare_konumu_label.config(text=f"Farenin Konumu: {fare_konumu}")
    root.after(100, guncelle_fare_konumu)

# Fare tıklama işlemini gerçekleştiren fonksiyon
def fare_tikla():
    x = int(x_entry.get())
    y = int(y_entry.get())
    tıklama_sayısı = int(tiklama_sayisi_entry.get())
    bekleme_süresi = int(süre_entry.get())

    # Ekran resmi al ve PDF'ye ekle
    ekran_resmi_çek(x, y, tıklama_sayısı, bekleme_süresi)

# Ekran resmi çekip PDF'ye ekleyen fonksiyon
def ekran_resmi_çek(x, y, tıklama_sayısı, bekleme_süresi):
    pdf = canvas.Canvas("Ekran_Resimleri.pdf", pagesize=letter)
    for i in range(tıklama_sayısı):
        im = ImageGrab.grab(bbox=(x, y, x + 100, y + 100))  # Belirli bir bölgeden ekran resmi al
        im.save(f"ekran_resmi_{i}.png")  # Resmi kaydet
        pdf.drawImage(f"ekran_resmi_{i}.png", 100, 100, width=400, height=400)
        if i < tıklama_sayısı - 1:
            pyautogui.click(x=x, y=y)
            root.after(bekleme_süresi, lambda: None)  # Bekleme süresi ekran güncellemesi için
    pdf.save()

# Etiketler (labels) ve giriş kutuları (entry) oluştur
fare_konumu_label = tk.Label(root, text="")
fare_konumu_label.pack(padx=20, pady=20)

x_label = tk.Label(root, text="X Konumu:")
x_label.pack()
x_entry = tk.Entry(root)
x_entry.pack()

y_label = tk.Label(root, text="Y Konumu:")
y_label.pack()
y_entry = tk.Entry(root)
y_entry.pack()

tiklama_sayisi_label = tk.Label(root, text="Tıklama Sayısı:")
tiklama_sayisi_label.pack()
tiklama_sayisi_entry = tk.Entry(root)
tiklama_sayisi_entry.pack()

süre_label = tk.Label(root, text="Bekleme Süresi (ms):")
süre_label.pack()
süre_entry = tk.Entry(root)
süre_entry.pack()

tikla_button = tk.Button(root, text="Tıkla ve Ekran Resmi Al", command=fare_tikla)
tikla_button.pack()

# Fare konumunu güncellemeyi başlat
guncelle_fare_konumu()

# Pencereyi göster
root.mainloop()
