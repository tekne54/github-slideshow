"""
main.py    Basit bir Not Defteri uygulaması

Bu sürüm, veri işleme mantığını `log_islemleri.py` modülüne taşıyarak
yeniden düzenlenmiştir.
"""
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os

# Veri işleme fonksiyonunu yeni adıyla içe aktarıyoruz.
from log_islemleri import loglari_isle_ve_kaydet, LOG_DOSYASI

def veri_aktar_arayuz():
    """
    Arayüz için veri aktarımını başlatan fonksiyon.
    İşlem sonucunu bir mesaj kutusu ile kullanıcıya bildirir.
    """
    try:
        # Yeni fonksiyonu çağırıyoruz ve dönen kayıt sayısını alıyoruz.
        kayit_sayaci = loglari_isle_ve_kaydet()
        messagebox.showinfo("Başarılı", f"{kayit_sayaci} adet kayıt veritabanına başarıyla aktarıldı.")
    except FileNotFoundError:
        messagebox.showerror("Hata", f"Log dosyası bulunamadı! '{LOG_DOSYASI}' dosyasının programla aynı dizinde olduğundan emin olun.")
    except Exception as e:
        messagebox.showerror("Hata", f"Beklenmedik bir hata oluştu:\n{e}")

def dosyaAc():
	pencere.filename =  filedialog.askopenfilename(title = "Dosya Aç",filetypes = (("Metin Dosyaları","*.txt"),("Bütün Dosyalar","*.*"),
																	("Zengin Metin Dosyaları","*.rtf"),
																	("Python Files","*.py"),
																	("html Documents","*.html"),
																	("Javascript Files","*.js"),
																	("Php Files","*.php")))
	if pencere.filename=="":
		pencere.filename=None
	else:
		pencere.title(os.path.basename(pencere.filename) + " - Not Defteri")
		metinKutu.delete(1.0,END)

		# Dosya açarken encoding belirtmek önemlidir.
		with open(pencere.filename,"r", encoding="utf-8", errors="ignore") as dosya:
			metinKutu.insert(1.0,dosya.read())

def yeniDosya():
	pencere.title("İsimsiz - Not Defteri")
	metinKutu.delete(1.0,END)
	pencere.filename=None


def dosyaKaydet():
	if pencere.filename == None:
		pencere.filename = filedialog.asksaveasfilename(initialfile='isimsiz.txt', defaultextension=".txt",
										filetypes=[("Bütün Dosyalar","*.*"),
										("Metin Dosyaları","*.txt"),
										("Zengin Metin Dosyaları","*.rtf"),
										("Python Files","*.py"),
										("html Documents","*.html"),
										("Javascript Files","*.js"),
										("Php Files","*.php")])

		if pencere.filename == "":
			pencere.filename = None

		else:
			# Dosya yazarken encoding belirtmek önemlidir.
			with open(pencere.filename,"w", encoding="utf-8") as dosya:
				dosya.write(metinKutu.get(1.0,END))

			pencere.title(os.path.basename(pencere.filename) + " - Not Defteri")

	else:
		with open(pencere.filename,"w", encoding="utf-8") as dosya:
			dosya.write(metinKutu.get(1.0,END))

def yapistir():
	metinKutu.event_generate('<Control-v>')

def kes():
	metinKutu.event_generate('<Control-x>')

def kopyala():
	metinKutu.event_generate('<Control-c>')

def kalinYaz():
	metinKutu.tag_add("kln", "sel.first", "sel.last")

def egikYaz():
	metinKutu.tag_add("egk", "sel.first", "sel.last")

def hakkinda():
	messagebox.showinfo("Not Defteri","Akarsu")

def aktar():
    messagebox.showinfo("Bilgi", "Bu fonksiyon henüz tanımlanmamıştır." )


pencere=Tk()
pencere.geometry("500x300")
pencere.title("İsimsiz - Not Defteri")
pencere.filename=None

menu=Menu(pencere)
pencere.config(menu=menu)

dosyaMenu = Menu(menu)
menu.add_cascade(label="Dosya", menu=dosyaMenu)
dosyaMenu.add_command(label="Yeni", command=yeniDosya)
dosyaMenu.add_command(label="Aç...", command=dosyaAc)
dosyaMenu.add_command(label="Kaydet", command=dosyaKaydet)
dosyaMenu.add_separator()
dosyaMenu.add_command(label="Veri Tabanına Aktar", command=veri_aktar_arayuz)
dosyaMenu.add_command(label="Kapat", command=pencere.quit)

duzenMenu=Menu(menu)
menu.add_cascade(label="Düzen", menu=duzenMenu)
duzenMenu.add_command(label="Kes", command=kes)
duzenMenu.add_command(label="Kopyala", command=kopyala)
duzenMenu.add_command(label="Yapıştır", command=yapistir)
duzenMenu.add_separator()
duzenMenu.add_command(label="Kalın", command=kalinYaz)
duzenMenu.add_command(label="Eğik", command=egikYaz)

yardimMenu = Menu(menu)
menu.add_cascade(label="Yardım", menu=yardimMenu)
yardimMenu.add_command(label="Hakkında", command=hakkinda)

yataySb=Scrollbar(pencere, orient=HORIZONTAL)
yataySb.pack(side=BOTTOM, fill= X)

dikeySb=Scrollbar(pencere, orient=VERTICAL)
dikeySb.pack( side = RIGHT, fill = Y )

metinKutu=Text(pencere, width=500, height=300,wrap=NONE, xscrollcommand=yataySb.set, yscrollcommand = dikeySb.set)
metinKutu.config(insertofftime=600, insertontime=1000, insertwidth=5, selectbackground="darkgray", font="Arial 10")
metinKutu.tag_config("kln", font="Arial 10 bold")
metinKutu.tag_config("egk", font="Arial 10 italic")
metinKutu.pack()

dikeySb.config( command=metinKutu.yview)
yataySb.config(command=metinKutu.xview)

pencere.mainloop()
