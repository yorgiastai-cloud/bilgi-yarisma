import streamlit as st
import time
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Sosyalist Teori Yarışması", layout="centered")

# Google Sheets Bağlantısı (Ayarları Streamlit Cloud panelinden alacak)
conn = st.connection("gsheets", type=GSheetsConnection)

# 15 Kavramsal Soru Paketi
sorular = [
    {"soru": "Karl Marx ve Friedrich Engels'in 'tarihin motoru' olarak tanımladığı kavram nedir?", "cevaplar": ["Teknoloji", "Sınıf Mücadelesi", "Eğitim", "Din"], "dogru": "Sınıf Mücadelesi"},
    {"soru": "Kapitalizmde üretilen metaların kullanım değeri ile değişim değeri arasındaki fark ne olarak adlandırılır?", "cevaplar": ["Kar", "Artı Değer", "Faiz", "Maliyet"], "dogru": "Artı Değer"},
    {"soru": "Antonio Gramsci'nin egemen sınıfın kültürel ve ideolojik hakimiyetini kurma biçimi olarak tanımladığı kavram nedir?", "cevaplar": ["Otorite", "Hegemonya", "Baskı", "Propaganda"], "dogru": "Hegemonya"},
    {"soru": "Tarihsel Materyalizm'e göre toplumun hukuki, siyasi ve ideolojik yapısını (Üstyapı) belirleyen temel unsur (Altyapı) nedir?", "cevaplar": ["Düşünceler", "Üretim Tarzı", "Coğrafya", "Kültür"], "dogru": "Üretim Tarzı"},
    {"soru": "Lenin'in, kapitalizmin tekelleşme ve finans sermayesinin egemenliğiyle küreselleşmesini tanımladığı kavram hangisidir?", "cevaplar": ["Küreselleşme", "Emperyalizm", "Merkantilizm", "Kolonizasyon"], "dogru": "Emperyalizm"},
    {"soru": "Rosa Luxemburg'un reformizm eleştirisinde savunduğu, kapitalizmin krizlerinin reformlarla çözülemeyeceğini ve devrimin zorunlu olduğunu anlatan ilke nedir?", "cevaplar": ["Reform veya Devrim", "Evrimsel Sosyalizm", "Revizyonizm", "Barışçıl Geçiş"], "dogru": "Reform veya Devrim"},
    {"soru": "Maoizmde, feodalizm ve emperyalizmin boyunduruğundaki az gelişmiş ülkelerde, devlet gücünü elinde tutan büyük sermayenin devletle bütünleşmesini ifade eden kavram nedir?", "cevaplar": ["Serbest Piyasa", "Bürokratik Kapitalizm", "Devlet Sosyalizmi", "Komprador Burjuvazi"], "dogru": "Bürokratik Kapitalizm"},
    {"soru": "Sovyetler Birliği'nde 1920'lerde şekillenen, dünya devrimini beklemeden öncelikle mevcut topraklarda sosyalist inşayı tamamlamayı hedefleyen tez hangisidir?", "cevaplar": ["Sürekli Devrim", "Tek Ülkede Sosyalizm", "Kalıcı Devrim", "Enternasyonalizm"], "dogru": "Tek Ülkede Sosyalizm"},
    {"soru": "İşçinin ürettiği ürüne, üretim sürecine ve kendi emeğine yabancılaşmasını ifade eden Marksist kavram hangisidir?", "cevaplar": ["Yabancılaşma", "Sömürü", "Yoksullaşma", "Anomi"], "dogru": "Yabancılaşma"},
    {"soru": "Üretim araçlarının özel mülkiyetinin yerini toplumsal mülkiyetin aldığı ve devletin kademeli olarak sönümlenmesini öngören nihai aşama nedir?", "cevaplar": ["Sosyalizm", "Komünizm", "Kapitalizm", "Sosyal Demokrasi"], "dogru": "Komünizm"},
    {"soru": "Kapitalist toplumda pazar için üretilen ve bir ihtiyacı tatmin etme özelliği (kullanım değeri) olan her türlü insan emeği ürününe ne ad verilir?", "cevaplar": ["Meta", "Sermaye", "Hammadde", "Para"], "dogru": "Meta"},
    {"soru": "Karl Marx'ın Hegel'den alıp materyalist bir temele oturttuğu, çelişkilerin ve zıtların birliğinin dönüşümünü inceleyen düşünce yöntemi nedir?", "cevaplar": ["Diyalektik Materyalizm", "İdealizm", "Pozitivizm", "Rasyonalizm"], "dogru": "Diyalektik Materyalizm"},
    {"soru": "Sosyalist teoride, kapitalizmden komünizme geçiş sürecinde işçi sınıfının siyasi iktidarı elinde tuttuğu geçici devlet biçimi nedir?", "cevaplar": ["Proletarya Diktatörlüğü", "Burjuva Demokrasisi", "Tek Parti Rejimi", "Otokrasi"], "dogru": "Proletarya Diktatörlüğü"},
    {"soru": "Metaların arkasındaki insan emeğinin unutulup, nesnelerin kendi aralarında mistik ve bağımsız bir ilişkiye sahipmiş gibi görünmesi durumuna ne denir?", "cevaplar": ["Meta Fetişizmi", "Reifikasyon", "Yabancılaşma", "Sermaye Birikimi"], "dogru": "Meta Fetişizmi"},
    {"soru": "Lenin'in 'Devlet ve Devrim' eserinde de vurguladığı, devletin tarafsız bir hakem değil, belirli bir sınıfın diğer sınıf üzerindeki ne aracı olduğunu savunur?", "cevaplar": ["Uzlaşma", "Baskı ve Tahakküm", "Hizmet", "Eğitim"], "dogru": "Baskı ve Tahakküm"}
]

