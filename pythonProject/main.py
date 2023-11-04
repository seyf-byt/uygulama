import tkinter as tk
from tkinter.simpledialog import askinteger
import pyautogui
from PIL import ImageGrab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from PIL import Image
import threading

# Pencereyi oluştur
root = tk.Tk()
root.title("Fare Tıklama ve Ekran Resmi Alma Uygulaması")

# Klasör adı
klasor_adi = "ekran_resimleri"
if not os.path.exists(klasor_adi):
    os.makedirs(klasor_adi)


# Fare konumu güncelleyen fonksiyon
def guncelle_fare_konumu():
    fare_konumu = pyautogui.position()
    fare_konumu_label.config(text=f"Farenin Konumu: {fare_konumu}")
    root.after(100, guncelle_fare_konumu)


# Ekran resmini al ve klasöre kaydet
def ekran_resmi_al():
    baslangic_x = int(baslangic_x_entry.get())
    baslangic_y = int(baslangic_y_entry.get())
    bitis_x = int(bitis_x_entry.get())
    bitis_y = int(bitis_y_entry.get())

    ekran_resmi = ImageGrab.grab(bbox=(baslangic_x, baslangic_y, bitis_x, bitis_y))
    resim_adi = os.path.join(klasor_adi, "ekran_resmi.png")
    ekran_resmi.save(resim_adi)


# Tıklama işlemini gerçekleştiren fonksiyon
def fare_tikla():
    x = int(tiklama_x_entry.get())
    y = int(tiklama_y_entry.get())
    tiklama_sayisi = askinteger("Tıklama Sayısı", "Kaç defa tıklamak istersiniz?")
    tiklama_araligi = askinteger("Tıklama Aralığı (ms)", "Tıklamalar arasındaki süre (milisaniye cinsinden) nedir?")

    def tıklamalari_gerceklestir():
        for _ in range(tiklama_sayisi):
            ekran_resmi_al()
            pyautogui.click(x=x, y=y)
            root.after(tiklama_araligi, lambda: None)

    threading.Thread(target=tıklamalari_gerceklestir).start()


# Klasördeki tüm ekran resimlerini tek bir PDF yap
def klasordaki_resimleri_pdf_yap():
    resimler = [f for f in os.listdir(klasor_adi) if f.endswith(".png")]
    pdf = canvas.Canvas("Klasor_Ekran_Resimleri.pdf", pagesize=letter)
    for resim_adi in resimler:
        resim_yolu = os.path.join(klasor_adi, resim_adi)
        im = Image.open(resim_yolu)
        pdf.drawInlineImage(im, 100, 100, width=400, height=400)
        pdf.showPage()  # Yeni bir sayfa ekle
    pdf.save()


# Ekran resmi almadan önce koordinatları soran fonksiyon
def ekran_resmi_koordinatlari_sor():
    global baslangic_x_entry, baslangic_y_entry, bitis_x_entry, bitis_y_entry
    baslangic_x = askinteger("Başlangıç Koordinat Sorusu", "Başlangıç X Koordinatını Girin:")
    baslangic_y = askinteger("Başlangıç Koordinat Sorusu", "Başlangıç Y Koordinatını Girin:")
    bitis_x = askinteger("Bitiş Koordinat Sorusu", "Bitiş X Koordinatını Girin:")
    bitis_y = askinteger("Bitiş Koordinat Sorusu", "Bitiş Y Koordinatını Girin:")

    baslangic_x_entry.delete(0, tk.END)
    baslangic_y_entry.delete(0, tk.END)
    bitis_x_entry.delete(0, tk.END)
    bitis_y_entry.delete(0, tk.END)

    baslangic_x_entry.insert(0, baslangic_x)
    baslangic_y_entry.insert(0, baslangic_y)
    bitis_x_entry.insert(0, bitis_x)
    bitis_y_entry.insert(0, bitis_y)


# Etiketler (labels) ve giriş kutuları (entry) oluştur
fare_konumu_label = tk.Label(root, text="")
fare_konumu_label.pack(padx=20, pady=20)

baslangic_x_label = tk.Label(root, text="Başlangıç X Koordinatı:")
baslangic_x_label.pack()
baslangic_x_entry = tk.Entry(root)
baslangic_x_entry.pack()

baslangic_y_label = tk.Label(root, text="Başlangıç Y Koordinatı:")
baslangic_y_label.pack()
baslangic_y_entry = tk.Entry(root)
baslangic_y_entry.pack()

bitis_x_label = tk.Label(root, text="Bitiş X Koordinatı:")
bitis_x_label.pack()
bitis_x_entry = tk.Entry(root)
bitis_x_entry.pack()

bitis_y_label = tk.Label(root, text="Bitiş Y Koordinatı:")
bitis_y_label.pack()
bitis_y_entry = tk.Entry(root)
bitis_y_entry.pack()

ekran_resmi_al_button = tk.Button(root, text="Ekran Resmi Al", command=ekran_resmi_al)
ekran_resmi_al_button.pack()

tiklama_x_label = tk.Label(root, text="Tıklama X Koordinatı:")
tiklama_x_label.pack()
tiklama_x_entry = tk.Entry(root)
tiklama_x_entry.pack()

tiklama_y_label = tk.Label(root, text="Tıklama Y Koordinatı:")
tiklama_y_label.pack()
tiklama_y_entry = tk.Entry(root)
tiklama_y_entry.pack()

tikla_button = tk.Button(root, text="Tıkla", command=fare_tikla)
tikla_button.pack()

pdf_yap_button = tk.Button(root, text="Klasördeki Tüm Ekran Resimlerini PDF Yap", command=klasordaki_resimleri_pdf_yap)
pdf_yap_button.pack()

koordinat_sor_button = tk.Button(root, text="Ekran Resmi Koordinatlarını Sor", command=ekran_resmi_koordinatlari_sor)
koordinat_sor_button.pack()

# Fare konumunu güncellemeyi başlat
guncelle_fare_konumu()

# Pencereyi göster
root.mainloop()
