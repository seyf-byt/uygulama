import tkinter as tk
import pyautogui

# Pencereyi oluştur
root = tk.Tk()
root.title("Fare Konumu")

# Fare konumunu güncelleyen fonksiyon
def guncelle_fare_konumu():
    fare_konumu = pyautogui.position()
    label.config(text=f"Farenin Konumu: {fare_konumu}")
    root.after(100, guncelle_fare_konumu)

# Etiket (label) oluştur
label = tk.Label(root, text="")
label.pack(padx=20, pady=20)

# Fare konumu güncellemesi başlat
guncelle_fare_konumu()

# Pencereyi göster
root.mainloop()
