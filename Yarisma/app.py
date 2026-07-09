import streamlit as st
import time
import random

st.set_page_config(page_title="MLM Devrim Tarihi Yarışması", layout="centered")

@st.cache_resource
def get_liderlik_tablosu():
    return {}

global_skorlar = get_liderlik_tablosu()

def skor_ekle(isim, puan):
    mevcut_puan = global_skorlar.get(isim, 0)
    if puan > mevcut_puan:
        global_skorlar[isim] = puan

# 100 SORULUK DEVASA SORU HAVUZU
soru_havuzu = [
    # --- 1-20: Ekim Devrimi & Sovyet Tarihi ---
    {"soru": "1917 Ekim Devrimi sırasında 'Bütün İktidar Sovyetlere!' sloganıyla öne çıkan ve devrimin yol haritası kabul edilen Lenin'in ünlü metni hangisidir?", "cevaplar": ["Nisan Tezleri", "Devlet ve Devrim", "Ne Yapmalı?", "Sol Komünizm"], "dogru": "Nisan Tezleri"},
    {"soru": "Ekim Devrimi'nin hemen ardından, devrimi ve Sovyet iktidarını korumak amacıyla kurulan gizli siyasi polis teşkilatı hangisidir?", "cevaplar": ["KGB", "Çeka", "NKVD", "Gruman"], "dogru": "Çeka"},
    {"soru": "Ekim Devrimi'ni fiilen organize eden, Askeri Devrimci Komite'nin başında yer alan ve Kızıl Ordu'nun kurucusu olan lider kimdir?", "cevaplar": ["Stalin", "Troçki", "Buharin", "Kamenev"], "dogru": "Troçki"},
    {"soru": "Ekim Devrimi öncesinde, Temmuz Günleri'nin ardından Lenin'in saklandığı kulübede yazdığı, devletin sönümlenmesi teorisini ele alan başyapıtı hangisidir?", "cevaplar": ["Emperyalizm", "Devlet ve Devrim", "Ne Yapmalı?", "Marx Üzerine"], "dogru": "Devlet ve Devrim"},
    {"soru": "Ekim Devrimi'ni başlatan ve Geçici Hükümet'in bulunduğu Kışlık Saray'ın bombalanması işaretini veren ünlü zırhlı geminin adı nedir?", "cevaplar": ["Potemkin", "Aurora", "Kronstadt", "Varyag"], "dogru": "Aurora"},
    {"soru": "Lenin'in ölümünden sonra SSCB'nin sanayileşme ve kolektifleştirme hamlelerini başlatan, beş yıllık kalkınma planlarını uygulayan lider kimdir?", "cevaplar": ["Hruşçov", "Stalin", "Breznev", "Malenkov"], "dogru": "Stalin"},
    {"soru": "1917 Ekim Devrimi'nin hemen ardından imzalanan ve Sovyet Rusya'nın I. Dünya Savaşı'ndan çekilmesini sağlayan antlaşma hangisidir?", "cevaplar": ["Brest-Litovsk", "Versay", "Mondros", "Litvinov Paktı"], "dogru": "Brest-Litovsk"},
    {"soru": "1921 yılında SSCB'de köylü ayaklanmaları ve ekonomik kriz sonrası Lenin tarafından ilan edilen, geçici olarak küçük ölçekli kapitalist üretime izin veren politikanın adı nedir?", "cevaplar": ["NEP (Yeni Ekonomik Politika)", "Kolektifleştirme", "Savaş Komünizmi", "Beş Yıllık Plan"], "dogru": "NEP (Yeni Ekonomik Politika)"},
    {"soru": "Lenin, 1917 devrimi öncesi sürgünden Rusya'ya hangi araçla dönmüştür?", "cevaplar": ["Gemi", "Mühürlü Tren", "Uçak", "At Arabası"], "dogru": "Mühürlü Tren"},
    {"soru": "Lenin'in kurduğu ve Sovyetler Birliği'nin temelini atan parti hangisidir?", "cevaplar": ["Menşevik", "Bolşevik", "Sosyalist Devrimci", "Anarşist"], "dogru": "Bolşevik"},
    {"soru": "Stalin, hangi savaş sırasında 'Başkomutan' sıfatıyla ordunun başındaydı?", "cevaplar": ["I. Dünya Savaşı", "İç Savaş", "II. Dünya Savaşı", "Kore Savaşı"], "dogru": "II. Dünya Savaşı"},
    {"soru": "Lenin, hangi ünlü takma adı (Lenin) kullanmadan önce gençlik yıllarında hangi nehrin adından esinlenmiştir?", "cevaplar": ["Volga", "Lena", "Don", "Dinyeper"], "dogru": "Lena"},
    {"soru": "Sovyetler Birliği'nde 1920'lerde şekillenen, dünya devrimini beklemeden öncelikle mevcut topraklarda sosyalist inşayı tamamlamayı hedefleyen tez hangisidir?", "cevaplar": ["Sürekli Devrim", "Tek Ülkede Sosyalizm", "Kalıcı Devrim", "Enternasyonalizm"], "dogru": "Tek Ülkede Sosyalizm"},
    {"soru": "Ekim Devrimi'nin ilk yıllarında (1918-1921) iç savaş koşullarında uygulanan sert ekonomik ve siyasi politikalara ne ad verilir?", "cevaplar": ["Savaş Komünizmi", "NEP", "Kolektifleştirme", "Kültür Devrimi"], "dogru": "Savaş Komünizmi"},
    {"soru": "Lenin'in 1902 yılında yazdığı, devrimci örgüt ve profesyonel devrimciler partisi fikrini ilk kez akademik olarak ortaya koyduğu eserin adı nedir?", "cevaplar": ["Ne Yapmalı?", "Devlet ve Devrim", "Sol Komünizm", "Emperyalizm"], "dogru": "Ne Yapmalı?"},
    {"soru": "Bolşevik Partisi'nin 1903 yılındaki 2. Kongresi'nde yaşanan bölünmede Lenin'in azınlıkta kalan muhaliflerine ne ad verilmiştir?", "cevaplar": ["Menşevik", "Trudovik", "Kadret", "Eser"], "dogru": "Menşevik"},
    {"soru": "1905 Rus Devrimi'ni ateşleyen ve çarın askerlerinin silahsız işçilere ateş açtığı tarihi olaya ne ad verilir?", "cevaplar": ["Kanlı Pazar", "Temmuz Günleri", "Ekim İsyanı", "Kış Sarayı Baskını"], "dogru": "Kanlı Pazar"},
    {"soru": "1921 yılında Bolşevik iktidarına karşı isyan eden ve 'Sovyetler evet, Bolşevikler hayır' sloganını kullanan ünlü deniz üssü hangisidir?", "cevaplar": ["Kronstadt", "Sivastopol", "Odesa", "Murmansk"], "dogru": "Kronstadt"},
    {"soru": "SSCB'nin ikinci anayasası olan ve 1936 yılında yürürlüğe giren genel oy hakkı içeren anayasa hangi liderin adıyla anılır?", "cevaplar": ["Stalin Anayasası", "Lenin Anayasası", "Breznev Anayasası", "Hruşçov Anayasası"], "dogru": "Stalin Anayasası"},
    {"soru": "Ekim Devrimi'nden sonra kurulan ilk Sovyet hükümetinin resmi adı nedir?", "cevaplar": ["Halk Komiserleri Konseyi (Sovnarkom)", "Yüksek Sovyet Prezidyumu", "Geçici Devrim Komitesi", "Merkez Komitesi"], "dogru": "Halk Komiserleri Konseyi (Sovnarkom)"},

    # --- 21-40: Çin Devrimi & Maoizm ---
    {"soru": "Çin Devrimi'nin stratejik temelini oluşturan, kırlardan şehirlere doğru ilerleyen devrimci savaş stratejisine ne ad verilir?", "cevaplar": ["Topyekün Savaş", "Halk Savaşı", "Gerilla Doktrini", "Kızıl Harekat"], "dogru": "Halk Savaşı"},
    {"soru": "Mao Zedong'un, sosyalist inşa sürecinde toplumdaki çelişkilerin barışçıl ve tartışma yoluyla çözülmesi gerektiğini savunduğu ünlü kampanyasının adı nedir?", "cevaplar": ["Yüz Çiçek Açsın", "Büyük İleri Atılım", "Kültür Devrimi", "Kızıl Bayrak"], "dogru": "Yüz Çiçek Açsın"},
    {"soru": "Çin Devrimi süreçinde, sanayileşmiş bir işçi sınıfının azınlıkta olması nedeniyle Mao'nun devrimin temel gücü olarak konumlandırdığı sınıf hangisidir?", "cevaplar": ["Köylülük", "Komprador Burjuvazi", "Küçük Burjuvazi", "Lumpen Proletarya"], "dogru": "Köylülük"},
    {"soru": "Maoizmde, bir toplumdaki temel çelişkinin yanı sıra, o anki tarihsel aşamada devrimin önündeki en büyük engeli oluşturan çelişki türüne ne ad verilir?", "cevaplar": ["Baş Çelişki", "Antagonistik Çelişki", "İkincil Çelişki", "İç Çelişki"], "dogru": "Baş Çelişki"},
    {"soru": "Mao Zedong'un, Çin'in geleneksel yapısını kırıp kapitalist geri dönüşü engellemek amacıyla 1966'da başlattığı kitlesel hareketin adı nedir?", "cevaplar": ["Büyük İleri Atılım", "Büyük Proleter Kültür Devrimi", "Dörtlü Çete Hareketi", "Kızıl Muhafızlar Seferi"], "dogru": "Büyük Proleter Kültür Devrimi"},
    {"soru": "Çin Devrimi'nde ilan edilen, emperyalizme ve feodalizme karşı işçi, köylü, küçük burjuvazi ve ulusal burjuvazinin ittifakına dayanan devlet modeline ne ad verilir?", "cevaplar": ["Yeni Demokrasi", "Proletarya Diktatörlüğü", "Halk Cumhuriyeti", "Sosyalist Blok"], "dogru": "Yeni Demokrasi"},
    {"soru": "Maoizmde, devrimci süreçte kitlelerin taleplerini toplayıp teorik bir çerçeveye oturtarak tekrar kitlelere götürmeyi esas alan örgütsel yönteme ne ad verilir?", "cevaplar": ["Kitle Çizgisi", "Öncü Siyaset", "Yukarıdan Aşağı Yönetim", "Sınıf İttifakı"], "dogru": "Kitle Çizgisi"},
    {"soru": "Mao Zedong'un dogmatizme karşı yazdığı, pratiğin teoriden önce geldiğini ve gerçeğin olgulardan aranması gerektiğini savunan ünlü felsefi makalesi hangisidir?", "cevaplar": ["Pratik Üzerine", "Çelişki Üzerine", "Kültür Devrimi Notları", "Halk Savaşı"], "dogru": "Pratik Üzerine"},
    {"soru": "Maoizmde, bir çelişkinin taraflarının birbirini tamamen yok etme eğiliminde olduğu, uzlaşmaz toplumsal çelişki türüne ne ad verilir?", "cevaplar": ["Antagonistik Çelişki", "Uzlaşabilir Çelişki", "İkincil Çelişki", "İç Çelişki"], "dogru": "Antagonistik Çelişki"},
    {"soru": "Mao Zedong'un 1934-1935 yılları arasında önderlik ettiği meşhur geri çekilme harekâtı nedir?", "cevaplar": ["Büyük Yürüyüş", "Kültür Devrimi", "İleri Atılım", "Kızıl Ordu Seferi"], "dogru": "Büyük Yürüyüş"},
    {"soru": "Mao Zedong, hangi siyasi doktrinin Çin şartlarına uyarlanmış halini geliştirmiştir?", "cevaplar": ["Troçkizm", "Marksizm-Leninizm", "Anarko-Komünizm", "Sosyal Demokrasi"], "dogru": "Marksizm-Leninizm"},
    {"soru": "Mao Zedong'un ünlü 'Küçük Kırmızı Kitap'ı hangi dönemde yaygınlaşmıştır?", "cevaplar": ["Uzun Yürüyüş", "Kültür Devrimi", "İç Savaş", "Devrim Öncesi"], "dogru": "Kültür Devrimi"},
    {"soru": "Mao Zedong, gençlik yıllarında Pekin Üniversitesi'nde hangi görevde çalışmıştır?", "cevaplar": ["Kütüphane Memuru", "Tarih Profesörü", "Matbaa İşçisi", "Çevirmen"], "dogru": "Kütüphane Memuru"},
    {"soru": "Maoizmde, feodalizm ve emperyalizmin boyunduruğundaki az gelişmiş ülkelerde, devlet gücünü elinde tutan büyük sermayenin devletle bütünleşmesini ifade eden kavram nedir?", "cevaplar": ["Serbest Piyasa", "Bürokratik Kapitalizm", "Devlet Sosyalizmi", "Komprador Burjuvazi"], "dogru": "Bürokratik Kapitalizm"},
    {"soru": "Çin Devrimi'nin başarıya ulaşarak Çin Halk Cumhuriyeti'nin ilan edildiği tarihi yıl hangisidir?", "cevaplar": ["1911", "1927", "1945", "1949"], "dogru": "1949"},
    {"soru": "Çin'de Mao önderliğinde 1958-1962 yılları arasında uygulanan, hızlı sanayileşme ve kolektifleştirme hamlesi nedir?", "cevaplar": ["Büyük İleri Atılım", "Kültür Devrimi", "Dört Modernizasyon", "Halk Komünleri Hareketi"], "dogru": "Büyük İleri Atılım"},
    {"soru": "Çin Devrimi sürecinde komünistlerin savaştığı, Çan Kay-şek liderliğindeki milliyetçi partinin adı nedir?", "cevaplar": ["Kuomintang", "Çin Milliyetçi Cephesi", "Kızıl Kuşak", "Ming Partisi"], "dogru": "Kuomintang"},
    {"soru": "Mao Zedong'un felsefi katkılarından biri olan, evrendeki her şeyin zıtların birliği ve mücadelesinden oluştuğunu savunan eseri hangisidir?", "cevaplar": ["Çelişki Üzerine", "Pratik Üzerine", "Liberalizmi Eleştir", "Doğru Tutum"], "dogru": "Çelişki Üzerine"},
    {"soru": "Maoizmde, emperyalist ülkelerin yerli işbirlikçisi olan ve devrimin baş hedeflerinden biri sayılan burjuvazi kesimine ne ad verilir?", "cevaplar": ["Komprador Burjuvazi", "Ulusal Burjuvazi", "Küçük Burjuvazi", "Bürokrat Burjuvazi"], "dogru": "Komprador Burjuvazi"},
    {"soru": "Kültür Devrimi sırasında Mao'nun fikirlerini radikal bir şekilde savunan genç militan kitlelere ne ad verilirdi?", "cevaplar": ["Kızıl Muhafızlar", "Kızıl Tugaylar", "Halk Öncüleri", "Devrim Muhafızları"], "dogru": "Kızıl Muhafızlar"},

    # --- 41-60: Karl Marx & Friedrich Engels ---
    {"soru": "Karl Marx hangi şehirde doğmuştur?", "cevaplar": ["Berlin", "Trier", "Londra", "Paris"], "dogru": "Trier"},
    {"soru": "Friedrich Engels, Marx'ın hangi eserinin bitirilmesine büyük katkı sağlamıştır?", "cevaplar": ["Kapital", "Manifesto", "Grundrisse", "18. Brumaire"], "dogru": "Kapital"},
    {"soru": "Marx'ın hayatının büyük bir kısmını geçirdiği ve 'Kapital'i yazdığı kütüphane hangi şehirdedir?", "cevaplar": ["Paris", "Londra", "Berlin", "Brüksel"], "dogru": "Londra"},
    {"soru": "Engels, Manchester'da ne iş yapıyordu?", "cevaplar": ["Gazetecilik", "Fabrika Yöneticiliği", "Hukukçuluk", "Tıp"], "dogru": "Fabrika Yöneticiliği"},
    {"soru": "Marx'ın mezarı hangi şehirdedir?", "cevaplar": ["Trier", "Berlin", "Londra", "Paris"], "dogru": "Londra"},
    {"soru": "Friedrich Engels'in 'İngiltere'de İşçi Sınıfının Durumu' adlı eseri hangi şehri anlatır?", "cevaplar": ["Londra", "Manchester", "Liverpool", "Birmingham"], "dogru": "Manchester"},
    {"soru": "Karl Marx, üniversite eğitimini hangi alanda tamamlamıştır?", "cevaplar": ["Tıp", "Hukuk ve Felsefe", "Ekonomi", "Siyaset Bilimi"], "dogru": "Hukuk ve Felsefe"},
    {"soru": "Friedrich Engels, çok genç yaşta orduya katılarak hangi birlikte askeri eğitim almıştır?", "cevaplar": ["Prusya Topçu Birliği", "Fransız Süvarileri", "Rus Piyadeleri", "İngiliz Donanması"], "dogru": "Prusya Topçu Birliği"},
    {"soru": "Karl Marx ve Friedrich Engels'in 'tarihin motoru' olarak tanımladığı kavram nedir?", "cevaplar": ["Teknoloji", "Sınıf Mücadelesi", "Eğitim", "Din"], "dogru": "Sınıf Mücadelesi"},
    {"soru": "Karl Marx'ın Hegel'den alıp materyalist bir temele oturttuğu, çelişkilerin ve zıtların birliğinin dönüşümünü inceleyen düşünce yöntemi nedir?", "cevaplar": ["Diyalektik Materyalizm", "İdealizm", "Pozitivizm", "Rasyonalizm"], "dogru": "Diyalektik Materyalizm"},
    {"soru": "Karl Marx ve Friedrich Engels'in birlikte kaleme aldığı, 'Avrupa'da bir hayalet dolaşıyor' cümlesiyle başlayan tarihi belge hangisidir?", "cevaplar": ["Komünist Manifesto", "Alman İdeolojisi", "Kutsal Aile", "Gotha Programının Eleştirisi"], "dogru": "Komünist Manifesto"},
    {"soru": "Friedrich Engels'in, özel mülkiyetin ve sınıflı toplumun kökenlerini antropolojik verilerle incelediği ünlü eseri hangisidir?", "cevaplar": ["Ailenin, Özel Mülkiyetin ve Devletin Kökeni", "Anti-Dühring", "Doğanın Diyalektiği", "Ütopyacı Sosyalizm ve Bilimsel Sosyalizm"], "dogru": "Ailenin, Özel Mülkiyetin ve Devletin Kökeni"},
    {"soru": "Karl Marx'ın, Louis Bonaparte'ın hükümet darbesini ve devlet mekanizmasını tarihsel materyalist açıdan analiz ettiği eseri hangisidir?", "cevaplar": ["Louis Bonaparte'ın 18 Brumaire'i", "Kutsal Aile", "Felsefenin Sefaleti", "Fransa'da İç Savaş"], "dogru": "Louis Bonaparte'ın 18 Brumaire'i"},
    {"soru": "Marx'ın Paris'te gençlik yıllarında yazdığı, yabancılaşma teorisini ilk kez kapsamlıca ele aldığı el yazmaları hangi yıla aittir?", "cevaplar": ["1844", "1848", "1859", "1867"], "dogru": "1844"},
    {"soru": "Marx'ın ekonomi-politiğin eleştirisine giriş mahiyetindeki, Capital'in taslağı olarak kabul edilen devasa notlar bütünü nedir?", "cevaplar": ["Grundrisse", "Değer Teorisi", "Artı-Değer Teorileri", "Alman İdeolojisi"], "dogru": "Grundrisse"},
    {"soru": "Marx ve Engels'in, genç Hegelyanların idealist görüşlerini eleştirmek amacıyla yazdıkları ancak hayattayken basılamayan ortak eserleri hangisidir?", "cevaplar": ["Alman İdeolojisi", "Kutsal Aile", "Felsefenin Sefaleti", "Anti-Dühring"], "dogru": "Alman İdeolojisi"},
    {"soru": "Marx'ın, Alman Sosyal Demokrat Partisi'nin program taslağını sertçe eleştirdiği ve komünizmin aşamalarını tartıştığı eseri hangisidir?", "cevaplar": ["Gotha Programının Eleştirisi", "Erfurt Programı", "Komünizmin İlkeleri", "Ücret, Fiyat, Kar"], "dogru": "Gotha Programının Eleştirisi"},
    {"soru": "Friedrich Engels'in, Eugen Dühring'in teorilerine yanıt olarak yazdığı ve Marksizmin adeta bir ansiklopedisi haline gelen eseri hangisidir?", "cevaplar": ["Anti-Dühring", "Doğanın Diyalektiği", "Konut Sorunu", "Ludwig Feuerbach"], "dogru": "Anti-Dühring"},
    {"soru": "Marx'ın, Proudhon'un 'Sefaletin Felsefesi' adlı kitabına ironik bir başlıkla yanıt vererek onu idealizmle eleştirdiği eseri hangisidir?", "cevaplar": ["Felsefenin Sefaleti", "Kutsal Aile", "Kapital", "Ekonomi Politiğin Eleştirisine Katkı"], "dogru": "Felsefenin Sefaleti"},
    {"soru": "Engels'in, sosyalizmin ahlaki bir temenniden bilimsel bir yönteme nasıl evrildiğini yalın bir dille anlattığı popüler broşürü hangisidir?", "cevaplar": ["Ütopyacı Sosyalizm ve Bilimsel Sosyalizm", "Komünizmin İlkeleri", "Doğanın Diyalektiği", "Konut Sorunu"], "dogru": "Ütopyacı Sosyalizm ve Bilimsel Sosyalizm"},

    # --- 61-80: Temel Kavramlar & Ekonomi-Politik ---
    {"soru": "Kapitalizmde üretilen metaların kullanım değeri ile değişim değeri arasındaki fark ne olarak adlandırılır?", "cevaplar": ["Kar", "Artı Değer", "Faiz", "Maliyet"], "dogru": "Artı Değer"},
    {"soru": "Tarihsel Materyalizm'e göre toplumun hukuki, siyasi ve ideolojik yapısını (Üstyapı) belirleyen temel unsur (Altyapı) nedir?", "cevaplar": ["Düşünceler", "Üretim Tarzı", "Coğrafya", "Kültür"], "dogru": "Üretim Tarzı"},
    {"soru": "İşçinin ürettiği ürüne, üretim sürecine ve kendi emeğine yabancılaşmasını ifade eden Marksist kavram hangisidir?", "cevaplar": ["Yabancılaşma", "Sömürü", "Yoksullaşma", "Anomi"], "dogru": "Yabancılaşma"},
    {"soru": "Üretim araçlarının özel mülkiyetinin yerini toplumsal mülkiyetin aldığı ve devletin kademeli olarak sönümlenmesini öngören nihai aşama nedir?", "cevaplar": ["Sosyalizm", "Komünizm", "Kapitalizm", "Sosyal Demokrasi"], "dogru": "Komünizm"},
    {"soru": "Kapitalist toplumda pazar için üretilen ve bir ihtiyacı tatmin etme özelliği (kullanım değeri) olan her türlü insan emeği ürününe ne ad verilir?", "cevaplar": ["Meta", "Sermaye", "Hammadde", "Para"], "dogru": "Meta"},
    {"soru": "Sosyalist teoride, kapitalizmden komünizme geçiş sürecinde işçi sınıfının siyasi iktidarı elinde tuttuğu geçici devlet biçimi nedir?", "cevaplar": ["Proletarya Diktatörlüğü", "Burjuva Demokrasisi", "Tek Parti Rejimi", "Otokrasi"], "dogru": "Proletarya Diktatörlüğü"},
    {"soru": "Metaların arkasındaki insan emeğinin unutulup, nesnelerin kendi aralarında mistik ve bağımsız bir ilişkiye sahipmiş gibi görünmesi durumuna ne denir?", "cevaplar": ["Meta Fetişizmi", "Reifikasyon", "Yabancılaşma", "Sermaye Birikimi"], "dogru": "Meta Fetişizmi"},
    {"soru": "Marksist teoride, üretim sürecinde kullanılan makineler, fabrikalar ve hammaddeler ile bunları kullanan insan emeğinin bütününü ifade eden kavram hangisidir?", "cevaplar": ["Üretim İlişkileri", "Üretici Güçler", "Üretim Tarzı", "Altyapı"], "dogru": "Üretici Güçler"},
    {"soru": "İşçi sınıfının kendi tarihsel rolünün bilincine varmadan önceki nesnel durumunu ifade eden kavram hangisidir?", "cevaplar": ["Kendisi İçin Sınıf", "Kendinde Sınıf", "Sınıf Bilinci", "Lumpen Proletarya"], "dogru": "Kendinde Sınıf"},
    {"soru": "Kapitalizmde işçinin hayatta kalması ve çalışmaya devam edebilmesi için gerekli olan emek zamanının ötesinde harcadığı emek süresine ne denir?", "cevaplar": ["Gerekli Emek", "Artı Emek", "Soyut Emek", "Somut Emek"], "dogru": "Artı Emek"},
    {"soru": "Metaların değerinin, onları üretmek için toplumsal olarak gerekli olan emek zamanı tarafından belirlendiğini savunan teori hangisidir?", "cevaplar": ["Emek-Değer Teorisi", "Marjinal Fayda Teorisi", "Arz-Talep Dengesi", "Kullanım Değeri Teorisi"], "dogru": "Emek-Değer Teorisi"},
    {"soru": "Sermayenin, makineler ve hammaddeler gibi sabit unsurları (değişmez sermaye) ile işgücü (değişken sermaye) arasındaki orana ne ad verilir?", "cevaplar": ["Sermayenin Organik Bileşimi", "Artı Değer Oranı", "Kar Oranı", "Sermaye Yoğunluğu"], "dogru": "Sermayenin Organik Bileşimi"},
    {"soru": "Kapitalistlerin rekabet nedeniyle sürekli yeni teknolojilere yatırım yapması sonucu uzun vadede ortaya çıkan kriz eğilimi nedir?", "cevaplar": ["Kar Oranlarının Azalma Eğilimi Yasası", "Eksik Tüketim Krizi", "Mali Çöküş Yasası", "Enflasyon Eğilimi"], "dogru": "Kar Oranlarının Azalma Eğilimi Yasası"},
    {"soru": "Kapitalist üretim tarzının tarihsel başlangıcında, üreticilerin mülksüzleştirilmesi ve servetin belirli ellerde toplanması sürecine ne ad verilir?", "cevaplar": ["İlkel Birikim (Sermayenin İlk Birikimi)", "Sermaye Merkezileşmesi", "Merkantilist Dönem", "Emperyalist Genişleme"], "dogru": "İlkel Birikim (Sermayenin İlk Birikimi)"},
    {"soru": "Locksley'de felsefe dünyayı yalnızca çeşitli biçimlerde yorumlamıştır, aslolan onu değiştirmektir fikrini özetleyen pratik felsefe kavramı nedir?", "cevaplar": ["Praksis", "Dogmatizm", "Skolastik Düşünce", "Pozitivizm"], "dogru": "Praksis"},
    {"soru": "Kapitalist üretim ilişkilerinin içinde doğup büyüdüğü ve üretim araçlarının özel mülkiyetine dayanan ekonomik temel yapı hangisidir?", "cevaplar": ["Altyapı", "Üstyapı", "İdeolojik Aygıt", "Kültürel Yapı"], "dogru": "Altyapı"},
    {"soru": "Üretim araçlarına sahip olan ve işçi sınıfını sömüren kapitalist mülkiyet sahibi sınıfa ne ad verilir?", "cevaplar": ["Burjuvazi", "Proletarya", "Aristokrasi", "Rantiyeler"], "dogru": "Burjuvazi"},
    {"soru": "Geçimini sadece kendi işgücünü (emeğini) satarak sağlayan modern ücretli işçi sınıfına ne ad verilir?", "cevaplar": ["Proletarya", "Burjuvazi", "Köylülük", "Serf"], "dogru": "Proletarya"},
    {"soru": "İşçi sınıfı içinde yer alan ancak sınıf bilincinden yoksun, düzene kolayca alet olabilen güvencesiz ve dışlanmış kesimlere ne ad verilir?", "cevaplar": ["Lumpen Proletarya", "Aristokrat İşçiler", "Öncü İşçiler", "Küçük Burjuvazi"], "dogru": "Lumpen Proletarya"},
    {"soru": "Maddi dünyanın insan düşüncesinden bağımsız olarak var olduğunu ve bilincin madde tarafından belirlendiğini savunan felsefi akım hangisidir?", "cevaplar": ["Materyalizm", "İidealizm", "Rasyonalizm", "Mistisizm"], "dogru": "Materyalizm"},

    # --- 81-100: Turnuvalar, Örgütler & Diğer Kuramcılar ---
    {"soru": "Antonio Gramsci'nin egemen sınıfın kültürel ve ideolojik hakimiyetini kurma biçimi olarak tanımladığı kavram nedir?", "cevaplar": ["Otorite", "Hegemonya", "Baskı", "Propaganda"], "dogru": "Hegemonya"},
    {"soru": "Lenin'in, kapitalizmin tekelleşme ve finans sermayesinin egemenliğiyle küreselleşmesini tanımladığı kavram hangisidir?", "cevaplar": ["Küreselleşme", "Emperyalizm", "Merkantilizm", "Kolonizasyon"], "dogru": "Emperyalizm"},
    {"soru": "Rosa Luxemburg'un reformizm eleştirisinde savunduğu, kapitalizmin krizlerinin reformlarla çözülemeyeceğini ve devrimin zorunlu olduğunu anlatan ilke nedir?", "cevaplar": ["Reform veya Devrim", "Evrimsel Sosyalizm", "Revizyonizm", "Barışçıl Geçiş"], "dogru": "Reform veya Devrim"},
    {"soru": "Lenin'in 'Devlet ve Devrim' eserinde de vurguladığı, devletin tarafsız bir hakem değil, belirli bir sınıfın diğer sınıf üzerindeki ne aracı olduğunu savunur?", "cevaplar": ["Uzlaşma", "Baskı ve Tahakküm", "Hizmet", "Eğitim"], "dogru": "Baskı ve Tahakküm"},
    {"soru": "1871 yılında işçi sınıfının tarihte ilk kez siyasi iktidarı ele geçirerek kurduğu ve Marx'ın 'nihayet keşfedilen siyasi biçim' olarak övdüğü tarihsel deneyim hangisidir?", "cevaplar": ["Paris Komünü", "Ekim Devrimi", "Spartaküs Ayaklanması", "Fransız Devrimi"], "dogru": "Paris Komünü"},
    {"soru": "Lenin'in Marksist teoriye yaptığı en büyük katkılardan biri olan, emperyalist zincirin en zayıf halkasından kopacağı fikri hangi kavramla ifade edilir?", "cevaplar": ["En Zayıf Halka Teorisi", "Eşitsiz Gelişim Yasası", "Sürekli Devrim", "Tek Ülkede Sosyalizm"], "dogru": "En Zayıf Halka Teorisi"},
    {"soru": "1864 yılında Londra'da Karl Marx'ın da katılımıyla kurulan, tarihteki ilk uluslararası işçi örgütünün adı nedir?", "cevaplar": ["Birinci Enternasyonal", "İkinci Enternasyonal", "Komintern", "Kominform"], "dogru": "Birinci Enternasyonal"},
    {"soru": "1919 yılında Lenin önderliğinde Moskova'da kurulan and dünya devrimini hedefleyen Üçüncü Enternasyonal'in kısa adı nedir?", "cevaplar": ["Komintern", "Kominform", "Proletkult", "Glavlit"], "dogru": "Komintern"},
    {"soru": "Almanya'da 1919 ayaklanmasında katledilen, 'Sermayenin Birikimi' kitabının yazarı ünlü Marksist kadın teorisyen kimdir?", "cevaplar": ["Rosa Luxemburg", "Clara Zetkin", "Nadejda Krupskaya", "Aleksandra Kollontay"], "dogru": "Rosa Luxemburg"},
    {"soru": "İtalyan faşizmi tarafından hapsedilen ve hapishanede yazdığı notlarla Marksist kültürel çalışmaları derinden etkileyen düşünür kimdir?", "cevaplar": ["Antonio Gramsci", "Amadeo Bordiga", "Palmiro Togliatti", "Louis Althusser"], "dogru": "Antonio Gramsci"},
    {"soru": "Fransız Marksist düşünür, devletin baskı aygıtlarının yanında okul, aile ve medya gibi unsurları 'Devletin İdeolojik Aygıtları' olarak tanımlayan kimdir?", "cevaplar": ["Louis Althusser", "Jean-Paul Sartre", "Michel Foucault", "Henri Lefebvre"], "dogru": "Louis Althusser"},
    {"soru": "Lenin'in eşi ve Sovyet eğitim sisteminin kurulmasında en büyük rolü oynayan devrimci eğitimci kimdir?", "cevaplar": ["Nadejda Krupskaya", "Inessa Armand", "Aleksandra Kollontay", "Fanya Kaplan"], "dogru": "Nadejda Krupskaya"},
    {"soru": "Stalin'in asıl adı nedir?", "cevaplar": ["Lev Troçki", "İosif Cuğaşvili", "Nikolay Buharin", "Sergey Kirov"], "dogru": "İosif Cuğaşvili"},
    {"soru": "Stalin, gençliğinde hangi meslek için eğitim alıyordu?", "cevaplar": ["Demircilik", "Ruhbanlık", "Askerlik", "Terzilik"], "dogru": "Ruhbanlık"},
    {"soru": "Stalin'in gençlik yıllarında gizli devrimci faaliyetler yürütürken kullandığı ve Gürcü edebiyatından esinlenen ilk lakabı nedir?", "cevaplar": ["Koba", "Soso", "Kobaşvili", "Leninşvili"], "dogru": "Koba"},
    {"soru": "Fransa'da 1848 devrimleri sonrasında işçi sınıfının burjuvaziye karşı ilk bağımsız silahlı kalkışması olan tarihi ay hangisidir?", "cevaplar": ["Haziran Günleri", "Şubat İsyanı", "Temmuz Vakası", "Brumaire Darbesi"], "dogru": "Haziran Günleri"},
    {"soru": "1889'da kurulan, 1 Mayıs'ı işçi sınıfının uluslararası birlik ve mücadele günü ilan eden örgüt hangisidir?", "cevaplar": ["İkinci Enternasyonal", "Birinci Enternasyonal", "Komintern", "Kızıl Sendika Enternasyonal"], "dogru": "İkinci Enternasyonal"},
    {"soru": "Lenin'in, kapitalizmin serbest rekabetçi dönemden tekelci döneme geçişini emperyalizm olarak adlandırdığı ünlü eseri hangisidir?", "cevaplar": ["Emperyalizm, Kapitalizmin En Yüksek Aşaması", "Devlet ve Devrim", "Gelişen Kapitalizm", "Finans Sermayesi"], "dogru": "Emperyalizm, Kapitalizmin En Yüksek Aşaması"},
    {"soru": "Bolşevik hükümetinde Kadın Sorunlarından Sorumlu olan ve tarihteki ilk kadın büyükelçilerden biri olan devrimci kimdir?", "cevaplar": ["Aleksandra Kollontay", "Clara Zetkin", "Rosa Luxemburg", "Inessa Armand"], "dogru": "Aleksandra Kollontay"},
    {"soru": "8 Mart'ın 'Dünya Emekçi Kadınlar Günü' olarak kutlanmasını İkinci Enternasyonal'de öneren ve kabul ettiren Alman devrimci kimdir?", "cevaplar": ["Clara Zetkin", "Rosa Luxemburg", "Aleksandra Kollontay", "Nadejda Krupskaya"], "dogru": "Clara Zetkin"}
]

