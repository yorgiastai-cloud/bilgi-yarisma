import streamlit as st
import time
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Sosyalist Teori ve Devrim Tarihi Yarışması", layout="centered")

# Google Sheets Bağlantısı
conn = st.connection("gsheets", type=GSheetsConnection)

# 15 Yeni Kavramsal ve Tarihsel Soru Paketi
sorular = [
    {"soru": "1917 Ekim Devrimi sırasında 'Bütün İktidar Sovyetlere!' sloganıyla öne çıkan ve devrimin yol haritası kabul edilen Lenin'in ünlü metni hangisidir?", "cevaplar": ["Nisan Tezleri", "Devlet ve Devrim", "Ne Yapmalı?", "Sol Komünizm"], "dogru": "Nisan Tezleri"},
    {"soru": "Çin Devrimi'nin stratejik temelini oluşturan, kırlardan şehirlere doğru ilerleyen devrimci savaş stratejisine ne ad verilir?", "cevaplar": ["Topyekün Savaş", "Halk Savaşı", "Gerilla Doktrini", "Kızıl Harekat"], "dogru": "Halk Savaşı"},
    {"soru": "Lenin'e göre, işçi sınıfına kendiliğinden sadece sendikal bilinç ulaşabilir. Sosyalist bilincin sınıfa dışarıdan, öncü parti aracılığıyla götürülmesi gerektiğini savunduğu kavram hangisidir?", "cevaplar": ["Kendiliğindenlik", "Öncü Parti Teorisi", "Demokratik Merkeziyetçilik", "Sınıf Bilinci"], "dogru": "Öncü Parti Teorisi"},
    {"soru": "Ekim Devrimi'nin hemen ardından, devrimi ve Sovyet iktidarını korumak amacıyla kurulan gizli siyasi polis teşkilatı hangisidir?", "cevaplar": ["KGB", "Çeka", "NKVD", "Gruman"], "dogru": "Çeka"},
    {"soru": "Mao Zedong'un, sosyalist inşa sürecinde toplumdaki çelişkilerin barışçıl ve tartışma yoluyla çözülmesi gerektiğini savunduğu ünlü kampanyasının adı nedir?", "cevaplar": ["Yüz Çiçek Açsın", "Büyük İleri Atılım", "Kültür Devrimi", "Kızıl Bayrak"], "dogru": "Yüz Çiçek Açsın"},
    {"soru": "Marksizm-Leninizm'de, partinin kararlar alınırken tam bir tartışma özgürlüğü, karar alındıktan sonra ise tam bir eylem birliği içinde hareket etmesini öngören ilke nedir?", "cevaplar": ["Bürokratizm", "Demokratik Merkeziyetçilik", "Fraksiyonizm", "Kolektif Önderlik"], "dogru": "Demokratik Merkeziyetçilik"},
    {"soru": "Çin Devrimi sürecinde, sanayileşmiş bir işçi sınıfının azınlıkta olması nedeniyle Mao'nun devrimin temel gücü olarak konumlandırdığı sınıf hangisidir?", "cevaplar": ["Köylülük", "Komprador Burjuvazi", "Küçük Burjuvazi", "Lumpen Proletarya"], "dogru": "Köylülük"},
    {"soru": "Ekim Devrimi'ni fiilen organize eden, Askeri Devrimci Komite'nin başında yer alan ve Kızıl Ordu'nun kurucusu olan lider kimdir?", "cevaplar": ["Stalin", "Troçki", "Buharin", "Kamenev"], "dogru": "Troçki"},
    {"soru": "Maoizmde, bir toplumdaki temel çelişkinin yanı sıra, o anki tarihsel aşamada devrimin önündeki en büyük engeli oluşturan çelişki türüne ne ad verilir?", "cevaplar": ["Baş Çelişki", "Antagonistik Çelişki", "İkincil Çelişki", "İç Çelişki"], "dogru": "Baş Çelişki"},
    {"soru": "Ekim Devrimi öncesinde, Temmuz Günleri'nin ardından Lenin'in saklandığı kulübede yazdığı, devletin sönümlenmesi teorisini ele alan başyapıtı hangisidir?", "cevaplar": ["Emperyalizm", "Devlet ve Devrim", "Ne Yapmalı?", "Marx Üzerine"], "dogru": "Devlet ve Devrim"},
    {"soru": "Mao Zedong'un, Çin'in geleneksel yapısını kırıp kapitalist geri dönüşü engellemek amacıyla 1966'da başlattığı kitlesel hareketin adı nedir?", "cevaplar": ["Büyük İleri Atılım", "Büyük Proleter Kültür Devrimi", "Dörtlü Çete Hareketi", "Kızıl Muhafızlar Seferi"], "dogru": "Büyük Proleter Kültür Devrimi"},
    {"soru": "Ekim Devrimi'ni başlatan ve Geçici Hükümet'in bulunduğu Kışlık Saray'ın bombalanması işaretini veren ünlü zırhlı geminin adı nedir?", "cevaplar": ["Potemkin", "Aurora", "Kronstadt", "Varyag"], "dogru": "Aurora"},
    {"soru": "Marksist teoride, üretim sürecinde kullanılan makineler, fabrikalar ve hammaddeler ile bunları kullanan insan emeğinin bütününü ifade eden kavram hangisidir?", "cevaplar": ["Üretim İlişkileri", "Üretici Güçler", "Üretim Tarzı", "Altyapı"], "dogru": "Üretici Güçler"},
    {"soru": "Lenin'in ölümünden sonra SSCB'nin sanayileşme ve kolektifleştirme hamlelerini başlatan, beş yıllık kalkınma planlarını uygulayan lider kimdir?", "cevaplar": ["Hruşçov", "Stalin", "Breznev", "Malenkov"], "dogru": "Stalin"},
    {"soru": "Çin Devrimi'nde ilan edilen, emperyalizme ve feodalizme karşı işçi, köylü, küçük burjuvazi ve ulusal burjuvazinin ittifakına dayanan devlet modeline ne ad verilir?", "cevaplar": ["Yeni Demokrasi", "Proletarya Diktatörlüğü", "Halk Cumhuriyeti", "Sosyalist Blok"], "dogru": "Yeni Demokrasi"}
]

