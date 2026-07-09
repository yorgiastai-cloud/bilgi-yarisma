import streamlit as st
import time

st.set_page_config(page_title="Sosyalist Tarih Yarışması", layout="centered")

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

if 'puan' not in st.session_state: 
    st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'isim': '', 'soru_baslangic': 0})

st.title("☭ Sosyalist Tarih Bilgi Yarışması")

if not st.session_state.oyun_basladi:
    isim = st.text_input("Yoldaş Adı:")
    if st.button("🚀 Mücadeleye Başla"):
        if isim:
            st.session_state.isim = isim
            st.session_state.oyun_basladi = True
            st.session_state.soru_baslangic = time.time()
            st.rerun()
else:
    if st.session_state.soru_index < len(sorular):
        q = sorular[st.session_state.soru_index]
        
        # Süre hesaplama
        gecen_sure = time.time() - st.session_state.soru_baslangic
        kalan_sure = int(10 - gecen_sure)
        
        if kalan_sure <= 0:
            st.error("⏳ Süre doldu!")
            time.sleep(1)
            st.session_state.soru_index += 1
            st.session_state.soru_baslangic = time.time()
            st.rerun()
        
        st.subheader(f"Soru {st.session_state.soru_index + 1}: {q['soru']}")
        st.warning(f"⏱️ Kalan Süre: **{kalan_sure}** saniye")
        
        for secenek in q['cevaplar']:
            if st.button(secenek):
                cevap_suresi = gecen_sure
                if secenek == q['dogru']:
                    puan = 1
                    if cevap_suresi < 3:
                        puan += 1
                        st.success("✅ Doğru! +1 Hız Bonusu!")
                    else: 
                        st.success("✅ Doğru!")
                    st.session_state.puan += puan
                else: 
                    st.error(f"❌ Yanlış! Doğrusu: {q['dogru']}")
                
                time.sleep(1.2)
                st.session_state.soru_index += 1
                st.session_state.soru_baslangic = time.time()
                st.rerun()
        
        # Her saniye akışı tetiklemek için ufak bir gecikme ve yenileme
        time.sleep(1)
        st.rerun()
        
    else:
        st.write(f"Oyun bitti {st.session_state.isim}! Toplam Skor: {st.session_state.puan}")
        if st.button("🏆 Skorunu Kaydet"):
            with open("skorlar.txt", "a") as f:
                f.write(f"{st.session_state.isim} - {st.session_state.puan}\n")
            st.success("Kaydedildi!")
        
        if st.button("Tekrar Oyna"):
            st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'soru_baslangic': time.time()})
            st.rerun()