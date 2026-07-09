import streamlit as st
import time

st.set_page_config(page_title="Sosyalist Tarih Yarışması", layout="centered")

# Tüm İstekleri İçeren 15 Soruluk Yeni Paket
import streamlit as st
import time

st.set_page_config(page_title="Sosyalist Tarih Yarışması", layout="centered")

# Tüm İstekleri İçeren 15 Soruluk Yeni Paket
sorular = [
    {"soru": "Karl Marx hangi şehirde doğmuştur?", "cevaplar": ["Berlin", "Trier", "Londra", "Paris"], "dogru": "Trier"},
    {"soru": "Friedrich Engels, Marx'ın hangi eserinin bitirilmesine büyük katkı sağlamıştır?", "cevaplar": ["Kapital", "Manifesto", "Grundrisse", "18. Brumaire"], "dogru": "Kapital"},
    {"soru": "Lenin, 1917 devrimi öncesi sürgünden Rusya'ya hangi araçla dönmüştür?", "cevaplar": ["Gemi", "Mühürlü Tren", "Uçak", "At Arabası"], "dogru": "Mühürlü Tren"},
    {"soru": "Stalin'in asıl adı nedir?", "cevaplar": ["Lev Troçki", "İosif Cuğaşvili", "Nikolay Buharin", "Sergey Kirov"], "dogru": "İosif Cuğaşvili"},
    {"soru": "Mao Zedong'un 1934-1935 yılları arasında önderlik ettiği meşhur geri çekilme harekâtı nedir?", "cevaplar": ["Büyük Yürüyüş", "Kültür Devrimi", "İleri Atılım", "Kızıl Ordu Seferi"], "dogru": "Büyük Yürüyüş"},
    {"soru": "Marx'ın hayatının büyük bir kısmını geçirdiği ve 'Kapital'i yazdığı kütüphane hangi şehirdedir?", "cevaplar": ["Paris", "Londra", "Berlin", "Brüksel"], "dogru": "Londra"},
    {"soru": "Lenin'in kurduğu ve Sovyetler Birliği'nin temelini atan parti hangisidir?", "cevaplar": ["Menşevik", "Bolşevik", "Sosyalist Devrimci", "Anarşist"], "dogru": "Bolşevik"},
    {"soru": "Stalin, gençliğinde hangi meslek için eğitim alıyordu?", "cevaplar": ["Demircilik", "Ruhbanlık", "Askerlik", "Terzilik"], "dogru": "Ruhbanlık"},
    {"soru": "Mao Zedong, hangi siyasi doktrinin Çin şartlarına uyarlanmış halini geliştirmiştir?", "cevaplar": ["Troçkizm", "Marksizm-Leninizm", "Anarko-Komünizm", "Sosyal Demokrasi"], "dogru": "Marksizm-Leninizm"},
    {"soru": "Engels, Manchester'da ne iş yapıyordu?", "cevaplar": ["Gazetecilik", "Fabrika Yöneticiliği", "Hukukçuluk", "Tıp"], "dogru": "Fabrika Yöneticiliği"},
    {"soru": "Lenin'in eşi ve en yakın çalışma arkadaşı kimdir?", "cevaplar": ["Rosa Luxemburg", "Nadejda Krupskaya", "Aleksandra Kollontay", "Inessa Armand"], "dogru": "Nadejda Krupskaya"},
    {"soru": "Stalin, hangi savaş sırasında 'Başkomutan' sıfatıyla ordunun başındaydı?", "cevaplar": ["I. Dünya Savaşı", "İç Savaş", "II. Dünya Savaşı", "Kore Savaşı"], "dogru": "II. Dünya Savaşı"},
    {"soru": "Marx'ın mezarı hangi şehirdedir?", "cevaplar": ["Trier", "Berlin", "Londra", "Paris"], "dogru": "Londra"},
    {"soru": "Mao Zedong'un ünlü 'Küçük Kırmızı Kitap'ı hangi dönemde yaygınlaşmıştır?", "cevaplar": ["Uzun Yürüyüş", "Kültür Devrimi", "İç Savaş", "Devrim Öncesi"], "dogru": "Kültür Devrimi"},
    {"soru": "Friedrich Engels'in 'İngiltere'de İşçi Sınıfının Durumu' adlı eseri hangi şehri anlatır?", "cevaplar": ["Londra", "Manchester", "Liverpool", "Birmingham"], "dogru": "Manchester"}
]

