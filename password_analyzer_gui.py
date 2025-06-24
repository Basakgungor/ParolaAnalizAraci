from tkinter import Tk, Label, Button, Entry, messagebox, Scale, HORIZONTAL, StringVar
import re
from tkinter.ttk import Progressbar
#---- ANA ANALIZ FONKSIYONU (Onceki Adımdan kopyalandi) ----
# Bu fonksiyon, parolanin gucunu hesaplayan ve geri bildirim saglayan kalptir.

def analyze_password_strength(password):
    score = 0
    feedback = []
    
    lenght= len(password)
    if lenght >= 12:
        score = score + 25 
        feedback.append("Parola uzunluğu yeterli.")
    elif lenght >= 8: 
        score += 15 #Uzunluk 8 ile 11 arasinda ise 15 puan ekle.
        feedback.append("Parola yeterince uzun, fakat güvenlik için daha uzun bir şifre koymalısın.")
    else:
        score+=5 #parola uzunlugu 8 den kisa ise 5 puan ekle.
        feedback.append("Parola çok kısa, en az 8 karakter olmalı.")
        
    has_lowercase= bool(re.search(r'[a-z]',password)) # Kucuk harf var mi?
    has_uppercase= bool(re.search(r'[A-Z]',password)) 
    has_digit= bool(re.search(r'\d',password)) # Sayı var mı? (\d, herhangi bir rakam anlamına gelir)
    #ozel karakterler: buradaki karakterleri kendin belirleyebilirsin,yaygın olanlar bunlar)
    has_special= bool(re.search(r'[!@#$%^&*()_+=\-{}\[\]:;"\'<>,.?/|`~]',password))
    
    char_types=0 # Kac farkli karakter turu var?
    if has_lowercase: char_types+=1
    if has_uppercase: char_types+=1
    if has_digit: char_types+=1
    if has_special: char_types+=1
    
    if char_types ==4:
        score +=30 # Tum 4 turde varsa en yuksek puan
        feedback.append("Tüm karakter türlerini (büyük/küçük harf, sayı, özel) içeriyor.")
        
    elif char_types ==3:
        score+=20
        feedback.append("3 farklı karakter türünü içeriyor. Güvenlik için tüm karakter tiplerini kullanmanız önerilir.")
    
    elif char_types ==2:
        score+=10
        feedback.append("2 farklı karakter türünü içeriyor.Daha fazla çeşitlilik ekleyin.")
        
    else:
        feedback.append("Sadece 1 karakter türü içeriyor. Karmaşıklığı arttırın.")
        
    # Hangi turlerin eksik olduguna dair spesifik geri bildirimler ekleyebiliriz.
    if not has_lowercase: feedback.append("Küçük harf ekleyin.")
    if not has_uppercase: feedback.append("Büyük harf ekleyin.")
    if not has_digit: feedback.append("Sayı ekleyin.")
    if not has_special: feedback.append("Özel karakter ekleyin.")
    
    
    #KRITER 3: Yaygin desenler kontrolu
    # Bu kisim kolay tahmin edilebilir veya yaygin zayif parolalari yakalamaya calisir.
    
    #Tekrar eden karakterler(or."aaaa","111")
    #Parola icinde 3 veya daha fazla ayni karakterin ard arda gelip gelmedigini kontrol eder.
    for i in range(lenght-2): #sondan 2 karakter kalana kadar dongu
        if password[i] == password[i+1]== password[i+2]:
            score = score - 10
            feedback.append("Aynı karakterler art arda tekrarlanıyor,kaçının")
            break #Bir kez buldugunda yeterli donguden cik.
        
        
    # Sirali karakterler(or."qwerty","123456")
    common_sequences=["qwerty","asdfgh","zxcvbn","123456","654321","abcdef","fedcba"]
    for seq in common_sequences:
        if seq in password.lower(): #Parolayi kucuk harfe cevirip sirali diziyi arar.
            score = score - 15
            feedback.append(f"Yaygın sıralı diziler ('{seq}') içeriyor, kaçının.")
            break
        
    # Eger parola, tek bir karakterden uzun ve tum karakterleri ayniysa "aaaaaaaaa"
    if lenght > 1 and len(set(password)) == 1: # set(password) benzersiz karakterleri verir
        score -= 20
        feedback.append("Parola sadece aynı karakterin tekrarından oluşuyor, çok zayıf.")
        
        
    #--- SON PUAN AYARLAMASI ---
    # Puanın 0 dan dusuk veya 100 den buyuk olmasini engelleriz. score = max(0, min(100,score))
    if score <0 :
        score=0
    elif score > 100:
        score=100
        
    # Puani metinsel guce cevir.
    if score >= 90:
        strength_text= "Mükemmel"
        color= "green" 
    elif score>=75:
        strength_text="Güçlü"
        color="green"
    elif score >= 55:
        strength_text= "Güçlü"
        color = "lightgreen" #acik yesil
    elif score >=35:
        strength_text="Orta"
        color= "orange"
    elif score >=15:
        strength_text="Zayıf"
        color= "red"
    else:
        strength_text="Çok Zayıf"
        color="darkred"
    #GUI icin ek olarak renk bilgisini de donduruyoruz.
    # Fonksiyon, hesaplanan puanı, metinsel gücü ve geri bildirim listesini döndürür.
    return score, strength_text, feedback, color

