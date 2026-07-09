import streamlit as st
import time

st.set_page_config(page_title="Devrim Tarihi Yarışması", layout="centered")

# Modern Streamlit sürümleriyle tam uyumlu, sunucu seviyesinde ortak canlı hafıza
@st.cache_resource
def get_liderlik_tablosu():
    return {}  # Tüm kullanıcılar için ortak bir skor sözlüğü oluşturur

global_skorlar = get_liderlik_tablosu()

def skor_ekle(isim, puan):
    # Eğer aynı isim daha önce kaydedilmişse, sadece daha yüksek olan skoru sakla
    mevcut_puan = global_skorlar.get(isim, 0)
    if puan > mevcut_puan:
        global_skorlar[isim] = puan

# 15 Kavramsal ve Tarihsel Soru Paketi
sorular = [
    {"soru": "1871 yılında işçi sınıfının tarihte ilk kez siyasi iktidarı ele geçirerek kurduğu ve Marx'ın 'nihayet keşfedilen siyasi biçim' olarak övdüğü tarihsel deneyim hangisidir?", "cevaplar": ["Paris Komünü", "Ekim Devrimi", "Spartaküs Ayaklanması", "Fransız Devrimi"], "dogru": "Paris Komünü"},
    {"soru": "Lenin'in, kapitalist devlet mekanizmasının reformlarla dönüştürülemeyeceğini, aksine devrimle parçalanması gerektiğini savunduğu temel Marksist ilke hangisidir?", "cevaplar": ["Devlet Cihazının Parçalanması", "Barışçıl Geçiş", "Anayasal Reform", "Sivil Toplum Teorisi"], "dogru": "Devlet Cihazının Parçalanması"},
    {"soru": "Maoizmde, devrimci süreçte kitlelerin taleplerini toplayıp teorik bir çerçeveye oturtarak tekrar kitlelere götürmeyi esas alan örgütsel yönteme ne ad verilir?", "cevaplar": ["Kitle Çizgisi", "Öncü Siyaset", "Yukarıdan Aşağı Yönetim", "Sınıf İttifakı"], "dogru": "Kitle Çizgisi"},
    {"soru": "Karl Marx'ın, kapitalist üretim tarzının işleyiş yasalarını ve sermayenin birikim mantığını en kapsamlı şekilde analiz ettiği başyapıtı hangisidir?", "cevaplar": ["Kapital", "Felsefenin Sefaleti", "Fransa'da Sınıf Mücadeleleri", "Grundrisse"], "dogru": "Kapital"},
    {"soru": "Lenin'in Marksist teoriye yaptığı en büyük katkılardan biri olan, emperyalist zincirin en zayıf halkasından kopacağı fikri hangi kavramla ifade edilir?", "cevaplar": ["En Zayıf Halka Teorisi", "Eşitsiz Gelişim Yasası", "Sürekli Devrim", "Tek Ülkede Sosyalizm"], "dogru": "En Zayıf Halka Teorisi"},
    {"soru": "Kapitalistlerin, üretim araçlarına sahip olmayan işçilerin emeğine el koyarak elde ettikleri ve sermaye birikiminin temel kaynağı olan değer nedir?", "cevaplar": ["Artı Değer", "Kullanım Değeri", "Değişim Değeri", "Finansal Kar"], "dogru": "Artı Değer"},
    {"soru": "Mao Zedong'un dogmatizme karşı yazdığı, pratiğin teoriden önce geldiğini ve gerçeğin olgulardan aranması gerektiğini savunan ünlü felsefi makalesi hangisidir?", "cevaplar": ["Pratik Üzerine", "Çelişki Üzerine", "Kültür Devrimi Notları", "Halk Savaşı"], "dogru": "Pratik Üzerine"},
    {"soru": "1917 Ekim Devrimi'nin hemen ardından imzalanan ve Sovyet Rusya'nın I. Dünya Savaşı'ndan çekilmesini sağlayan antlaşma hangisidir?", "cevaplar": ["Brest-Litovsk", "Versay", "Mondros", "Litvinov Paktı"], "dogru": "Brest-Litovsk"},
    {"soru": "Karl Marx ve Friedrich Engels'in birlikte kaleme aldığı, 'Avrupa'da bir hayalet dolaşıyor' cümlesiyle başlayan tarihi belge hangisidir?", "cevaplar": ["Komünist Manifesto", "Alman İdeolojisi", "Kutsal Aile", "Gotha Programının Eleştirisi"], "dogru": "Komünist Manifesto"},
    {"soru": "Marksizme göre, sömürgeci ülkelerin az gelişmiş halkları ekonomik ve siyasi olarak kendilerine bağımlı kılma sürecine ne ad verilir?", "cevaplar": ["Emperyalizm", "Merkantilizm", "Liberalizm", "Feodalizm"], "dogru": "Emperyalizm"},
    {"soru": "Lenin'in, çarlık Rusyası'nda devrimci bir gazetenin ve merkezi bir örgütün önemini tartışarak 'Bize bir devrimciler örgütü verin, Rusya'yı yerinden oynatalım' dediği meşhur eseri hangisidir?", "cevaplar": ["Ne Yapmalı?", "Nisan Tezleri", "Devlet ve Devrim", "Bir Adım İleri, İki Adım Geri"], "dogru": "Ne Yapmalı?"},
    {"soru": "Maoizmde, bir çelişkinin taraflarının birbirini tamamen yok etme eğiliminde olduğu, uzlaşmaz toplumsal çelişki türüne ne ad verilir?", "cevaplar": ["Antagonistik Çelişki", "Uzlaşabilir Çelişki", "İkincil Çelişki", "İç Çelişki"], "dogru": "Antagonistik Çelişki"},
    {"soru": "Friedrich Engels'in, özel mülkiyetin ve sınıflı toplumun kökenlerini antropolojik verilerle incelediği ünlü eseri hangisidir?", "cevaplar": ["Ailenin, Özel Mülkiyetin ve Devletin Kökeni", "Anti-Dühring", "Doğanın Diyalektiği", "Ütopyacı Sosyalizm ve Bilimsel Sosyalizm"], "dogru": "Ailenin, Özel Mülkiyetin ve Devletin Kökeni"},
    {"soru": "1921 yılında SSCB'de köylü ayaklanmaları ve ekonomik kriz sonrası Lenin tarafından ilan edilen, geçici olarak küçük ölçekli kapitalist üretime izin veren politikanın adı nedir?", "cevaplar": ["NEP (Yeni Ekonomik Politika)", "Kolektifleştirme", "Savaş Komünizmi", "Beş Yıllık Plan"], "dogru": "NEP (Yeni Ekonomik Politika)"},
    {"soru": "Marksist tarih anlayışına göre, insanlığın sınıflara bölünmediği, üretim araçlarının ortak olduğu ilk tarihsel aşamaya ne ad verilir?", "cevaplar": ["İlkel Komünizm", "Feodalizm", "Kölelik Düzeni", "Asya Tipi Üretim Tarzı"], "dogru": "İlkel Komünizm"}
]

