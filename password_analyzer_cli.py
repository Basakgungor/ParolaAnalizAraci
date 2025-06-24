import re 

def analyze_password_strength(password):
    """Bir parolanin gucunu analiz eder ve bir puan ile
    geri bildirim saglar. Puan araligi: 0-100 (yuksek puan=guclu parola)
    """
    
    score=0 #Parola Guc Puani
    feedback=[]#Kullaniciya gosterilecek geri bildiirmler
    
    #KRITER 1:Uzunluk kontrolu
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
        
    #KRITER 2: Karakter Turleri Kontrolu
    # regex lerle parolanin icinde buyuk/kucuk harf,sayi veya ozel karakter olup olmadigini kontrol ediyoruz.
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
    if score >= 80:
        strength_text= "Çok Güçlü"
    elif score >= 60:
        strength_text= "Güçlü"
    elif score >=40:
        strength_text="Orta"
    elif score >=20:
        strength_text="Zayıf"
    else:
        strength_text="Çok Zayıf"
        
    # Fonksiyon, hesaplanan puanı, metinsel gücü ve geri bildirim listesini döndürür.
    return score, strength_text, feedback

    #Uygulamayi komut satirinda calistirma kismi
    #Bu bolum, kodu dogrudan calistirdigimizda devreye girer.
if __name__ == "__main__":
        print("Parola Gücü Analiz Aracı (CLI versiyon)")
        print("---------------------------------------")
        
        while True: # Surekli parola girmek icin bir dongu (sen break diyene kadar devam eder)
            password = input("Bir parola girin(çıkmak için 'q' tuşlayın:)")
            if password.lower() == 'q': #Kullanıcı q yazarsa çık.
                break
            if not password: #Bos parola girerse
                print("Lütfen bir parola giriniz.")
                continue # Döngü while True olduğu için en başa döner ve yeniden parola sorar.
            
            # analyze_password_strength fonskiyonunu cagir ve sonuclari al.
            score, strength_text, feedback= analyze_password_strength(password)
            
            # Sonuclari ekrana yazdir.
            print(f"\nGirilen Parola: {password}")
            print(f"Güç Puanı: {score}/100")
            print(f"Güç Seviyesi: {strength_text}")
            print("Geri bildirimler:")
            for item in feedback: #Her bir geri bildirim ayri satirda yazar
                print(f" - {item}")
                
            print("-" * 30) #Ayırıcı çizgi 30 kez * basar
            
            
            