# Kullanıcı oturum hafızası
if 'puan' not in st.session_state: 
    st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'isim': '', 'start_time': 0, 'skor_kaydedildi': False, 'secilen_sorular': []})

# Yenilenen Başlık
st.title("☭ MLM Devrim Tarihi Yarışması")

# 1. GİRİŞ EKRANI
if not st.session_state.oyun_basladi:
    isim = st.text_input("Yoldaş Adı:", key="giris_yoldas_adi")
    if st.button("🚀 Mücadeleye Başla", key="but_basla"):
        if isim:
            st.session_state.isim = isim
            st.session_state.oyun_basladi = True
            st.session_state.start_time = time.time()
            st.session_state.skor_kaydedildi = False
            st.session_state.secilen_sorular = random.sample(soru_havuzu, 15)
            st.rerun()
        else: st.warning("Lütfen bir isim gir yoldaş!")
    
    st.subheader("🏅 En Yüksek Skorlar (Canlı — İlk 10)")
    try:
        if global_skorlar:
            sirali_skorlar = sorted(global_skorlar.items(), key=lambda x: int(x[1]), reverse=True)
            for k, v in sirali_skorlar[:10]:
                st.write(f"🌟 {k} — {v} Puan")
        else:
            st.write("Henüz skor yok, ilk sen ol!")
    except:
        st.write("Skor tablosu yükleniyor...")

