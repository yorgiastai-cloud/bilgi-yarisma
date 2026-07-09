import streamlit as st
import time

st.set_page_config(page_title="Hızlı Yarışma", layout="centered")

sorular = [
    {"soru": "Dünyanın en derin noktası olan Mariana Çukuru hangi okyanustadır?", "cevaplar": ["Atlantik", "Pasifik", "Hint", "Arktik"], "dogru": "Pasifik"},
    {"soru": "Tarihteki ilk yazılı kanunlar olan Hammurabi Kanunları hangi uygarlığa aittir?", "cevaplar": ["Sümer", "Babil", "Asur", "Akad"], "dogru": "Babil"},
    {"soru": "Güneş sistemimizde kendi etrafında ters yönde dönen tek gezegen hangisidir?", "cevaplar": ["Mars", "Venüs", "Jüpiter", "Satürn"], "dogru": "Venüs"},
    {"soru": "Fransız Devrimi'nin temel sloganı olan 'Özgürlük, Eşitlik, Kardeşlik' hangi dildedir?", "cevaplar": ["Latince", "Fransızca", "İtalyanca", "İspanyolca"], "dogru": "Fransızca"},
    {"soru": "Ünlü düşünür Karl Marx'ın Friedrich Engels ile birlikte yazdığı eser nedir?", "cevaplar": ["Kapital", "Komünist Manifesto", "İdeoloji", "Proletarya"], "dogru": "Komünist Manifesto"},
    {"soru": "Hangi elementin simgesi 'Au'dur?", "cevaplar": ["Gümüş", "Bakır", "Altın", "Alüminyum"], "dogru": "Altın"},
    {"soru": "Dünya üzerindeki en uzun dağ silsilesi hangisidir?", "cevaplar": ["Himalayalar", "And Dağları", "Alpler", "Kafkaslar"], "dogru": "And Dağları"},
    {"soru": "Modern bilgisayar biliminin babası kabul edilen ve İkinci Dünya Savaşı'nda Enigma kodlarını kıran kişi kimdir?", "cevaplar": ["Alan Turing", "Ada Lovelace", "Bill Gates", "Steve Jobs"], "dogru": "Alan Turing"},
    {"soru": "Hangi ülke hem Asya hem de Avrupa kıtasında toprağa sahiptir?", "cevaplar": ["Yunanistan", "Türkiye", "İspanya", "İtalya"], "dogru": "Türkiye"},
    {"soru": "Dünya Sağlık Örgütü (WHO) merkezi nerededir?", "cevaplar": ["New York", "Cenevre", "Brüksel", "Viyana"], "dogru": "Cenevre"}
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