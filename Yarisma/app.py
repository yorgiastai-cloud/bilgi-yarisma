import streamlit as st
import time

st.set_page_config(page_title="MLM Tarihi Yarışması", layout="centered")

# Ekstra hiçbir kütüphane istemeyen, sunucu seviyesinde ortak canlı hafıza
@st.cache_data(ttl="2s")  # Skor tablosunu 2 saniyede bir canlı yeniler
def get_liderlik_tablosu():
    if 'global_skorlar' not in st.experimental_singleton:
        st.experimental_singleton['global_skorlar'] = {}
    return st.experimental_singleton['global_skorlar']

def skor_ekle(isim, puan):
    if 'global_skorlar' not in st.experimental_singleton:
        st.experimental_singleton['global_skorlar'] = {}
    
    # Eğer aynı isim varsa ve yeni puan daha yüksekse güncelle
    mevcut = st.experimental_singleton['global_skorlar'].get(isim, 0)
    if puan > mevcut:
        st.experimental_singleton['global_skorlar'][isim] = puan

# 15 Kavramsal ve Tarihsel Soru Paketi
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

if 'global_skorlar' not in st.experimental_singleton:
    st.experimental_singleton['global_skorlar'] = {}

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
        skorlar_dict = st.experimental_singleton['global_skorlar']
        if skorlar_dict:
            sirali_skorlar = sorted(skorlar_dict.items(), key=lambda x: int(x[1]), reverse=True)
            for k, v in sirali_skorlar[:5]:
                st.write(f"🌟 {k} — {v} Puan")
        else: st.write("Henüz skor yok!")
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
                skor_ekle(st.session_state.isim, st.session_state.puan)
                st.session_state.skor_kaydedildi = True
                st.success("Skorun başarıyla kaydedildi!")
                st.balloons()
                time.sleep(1)
                st.rerun()
        else: st.info("Skorun zaten kaydedildi yoldaş!")

        if st.button("🔄 Yeniden Oyna", key="btn_tekrar_oyna"):
            st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'skor_kaydedildi': False})
            st.rerun()