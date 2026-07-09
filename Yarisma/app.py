import streamlit as st
import time

st.set_page_config(page_title="Hızlı Yarışma", layout="centered")

sorular = [
    {"soru": "Dünyanın en büyük okyanusu hangisidir?", "cevaplar": ["Atlantik", "Hint", "Pasifik", "Arktik"], "dogru": "Pasifik"},
    {"soru": "Periyodik tabloda 'O' harfi hangi elementi simgeler?", "cevaplar": ["Altın", "Oksijen", "Osmiyum", "Gümüş"], "dogru": "Oksijen"},
    {"soru": "Shakespeare'in yazdığı ünlü oyun hangisidir?", "cevaplar": ["Sefiller", "Hamlet", "İlahi Komedya", "Suç ve Ceza"], "dogru": "Hamlet"},
    {"soru": "Eyfel Kulesi hangi şehirde yer alır?", "cevaplar": ["Londra", "Berlin", "Paris", "Roma"], "dogru": "Paris"},
    {"soru": "Güneş sistemindeki en büyük gezegen hangisidir?", "cevaplar": ["Satürn", "Mars", "Jüpiter", "Dünya"], "dogru": "Jüpiter"},
    {"soru": "Türkiye Cumhuriyeti hangi yıl ilan edilmiştir?", "cevaplar": ["1920", "1923", "1925", "1930"], "dogru": "1923"},
    {"soru": "Hangi ülkenin bayrağında bir akçaağaç yaprağı bulunur?", "cevaplar": ["ABD", "Kanada", "Avustralya", "Yeni Zelanda"], "dogru": "Kanada"},
    {"soru": "Nobel Ödülleri hangi şehirde verilmektedir?", "cevaplar": ["Oslo", "Stockholm", "Cenevre", "Viyana"], "dogru": "Stockholm"},
    {"soru": "'Habeas Corpus' hangi hukuk terimiyle ilişkilidir?", "cevaplar": ["Kişi özgürlüğü", "Mülkiyet hakkı", "Savaş suçu", "Vergi yasası"], "dogru": "Kişi özgürlüğü"},
    {"soru": "Işık hızı saniyede yaklaşık kaç kilometredir?", "cevaplar": ["100.000", "200.000", "300.000", "400.000"], "dogru": "300.000"}
]

if 'puan' not in st.session_state: 
    st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'isim': '', 'baslangic_zamani': 0})

st.title("🏆 Hızlı Bilgi Yarışması")

if not st.session_state.oyun_basladi:
    isim = st.text_input("Yarışmacı Adı:")
    if st.button("🚀 Oyunu Başlat"):
        if isim:
            st.session_state.isim = isim
            st.session_state.oyun_basladi = True
            st.rerun()
        else:
            st.warning("Lütfen başlamadan önce adını gir!")

elif st.session_state.soru_index < len(sorular):
    q = sorular[st.session_state.soru_index]
    col1, col2 = st.columns([3, 1])
    col1.subheader(f"Soru {st.session_state.soru_index + 1}: {q['soru']}")
    
    timer_placeholder = col2.empty()
    st.session_state.baslangic_zamani = time.time()
    
    for secenek in q['cevaplar']:
        if st.button(secenek, key=secenek):
            gecen_sure = time.time() - st.session_state.baslangic_zamani
            if secenek == q['dogru']:
                puan_artisi = 1
                if gecen_sure <= 3:
                    puan_artisi += 1
                    st.success("✅ Doğru! +1 Hız Bonusu!")
                else:
                    st.success("✅ Doğru!")
                st.session_state.puan += puan_artisi
            else:
                st.error(f"❌ Yanlış! Doğrusu: {q['dogru']}")
            time.sleep(1)
            st.session_state.soru_index += 1
            st.rerun()

    for saniye in range(10, 0, -1):
        timer_placeholder.metric("Süre", f"{saniye} sn")
        time.sleep(1)
    
    st.error("⏰ Süre doldu!")
    time.sleep(1)
    st.session_state.soru_index += 1
    st.rerun()

else:
    st.write(f"Oyun bitti {st.session_state.isim}! Toplam Skor: {st.session_state.puan}")
    if st.button("Tekrar Oyna"):
        st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False})
        st.rerun()