if 'puan' not in st.session_state: 
    st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'isim': '', 'start_time': 0, 'skor_kaydedildi': False})

st.title("☭ Teori ve Devrim Tarihi Yarışması")

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
        df = conn.read(ttl="5s")
        if not df.empty:
            df['Puan'] = pd.to_numeric(df['Puan'])
            sirali_df = df.sort_values(by="Puan", ascending=False)
            for index, row in sirali_df.head(5).iterrows():
                st.write(f"🌟 {row['İsim']} — {int(row['Puan'])} Puan")
        else: st.write("Henüz skor yok!")
    except: 
        st.write("Skor tablosu yükleniyor...")

# 2. SORU EKRANI
else:
    if st.session_state.soru_index < len(sorular):
        q = sorular[st.session_state.soru_index]
        st.subheader(f"Soru {st.session_state.soru_index + 1}: {q['soru']}")
        
        # 30 Saniyeden Geriye Sayım
        gecen_sure = time.time() - st.session_state.start_time
        kalan_sure = 30 - int(gecen_sure)
        
        if kalan_sure > 0:
            st.metric("⏱️ Kalan Süre", f"{kalan_sure} sn")
            for secenek in q['cevaplar']:
                if st.button(secenek, key=f"btn_{secenek}_{st.session_state.soru_index}"):
                    if secenek == q['dogru']:
                        taban_puan = 10
                        # Hız bonusu süresini de 3 saniyeden 6 saniyeye çıkardım (Süre uzadığı için adil olsun diye)
                        if gecen_sure < 6:
                            taban_puan += 5
                            st.success("⚡ Müthiş Hız! 15 Puan (10 Doğru + 5 Hız Bonusu)")
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
                    df = conn.read(ttl="0s")
                    new_row = pd.DataFrame([{"İsim": st.session_state.isim, "Puan": st.session_state.puan}])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    
                    st.session_state.skor_kaydedildi = True
                    st.success("Skorun başarıyla Google Sheets'e kaydedildi!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                except:
                    st.error("Kayıt sırasında bir hata oluştu.")
        else: st.info("Skorun zaten kaydedildi yoldaş!")

        if st.button("🔄 Yeniden Oyna", key="btn_tekrar_oyna"):
            st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'skor_kaydedildi': False})
            st.rerun()