# Hafızayı Başlatma (Session State)
if 'puan' not in st.session_state: 
    st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'isim': '', 'start_time': 0, 'skor_kaydedildi': False})

st.title("☭ Sosyalist Tarih Bilgi Yarışması")

# 1. GİRİŞ EKRANI
if not st.session_state.oyun_basladi:
    isim = st.text_input("Yoldaş Adı:")
    if st.button("🚀 Mücadeleye Başla"):
        if isim:
            st.session_state.isim = isim
            st.session_state.oyun_basladi = True
            st.session_state.start_time = time.time()
            st.session_state.skor_kaydedildi = False
            st.rerun()
        else: 
            st.warning("Lütfen bir isim gir yoldaş!")
    
    # Giriş ekranındaki liderlik tablosu
    st.subheader("🏅 En Yüksek Skorlar")
    try:
        with open("skorlar.txt", "r") as f:
            skorlar = f.readlines()
            # Skorları puana göre yüksekten düşüğe sırala
            sirali_skorlar = sorted(skorlar, key=lambda x: int(x.split('-')[1].strip()), reverse=True)
            for s in sirali_skorlar[:5]:
                st.write(s.strip())
    except: 
        st.write("Henüz kaydedilmiş skor yok, ilk sen ol!")

# 2. SORU EKRANI
else:
    if st.session_state.soru_index < len(sorular):
        q = sorular[st.session_state.soru_index]
        st.subheader(f"Soru {st.session_state.soru_index + 1}: {q['soru']}")
        
        # 10 Saniyeden Geriye Sayım Hesaplama
        gecen_sure = time.time() - st.session_state.start_time
        kalan_sure = 10 - int(gecen_sure)
        
        if kalan_sure > 0:
            st.metric("⏳ Kalan Süre", f"{kalan_sure} sn")
            
            # Şıklar/Butonlar
            for secenek in q['cevaplar']:
                if st.button(secenek, key=f"{secenek}_{st.session_state.soru_index}"):
                    # Doğru / Yanlış Kontrolü
                    if secenek == q['dogru']:
                        taban_puan = 10
                        if gecen_sure < 3:
                            taban_puan += 5
                            st.success("✅ Harika! 15 Puan (10 Doğru + 5 Hız Bonusu)")
                        else: 
                            st.success("✅ Doğru! 10 Puan")
                        st.session_state.puan += taban_puan
                    else: 
                        st.error(f"❌ Yanlış! Doğrusu: {q['dogru']}")
                    
                    time.sleep(1.5) # Sonucu görmeleri için kısa bir bekleme
                    st.session_state.soru_index += 1
                    st.session_state.start_time = time.time()
                    st.rerun()
            
            # Ekranın akması için küçük bir bekleme süresi tetikleyicisi
            time.sleep(0.1)
            st.rerun()
        else:
            st.error("⏳ Süre doldu!")
            time.sleep(1.5)
            st.session_state.soru_index += 1
            st.session_state.start_time = time.time()
            st.rerun()

    # 3. OYUN BİTTİ EKRANI
    else:
        st.subheader(f"🎉 Oyun bitti, tebrikler {st.session_state.isim}!")
        st.write(f"**Toplam Skorun:** {st.session_state.puan}")
        
        # Butonla Skor Kaydetme (Çift yazmayı engeller)
        if not st.session_state.skor_kaydedildi:
            if st.button("🏆 Skorumu Liderlik Tablosuna Kaydet"):
                with open("skorlar.txt", "a") as f:
                    f.write(f"{st.session_state.isim} - {st.session_state.puan}\n")
                st.session_state.skor_kaydedildi = True
                st.success("Skorun başarıyla kaydedildi!")
                st.balloons()
                time.sleep(1)
                st.rerun()
        else:
            st.info("Skorun zaten kaydedildi yoldaş!")

        if st.button("🔄 Yeniden Oyna"):
            st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'skor_kaydedildi': False})
            st.rerun()