# Kullanıcı oturum hafızası
if 'puan' not in st.session_state: 
    st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'isim': '', 'start_time': 0, 'skor_kaydedildi': False})

st.title("☭ MLM Tarihi Yarışması")

# 1. GİRİŞ EKRANI
if not st.session_state.oyun_basladi:
    isim = st.text_input("Yoldaş Adı:", key="giris_yoldas_adi")
    if st.button("🚀 Mücadeleye Başla", key="but_basla"):
        if isim:
            st.session_state.isim = isim
            st.session_state.oyun_basladi = True
            st.session_state.start_time = time.time()
            st.session_state.skor_kaydedildi = False
            st.rerun()
        else: st.warning("Lütfen bir isim gir yoldaş!")
    
    st.subheader("🏅 En Yüksek Skorlar (Canlı)")
    try:
        if global_skorlar:
            # Skorları yüksekten düşüğe doğru sırala
            sirali_skorlar = sorted(global_skorlar.items(), key=lambda x: int(x[1]), reverse=True)
            for k, v in sirali_skorlar[:10]:
                st.write(f"🌟 {k} — {v} Puan")
        else:
            st.write("Henüz skor yok, ilk sen ol!")
    except:
        st.write("Skor tablosu yükleniyor...")

# 2. SORU EKRANI
else:
    if st.session_state.soru_index < len(sorular):
        q = sorular[st.session_state.soru_index]
        st.subheader(f"Soru {st.session_state.soru_index + 1}: {q['soru']}")
        
        gecen_sure = time.time() - st.session_state.start_time
        kalan_sure = 30 - int(gecen_sure)
        
        if kalan_sure > 0:
            st.metric("⏱️ Kalan Süre", f"{kalan_sure} sn")
            for secenek in q['cevaplar']:
                if st.button(secenek, key=f"btn_{secenek}_{st.session_state.soru_index}"):
                    if secenek == q['dogru']:
                        taban_puan = 10
                        if gecen_sure < 6:
                            taban_puan += 5
                            st.success("⚡ Müthiş Hız! 15 Puan (10 Doğru + 5 Hız Bonusu)")
                        else: st.success("✅ Bravo Yoldaş! 10 Puan")
                        st.session_state.puan += taban_puan
                    else: st.error(f"❌ Yeniden Dene Yoldaş! Doğrusu: {q['dogru']}")
                    
                    time.sleep(1.5)
                    st.session_state.soru_index += 1
                    st.session_state.start_time = time.time()
                    st.rerun()
            time.sleep(0.1)
            st.rerun()
        else:
            st.error("⏳ Süre doldu yoldaş!")
            time.sleep(1.5)
            st.session_state.soru_index += 1
            st.session_state.start_time = time.time()
            st.rerun()

    # 3. OYUN BİTTİ EKRANI
    else:
        st.subheader(f"🎉 Oyun bitti yoldaş, devrimci kal {st.session_state.isim}!")
        st.write(f"**Toplam Skorun:** {st.session_state.puan}")
        
        if not st.session_state.skor_kaydedildi:
            if st.button("🏆 Skorumu Liderlik Tablosuna Kaydet", key="btn_skor_kaydet"):
                skor_ekle(st.session_state.isim, st.session_state.puan)
                st.session_state.skor_kaydedildi = True
                st.success("Skorun başarıyla sisteme kaydedildi!")
                st.balloons()
                time.sleep(1)
                st.rerun()
        else: st.info("Skorun zaten kaydedildi yoldaş!")

        if st.button("🔄 Yeniden Oyna", key="btn_tekrar_oyna"):
            st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'skor_kaydedildi': False})
            st.rerun()