# ---- GUI SINIFI ----
#Bu sinif, pencereyi ve uzerindeki tum elemanlari (input kutusu, butonlar, metinler vb.) olusturur ve yonetir.
class PasswordAnalyzerApp:
    def __init__(self,master):
        self.master= master # Ana pencere (root)
        master.title("Parola Gücü Analizi Aracı")
        master.geometry("400x450")#pencerenin baslangic boyutu(genislikxyuseklik)
        
        #1. Parola Gırıs Araci
        self.password_label= Label(master,text="Parolanızı buraya giriniz:")
        self.password_label.pack(pady=10) # Pencereye ekle ve ustten 10 piksel bosluk birak
        
        self.password_entry= Entry(master,width=40,show='*') #Entry, Tkinter’da bir tek satirlik metin giris kutusudur.
        self.password_entry.pack(pady=5)#Giriş kutusunu pencereye yerleştirir.
        self.password_entry.bind("<KeyRelease>", self.analyze_on_type)
        # Her tusa basildiginda (tus birakildiginda) analyze_on_type fonksiyonunu cagir
        
        #2. Guc puani gostergesi
        self.score_label=Label(master,text="Güç Puanı: N/A") # Başlangıçta N/A (Not Applicable) göster.yani şu anda geçerli bir değer yok anlamına gelir.
        self.score_label.pack(pady=5)# Bu etiket pencereye yerlestirilir.
        
        #ProgressBar 
        self.progress=Progressbar(master,orient="horizontal",length=300,mode="determinate",maximum=100)
        self.progress.pack(pady=5)
        
        #Guc seviyesi metni (Orn.Cok guclu)
        self.strength_text_var= StringVar()#Tkinter’da StringVar, metin saklamak ve dinamik olarak degistirmek icin kullanilir.
        self.strength_text_var.set("Güç Seviyesi: N/A")
        self.strength_text_label=Label(master,textvariable=self.strength_text_var,font=("Arial", 14, "bold"))
        self.strength_text_label.pack(pady=5)
        
        #3. Geri bildirim alani
        self.feedback_label=Label(master,text="Geri Bildirimler:",justify="left",font=("Arial", 11, "bold"))
        #justify=left: Cok satirli yazi olursa satirlari sola yaslar.
        self.feedback_label.pack(pady=10)
        
        #Geri Bildirimlerin gosterilecegi metin alani
        self.feedback_text= StringVar()
        self.feedback_text_display=Label(master,textvariable=self.feedback_text,justify="left",wraplength=350,bg="lightgray", padx=10, pady=10, relief="groove")
        self.feedback_text_display.pack(pady=5,padx=20,fill="both",expand=True)
        
        
    def analyze_on_type(self,event=None): #Bu bir metot.Her tuş bırakıldığında bind ile otomatik çalışır.
        """
        Kullanıcı parola giriş kutusuna her yazdığında (tuş bırakıldığında) bu fonksiyon çağrılır.
        Parolayı analiz eder ve GUI'yi günceller.
        """
        password = self.password_entry.get() # Giriş kutusundaki parolayı al

        if not password: #Eger parola bossa her seyi sifirla.
            self.score_label.config(text="Güç Puanı: N/A")
            self.progress["value"]=0
            self.strength_text_var.set("Güç Seviyesi: N/A")
            self.strength_text_label.config(fg="black")# Metin rengini siyah yap
            self.feedback_text.set("")# Geri bildirimleri temizle
            return
        
        #Ana analiz fonksiyonunu cagir ve sonuclari al.
        score, strength_text, feedback_list, color= analyze_password_strength(password)
        
        
        # GUI Elemanlarini guncelle
        self.score_label.config(text=f"Güç Puanı: {score}/100")
        self.progress["value"]=score
        self.strength_text_var.set(f"Güç Seviyesi: {strength_text}")
        self.strength_text_label.config(fg=color)# Guc seviyesi metninin rengini ayarla
        
        #Geri bildirimleri yeni satirlarla birlestir ve goster.
        self.feedback_text.set("\n".join(feedback_list))
        

    #---- UYGULAMANIN BASLANGIC NOKTASI----
    # Bu bolum kodu dogrudan calistirdigimizda devreye girer ve pencereyi olusturur.
if __name__=="__main__":
    root=Tk() # Tkinter ana penceresini olusturur.
    app= PasswordAnalyzerApp(root) #Uygulama Sinifimizin bir ornegini olusturu.
    root.mainloop()# Pencereyi görünür yap ve olaylari dinlemeye basla (butona basma, yazi yazma vb.)
        