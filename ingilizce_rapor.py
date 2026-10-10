# -*- coding: utf-8 -*-
"""
Günlük İngilizce Öğrenme Bülteni v2
+ Gramer köşesi (sıfırdan)
+ Telaffuz rehberi
+ Görsel anlatım (emoji + tablo)
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")
MAIL_TO = os.environ.get("MAIL_TO")

# ============================================================
# GRAMER KÖŞESİ — SIFIRDAN BAŞLAYAN 30 DERS
# ============================================================
GRAMER_DERSLERI = [
    # HAFTA 1: TEMELLER
    ("Ders 1: Alfabe ve Sesler",
     "İngilizce alfabede 26 harf var: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z. Ancak İngilizce'de 44 ses vardır. Yani harfler her zaman aynı sesi vermez.",
     "🅰️ A = 'ey' | 🅱️ B = 'bi' | 🆑 C = 'si' | 🅳 D = 'di' | 🅴 E = 'i'",
     "Örnek: 'cat' 3 harf ama tek hece: KET. 'e' harfi burada 'e' sesi verir."),
    
    ("Ders 2: Selamlaşma ve To Be",
     "'To be' fiili İngilizce'nin temelidir. Am, is, are olarak üç şekli vardır. Ben için AM, o için IS, sen/biz/onlar için ARE kullanılır.",
     "🔹 I am (ay em) = Ben ...-im\n🔹 You are (yu ar) = Sen ...-sin\n🔹 He is (hi iz) = O (erkek) ...-dir\n🔹 She is (şi iz) = O (kadın) ...-dir\n🔹 It is (it iz) = O (nesne) ...-dir\n🔹 We are (vi ar) = Biz ...-iz\n🔹 They are (dhey ar) = Onlar ...-dir",
     "Örnek: I am a teacher (ay em ı tiçır) = Ben bir öğretmenim."),
    
    ("Ders 3: İşaret Zamirleri",
     "Bir şeyi işaret ederken kullanılır. Yakındaki ve uzaktaki nesneler için farklı kelimeler vardır. Tekil ve çoğul da farklıdır.",
     "👉 YAKIN: This (dhis) = Bu | These (dhiiz) = Bunlar\n👉 UZAK: That (dhet) = Şu | Those (dhouz) = Şunlar",
     "Örnek: This is a book (dhis iz ı buk) = Bu bir kitap."),
    
    ("Ders 4: Basit Şimdiki Zaman",
     "Her gün yapılan alışkanlıkları anlatır. 'I/You/We/They' ile fiil yalın halde, 'He/She/It' ile fiile -s eklenir.",
     "📌 I work (ay vırk) = Çalışırım\n📌 You work (yu vırk) = Çalışırsın\n📌 He works (hi vırks) = Çalışır\n📌 She works (şi vırks) = Çalışır\n📌 We work (vi vırk) = Çalışırız",
     "⚠️ Dikkat: He/She/It ile fiile MUTLAKA -s eklenir!"),
    
    ("Ders 5: Şimdiki Zaman (Şu An)",
     "Şu anda devam eden eylemleri anlatır. 'am/is/are' + fiil+ing şeklinde kurulur.",
     "🎬 I am working (ay em vırking) = Şu an çalışıyorum\n🎬 She is reading (şi iz riiding) = Okuyor\n🎬 They are playing (dhey ar pleying) = Oynuyorlar",
     "⚠️ Dikkat: 'am/is/are' ile fiilin -ing hali birlikte kullanılır."),
    
    ("Ders 6: Geçmiş Zaman",
     "Geçmişte olan olayları anlatır. Düzenli fiiller -ed alır, düzensiz fiiller değişir.",
     "⏮️ Düzenli: work → worked (vırkt)\n⏮️ Düzenli: play → played (pleyd)\n⏮️ Düzensiz: go → went (vent)\n⏮️ Düzensiz: eat → ate (eyt)\n⏮️ Düzensiz: see → saw (so)",
     "Örnek: I worked yesterday (ay vırkt yestırdey) = Dün çalıştım."),
    
    ("Ders 7: Gelecek Zaman (Will)",
     "Gelecekte olacak olayları anlatır. 'will + fiil' şeklinde kurulur. Ani kararlar için kullanılır.",
     "⏭️ I will go (ay vil gou) = Gideceğim\n⏭️ She will come (şi vil kam) = Gelecek\n⏭️ We will see (vi vil sii) = Göreceğiz",
     "💡 Kısaltma: I will = I'll (ayl) | She will = She'll (şil)"),
    
    # HAFTA 2: YAPI
    ("Ders 8: Sahiplik Sıfatları",
     "Bir şeyin kime ait olduğunu gösterir. Türkçe'deki '-im, -in, -i' eklerinin karşılığıdır.",
     "👤 My (may) = Benim\n👤 Your (yor) = Senin\n👤 His (hiz) = Onun (erkek)\n👤 Her (hır) = Onun (kadın)\n👤 Its (its) = Onun (nesne)\n👤 Our (aur) = Bizim\n👤 Their (dheir) = Onların",
     "Örnek: My book (may buk) = Benim kitabım"),
    
    ("Ders 9: Çoğul Yapma",
     "İngilizce'de çoğul yapmak için kelimenin sonuna -s veya -es eklenir. Bazı kelimeler düzensizdir.",
     "📚 book → books (buks)\n📚 box → boxes (baksız)\n📚 city → cities (sitiz)\n📚 child → children (çildrın) ⚠️\n📚 man → men (men) ⚠️\n📚 woman → women (vimin) ⚠️",
     "💡 Kural: -s, -ss, -sh, -ch, -x ile bitenler -es alır."),
    
    ("Ders 10: Soru Cümleleri",
     "İngilizce'de soru sormak için soru kelimesi kullanılır. Türkçe'den farklı olarak özne değişmez, kelime başa gelir.",
     "❓ What (vat) = Ne\n❓ Where (ver) = Nerede\n❓ When (ven) = Ne zaman\n❓ Who (hu) = Kim\n❓ Why (vay) = Neden\n❓ How (hau) = Nasıl",
     "Örnek: Where are you? (ver ar yu) = Neredesin?"),
    
    ("Ders 11: Olumsuz Cümleler",
     "Bir şeyi reddetmek için kullanılır. 'am/is/are' fiillerinden sonra NOT gelir. Diğer fiiller için do/does + not kullanılır.",
     "🚫 I am not (ay em nat) = Değilim\n🚫 She is not (şi iz nat) = Değil\n🚫 I do not work (ay du nat vırk) = Çalışmam\n🚫 She does not work (şi daz nat vırk) = Çalışmaz",
     "💡 Kısaltma: is not = isn't | do not = don't | does not = doesn't"),
    
    ("Ders 12: There is / There are",
     "Bir şeyin var olduğunu söylemek için kullanılır. Türkçe'deki 'var' kelimesinin karşılığıdır.",
     "✅ There is a book (dher iz ı buk) = Bir kitap var (tekil)\n✅ There are books (dher ar buks) = Kitaplar var (çoğul)\n✅ Is there a book? (iz dher ı buk) = Kitap var mı?\n❌ There isn't a book = Kitap yok",
     "💡 Kural: Tekil isimler için 'There is', çoğul için 'There are'"),
    
    ("Ders 13: Can / Cannot",
     "'Can' yetenek ve izin için kullanılır. Türkçe'deki '-ebilmek' ekine karşılık gelir. Yalın fiille kullanılır.",
     "💪 I can swim (ay ken svim) = Yüzebilirim\n💪 She can drive (şi ken drayv) = Araba sürebilir\n🚫 I cannot come (ay kenat kam) = Gelemem\n❓ Can you help? (ken yu help) = Yardım edebilir misin?",
     "⚠️ Dikkat: 'Can' ile fiil arasına 'to' gelmez: I can to swim ❌"),
    
    ("Ders 14: Karşılaştırma",
     "İki şeyi karşılaştırmak için kullanılır. Kısa sıfatlara -er, uzun sıfatlara 'more' eklenir.",
     "📊 Big → bigger (biger) = daha büyük\n📊 Cheap → cheaper (çiipır) = daha ucuz\n📊 Expensive → more expensive (mor ekspensiv) = daha pahalı\n📊 Good → better (betır) ⚠️\n📊 Bad → worse (vırs) ⚠️",
     "Örnek: This is cheaper than that (dhis iz çiipır dhen dhet) = Bu şundan daha ucuz."),
    
    # HAFTA 3: EDATLAR VE ZAMAN
    ("Ders 15: Yer Edatları",
     "Bir şeyin nerede olduğunu söylemek için kullanılır. Türkçe'de ekle yapılır, İngilizce'de ayrı kelimedir.",
     "📍 In (in) = içinde\n📍 On (on) = üstünde\n📍 Under (andır) = altında\n📍 Behind (bihaynd) = arkasında\n📍 Next to (nekst tu) = yanında\n📍 Between (bitviin) = arasında",
     "Örnek: The book is on the table (buk iz on teybl) = Kitap masanın üstünde."),
    
    ("Ders 16: Zaman Edatları",
     "Zamanı belirtmek için kullanılır. Saat, gün, ay ve yıl için farklı edatlar kullanılır.",
     "⏰ AT + saat: at 5 o'clock (et fayv okılok)\n📅 ON + gün: on Monday (on mandey)\n📅 IN + ay/yıl: in July (in culay), in 2026 (in tventi tventi siks)\n📅 IN + mevsim: in summer (in samır)",
     "⚠️ Dikkat: Türkçe'de saat için 'de/da' eklenir, İngilizce'de 'at' kullanılır."),
    
    ("Ders 17: Sıklık Zarfları",
     "Bir eylemin ne sıklıkta yapıldığını gösterir. Genellikle fiilden önce gelir.",
     "🔄 Always (olveys) = Her zaman (%100)\n🔄 Usually (yujıli) = Genellikle (%90)\n🔄 Often (ofın) = Sık sık (%70)\n🔄 Sometimes (samteymz) = Bazen (%50)\n🔄 Rarely (reerli) = Nadiren (%10)\n🔄 Never (nevır) = Asla (%0)",
     "Örnek: I usually walk to work (ay yujıli vok tu vırk) = Genellikle işe yürürüm."),
    
    ("Ders 18: Sayılabilen ve Sayılamayan İsimler",
     "İngilizce'de bazı isimler sayılabilir (bir, iki, üç), bazıları sayılamaz (su, ekmek, para gibi).",
     "🔢 Sayılabilen: apple, book, car → 'How many?'\n💧 Sayılamayan: water, bread, money → 'How much?'",
     "Örnek: How many books? (hau meni buks) = Kaç kitap?\nÖrnek: How much water? (hau maç votır) = Ne kadar su?"),
    
    ("Ders 19: Much / Many / A lot of",
     "Miktar belirtmek için kullanılır. Sayılamayan için 'much', sayılabilen için 'many', ikisi için 'a lot of' kullanılır.",
     "📊 Many books (meni buks) = Çok kitap\n📊 Much water (maç votır) = Çok su\n📊 A lot of books (ı lot ov buks) = Çok kitap\n📊 A few books (ı fyu buks) = Birkaç kitap\n📊 A little water (ı litıl votır) = Biraz su",
     "⚠️ Olumsuz ve soru cümlelerinde 'much/many' kullanılır."),
    
    ("Ders 20: Modal Fiiller (Should, Must)",
     "Tavsiye ve zorunluluk belirtmek için kullanılır.",
     "💡 Should (şud) = -meli, -malı (tavsiye)\n💡 Must (mast) = -meli, -malı (zorunluluk)\n💡 Have to (hev tu) = -mek zorunda\n💡 Could (kud) = -ebilir (kibarca)\n💡 Might (mayt) = -ebilir (olasılık)",
     "Örnek: You should rest (yu şud rest) = Dinlenmelisin.\nÖrnek: I must go (ay mast gou) = Gitmeliyim."),
    
    ("Ders 21: Geçmiş Zaman Soruları",
     "Geçmişte olan olayları soru şeklinde sormak için 'did' kullanılır. Ana fiil yalın hale döner.",
     "❓ Did you go? (did yu gou) = Gittin mi?\n❓ Did she come? (did şi kam) = Geldi mi?\n❓ Where did you go? (ver did yu gou) = Nereye gittin?\n🚫 I didn't go (ay didnt gou) = Gitmedim",
     "⚠️ Dikkat: 'Did' ile fiil yalın kalır, -ed almaz: Did you went? ❌"),
    
    # HAFTA 4: İLERİ SEVİYE
    ("Ders 22: Present Perfect",
     "Geçmişte başlayıp şu ana kadar devam eden olayları anlatır. 'have/has + V3' şeklinde kurulur.",
     "✅ I have worked (ay hev vırkt) = Çalıştım (ve hâlâ çalışıyorum)\n✅ She has gone (şi hez gon) = Gitti (ve hâlâ yok)\n✅ Have you ever been? (hev yu evır biin) = Hiç bulundun mu?\n✅ I have never seen (ay hev nevır siin) = Hiç görmedim",
     "💡 'For' ve 'since' ile sık kullanılır: for 3 years, since 2020."),
    
    ("Ders 23: If Cümleleri (1. Tip)",
     "Gerçekleşme olasılığı yüksek koşullar için kullanılır. 'If + geniş zaman, will + fiil' şeklinde kurulur.",
     "🔮 If it rains, I will stay home (if it reyns, ay vil stey houm) = Yağmur yağarsa evde kalırım.\n🔮 If you study, you will pass (if yu stadi, yu vil pes) = Çalışırsan geçersin.",
     "💡 'If' cümlesi başta veya sonda olabilir. Sonda olursa virgül kalkar."),
    
    ("Ders 24: Edilgen Yapı (Passive)",
     "Eylemi yapan kişi önemli değilse veya bilinmiyorsa kullanılır. 'be + V3' şeklinde kurulur.",
     "📝 The letter was sent (dı letır vaz sent) = Mektup gönderildi.\n📝 The house is being built (dı haus iz biing bilt) = Ev inşa ediliyor.\n📝 English is spoken here (ingliş iz spoukın hiır) = Burada İngilizce konuşulur.",
     "💡 Türkçe'de edilgen yapı '-ıl, -il' ekleriyle kurulur: yapıldı, satıldı."),
    
    ("Ders 25: İlgi Cümleleri (Who, Which, That)",
     "İki cümleyi birleştirmek için kullanılır. İnsanlar için 'who', nesneler için 'which', ikisi için 'that' kullanılır.",
     "🔗 The man who came (dı men hu keym) = Gelen adam\n🔗 The book which I read (dı buk viç ay riid) = Okuduğum kitap\n🔗 The car that I bought (dı kar dhet ay bot) = Aldığım araba",
     "💡 Bu yapı Türkçe'deki '-en, -an' sıfat fiil eklerine benzer."),
    
    ("Ders 26: Bağlaçlar (And, But, Or, Because)",
     "Cümleleri ve fikirleri birleştirmek için kullanılır.",
     "🔗 And (end) = ve\n🔗 But (bat) = ama\n🔗 Or (or) = veya\n🔗 Because (bikoz) = çünkü\n🔗 So (sou) = bu yüzden\n🔗 Although (oldhou) = -e rağmen\n🔗 However (hau Evır) = ancak",
     "Örnek: I like tea but I don't like coffee."),
    
    ("Ders 27: Dolaylı Anlatım",
     "Başkasının söylediğini aktarmak için kullanılır. Zaman bir adım geriye kayar.",
     "💬 'I am tired' dedi → He said he was tired.\n💬 'I will come' dedi → She said she would come.\n💬 'I went' dedi → He said he had gone.",
     "💡 'Say' ve 'tell' farkı: Say + bir şey, Tell + birine"),
    
    ("Ders 28: Kısaltmalar ve Günlük Konuşma",
     "Günlük İngilizce'de çok kullanılan kısaltmalar ve konuşma dilinde yaygın ifadeler.",
     "💬 I'm = I am (aym)\n💬 You're = You are (yor)\n💬 He's = He is (hiz)\n💬 Don't = Do not (dont)\n💬 Can't = Cannot (kent)\n💬 Won't = Will not (vont)\n💬 Gonna = Going to (gana) - günlük\n💬 Wanna = Want to (vana) - günlük",
     "⚠️ 'Gonna' ve 'wanna' resmi yazışmalarda kullanılmaz."),
    
    ("Ders 29: Yaygın Deyimler",
     "İngilizce'de sık kullanılan deyimler ve kalıplaşmış ifadeler.",
     "🎯 Break the ice (breyk dı ays) = Buzları eritmek\n🎯 Piece of cake (piis ov keyk) = Çok kolay iş\n🎯 Hit the books (hit dı buks) = Ders çalışmak\n🎯 Under the weather (andır dı vedhır) = Keyifsiz olmak\n🎯 Once in a blue moon (vans in ı blu muun) = Kırk yılda bir",
     "💡 Deyimler kelime kelime çevrilemez, kalıp olarak öğrenilir."),
    
    ("Ders 30: Genel Tekrar ve Sınav",
     "Tüm konuların özeti ve kendinizi test etme.",
     "📝 To be: am/is/are\n📝 Zamanlar: geniş, şimdiki, geçmiş, gelecek\n📝 Soru: What, Where, When, Why, How\n📝 Modal: can, should, must, could, might\n📝 Edatlar: in, on, at\n📝 Cümle yapısı: Özne + Fiil + Nesne",
     "🎯 Bu 30 ders sonunda A1-A2 seviyesine ulaşmış olacaksınız."),
]

# ============================================================
# TELAFFUZ REHBERİ — DETAYLI 20 KURAL
# ============================================================
TELAFFUZ_REHBERI = [
    ("th (sert) /θ/",
     "🔴 ÇOK ZOR - Türkçe'de YOK",
     "think 🧠, three 3️⃣, thank 🙏, month 📅",
     "Dil ucunu üst ve alt dişlerin ARASINA koy. Hava üfle. Ses teli titremez.",
     "❌ 's' demeyin: sink (lavabo) = yanlış\n❌ 't' demeyin: tink = yanlış\n✅ Doğru: parmağınızı önüne koyun, hava hissetmelisiniz.",
     "Ayna al, dilinin ucunu dişlerinin arasında gör. Kendini kaydet, dinle."),
    
    ("th (yumuşak) /ð/",
     "🔴 ÇOK ZOR - Türkçe'de YOK",
     "this 👉, that 👈, the, mother 👩, brother 👦",
     "Aynı dil konumu (dişlerin arasında), ama bu sefer ses teli TİTRER.",
     "❌ 'd' demeyin: dis = yanlış\n❌ 'z' demeyin: zat = yanlış\n✅ Elinizi boğazınıza koyun, titreşim hissetmelisiniz.",
     "En kolay: 'the' kelimesini 100 kez söyle. Titreşimi hissedene kadar."),
    
    ("w /w/",
     "🟡 ZOR - Türkçe'de YOK",
     "water 💧, we 👥, what ❓, work 💼",
     "Dudaklarınızı yuvarlayın (öpücük verir gibi). Dişler dudağa DEĞMEZ.",
     "❌ 'v' demeyin: vater = yanlış (Almanca gibi)\n✅ Doğru: 'w' sesinde üst diş alt dudağa değmez.",
     "Ayna al, dudakların yuvarlak olduğunu kontrol et."),
    
    ("v /v/",
     "🟡 ZOR - Türkçe'de YOK",
     "very ✨, voice 🎤, love ❤️, seven 7️⃣",
     "Üst dişler ALT DUDAĞA değmeli. Titreşim var.",
     "❌ 'w' ile karıştırmayın: wery = yanlış\n✅ 'v' sesi 'f' gibi ama titreşimli.",
     "Ayna al, üst dişlerin alt dudağa değdiğini gör."),
    
    ("r /r/",
     "🟡 ZOR - Türkçe 'r' farklı",
     "red 🔴, right ➡️, around 🔄, sorry 😔",
     "Dil ucu damağa DEĞMEZ. Hafif geriye kıvrılır, boşlukta durur.",
     "❌ Türkçe 'r' gibi yuvarlamayın (r'yi dil ucuyla titretmeyin).\n✅ Amerikan İngilizcesi: dil geriye kıvrılır.\n✅ İngiliz İngilizcesi: dil düzdür, hafif geriye.",
     "Aynada dilinin damağa değmediğini kontrol et."),
    
    ("ng /ŋ/",
     "🟡 ZOR - Türkçe'de YOK",
     "sing 🎵, long 📏, meeting 🤝, waiting ⏳",
     "Dilin ARKA kısmı damağa değer. Sonda 'g' duyulmaz.",
     "❌ 'sin-g' diye ayırmayın\n❌ 'g' eklemeyin\n✅ Tek bir yumuşak 'ng' sesi.",
     "'sing' derken ağzınızı kapatmayın, hava burundan çıkar."),
    
    ("Schwa /ə/",
     "🔴 EN ZOR - İngilizce'nin sırrı",
     "about 🔄, teacher 👨‍🏫, banana 🍌, computer 💻",
     "Vurgusuz hecelerde ÇOK KISA, gevşek 'ı' sesi. Ağız tamamen rahat.",
     "❌ Her harfi tam sesle okumayın: a-baut = yanlış\n❌ 'a-baut' değil, 'ı-baut' deyin (a çok kısa)\n✅ Vurgusuz heceler 'yutulur'.",
     "En sık ses: İngilizce'deki her 5 ünlüden 1'i schwa. 'Teacher' = 'Tİİ-çır' (a harfi yok)."),
    
    ("Kısa ve uzun ünlüler",
     "🟡 ÖNEMLİ",
     "ship 🚢 / sheep 🐑 | bit / beat | fit / feet",
     "Kısa ünlü: ağız gevşek, süre kısa.\nUzun ünlü: ağız gergin, süre uzun.",
     "❌ İkisini de aynı okumak anlamı değiştirir:\n• ship = gemi, sheep = koyun\n• live = yaşamak, leave = ayrılmak",
     "Uzun ünlüyü 2 kat uzun söyleyin: 'shiiip'."),
    
    ("A harfi /æ/ vs /eɪ/",
     "🟡 ÖNEMLİ",
     "cat 🐱, bad 👎 / cake 🍰, name 📛",
     "æ: Ağız GENİŞ açılır, 'a' ile 'e' arası.\n/eɪ/: 'ey' sesi, ağız kapanır.",
     "❌ 'cat' → 'ket' değil, 'kæt' (ağzı geniş aç)\n✅ 'cake' → 'keyk' (evet, 'ey' sesi)",
     "'Cat' derken ağzınızı geniş açın, 'cake' derken kapatın."),
    
    ("-ed eki 3 farklı okunur",
     "🟢 KURAL",
     "worked /t/, played /d/, wanted /ɪd/",
     "Sessiz harfle biten fiiller → /t/ (vırkt)\nÜnlü/sesli harfle biten → /d/ (pleyd)\nT veya D ile biten → /ɪd/ (vantıd)",
     "❌ Hepsini 'ed' diye okumak yanlış.\n✅ worked = vırkt, played = pleyd, wanted = vantıd",
     "3 grupta öğren, karıştırmayın."),
    
    ("-s eki 3 farklı okunur",
     "🟢 KURAL",
     "cats /s/, dogs /z/, buses /ɪz/",
     "Sessiz harfle biten → /s/ (kets)\nSesli harfle biten → /z/ (dogz)\nS, Z, SH, CH, X ile biten → /ɪz/ (basız)",
     "❌ Hepsini 's' diye okumak yanlış.\n✅ cats = kets, dogs = dogz, buses = basız",
     "Çoğul yaparken ses uyumuna dikkat."),
    
    ("C harfi",
     "🟢 KURAL",
     "cinema /s/, cat /k/, chocolate /ç/",
     "e, i, y'den önce → S (sinema)\na, o, u'dan önce → K (ket)\nCH yan yana → Ç (çaklıt)",
     "❌ 'cinema' → 'kinema' değil\n✅ 'cinema' → 'sinema'",
     "Kelimenin diğer harflerine bakarak C'nin sesini tahmin et."),
    
    ("G harfi",
     "🟢 KURAL",
     "gym /c/, go /g/",
     "e, i, y'den önce → C (cim)\na, o, u'dan önce → G (gou)",
     "❌ 'gym' → 'gim' değil\n✅ 'gym' → 'cim'",
     "G'nin ardından gelen harfe bak."),
    
    ("Sessiz Harfler",
     "🟢 KURAL",
     "know /nou/, write /rayt/, hour /auır/, listen /lisın/, island /ayland/",
     "Bazı harfler yazılır ama OKUNMAZ.",
     "❌ 'know' → 'kı-nou' değil\n✅ 'know' → 'nou' (k sessiz)\n✅ 'write' → 'rayt' (w sessiz)",
     "Bu kelimeleri kalıp olarak ezberle."),
    
    ("Vurgu (Stress)",
     "🔴 ÇOK ÖNEMLİ",
     "TA-ble, be-CAUSE, PHO-to-gra-pher",
     "Çok heceli kelimelerde bir hece diğerlerinden daha GÜÇLÜ ve UZUN okunur.",
     "❌ Vurgu yanlış olursa kelime anlaşılmaz.\n❌ 'TABLE' yerine 'taBLE' demek kafa karıştırır.",
     "Sözlükte IPA'ya bakın: /ˈteɪbl/ — ˈ işareti vurguyu gösterir."),
    
    ("Cümle Ritmi",
     "🟡 İLERİ SEVİYE",
     "I want to go to the market",
     "Önemli kelimeler (isim, fiil, sıfat) vurgulanır.\nKüçük kelimeler (to, the, of, a) hızlı ve zayıf okunur.",
     "❌ Her kelimeyi aynı güçte okumak → robot gibi\n✅ 'ay WANT t' GO t' d' MARKET' gibi",
     "Anadili İngilizce olanlar 'yutuyor' gibi duyulur, sebebi budur."),
    
    ("Soru Tonu",
     "🟢 KURAL",
     "Are you coming? ↗ | Where are you? ↘",
     "Yes/No soruları: ses YUKARI çıkar ↗\nWh- soruları: ses AŞAĞI iner ↘",
     "❌ Her soruyu aynı tonla sormak yanlış.\n✅ Yes/No: 'Are you coming?' → ↗\n✅ Wh-: 'Where are you?' → ↘",
     "Aynada kendinizi izleyerek pratik yapın."),
    
    ("Bağlantılı Konuşma",
     "🟡 İLERİ SEVİYE",
     "What are you doing? → Whatcha doin'?",
     "Günlük konuşmada kelimeler birleşir ve kısalır.",
     "📌 What are you = Whatcha\n📌 Going to = Gonna\n📌 Want to = Wanna\n📌 Did you = Dija\n📌 Let me = Lemme",
     "Resmi yazışmalarda kullanmayın, günlük konuşmada normaldir."),
    
    ("Amerikan vs İngiliz",
     "🟡 FARK",
     "water: Amerikan 'vodır' / İngiliz 'votı'",
     "Amerikan: 'r' belirgin, 't' yumuşak\nİngiliz: 'r' yumuşak, 't' belirgin",
     "📌 Schedule: Amerikan 'skecul' / İngiliz 'şedyul'\n📌 Either: Amerikan 'iidhır' / İngiliz 'aydhır'\n📌 Tomato: Amerikan 'tomeytou' / İngiliz 'tomatou'",
     "Hangi aksanı öğreniyorsanız ona sadık kalın."),
]

# ============================================================
# GÖRSELLİ KALIP HAVUZU
# ============================================================
KALIPLAR = [
    # Kategori: SELAMLAŞMA
    ("👋 SELAMLAŞMA", "Hello!", "helou", "Merhaba!", "Hello, how are you?"),
    ("👋 SELAMLAŞMA", "Good morning!", "gud morning", "Günaydın!", "Good morning, everyone!"),
    ("👋 SELAMLAŞMA", "How are you?", "hau ar yu", "Nasılsın?", "How are you today?"),
    ("👋 SELAMLAŞMA", "Nice to meet you.", "nays tu miit yu", "Tanıştığıma memnun oldum.", "Nice to meet you, Sara."),
    ("👋 SELAMLAŞMA", "See you later.", "sii yu leytır", "Sonra görüşürüz.", "See you later, Ali!"),
    
    # Kategori: İŞ YERİ
    ("💼 İŞ YERİ", "Let's get started.", "lets get startıd", "Başlayalım.", "Let's get started with the meeting."),
    ("💼 İŞ YERİ", "Could you give me an update?", "kud yu giv mi ın apdeyt", "Güncel durumu aktarır mısınız?", "Could you give me an update on the project?"),
    ("💼 İŞ YERİ", "Let me check and get back to you.", "let mi çek end get bek tu yu", "Kontrol edip döneyim.", "Let me check and get back to you tomorrow."),
    ("💼 İŞ YERİ", "What's the deadline?", "vats dı dedlayn", "Son tarih ne zaman?", "What's the deadline for this report?"),
    ("💼 İŞ YERİ", "I'll send you the details.", "ayl send yu dı diiteylz", "Detayları göndereceğim.", "I'll send you the details by email."),
    
    # Kategori: RESTORAN
    ("🍽️ RESTORAN", "A table for two, please.", "ı teybl for tu pliiz", "İki kişilik masa, lütfen.", "A table for two, please."),
    ("🍽️ RESTORAN", "Could I see the menu?", "kud ay sii dı menyu", "Menüyü görebilir miyim?", "Could I see the menu, please?"),
    ("🍽️ RESTORAN", "What do you recommend?", "vat du yu rekımend", "Ne tavsiye edersiniz?", "What do you recommend as a starter?"),
    ("🍽️ RESTORAN", "Could we get the bill, please?", "kud vi get dı bil pliiz", "Hesabı alabilir miyiz?", "Could we get the bill, please?"),
    ("🍽️ RESTORAN", "This is delicious!", "dhis iz dilişıs", "Bu çok lezzetli!", "This is delicious, thank you!"),
    
    # Kategori: SEYAHAT
    ("✈️ SEYAHAT", "Where is the check-in counter?", "ver iz dı çekin kauntır", "Check-in nerede?", "Where is the check-in counter?"),
    ("✈️ SEYAHAT", "I'd like to book a room.", "ayd layk tu buk ı ruum", "Oda ayırtmak istiyorum.", "I'd like to book a room for two nights."),
    ("✈️ SEYAHAT", "How do I get to the city center?", "hau du ay get tu dı siti sentır", "Şehir merkezine nasıl giderim?", "How do I get to the city center?"),
    ("✈️ SEYAHAT", "Can I pay by card?", "ken ay pey bay kard", "Kartla ödeyebilir miyim?", "Can I pay by card?"),
    ("✈️ SEYAHAT", "I'm lost. Can you help me?", "aym lost ken yu help mi", "Kayboldum. Yardım eder misiniz?", "I'm lost. Can you help me?"),
    
    # Kategori: ALIŞVERİŞ
    ("🛒 ALIŞVERİŞ", "How much does it cost?", "hau maç daz it kost", "Ne kadar?", "How much does it cost?"),
    ("🛒 ALIŞVERİŞ", "Do you have this in a different size?", "du yu hev dhis in ı difrınt sayz", "Farklı bedeni var mı?", "Do you have this in a different size?"),
    ("🛒 ALIŞVERİŞ", "I'm just looking, thanks.", "aym cast luking thenks", "Sadece bakıyorum.", "I'm just looking, thanks."),
    ("🛒 ALIŞVERİŞ", "I'd like to return this.", "ayd layk tu ritırn dhis", "İade etmek istiyorum.", "I'd like to return this, please."),
    ("🛒 ALIŞVERİŞ", "Could you wrap it for me?", "kud yu rep it for mi", "Paketler misiniz?", "Could you wrap it for me?"),
    
    # Kategori: DUYGULAR
    ("💭 DUYGULAR", "I'm happy.", "aym hepi", "Mutluyum.", "I'm happy to see you."),
    ("💭 DUYGULAR", "I'm tired.", "aym tayırd", "Yorgunum.", "I'm tired today."),
    ("💭 DUYGULAR", "I don't understand.", "ay dont andırstend", "Anlamıyorum.", "I don't understand, sorry."),
    ("💭 DUYGULAR", "Can you repeat that?", "ken yu ripit dhet", "Tekrar eder misiniz?", "Can you repeat that, please?"),
    ("💭 DUYGULAR", "I'm learning English.", "aym lırning ingliş", "İngilizce öğreniyorum.", "I'm learning English every day."),
    
    # Kategori: İŞ EMAİL
    ("📧 İŞ EMAİL", "Please find attached...", "pliiz faynd ıteçt", "Ekte bulabilirsiniz...", "Please find attached the report."),
    ("📧 İŞ EMAİL", "I look forward to hearing from you.", "ay luk forvırd tu hiiring frım yu", "Haberinizi bekliyorum.", "I look forward to hearing from you."),
    ("📧 İŞ EMAİL", "Thank you for your prompt reply.", "thenk yu for yur prompt riplay", "Hızlı yanıtınız için teşekkürler.", "Thank you for your prompt reply."),
    ("📧 İŞ EMAİL", "Please let me know if you have any questions.", "pliiz let mi nou if yu hev eni kvesçınz", "Sorunuz olursa bildirin.", "Please let me know if you have any questions."),
    ("📧 İŞ EMAİL", "I apologize for the delay.", "ay ıpolıcayz for dı diley", "Gecikme için özür dilerim.", "I apologize for the delay in my response."),
]

# ============================================================
# TELAFFUZ İPUÇLARI (eski)
# ============================================================
TELAFFUZ_NOTLARI = [
    ("th (sert)", "think, three, thank", "Dil ucunu dişler arasına koy, hava üfle.", "s veya t demeyin."),
    ("th (yumuşak)", "this, that, the", "Aynı konum, ses teli titrer.", "d veya z demeyin."),
    ("w", "water, we, what", "Dudaklar yuvarlak, dişler değmez.", "v demeyin."),
    ("v", "very, voice", "Üst dişler alt dudağa değer.", "w ile karıştırmayın."),
    ("r", "red, right", "Dil ucu damağa değmez.", "Türkçe r gibi yuvarlamayın."),
    ("ng", "sing, long", "Dilin arkası damağa değer.", "sin-g diye ayırmayın."),
    ("schwa /ə/", "about, teacher", "Vurgusuz hecelerde kısa 'ı'.", "Her harfi tam sesle okumayın."),
    ("kısa/uzun ünlü", "ship / sheep", "Kısa: gevşek, uzun: gergin.", "İkisini de aynı okumayın."),
]

def gunun_gramer_dersi():
    gun = datetime.now().timetuple().tm_yday
    return GRAMER_DERSLERI[gun % len(GRAMER_DERSLERI)]

def gunun_telaffuz_rehberi():
    gun = datetime.now().timetuple().tm_yday
    return TELAFFUZ_REHBERI[gun % len(TELAFFUZ_REHBERI)]

def gunun_kaliplari():
    gun = datetime.now().timetuple().tm_yday
    baslangic = (gun * 10) % len(KALIPLAR)
    return KALIPLAR[baslangic:baslangic + 10]

def e_posta_gonder():
    tarih = datetime.now().strftime('%d.%m.%Y %A')
    kaliplar = gunun_kaliplari()
    gramer = gunun_gramer_dersi()
    telaffuz = gunun_telaffuz_rehberi()
    
    # GRAMER BÖLÜMÜ (en başta)
    gramer_html = f'''
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; padding: 20px; border-radius: 12px; margin-bottom: 15px;">
        <h2 style="margin: 0;">📚 GÜNÜN GRAMER DERSİ</h2>
        <h3 style="margin: 8px 0; color: #fff;">{gramer[0]}</h3>
    </div>
    <div style="background: #f0f4ff; padding: 15px; border-radius: 8px; 
    border-left: 5px solid #667eea; margin-bottom: 15px;">
        <p style="font-size: 14px; line-height: 1.7;"><strong>📖 Açıklama:</strong> {gramer[1]}</p>
    </div>
    <div style="background: #fff9e6; padding: 15px; border-radius: 8px; 
    border-left: 5px solid #f39c12; margin-bottom: 15px;">
        <p style="font-size: 14px; line-height: 1.8;"><strong>📋 Kural:</strong><br>{gramer[2].replace(chr(10), '<br>')}</p>
    </div>
    <div style="background: #e8f8f5; padding: 15px; border-radius: 8px; 
    border-left: 5px solid #27ae60;">
        <p style="font-size: 14px;"><strong>💡 Örnek:</strong> {gramer[3]}</p>
    </div>
    '''
    
    # TELAFFUZ REHBERİ BÖLÜMÜ
    telaffuz_html = f'''
    <div style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); 
    color: white; padding: 20px; border-radius: 12px; margin: 15px 0;">
        <h2 style="margin: 0;">🗣️ GÜNÜN TELAFFUZ REHBERİ</h2>
        <h3 style="margin: 8px 0; color: #fff;">{telaffuz[0]}</h3>
        <span style="background: rgba(255,255,255,0.3); padding: 4px 10px; 
        border-radius: 12px; font-size: 12px;">{telaffuz[1]}</span>
    </div>
    <div style="background: #fdedec; padding: 15px; border-radius: 8px; 
    border-left: 5px solid #e74c3c; margin-bottom: 15px;">
        <p style="font-size: 14px;"><strong>🎯 Örnek Kelimeler:</strong> {telaffuz[2]}</p>
    </div>
    <div style="background: #fff9e6; padding: 15px; border-radius: 8px; 
    border-left: 5px solid #f39c12; margin-bottom: 15px;">
        <p style="font-size: 14px;"><strong>👄 Nasıl Çıkarılır:</strong> {telaffuz[3]}</p>
    </div>
    <div style="background: #ffeaa7; padding: 15px; border-radius: 8px; 
    border-left: 5px solid #d35400; margin-bottom: 15px;">
        <p style="font-size: 14px;"><strong>❌ Sık Yapılan Hatalar:</strong><br>{telaffuz[4].replace(chr(10), '<br>')}</p>
    </div>
    <div style="background: #d4edda; padding: 15px; border-radius: 8px; 
    border-left: 5px solid #28a745;">
        <p style="font-size: 14px;"><strong>🎯 Pratik İpucu:</strong> {telaffuz[5]}</p>
    </div>
    '''
    
    # GÖRSELLİ KALIP TABLOSU
    kalip_html = '''
    <div style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
    color: white; padding: 20px; border-radius: 12px; margin: 15px 0;">
        <h2 style="margin: 0;">📖 GÜNÜN 10 KALIBI (Görselli)</h2>
        <p style="margin: 8px 0 0 0; opacity: 0.9;">Her kalıbın yanındaki simge, kullanım alanını gösterir</p>
    </div>
    <table style="border-collapse: collapse; width: 100%; font-size: 13px; 
    border-radius: 8px; overflow: hidden;">
    <tr style="background: #2c3e50; color: white;">
        <th style="padding: 10px;">Kategori</th>
        <th style="padding: 10px;">Kalıp</th>
        <th style="padding: 10px;">Türkçe Okunuş</th>
        <th style="padding: 10px;">Anlam</th>
        <th style="padding: 10px;">Örnek</th>
    </tr>
    '''
    for i, (kategori, ing, okunus, anlam, ornek) in enumerate(kaliplar):
        bg = "#f8f9fa" if i % 2 == 0 else "white"
        kalip_html += f'''
        <tr style="background: {bg};">
            <td style="padding: 8px; border: 1px solid #ecf0f1; font-size: 11px;">{kategori}</td>
            <td style="padding: 8px; border: 1px solid #ecf0f1;"><strong>{ing}</strong></td>
            <td style="padding: 8px; border: 1px solid #ecf0f1; color: #27ae60;">{okunus}</td>
            <td style="padding: 8px; border: 1px solid #ecf0f1;">{anlam}</td>
            <td style="padding: 8px; border: 1px solid #ecf0f1; font-style: italic;">{ornek}</td>
        </tr>
        '''
    kalip_html += '</table>'
    
    html_body = f'''
    <html><body style="font-family: Arial, sans-serif; max-width: 950px; 
    margin: auto; background-color: #ecf0f1; padding: 20px;">
    
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
    color: white; padding: 25px; border-radius: 12px; text-align: center;">
        <h1 style="margin: 0;">📚 Günlük İngilizce Bülteni</h1>
        <p style="margin: 8px 0 0 0;">{tarih}</p>
        <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 12px;">
        📖 Gramer + 🗣️ Telaffuz + 🎨 Görselli Kalıplar</p>
    </div>
    
    <div style="background: white; padding: 20px; margin-top: 15px; border-radius: 12px;">
    {gramer_html}
    </div>
    
    <div style="background: white; padding: 20px; margin-top: 15px; border-radius: 12px;">
    {telaffuz_html}
    </div>
    
    <div style="background: white; padding: 20px; margin-top: 15px; border-radius: 12px;">
    {kalip_html}
    </div>
    
    <div style="background: #34495e; color: white; padding: 15px; margin-top: 15px; 
    border-radius: 12px; font-size: 11px; text-align: center;">
    <strong>📌 Nasıl Çalışmalısınız?</strong><br>
    1️⃣ Gramer dersini oku (5 dk) → 2️⃣ Telaffuz kuralını sesli tekrarla (3 dk)<br>
    3️⃣ 10 kalıbı sesli oku (5 dk) → 4️⃣ Kendi cümlenizi kurun (2 dk)<br>
    Toplam: 15 dakika
    </div>
    </body></html>
    '''
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"📚 İngilizce Bülteni - {datetime.now().strftime('%d.%m.%Y')}"
    msg['From'] = MAIL_USER
    msg['To'] = MAIL_TO
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(MAIL_USER, MAIL_PASS)
            server.sendmail(MAIL_USER, MAIL_TO, msg.as_string())
        print("✅ E-posta gönderildi.")
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    print("İngilizce bülteni hazırlanıyor...")
    e_posta_gonder()