# Hafızayı Başlatma (Session State)
if 'puan' not in st.session_state: 
    st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'isim': '', 'start_time': 0, 'skor_kaydedildi': False})

st.title("☭ Sosyalist Tarih Bilgi Yarışması")

# 1. GİRİŞ EKRANI
if not st.session_state.oyun_basladi:
    isim = st.text_input("Yoldaş Adı:")
    if st.button("🚀 Mücadeleye Başla"):
        if isim:
            st.session_state.isim = isim
            st.session_state.oyun_basladi = True
            st.session_state.start_time = time.time()
            st.session_state.skor_kaydedildi = False
            st.rerun()
        else: 
            st.warning("Lütfen bir isim gir yoldaş!")
    
    # Giriş ekranındaki liderlik tablosu
    st.subheader("🏅 En Yüksek Skorlar")
    try:
        with open("skorlar.txt", "r") as f:
            skorlar = f.readlines()
            # Skorları puana göre yüksekten düşüğe sırala
            sirali_skorlar = sorted(skorlar, key=lambda x: int(x.split('-')[1].strip()), reverse=True)
            for s in sirali_skorlar[:5]:
                st.write(s.strip())
    except: 
        st.write("Henüz kaydedilmiş skor yok, ilk sen ol!")

# 2. SORU EKRANI
else:
    if st.session_state.soru_index < len(sorular):
        q = sorular[st.session_state.soru_index]
        st.subheader(f"Soru {st.session_state.soru_index + 1}: {q['soru']}")
        
        # 10 Saniyeden Geriye Sayım Hesaplama
        gecen_sure = time.time() - st.session_state.start_time
        kalan_sure = 10 - int(gecen_sure)
        
        if kalan_sure > 0:
            st.metric("⏳ Kalan Süre", f"{kalan_sure} sn")
            
            # Şıklar/Butonlar
            for secenek in q['cevaplar']:
                if st.button(secenek, key=f"{secenek}_{st.session_state.soru_index}"):
                    # Doğru / Yanlış Kontrolü
                    if secenek == q['dogru']:
                        taban_puan = 10
                        if gecen_sure < 3:
                            taban_puan += 5
                            st.success("✅ Harika! 15 Puan (10 Doğru + 5 Hız Bonusu)")
                        else: 
                            st.success("✅ Doğru! 10 Puan")
                        st.session_state.puan += taban_puan
                    else: 
                        st.error(f"❌ Yanlış! Doğrusu: {q['dogru']}")
                    
                    time.sleep(1.5) # Sonucu görmeleri için kısa bir bekleme
                    st.session_state.soru_index += 1
                    st.session_state.start_time = time.time()
                    st.rerun()
            
            # Ekranın akması için küçük bir bekleme süresi tetikleyicisi
            time.sleep(0.1)
            st.rerun()
        else:
            st.error("⏳ Süre doldu!")
            time.sleep(1.5)
            st.session_state.soru_index += 1
            st.session_state.start_time = time.time()
            st.rerun()

    # 3. OYUN BİTTİ EKRANI
    else:
        st.subheader(f"🎉 Oyun bitti, tebrikler {st.session_state.isim}!")
        st.write(f"**Toplam Skorun:** {st.session_state.puan}")
        
        # Butonla Skor Kaydetme (Çift yazmayı engeller)
        if not st.session_state.skor_kaydedildi:
            if st.button("🏆 Skorumu Liderlik Tablosuna Kaydet"):
                with open("skorlar.txt", "a") as f:
                    f.write(f"{st.session_state.isim} - {st.session_state.puan}\n")
                st.session_state.skor_kaydedildi = True
                st.success("Skorun başarıyla kaydedildi!")
                st.balloons()
                time.sleep(1)
                st.rerun()
        else:
            st.info("Skorun zaten kaydedildi yoldaş!")

        if st.button("🔄 Yeniden Oyna"):
            st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'skor_kaydedildi': False})
            st.rerun()