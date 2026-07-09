import streamlit as st
import time

st.set_page_config(page_title="Sosyalist Teori Yarışması", layout="centered")

# 10 Sosyalizm Temalı Soru
sorular = [
    {"soru": "Karl Marx ve Friedrich Engels'in 'tarihin motoru' olarak tanımladığı kavram nedir?", "cevaplar": ["Teknoloji", "Sınıf Mücadelesi", "Eğitim", "Din"], "dogru": "Sınıf Mücadelesi"},
    {"soru": "Ütopyacı sosyalizmin öncülerinden olan ve 'Yeni bir dünya düzeni' kavramını geliştiren İngiliz sanayici kimdir?", "cevaplar": ["Robert Owen", "Charles Fourier", "Henri de Saint-Simon", "Thomas More"], "dogru": "Robert Owen"},
    {"soru": "Kapitalizmde üretilen metaların kullanım değeri ile değişim değeri arasındaki fark ne olarak adlandırılır?", "cevaplar": ["Kar", "Artı Değer", "Faiz", "Maliyet"], "dogru": "Artı Değer"},
    {"soru": "Rus Devrimi'nin lideri Lenin'in, emperyalizmi nasıl tanımladığı eseri hangisidir?", "cevaplar": ["Devlet ve Devrim", "Nisan Tezleri", "Emperyalizm: Kapitalizmin En Yüksek Aşaması", "Ne Yapmalı?"], "dogru": "Emperyalizm: Kapitalizmin En Yüksek Aşaması"},
    {"soru": "Rosa Luxemburg'un savunduğu, reformizm ve devrim ikilemi üzerine yazdığı ünlü eser nedir?", "cevaplar": ["Reform veya Devrim", "Sermaye Birikimi", "İşçi Hareketi", "Spartaküs"], "dogru": "Reform veya Devrim"},
    {"soru": "Toplumsal üretim araçlarının mülkiyetinin devlet elinde toplandığı, geçiş dönemi sistemi nedir?", "cevaplar": ["Liberalizm", "Anarşizm", "Sosyalizm", "Feodalizm"], "dogru": "Sosyalizm"},
    {"soru": "Antonio Gramsci'nin egemen sınıfın kültürel hakimiyetini kurma biçimi olarak tanımladığı kavram nedir?", "cevaplar": ["Otorite", "Hegemonya", "Baskı", "Propaganda"], "dogru": "Hegemonya"},
    {"soru": "1917 Ekim Devrimi gerçekleştiğinde Rusya'da iktidarda olan geçici hükümetin lideri kimdi?", "cevaplar": ["Kerenski", "Troçki", "Stalin", "Çar II. Nikola"], "dogru": "Kerenski"},
    {"soru": "Tarihsel Materyalizm'e göre toplumun hukuki ve siyasi yapısını belirleyen temel unsur nedir?", "cevaplar": ["Düşünceler", "Üretim Tarzı", "Coğrafya", "Kültür"], "dogru": "Üretim Tarzı"},
    {"soru": "Jean-Jacques Rousseau'nun sosyalizm fikirlerini etkileyen ünlü eseri hangisidir?", "cevaplar": ["Toplum Sözleşmesi", "İtiraflar", "Emile", "Söylev"], "dogru": "Toplum Sözleşmesi"}
]

# Değişkenleri başlat
if 'puan' not in st.session_state: st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'isim': ''})

st.title("☭ Sosyalist Teori Bilgi Yarışması")

if not st.session_state.oyun_basladi:
    isim = st.text_input("Yoldaş Adı:")
    if st.button("🚀 Mücadeleyi Başlat"):
        if isim:
            st.session_state.isim = isim
            st.session_state.oyun_basladi = True
            st.rerun()
        else: st.warning("İsmini gir yoldaş!")
    
    st.subheader("🏅 Liderlik Tablosu")
    try:
        with open("skorlar.txt", "r") as f:
            skorlar = f.readlines()
            for s in sorted(skorlar, key=lambda x: int(x.split('-')[1].strip()), reverse=True)[:5]:
                st.write(s.strip())
    except: st.write("Tablo boş, ilk sen doldur!")

elif st.session_state.soru_index < len(sorular):
    q = sorular[st.session_state.soru_index]
    st.subheader(f"Soru {st.session_state.soru_index + 1}: {q['soru']}")
    for secenek in q['cevaplar']:
        if st.button(secenek):
            if secenek == q['dogru']: st.session_state.puan += 1
            st.session_state.soru_index += 1
            st.rerun()
else:
    st.write(f"Oyun bitti {st.session_state.isim}! Skorun: {st.session_state.puan}")
    with open("skorlar.txt", "a") as f:
        f.write(f"{st.session_state.isim} - {st.session_state.puan}\n")
    if st.button("Tekrar Oyna"):
        st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False})
        st.rerun()