if 'puan' not in st.session_state: 
    st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'isim': '', 'start_time': 0, 'skor_kaydedildi': False})

st.title("☭ Sosyalist Teori Bilgi Yarışması")

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
        # Verileri Google Sheets'ten canlı oku
        df = conn.read(ttl="5s") # 5 saniyede bir güncellenir
        if not df.empty:
            df['Puan'] = pd.to_numeric(df['Puan'])
            sirali_df = df.sort_values(by="Puan", ascending=False)
            for index, row in sirali_df.head(5).iterrows():
                st.write(f"{row['İsim']} - {int(row['Puan'])}")
        else: st.write("Henüz skor yok!")
    except: 
        st.write("Skor tablosu yükleniyor veya henüz veri yok...")

# 2. SORU EKRANI
else:
    if st.session_state.soru_index < len(sorular):
        q = sorular[st.session_state.soru_index]
        st.subheader(f"Soru {st.session_state.soru_index + 1}: {q['soru']}")
        
        gecen_sure = time.time() - st.session_state.start_time
        kalan_sure = 10 - int(gecen_sure)
        
        if kalan_sure > 0:
            st.metric("⏳ Kalan Süre", f"{kalan_sure} sn")
            for secenek in q['cevaplar']:
                if st.button(secenek, key=f"btn_{secenek}_{st.session_state.soru_index}"):
                    if secenek == q['dogru']:
                        taban_puan = 10
                        if gecen_sure < 3:
                            taban_puan += 5
                            st.success("✅ Harika! 15 Puan (10 Doğru + 5 Hız Bonusu)")
                        else: st.success("✅ Doğru! 10 Puan")
                        st.session_state.puan += taban_puan
                    else: st.error(f"❌ Yanlış! Doğrusu: {q['dogru']}")
                    
                    time.sleep(1.5)
                    st.session_state.soru_index += 1
                    st.session_state.start_time = time.time()
                    st.rerun()
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
        
        if not st.session_state.skor_kaydedildi:
            if st.button("🏆 Skorumu Liderlik Tablosuna Kaydet", key="btn_skor_kaydet"):
                try:
                    # Mevcut veriyi çek, yeni skoru ekle ve geri yükle
                    df = conn.read(ttl="0s")
                    new_row = pd.DataFrame([{"İsim": st.session_state.isim, "Puan": st.session_state.puan}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    
                    st.session_state.skor_kaydedildi = True
                    st.success("Skorun başarıyla Google Sheets'e kaydedildi!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error("Kayıt sırasında bir hata oluştu, lütfen ayarlara bağlantı linkini eklediğinizden emin olun.")
        else: st.info("Skorun zaten kaydedildi yoldaş!")

        if st.button("🔄 Yeniden Oyna", key="btn_tekrar_oyna"):
            st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'skor_kaydedildi': False})
            st.rerun()