# 2. SORU EKRANI
else:
    sorular = st.session_state.secilen_sorular
    
    if st.session_state.soru_index < len(sorular):
        q = sorular[st.session_state.soru_index]
        st.subheader(f"Soru {st.session_state.soru_index + 1}: {q['soru']}")
        
        gecen_sure = time.time() - st.session_state.start_time
        kalan_sure = 30 - int(gecen_sure)
        
        if kalan_sure > 0:
            st.metric("⏱️ Kalan Süre", f"{kalan_sure} sn")
            
            mesaj_alani = st.empty()
            
            for secenek in q['cevaplar']:
                if st.button(secenek, key=f"btn_{secenek}_{st.session_state.soru_index}"):
                    if secenek == q['dogru']:
                        taban_puan = 10
                        if gecen_sure < 6:
                            taban_puan += 5
                            # Özelleştirilmiş Doğru Cevap Metni
                            mesaj_alani.success("⚡ Müthiş Hız! Bravo Yoldaş (+5 Hız Bonusu)")
                        else: 
                            mesaj_alani.success("✅ Bravo Yoldaş")
                        st.session_state.puan += taban_puan
                    else: 
                        # Özelleştirilmiş Yanlış Cevap Metni
                        mesaj_alani.error(f"❌ Yanlış cevap yoldaş doğrusu: {q['dogru']}")
                    
                    time.sleep(1.5)
                    mesaj_alani.empty()
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
        # Özelleştirilmiş Kapanış Mesajı
        st.subheader(f"🎉 oyun bitti yoldaş, devrimci kal {st.session_state.isim}!")
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
            st.session_state.update({'puan': 0, 'soru_index': 0, 'oyun_basladi': False, 'skor_kaydedildi': False, 'secilen_sorular': []})
            st.rerun()