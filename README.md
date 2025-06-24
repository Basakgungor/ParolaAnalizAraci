# Parola Gücü ve Kırılabilirlik Analiz Aracı

---

## 🚀 Proje Hakkında

Bu proje, kullanıcıların belirledikleri parolaların ne kadar güvenli olduğunu gerçek zamanlı olarak analiz eden ve zayıf yönlerini belirterek geri bildirim sağlayan bir masaüstü uygulamasıdır. Günümüzde siber güvenlik saldırılarının önemli bir kısmı zayıf veya kolay tahmin edilebilir parolalar üzerinden gerçekleşmektedir. Bu araç, kullanıcıları daha güçlü parola seçimleri konusunda bilinçlendirmeyi ve yönlendirmeyi amaçlamaktadır.

## ✨ Özellikler

* **Anlık Analiz:** Kullanıcı parolayı yazarken anında güç puanı ve seviye gösterimi.
* **Kapsamlı Güç Kriterleri:**
    * Parola uzunluğu kontrolü.
    * Büyük harf, küçük harf, sayı ve özel karakter kullanımının analizi.
    * Tekrarlayan karakter dizilerinin tespiti (örn. "aaa", "111").
    * Yaygın sıralı klavye veya sayı dizilerinin tespiti (örn. "qwerty", "123456").
* **Detaylı Geri Bildirimler:** Parolanın neden zayıf olduğuna dair spesifik tavsiyeler sunar (örn. "Sayı ekleyin", "Parola çok kısa").
* **Görsel Puanlama:** Renk kodlamalı metin ve ilerleme çubuğu ile parola gücünün kolay anlaşılması.
* **Kullanıcı Dostu Arayüz:** Tkinter ile geliştirilmiş basit ve sezgisel grafik kullanıcı arayüzü.

## 💻 Kullanılan Teknolojiler

* **Python 3:** Projenin ana programlama dili.
* **Tkinter:** Python'ın standart GUI (Grafik Kullanıcı Arayüzü) kütüphanesi.
* **`re` Modülü:** Düzenli ifadeler (Regular Expressions) kullanarak metin desenlerini analiz etmek için.

## ⬇️ Kurulum

Bu projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/Basakgungor/ParolaAnalizAraci.git
    ```
    (Eğer GitHub'a yüklemediysen, sadece klasörü indirmelerini söyle.)
2.  **Proje Dizine Gidin:**
    ```bash
    cd ParolaAnalizAraci
    ```
3.  **Gerekli Paketleri Yükleyin:**
    Bu proje için harici bir paket gerekmemektedir, Python'ın standart kütüphaneleri yeterlidir.
    (Eğer ileri bir aşamada `TextBlob` gibi bir şey ekleseydin buraya `pip install -r requirements.txt` ve `requirements.txt` dosyasından bahsederdin.)

## ▶️ Kullanım

Uygulamayı başlatmak için `password_analyzer_gui.py` dosyasını çalıştırın:

```bash
python3 password_analyzer_gui.py