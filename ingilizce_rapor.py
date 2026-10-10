# -*- coding: utf-8 -*-
"""
🎓 TAM KAPSAMLI İNGİLİZCE KURSU v3
+ Streak takibi
+ İlerleme kaydı
+ Adaptif zorluk
+ Bağlam hikayesi
+ Çoklu alıştırma tipi
+ Telaffuz pratiği
+ Haftalık değerlendirme
"""

import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")
MAIL_TO = os.environ.get("MAIL_TO")

# ============================================================
# İLERLEME TAKİBİ (STATE)
# ============================================================
STATE_FILE = "state.json"

def load_state():
    """Önceki ilerlemeyi yükler."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {
        "streak": 0,
        "last_run_date": "",
        "total_lessons": 0,
        "seen_words": [],
        "word_scores": {},
        "total_correct": 0,
        "total_wrong": 0,
        "start_date": str(datetime.now().date()),
        "last_weekly_report": ""
    }

def save_state(state):
    """İlerlemeyi kaydeder."""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def update_streak(state):
    """Seri takibini günceller."""
    today = str(datetime.now().date())
    yesterday = str((datetime.now() - timedelta(days=1)).date())
    
    if state["last_run_date"] == today:
        pass  # Bugün zaten çalıştı
    elif state["last_run_date"] == yesterday:
        state["streak"] += 1
    else:
        state["streak"] = 1
    
    state["last_run_date"] = today
    state["total_lessons"] += 1
    return state

def get_streak_message(streak):
    """Streak mesajı üretir."""
    if streak == 1:
        return "🔥 Yeni bir seri başladı! Yarın da devam et."
    elif streak < 7:
        return f"🔥 {streak} gündür üst üste çalışıyorsun!"
    elif streak < 30:
        return f"🔥🔥 Harika! {streak} günlük seri!"
    elif streak < 100:
        return f"🔥🔥🔥 {streak} gün! Sen bir efsanesin!"
    else:
        return f"🏆 {streak} GÜN! İnanılmaz!"

# ============================================================
# BÖLÜM 1: TELAFFUZ DERSLERİ (16 KURAL)
# ============================================================
TELAFFUZ_DERSLERI = [
    {
        "baslik": "C Harfi — 'S' mi 'K' mi?",
        "kural": "İngilizce'de C harfi iki farklı ses verir. Hangi harften önce geldiğine bağlıdır.",
        "detay": "e, i, y harflerinden önce → 'S' okunur\na, o, u harflerinden önce → 'K' okunur\nCH yan yana → 'Ç' okunur",
        "ornekler": [
            ("cinema", "Sİ-nı-mı", "sinema (S)"),
            ("city", "Sİ-ti", "şehir (S)"),
            ("cycle", "SAY-kıl", "bisiklet (S)"),
            ("cat", "KET", "kedi (K)"),
            ("cold", "KOULD", "soğuk (K)"),
            ("cup", "KAP", "fincan (K)"),
            ("chocolate", "ÇA-kı-lıt", "çikolata (Ç)"),
            ("chair", "ÇEYR", "sandalye (Ç)")
        ],
        "ipucu": "Pratik: 'Ca-co-cu, Ke-ki' diye tekrarlayın. Sonra 'city, cinema, cat, cup' deyin."
    },
    {
        "baslik": "G Harfi — 'C' mi 'G' mi?",
        "kural": "G harfi de C gibi iki farklı ses verir.",
        "detay": "e, i, y harflerinden önce → 'C' okunur\na, o, u harflerinden önce → 'G' okunur",
        "ornekler": [
            ("gym", "CİM", "spor salonu (C)"),
            ("giant", "CAY-ınt", "dev (C)"),
            ("giraffe", "ci-RAF", "zürafa (C)"),
            ("go", "GOU", "gitmek (G)"),
            ("game", "GEYM", "oyun (G)"),
            ("gum", "GAM", "sakız (G)")
        ],
        "ipucu": "Pratik: 'Gym, giant, giraffe' hepsinde 'c' sesi var. 'Go, game, gum' hepsinde 'g' sesi."
    },
    {
        "baslik": "TH Sesi — En Zor Ses!",
        "kural": "Türkçe'de olmayan bir ses. Dilinizi dişlerinizin arasına koyarak çıkarılır. İki türlü: sert ve yumuşak.",
        "detay": "SERT TH: Ses teli titremez. Hava üflenir.\nYUMUŞAK TH: Ses teli titrer (parmağınızı boğazınıza koyunca hissedersiniz).",
        "ornekler": [
            ("think", "THİNK (sert)", "düşünmek"),
            ("three", "THRİİ (sert)", "üç"),
            ("thank", "THENK (sert)", "teşekkür"),
            ("month", "MANTH (sert)", "ay"),
            ("this", "DHİS (yumuşak)", "bu"),
            ("that", "DHET (yumuşak)", "şu"),
            ("mother", "MA-dhır (yumuşak)", "anne"),
            ("brother", "BRA-dhır (yumuşak)", "erkek kardeş")
        ],
        "ipucu": "Ayna alın. Dilinizin ucunu üst ve alt dişlerinizin ARASINA koyun. 'TH' sesi çıkarken dilinizi ısırıyor gibi olacaksınız."
    },
    {
        "baslik": "W ve V — Karıştırılan İkili",
        "kural": "Türkçe'de W yok. V var. Ama İngilizce'de ikisi de var ve farklıdır.",
        "detay": "W: Dudaklar yuvarlak, dişler dudağa DEĞMEZ (öpücük verir gibi)\nV: Üst dişler alt dudağa DEĞER, titreşim var",
        "ornekler": [
            ("water", "VO-tır", "su (W)"),
            ("we", "Vİİ", "biz (W)"),
            ("what", "VAT", "ne (W)"),
            ("window", "VİN-dou", "pencere (W)"),
            ("very", "VE-ri", "çok (V)"),
            ("voice", "VOYS", "ses (V)"),
            ("love", "LAV", "sevmek (V)"),
            ("seven", "SE-vın", "yedi (V)")
        ],
        "ipucu": "W'de dudak yuvarlak, V'de diş dudakta. Aynaya bakarak pratik yapın."
    },
    {
        "baslik": "R Sesi — Türkçe'den Farklı",
        "kural": "İngilizce R Türkçe R'den tamamen farklıdır.",
        "detay": "Türkçe R: Dil ucu damağa vurur, titrer\nİngilizce R: Dil ucu damağa DEĞMEZ, hafif geriye kıvrılır",
        "ornekler": [
            ("red", "RED", "kırmızı"),
            ("right", "RAYT", "sağ/doğru"),
            ("around", "ı-RAUND", "etrafında"),
            ("sorry", "SO-ri", "üzgünüm"),
            ("car", "KAR", "araba"),
            ("park", "PARK", "park")
        ],
        "ipucu": "Dilinizin damağa değmediğini aynada kontrol edin. 'R' derken diliniz boşlukta olmalı."
    },
    {
        "baslik": "Sessiz Harfler — Yazılır ama Okunmaz",
        "kural": "Bazı harfler kelimede yazılır ama okunmaz. Bu kelimeleri kalıp olarak ezberlemek gerekir.",
        "detay": "K: know, knife, knee\nW: write, wrong, answer\nH: hour, honest\nS: island, isle\nT: listen, castle, often\nB: comb, climb, thumb",
        "ornekler": [
            ("know", "NOU", "bilmek (K sessiz)"),
            ("write", "RAYT", "yazmak (W sessiz)"),
            ("hour", "AU-ır", "saat (H sessiz)"),
            ("listen", "Lİ-sın", "dinlemek (T sessiz)"),
            ("island", "AY-lınd", "ada (S sessiz)"),
            ("comb", "KOUM", "tarak (B sessiz)")
        ],
        "ipucu": "Bu kelimeleri gördüğünüzde 'içinden' o harfi atlayın."
    },
    {
        "baslik": "Schwa /ə/ — İngilizce'nin Sırrı",
        "kural": "İngilizce'de vurgusuz hecelerde ünlü harfler 'yutulur'. Çok kısa, gevşek bir ses olur. Buna 'schwa' denir.",
        "detay": "Türkçe'de her harf tam okunur. İngilizce'de vurgusuz heceler kısalır.\nÖrnek: 'banana' = bı-NA-nı (ikinci hece vurgulu, diğerleri yutulur)",
        "ornekler": [
            ("banana", "bı-NA-nı", "muz"),
            ("teacher", "Tİİ-çır", "öğretmen (a yok!)"),
            ("computer", "kım-PYU-tır", "bilgisayar"),
            ("about", "ı-BAUT", "hakkında"),
            ("camera", "KE-mı-rı", "kamera"),
            ("animal", "E-nı-mıl", "hayvan")
        ],
        "ipucu": "Vurgusuz heceleri 'mırıldanın'. Türkçe'deki gibi net söylemeye çalışmayın."
    },
    {
        "baslik": "-ED Eki — 3 Farklı Okunur",
        "kural": "Geçmiş zaman eki -ed, 3 farklı şekilde okunur. Hangi harfin ardından geldiğine bağlıdır.",
        "detay": "Sessiz harften sonra → /t/ (worked = vırkt)\nSesli harften sonra → /d/ (played = pleyd)\nT veya D'den sonra → /ɪd/ (wanted = vantıd)",
        "ornekler": [
            ("worked", "VIRKT", "çalıştı (/t/)"),
            ("helped", "HELPT", "yardım etti (/t/)"),
            ("played", "PELYD", "oynadı (/d/)"),
            ("lived", "LİVD", "yaşadı (/d/)"),
            ("wanted", "VAN-tıd", "istedi (/ɪd/)"),
            ("needed", "Nİİ-dıd", "ihtiyaç duydu (/ɪd/)")
        ],
        "ipucu": "Kulağınızı eğitin: 'vırkt, pleyd, vantıd' — üçü farklı."
    },
    {
        "baslik": "-S Eki — 3 Farklı Okunur",
        "kural": "Çoğul eki -s, 3 farklı şekilde okunur.",
        "detay": "Sessiz harften sonra → /s/ (cats = kets)\nSesli harften sonra → /z/ (dogs = dogz)\nS, Z, SH, CH, X'ten sonra → /ɪz/ (buses = basız)",
        "ornekler": [
            ("cats", "KETS", "kediler (/s/)"),
            ("books", "BUKS", "kitaplar (/s/)"),
            ("dogs", "DOGZ", "köpekler (/z/)"),
            ("cars", "KARZ", "arabalar (/z/)"),
            ("buses", "BA-sız", "otobüsler (/ɪz/)"),
            ("boxes", "BAK-sız", "kutular (/ɪz/)")
        ],
        "ipucu": "Kulağınızı eğitin: 'kets, dogz, basız' — üç farklı."
    },
    {
        "baslik": "A Harfi — İki Ses",
        "kural": "A harfi iki farklı ses verir: kısa /æ/ ve uzun /eɪ/.",
        "detay": "Kısa A: Ağız GENİŞ açılır, 'a' ile 'e' arası bir ses\nUzun A: 'ey' sesi, ağız kapanır",
        "ornekler": [
            ("cat", "KET (geniş a)", "kedi"),
            ("bad", "BED (geniş a)", "kötü"),
            ("man", "MEN (geniş a)", "adam"),
            ("cake", "KEYK (ey)", "pasta"),
            ("name", "NEYM (ey)", "isim"),
            ("game", "GEYM (ey)", "oyun")
        ],
        "ipucu": "'Cat' derken ağzınızı geniş açın (gülümser gibi). 'Cake' derken kapatın."
    },
    {
        "baslik": "Vurgu (Stress) — Kelimenin Ritmi",
        "kural": "İngilizce'de çok heceli kelimelerde bir hece daha güçlü ve uzun okunur. Buna 'vurgu' denir.",
        "detay": "Vurgu yanlış olursa kelime anlaşılmaz.\nSözlükte IPA yazısında ' işareti vurguyu gösterir: /ˈteɪbl/ → TEY-bıl",
        "ornekler": [
            ("TA-ble", "TEY-bıl", "masa (1. hece)"),
            ("be-CAUSE", "bi-KOZ", "çünkü (2. hece)"),
            ("PHO-to-graph", "FOU-tı-graf", "fotoğraf (1. hece)"),
            ("pho-TO-gra-pher", "fı-TO-grı-fır", "fotoğrafçı (2. hece)"),
            ("IM-por-tant", "im-POR-tınt", "önemli (2. hece)"),
            ("HO-tel", "hou-TEL", "otel (2. hece)")
        ],
        "ipucu": "Her yeni kelimeyi öğrenirken hangi hecenin vurgulu olduğunu da öğrenin."
    },
    {
        "baslik": "Sessiz 'E' — Kelime Sonundaki E",
        "kural": "Kelime sonunda E harfi genellikle okunmaz ama önceki ünlüyü uzatır.",
        "detay": "make → MEYK (e okunmaz, a'yı uzatır)\nnot → NOT / note → NOUT\nkit → KİT / kite → KAYT",
        "ornekler": [
            ("make", "MEYK", "yapmak"),
            ("name", "NEYM", "isim"),
            ("cake", "KEYK", "pasta"),
            ("hope", "HOUP", "ummak"),
            ("note", "NOUT", "not"),
            ("tube", "TYUB", "tüp")
        ],
        "ipucu": "Sondaki E'yi sessizce geçin ama önceki ünlüyü uzatın."
    },
    {
        "baslik": "OO Sesi — İki Farklı",
        "kural": "OO harfleri iki farklı ses verir: kısa /ʊ/ ve uzun /uː/.",
        "detay": "Kısa OO: book, look, good, foot\nUzun OO: food, moon, soon, school",
        "ornekler": [
            ("book", "BUK", "kitap (kısa)"),
            ("look", "LUK", "bakmak (kısa)"),
            ("good", "GUD", "iyi (kısa)"),
            ("food", "FUUD", "yemek (uzun)"),
            ("moon", "MUUN", "ay (uzun)"),
            ("school", "SKUUL", "okul (uzun)")
        ],
        "ipucu": "Kısa OO kısa ve gevşek, uzun OO iki kat uzun."
    },
    {
        "baslik": "OU Sesi — 4 Farklı Okunur",
        "kural": "OU harfleri İngilizce'de en çok karıştırılan kombinasyon. 4 farklı okunuşu var.",
        "detay": "1. /aʊ/ → house, mouse, out\n2. /uː/ → soup, group, you\n3. /ʌ/ → country, young, touch\n4. /ɔː/ → thought, bought",
        "ornekler": [
            ("house", "HAUS", "ev (/aʊ/)"),
            ("mouse", "MAUS", "fare (/aʊ/)"),
            ("soup", "SUUP", "çorba (/uː/)"),
            ("group", "GRUUP", "grup (/uː/)"),
            ("country", "KAN-tri", "ülke (/ʌ/)"),
            ("young", "YANG", "genç (/ʌ/)")
        ],
        "ipucu": "Her kelimeyi ayrı öğrenmek gerekir. Sözlükten sesini dinleyin."
    },
    {
        "baslik": "Bağlantılı Konuşma — Günlük Kısaltmalar",
        "kural": "Günlük konuşmada kelimeler birleşir ve kısalır. Bu doğal İngilizce'nin sırrıdır.",
        "detay": "What are you → Whatcha\nGoing to → Gonna\nWant to → Wanna\nDid you → Dija\nLet me → Lemme",
        "ornekler": [
            ("What are you doing?", "Vatça duing?", "Ne yapıyorsun?"),
            ("I'm going to go.", "Aym gana gou.", "Gideceğim."),
            ("Do you want to eat?", "Du yu vana iit?", "Yemek ister misin?"),
            ("Did you see?", "Dija sii?", "Gördün mü?"),
            ("Let me help.", "Lemi help.", "Yardım edeyim.")
        ],
        "ipucu": "Resmi yazışmalarda kullanmayın ama günlük konuşmada normaldir."
    },
    {
        "baslik": "Y ve J — Türkçe'de Yok",
        "kural": "İngilizce Y ve J harfleri Türkçe'den farklı okunur.",
        "detay": "Y: 'y' değil, 'y' ve 'i' arası bir ses (yes → YES)\nJ: 'c' sesi (job → COB)",
        "ornekler": [
            ("yes", "YES", "evet"),
            ("you", "YU", "sen"),
            ("year", "YİIR", "yıl"),
            ("job", "COB", "iş"),
            ("jump", "CAMP", "zıplamak"),
            ("enjoy", "en-COY", "keyif almak")
        ],
        "ipucu": "J'yi 'c' gibi söyleyin: 'job' = 'cob'."
    }
]

# ============================================================
# BÖLÜM 2: KALIP DERSLERİ (150 KALIP, 10 TEMA)
# ============================================================
KALIP_DERSLERI = [
    # TEMA 1: SELAMLAŞMA (15 kalıp)
    ("👋 SELAMLAŞMA", "Hello!", "he-LOU", "Merhaba!", "Hello! How are you?"),
    ("👋 SELAMLAŞMA", "Good morning!", "gud MOR-ning", "Günaydın!", "Good morning, everyone!"),
    ("👋 SELAMLAŞMA", "How are you?", "hau ar YU", "Nasılsın?", "Hi Ali, how are you?"),
    ("👋 SELAMLAŞMA", "I'm fine, thanks.", "aym FAYN thenks", "İyiyim, teşekkürler.", "I'm fine, thanks. And you?"),
    ("👋 SELAMLAŞMA", "Nice to meet you.", "nays tu MİİT yu", "Tanıştığıma memnun oldum.", "Nice to meet you, Sara."),
    ("👋 SELAMLAŞMA", "What's your name?", "vats yor NEYM", "Adın ne?", "What's your name?"),
    ("👋 SELAMLAŞMA", "My name is...", "may NEYM iz", "Benim adım...", "My name is Yusuf."),
    ("👋 SELAMLAŞMA", "Where are you from?", "ver ar yu FRUM", "Nerelisin?", "Where are you from?"),
    ("👋 SELAMLAŞMA", "I'm from Turkey.", "aym frum TIR-ki", "Türkiye'denim.", "I'm from Turkey."),
    ("👋 SELAMLAŞMA", "See you later.", "Sİİ yu LEY-tır", "Sonra görüşürüz.", "See you later, Ali!"),
    ("👋 SELAMLAŞMA", "Take care.", "TEYK KER", "Kendine iyi bak.", "Take care of yourself."),
    ("👋 SELAMLAŞMA", "Have a nice day.", "hev ı NAYS DEY", "İyi günler.", "Have a nice day!"),
    ("👋 SELAMLAŞMA", "Good night.", "gud NAYT", "İyi geceler.", "Good night, sleep well."),
    ("👋 SELAMLAŞMA", "How's it going?", "hauz it GOU-ing", "Nasıl gidiyor?", "Hey man, how's it going?"),
    ("👋 SELAMLAŞMA", "Long time no see!", "long TAYM nou Sİİ", "Ne zamandır görüşemedik!", "Long time no see!"),

    # TEMA 2: İŞ YERİ (15 kalıp)
    ("💼 İŞ YERİ", "Let's get started.", "lets get STAR-tıd", "Başlayalım.", "Let's get started with the agenda."),
    ("💼 İŞ YERİ", "Could you give me an update?", "kud yu giv mi ın AP-deyt", "Güncel durumu aktarır mısınız?", "Could you give me an update on the project?"),
    ("💼 İŞ YERİ", "Let me check and get back to you.", "let mi çek end get BEK tu yu", "Kontrol edip döneyim.", "Let me check and get back to you tomorrow."),
    ("💼 İŞ YERİ", "What's the deadline?", "vats dı DED-layn", "Son tarih ne zaman?", "What's the deadline for this report?"),
    ("💼 İŞ YERİ", "I'll send you the details.", "ayl send yu dı Dİİ-teylz", "Detayları göndereceğim.", "I'll send you the details by email."),
    ("💼 İŞ YERİ", "We're running behind schedule.", "vir RA-ning bi-HAYND SKE-cul", "Programın gerisindeyiz.", "We're running behind schedule this week."),
    ("💼 İŞ YERİ", "That makes sense.", "dhet MEYKS SENS", "Mantıklı.", "That makes sense to me."),
    ("💼 İŞ YERİ", "I see your point, but...", "ay sii yur POYNT bat", "Anlıyorum ama...", "I see your point, but the cost is high."),
    ("💼 İŞ YERİ", "Let's schedule a meeting.", "lets SKE-cul ı Mİİ-ting", "Toplantı planlayalım.", "Let's schedule a meeting for Monday."),
    ("💼 İŞ YERİ", "Do you mind if I...?", "du yu MAYND if ay", "...sakıncası var mı?", "Do you mind if I open the window?"),
    ("💼 İŞ YERİ", "I'm on the same page.", "aym an dı SEYM PEYC", "Aynı fikirdeyim.", "I'm on the same page with you."),
    ("💼 İŞ YERİ", "Could you elaborate on that?", "kud yu i-LA-bı-reyt an dhet", "Bunu biraz açar mısınız?", "Could you elaborate on that point?"),
    ("💼 İŞ YERİ", "Let's touch base next week.", "lets TAÇ BEYS nekst viik", "Gelecek hafta görüşelim.", "Let's touch base next week."),
    ("💼 İŞ YERİ", "I'm afraid I can't make it.", "aym ı-FREYD ay kent MEYK it", "Maalesef gelemeyeceğim.", "I'm afraid I can't make it to the meeting."),
    ("💼 İŞ YERİ", "Sorry to keep you waiting.", "SO-ri tı KİİP yu VEY-ting", "Beklettiğim için özür dilerim.", "Sorry to keep you waiting."),

    # TEMA 3: RESTORAN (15 kalıp)
    ("🍽️ RESTORAN", "A table for two, please.", "ı TEY-bıl for TU pliiz", "İki kişilik masa, lütfen.", "A table for two, please."),
    ("🍽️ RESTORAN", "Could I see the menu?", "kud ay sii dı MEN-yu", "Menüyü görebilir miyim?", "Could I see the menu, please?"),
    ("🍽️ RESTORAN", "What do you recommend?", "vat du yu re-kı-MEND", "Ne tavsiye edersiniz?", "What do you recommend as a starter?"),
    ("🍽️ RESTORAN", "I'll have the same.", "ayl hev dı SEYM", "Aynısını alayım.", "I'll have the same as him."),
    ("🍽️ RESTORAN", "Could we get the bill, please?", "kud vi get dı BİL pliiz", "Hesabı alabilir miyiz?", "Could we get the bill, please?"),
    ("🍽️ RESTORAN", "Is service included?", "iz SIR-vis in-KLUU-dıd", "Servis dahil mi?", "Is service included in the bill?"),
    ("🍽️ RESTORAN", "I'm allergic to nuts.", "aym ı-LIR-cik tı NATS", "Kuruyemişe alerjim var.", "I'm allergic to nuts."),
    ("🍽️ RESTORAN", "Could I have some water, please?", "kud ay hev sam VO-tır pliiz", "Biraz su alabilir miyim?", "Could I have some water, please?"),
    ("🍽️ RESTORAN", "This is delicious!", "dhis iz di-Lİ-şıs", "Bu çok lezzetli!", "This is delicious, thank you!"),
    ("🍽️ RESTORAN", "I'm full, thank you.", "aym FUL THENK yu", "Doydum, teşekkürler.", "I'm full, thank you."),
    ("🍽️ RESTORAN", "Could I get a coffee?", "kud ay get ı KO-fi", "Bir kahve alabilir miyim?", "Could I get a coffee, please?"),
    ("🍽️ RESTORAN", "Rare, medium, or well-done?", "RER, Mİ-di-ım, or VEL-DAN", "Az, orta veya iyi pişmiş?", "How would you like your steak?"),
    ("🍽️ RESTORAN", "It's on me.", "its an Mİİ", "Benden.", "Don't worry, it's on me."),
    ("🍽️ RESTORAN", "Could we split the bill?", "kud vi SPLİT dı BİL", "Hesabı bölüşebilir miyiz?", "Could we split the bill?"),
    ("🍽️ RESTORAN", "Can I have the check, please?", "ken ay hev dı ÇEK pliiz", "Hesap lütfen.", "Can I have the check, please?"),

    # TEMA 4: SEYAHAT (15 kalıp)
    ("✈️ SEYAHAT", "Where is the check-in counter?", "ver iz dı ÇEK-in KAUN-tır", "Check-in nerede?", "Excuse me, where is the check-in counter?"),
    ("✈️ SEYAHAT", "I'd like to book a room.", "ayd layk tı BUK ı RUUM", "Oda ayırtmak istiyorum.", "I'd like to book a room for two nights."),
    ("✈️ SEYAHAT", "What time is check-out?", "vat taym iz ÇEK-aut", "Çıkış saati kaçta?", "What time is check-out?"),
    ("✈️ SEYAHAT", "Is breakfast included?", "iz BREK-fıst in-KLUU-dıd", "Kahvaltı dahil mi?", "Is breakfast included in the price?"),
    ("✈️ SEYAHAT", "How do I get to the city center?", "hau du ay get tı dı Sİ-ti SEN-tır", "Şehir merkezine nasıl giderim?", "How do I get to the city center?"),
    ("✈️ SEYAHAT", "I'm lost. Can you help me?", "aym LOST ken yu HELP mi", "Kayboldum. Yardım eder misiniz?", "I'm lost. Can you help me?"),
    ("✈️ SEYAHAT", "How much does it cost?", "hau MAÇ daz it KOST", "Ne kadar?", "How much does it cost to go there?"),
    ("✈️ SEYAHAT", "Can I pay by card?", "ken ay PEY bay KARD", "Kartla ödeyebilir miyim?", "Can I pay by card?"),
    ("✈️ SEYAHAT", "I have a reservation.", "ay hev ı re-zır-VEY-şın", "Rezervasyonum var.", "I have a reservation under the name Smith."),
    ("✈️ SEYAHAT", "Where is the bathroom?", "ver iz dı BAT-ruum", "Tuvalet nerede?", "Excuse me, where is the bathroom?"),
    ("✈️ SEYAHAT", "Can you take a photo?", "ken yu teyk ı FOU-tou", "Fotoğraf çeker misiniz?", "Can you take a photo of us?"),
    ("✈️ SEYAHAT", "I'm here on vacation.", "aym hiır an vey-KEY-şın", "Tatil için buradayım.", "I'm here on vacation for a week."),
    ("✈️ SEYAHAT", "Is it far from here?", "iz it FAR frım hiır", "Buradan uzak mı?", "Is it far from here?"),
    ("✈️ SEYAHAT", "Go straight, then turn left.", "gou STREYT, dhen TIRN LEFT", "Düz git, sonra sola dön.", "Go straight, then turn left."),
    ("✈️ SEYAHAT", "One ticket, please.", "VAN Tİ-kıt pliiz", "Bir bilet, lütfen.", "One ticket to London, please."),

    # TEMA 5: ALIŞVERİŞ (15 kalıp)
    ("🛒 ALIŞVERİŞ", "How much is this?", "hau MAÇ iz DHİS", "Bu ne kadar?", "How much is this shirt?"),
    ("🛒 ALIŞVERİŞ", "Do you have this in a different size?", "du yu hev dhis in ı DİF-rınt SAYZ", "Farklı bedeni var mı?", "Do you have this in a different size?"),
    ("🛒 ALIŞVERİŞ", "I'm just looking, thanks.", "aym cast LU-king THENKS", "Sadece bakıyorum, teşekkürler.", "I'm just looking, thanks."),
    ("🛒 ALIŞVERİŞ", "I'd like to return this.", "ayd layk tı ri-TIRN dhis", "İade etmek istiyorum.", "I'd like to return this, please."),
    ("🛒 ALIŞVERİŞ", "Could you wrap it for me?", "kud yu REP it for mi", "Paketler misiniz?", "Could you wrap it for me, please?"),
    ("🛒 ALIŞVERİŞ", "Can I try it on?", "ken ay TRAY it an", "Deneyebilir miyim?", "Can I try it on?"),
    ("🛒 ALIŞVERİŞ", "It's too expensive.", "its TU eks-PEN-siv", "Çok pahalı.", "It's too expensive for me."),
    ("🛒 ALIŞVERİŞ", "Do you have a discount?", "du yu hev ı DİS-kaunt", "İndirim var mı?", "Do you have a discount?"),
    ("🛒 ALIŞVERİŞ", "I'll take it.", "ayl TEYK it", "Alıyorum.", "I'll take it, thank you."),
    ("🛒 ALIŞVERİŞ", "Do you accept credit cards?", "du yu ık-SEPT KRE-dit KARDS", "Kredi kartı kabul ediyor musunuz?", "Do you accept credit cards?"),
    ("🛒 ALIŞVERİŞ", "Where is the fitting room?", "ver iz dı Fİ-ting RUUM", "Deneme kabini nerede?", "Where is the fitting room?"),
    ("🛒 ALIŞVERİŞ", "This is on sale.", "dhis iz an SEYL", "Bu indirimde.", "This is on sale, 50% off."),
    ("🛒 ALIŞVERİŞ", "Can I get a receipt?", "ken ay get ı ri-SİİT", "Fiş alabilir miyim?", "Can I get a receipt, please?"),
    ("🛒 ALIŞVERİŞ", "I'm looking for...", "aym LU-king for", "...arıyorum.", "I'm looking for a black jacket."),
    ("🛒 ALIŞVERİŞ", "Do you have this in black?", "du yu hev dhis in BLEK", "Bunun siyahı var mı?", "Do you have this in black?"),

    # TEMA 6: YARDIM (15 kalıp)
    ("🆘 YARDIM", "Could you help me?", "kud yu HELP mi", "Yardım eder misiniz?", "Excuse me, could you help me?"),
    ("🆘 YARDIM", "I don't understand.", "ay dont an-dır-STEND", "Anlamıyorum.", "Sorry, I don't understand."),
    ("🆘 YARDIM", "Can you repeat that?", "ken yu ri-PİİT dhet", "Tekrar eder misiniz?", "Can you repeat that, please?"),
    ("🆘 YARDIM", "Could you speak slowly?", "kud yu SPİİK SLOU-li", "Yavaş konuşabilir misiniz?", "Could you speak slowly, please?"),
    ("🆘 YARDIM", "What does this mean?", "vat daz dhis MİİN", "Bu ne anlama geliyor?", "What does this word mean?"),
    ("🆘 YARDIM", "How do you say... in English?", "hau du yu SEY ... in İNG-liş", "İngilizce'de ... nasıl denir?", "How do you say 'kitap' in English?"),
    ("🆘 YARDIM", "I'm learning English.", "aym LIR-ning İNG-liş", "İngilizce öğreniyorum.", "I'm learning English every day."),
    ("🆘 YARDIM", "Sorry, I don't know.", "SO-ri, ay dont NOU", "Üzgünüm, bilmiyorum.", "Sorry, I don't know."),
    ("🆘 YARDIM", "Could you write it down?", "kud yu RAYT it DAUN", "Yazar mısınız?", "Could you write it down, please?"),
    ("🆘 YARDIM", "Excuse me.", "eks-KYUZ mi", "Affedersiniz.", "Excuse me, are you Ali?"),
    ("🆘 YARDIM", "I'm sorry.", "aym SO-ri", "Üzgünüm.", "I'm sorry, I'm late."),
    ("🆘 YARDIM", "No problem.", "nou PROB-lım", "Sorun değil.", "No problem at all."),
    ("🆘 YARDIM", "Of course.", "ov KORS", "Elbette.", "Of course, I can help you."),
    ("🆘 YARDIM", "Just a moment, please.", "cast ı MOU-mınt pliiz", "Bir dakika lütfen.", "Just a moment, please."),
    ("🆘 YARDIM", "I'll be right back.", "ayl bii RAYT BEK", "Hemen döneceğim.", "I'll be right back."),

    # TEMA 7: DUYGULAR (15 kalıp)
    ("💭 DUYGULAR", "I'm happy.", "aym HE-pi", "Mutluyum.", "I'm happy to see you."),
    ("💭 DUYGULAR", "I'm tired.", "aym TAY-ırd", "Yorgunum.", "I'm tired today."),
    ("💭 DUYGULAR", "I'm hungry.", "aym HANG-ri", "Açım.", "I'm hungry, let's eat."),
    ("💭 DUYGULAR", "I'm thirsty.", "aym THIRS-ti", "Susadım.", "I'm thirsty, I need water."),
    ("💭 DUYGULAR", "I'm excited.", "aym ek-SAY-tıd", "Heyecanlıyım.", "I'm excited about the trip."),
    ("💭 DUYGULAR", "I'm worried.", "aym VIR-id", "Endişeliyim.", "I'm worried about the exam."),
    ("💭 DUYGULAR", "I think...", "ay THİNK", "Bence...", "I think it's a good idea."),
    ("💭 DUYGULAR", "In my opinion...", "in may ı-PİN-yın", "Bence...", "In my opinion, we should wait."),
    ("💭 DUYGULAR", "I agree.", "ay ı-GRİİ", "Katılıyorum.", "I agree with you on this point."),
    ("💭 DUYGULAR", "I disagree.", "ay dis-ı-GRİİ", "Katılmıyorum.", "I disagree with that idea."),
    ("💭 DUYGULAR", "I'm not sure.", "aym nat ŞUR", "Emin değilim.", "I'm not sure about that."),
    ("💭 DUYGULAR", "That's a good idea.", "dhets ı GUD ay-Dİ-ı", "Bu iyi bir fikir.", "That's a good idea, let's do it."),
    ("💭 DUYGULAR", "I hope so.", "ay HOUP sou", "Umarım öyle.", "I hope so too."),
    ("💭 DUYGULAR", "Never mind.", "NE-vır MAYND", "Önemli değil.", "Never mind, it's okay."),
    ("💭 DUYGULAR", "It doesn't matter.", "it DA-zınt ME-tır", "Önemli değil.", "It doesn't matter to me."),

    # TEMA 8: SOSYAL (15 kalıp)
    ("👥 SOSYAL", "Would you like to join us?", "vud yu layk tı COYN as", "Bize katılmak ister misin?", "Would you like to join us for dinner?"),
    ("👥 SOSYAL", "That sounds great!", "dhet SAUNDZ GREYT", "Kulağa harika geliyor!", "That sounds great! I'd love to."),
    ("👥 SOSYAL", "Maybe next time.", "MEY-bi nekst TAYM", "Belki bir dahaki sefere.", "Sorry, maybe next time."),
    ("👥 SOSYAL", "It was nice meeting you.", "it vaz NAYS Mİİ-ting yu", "Tanıştığımıza memnun oldum.", "It was nice meeting you."),
    ("👥 SOSYAL", "What's up?", "vats AP", "Ne haber?", "Hey, what's up?"),
    ("👥 SOSYAL", "Not much.", "nat MAÇ", "Pek bir şey yok.", "Not much, just working."),
    ("👥 SOSYAL", "How was your weekend?", "hau vaz yur Vİİ-kend", "Hafta sonun nasıldı?", "How was your weekend?"),
    ("👥 SOSYAL", "Do you want to hang out?", "du yu vant tı HENG AUT", "Takılmak ister misin?", "Do you want to hang out later?"),
    ("👥 SOSYAL", "Let's go out tonight.", "lets gou AUT tu-NAYT", "Bu akşam dışarı çıkalım.", "Let's go out tonight."),
    ("👥 SOSYAL", "I'm on my way.", "aym an may VEY", "Yoldayım.", "Don't worry, I'm on my way."),
    ("👥 SOSYAL", "Are you free tomorrow?", "ar yu FRİİ tu-MO-rou", "Yarın müsait misin?", "Are you free tomorrow evening?"),
    ("👥 SOSYAL", "I'd love to.", "ayd LAV tu", "Çok isterim.", "I'd love to come!"),
    ("👥 SOSYAL", "I'm busy right now.", "aym Bİ-zi RAYT nau", "Şu an meşgulüm.", "Sorry, I'm busy right now."),
    ("👥 SOSYAL", "Let me know.", "let mi NOU", "Haber ver.", "Let me know if you can come."),
    ("👥 SOSYAL", "Sounds like a plan.", "SAUNDZ layk ı PLEN", "Plan gibi görünüyor.", "Sounds like a plan!"),

    # TEMA 9: İŞ E-POSTA (15 kalıp)
    ("📧 E-POSTA", "Dear Sir/Madam,", "DİR SIR/ME-dım", "Sayın Yetkili,", "Dear Sir/Madam, I am writing to..."),
    ("📧 E-POSTA", "I'm writing to inquire about...", "aym RAY-ting tu in-KVAYR ı-BAUT", "...hakkında bilgi almak için yazıyorum.", "I'm writing to inquire about the position."),
    ("📧 E-POSTA", "Please find attached...", "pliiz FAYND ı-TEÇT", "Ekte bulabilirsiniz...", "Please find attached the report."),
    ("📧 E-POSTA", "I look forward to hearing from you.", "ay luk FOR-vırd tu HİR-ing frım yu", "Haberinizi bekliyorum.", "I look forward to hearing from you."),
    ("📧 E-POSTA", "Could you please confirm...?", "kud yu pliiz kın-FIRM", "...onaylayabilir misiniz?", "Could you please confirm the meeting time?"),
    ("📧 E-POSTA", "I apologize for the delay.", "ay ı-PO-lı-cayz for dı di-LEY", "Gecikme için özür dilerim.", "I apologize for the delay in my response."),
    ("📧 E-POSTA", "Thank you for your prompt reply.", "thenk yu for yur PROMPT ri-PLAY", "Hızlı yanıt için teşekkürler.", "Thank you for your prompt reply."),
    ("📧 E-POSTA", "I would appreciate it if...", "ay vud ı-PRİİ-şi-eyt it if", "...yaparsanız memnun olurum.", "I would appreciate it if you could send it today."),
    ("📧 E-POSTA", "Please let me know if you have any questions.", "pliiz let mi nou if yu hev ENi KYES-çınz", "Sorunuz olursa bildirin.", "Please let me know if you have any questions."),
    ("📧 E-POSTA", "Best regards,", "BEST ri-GARDS", "Saygılarımla,", "Best regards, Yusuf"),
    ("📧 E-POSTA", "I'm calling regarding...", "aym KO-ling ri-GAR-ding", "...hakkında arıyorum.", "I'm calling regarding your order."),
    ("📧 E-POSTA", "Could you hold on a moment?", "kud yu hould an ı MOU-mınt", "Bir dakika bekler misiniz?", "Could you hold on a moment, please?"),
    ("📧 E-POSTA", "May I take a message?", "mey ay teyk ı MES-ıc", "Mesaj alabilir miyim?", "May I take a message?"),
    ("📧 E-POSTA", "I'll transfer you.", "ayl TRANS-fır yu", "Sizi yönlendireceğim.", "I'll transfer you to the right department."),
    ("📧 E-POSTA", "Sorry, wrong number.", "SO-ri, RONG NAM-bır", "Üzgünüm, yanlış numara.", "Sorry, wrong number."),

    # TEMA 10: SUNUM (15 kalıp)
    ("📊 SUNUM", "Let's move on to the next point.", "lets MUUV an tu dı NEKST POYNT", "Bir sonraki konuya geçelim.", "Let's move on to the next point."),
    ("📊 SUNUM", "As you can see from the chart...", "ez yu ken Sİİ frım dı ÇART", "Grafikten de görebileceğiniz gibi...", "As you can see from the chart, sales are up."),
    ("📊 SUNUM", "Sales increased by 10%.", "seylz in-KRİİST bay ten pır-SENT", "Satışlar %10 arttı.", "Sales increased by 10% last quarter."),
    ("📊 SUNUM", "There was a slight decrease.", "dher vaz ı SLAY T di-KRİİS", "Hafif bir düşüş oldu.", "There was a slight decrease in profit."),
    ("📊 SUNUM", "We need to cut costs.", "vi niid tı KAT KOSTS", "Maliyetleri düşürmeliyiz.", "We need to cut costs to stay competitive."),
    ("📊 SUNUM", "Let's find a middle ground.", "lets FAYND ı Mİ-dıl GRAUND", "Orta bir yol bulalım.", "Let's find a middle ground on the price."),
    ("📊 SUNUM", "That's not acceptable.", "dhets nat ık-SEP-tı-bıl", "Bu kabul edilemez.", "That's not acceptable for us."),
    ("📊 SUNUM", "We can offer a discount.", "vi ken O-fır ı DİS-kaunt", "İndirim yapabiliriz.", "We can offer a 5% discount."),
    ("📊 SUNUM", "Let's agree on the terms.", "lets ı-GRİİ an dı TIRMZ", "Şartlar üzerinde anlaşalım.", "Let's agree on the terms before signing."),
    ("📊 SUNUM", "I'll get back to you with a decision.", "ayl get BEK tu yu vidh ı di-SİJ-ın", "Kararla döneceğim.", "I'll get back to you with a decision by Friday."),
    ("📊 SUNUM", "Let's summarize the key points.", "lets SA-mı-rayz dı Kİİ POYNTS", "Ana noktaları özetleyelim.", "Let's summarize the key points of the meeting."),
    ("📊 SUNUM", "To sum up...", "tu SAM AP", "Özetle...", "To sum up, we need more time."),
    ("📊 SUNUM", "Firstly... Secondly... Finally...", "FIRS-li, SE-kınd-li, FAY-nı-li", "Birincisi... İkincisi... Son olarak...", "Firstly, we need budget. Secondly, we need time."),
    ("📊 SUNUM", "Any questions?", "E-ni KYES-çınz", "Soru var mı?", "Any questions before we finish?"),
    ("📊 SUNUM", "Thank you for your attention.", "thenk yu for yur ı-TEN-şın", "Dinlediğiniz için teşekkürler.", "Thank you for your attention."),
]

# ============================================================
# BÖLÜM 3: GRAMER DERSLERİ (30 DERS)
# ============================================================
GRAMER_DERSLERI = [
    ("Ders 1: Alfabe ve Sesler",
     "İngilizce alfabede 26 harf var. Ancak 44 ses vardır. Yani harfler her zaman aynı sesi vermez.",
     "A = 'ey' | B = 'bi' | C = 'si' | D = 'di' | E = 'i' | F = 'ef' | G = 'ci' | H = 'eyç' | I = 'ay' | J = 'cey' | K = 'key' | L = 'el' | M = 'em' | N = 'en' | O = 'ou' | P = 'pi' | Q = 'kyu' | R = 'ar' | S = 'es' | T = 'ti' | U = 'yu' | V = 'vi' | W = 'dabılyu' | X = 'eks' | Y = 'vay' | Z = 'zi'",
     "Örnek: 'cat' 3 harf ama tek hece: KET."),
    ("Ders 2: To Be Fiili (am, is, are)",
     "İngilizce'nin temelidir. Türkçe'de 'ben öğretmenim' derken 'im' eki kullanılır. İngilizce'de ayrı bir kelime kullanılır: am/is/are.",
     "I am (ay em) | You are (yu ar) | He is (hi iz) | She is (şi iz) | It is (it iz) | We are (vi ar) | They are (dhey ar)",
     "Örnek: I am a teacher (ay em ı Tİİ-çır) = Ben bir öğretmenim."),
    ("Ders 3: İşaret Zamirleri",
     "Bir şeyi işaret ederken kullanılır.",
     "This (dhis) = Bu | These (dhiiz) = Bunlar | That (dhet) = Şu | Those (dhouz) = Şunlar",
     "Örnek: This is a book (dhis iz ı BUK) = Bu bir kitap."),
    ("Ders 4: Basit Şimdiki Zaman",
     "Her gün yapılan alışkanlıkları anlatır.",
     "I work | You work | He works | She works | We work | They work",
     "⚠️ He/She/It ile fiile MUTLAKA -s eklenir!"),
    ("Ders 5: Şimdiki Zaman (Şu An)",
     "Şu anda devam eden eylemleri anlatır.",
     "I am working | She is reading | They are playing",
     "⚠️ 'am/is/are' ile fiilin -ing hali birlikte kullanılır."),
    ("Ders 6: Geçmiş Zaman",
     "Geçmişte olan olayları anlatır.",
     "work → worked | play → played | go → went | eat → ate | see → saw",
     "Örnek: I worked yesterday = Dün çalıştım."),
    ("Ders 7: Gelecek Zaman (Will)",
     "Gelecekte olacak olayları anlatır.",
     "I will go | She will come | We will see",
     "💡 Kısaltma: I will = I'll | She will = She'll"),
    ("Ders 8: Sahiplik Sıfatları",
     "Bir şeyin kime ait olduğunu gösterir.",
     "My (benim) | Your (senin) | His (onun-e) | Her (onun-k) | Its (onun-n) | Our (bizim) | Their (onların)",
     "Örnek: My book = Benim kitabım"),
    ("Ders 9: Çoğul Yapma",
     "İngilizce'de çoğul yapmak için -s veya -es eklenir.",
     "book → books | box → boxes | city → cities | child → children ⚠️ | man → men ⚠️ | woman → women ⚠️",
     "💡 -s, -ss, -sh, -ch, -x ile bitenler -es alır."),
    ("Ders 10: Soru Cümleleri",
     "İngilizce'de soru sormak için soru kelimesi kullanılır.",
     "What (ne) | Where (nerede) | When (ne zaman) | Who (kim) | Why (neden) | How (nasıl)",
     "Örnek: Where are you? = Neredesin?"),
    ("Ders 11: Olumsuz Cümleler",
     "Bir şeyi reddetmek için kullanılır.",
     "I am not | She is not | I do not work | She does not work",
     "💡 Kısaltma: is not = isn't | do not = don't | does not = doesn't"),
    ("Ders 12: There is / There are",
     "Bir şeyin var olduğunu söylemek için kullanılır.",
     "There is a book | There are books | Is there a book?",
     "💡 Tekil için 'There is', çoğul için 'There are'"),
    ("Ders 13: Can / Cannot",
     "'Can' yetenek ve izin için kullanılır.",
     "I can swim | She can drive | I cannot come | Can you help?",
     "⚠️ 'Can' ile fiil arasına 'to' gelmez."),
    ("Ders 14: Karşılaştırma",
     "İki şeyi karşılaştırmak için kullanılır.",
     "Big → bigger | Cheap → cheaper | Expensive → more expensive | Good → better ⚠️ | Bad → worse ⚠️",
     "Örnek: This is cheaper than that = Bu şundan daha ucuz."),
    ("Ders 15: Yer Edatları",
     "Bir şeyin nerede olduğunu söylemek için kullanılır.",
     "In (içinde) | On (üstünde) | Under (altında) | Behind (arkasında) | Next to (yanında) | Between (arasında)",
     "Örnek: The book is on the table = Kitap masanın üstünde."),
    ("Ders 16: Zaman Edatları",
     "Zamanı belirtmek için kullanılır.",
     "AT + saat: at 5 o'clock | ON + gün: on Monday | IN + ay/yıl: in July, in 2026",
     "⚠️ Türkçe'de saat için 'de/da' eklenir, İngilizce'de 'at' kullanılır."),
    ("Ders 17: Sıklık Zarfları",
     "Bir eylemin ne sıklıkta yapıldığını gösterir.",
     "Always (%100) | Usually (%90) | Often (%70) | Sometimes (%50) | Rarely (%10) | Never (%0)",
     "Örnek: I usually walk to work = Genellikle işe yürürüm."),
    ("Ders 18: Sayılabilen ve Sayılamayan İsimler",
     "Bazı isimler sayılabilir, bazıları sayılamaz.",
     "Sayılabilen: apple, book, car → 'How many?' | Sayılamayan: water, bread, money → 'How much?'",
     "Örnek: How many books? = Kaç kitap? | How much water? = Ne kadar su?"),
    ("Ders 19: Much / Many / A lot of",
     "Miktar belirtmek için kullanılır.",
     "Many books | Much water | A lot of books | A few books | A little water",
     "⚠️ Olumsuz ve soru cümlelerinde 'much/many' kullanılır."),
    ("Ders 20: Modal Fiiller",
     "Tavsiye, zorunluluk, izin belirtmek için kullanılır.",
     "Should (-meli) | Must (-meli) | Have to (-mek zorunda) | Could (-ebilir) | Might (-ebilir)",
     "Örnek: You should rest = Dinlenmelisin. | I must go = Gitmeliyim."),
    ("Ders 21: Geçmiş Zaman Soruları",
     "Geçmişte olan olayları soru şeklinde sormak için 'did' kullanılır.",
     "Did you go? | Did she come? | Where did you go? | I didn't go",
     "⚠️ 'Did' ile fiil yalın kalır, -ed almaz."),
    ("Ders 22: Present Perfect",
     "Geçmişte başlayıp şu ana kadar devam eden olayları anlatır.",
     "I have worked | She has gone | Have you ever been? | I have never seen",
     "💡 'For' ve 'since' ile sık kullanılır."),
    ("Ders 23: If Cümleleri (1. Tip)",
     "Gerçekleşme olasılığı yüksek koşullar için kullanılır.",
     "If it rains, I will stay home | If you study, you will pass",
     "💡 'If' cümlesi başta veya sonda olabilir."),
    ("Ders 24: Edilgen Yapı (Passive)",
     "Eylemi yapan kişi önemli değilse kullanılır.",
     "The letter was sent | The house is being built | English is spoken here",
     "💡 Türkçe'de edilgen yapı '-ıl, -il' ekleriyle kurulur."),
    ("Ders 25: İlgi Cümleleri (Who, Which, That)",
     "İki cümleyi birleştirmek için kullanılır.",
     "The man who came | The book which I read | The car that I bought",
     "💡 Bu yapı Türkçe'deki '-en, -an' sıfat fiil eklerine benzer."),
    ("Ders 26: Bağlaçlar",
     "Cümleleri ve fikirleri birleştirmek için kullanılır.",
     "And (ve) | But (ama) | Or (veya) | Because (çünkü) | So (bu yüzden) | Although (-e rağmen) | However (ancak)",
     "Örnek: I like tea but I don't like coffee."),
    ("Ders 27: Dolaylı Anlatım",
     "Başkasının söylediğini aktarmak için kullanılır.",
     "'I am tired' → He said he was tired. | 'I will come' → She said she would come.",
     "💡 'Say' ve 'tell' farkı: Say + bir şey, Tell + birine"),
    ("Ders 28: Kısaltmalar ve Günlük Konuşma",
     "Günlük İngilizce'de çok kullanılan kısaltmalar.",
     "I'm = I am | You're = You are | He's = He is | Don't = Do not | Can't = Cannot | Won't = Will not",
     "⚠️ Kısaltmalar günlük konuşmada yaygın."),
    ("Ders 29: Yaygın Deyimler",
     "İngilizce'de sık kullanılan deyimler.",
     "Break the ice | Piece of cake | Hit the books | Under the weather | Once in a blue moon",
     "💡 Deyimler kelime kelime çevrilemez."),
    ("Ders 30: Genel Tekrar ve Sınav",
     "Tüm konuların özeti.",
     "To be | Zamanlar | Soru | Modal | Edatlar | Cümle yapısı",
     "🎯 Bu 30 ders sonunda A1-A2 seviyesine ulaşmış olacaksınız."),
]

# ============================================================
# BÖLÜM 4: BAĞLAM HİKAYELERİ (10 HİKAYE)
# ============================================================
BAGLAM_HIKAYELERI = [
    {
        "baslik": "Ofisteki İlk Gün",
        "hikaye": "Sarah: Hello! Are you the new employee?\nYusuf: Yes, I am. Nice to meet you.\nSarah: Nice to meet you too. Where are you from?\nYusuf: I'm from Turkey. I'm starting today.\nSarah: Welcome! Let's get started. I'll show you your desk.",
        "ceviri": "Sarah: Merhaba! Yeni çalışan sen misin?\nYusuf: Evet, benim. Tanıştığımıza memnun oldum.\nSarah: Ben de. Nerelisin?\nYusuf: Türkiye'denim. Bugün başlıyorum.\nSarah: Hoş geldin! Başlayalım. Masanı göstereceğim.",
        "kaliplar": ["Hello!", "Nice to meet you", "Where are you from?", "I'm from Turkey", "Let's get started"]
    },
    {
        "baslik": "Restoranda Akşam Yemeği",
        "hikaye": "Waiter: Good evening! A table for two?\nYusuf: Yes, please.\nWaiter: Here is the menu. What would you like to drink?\nYusuf: Could I have some water, please?\nWaiter: Of course. Are you ready to order?\nYusuf: Yes. What do you recommend?",
        "ceviri": "Garson: İyi akşamlar! İki kişilik masa?\nYusuf: Evet, lütfen.\nGarson: Menü burada. Ne içmek istersiniz?\nYusuf: Biraz su alabilir miyim?\nGarson: Elbette. Sipariş vermeye hazır mısınız?\nYusuf: Evet. Ne tavsiye edersiniz?",
        "kaliplar": ["Good evening!", "A table for two, please", "Could I have some water?", "What do you recommend?"]
    },
    {
        "baslik": "Havaalanında",
        "hikaye": "Yusuf: Excuse me, where is the check-in counter?\nStaff: It's over there, next to the coffee shop.\nYusuf: Thank you. What time is boarding?\nStaff: Boarding starts at 3 PM.\nYusuf: Great. Where is the bathroom?\nStaff: Just behind the security check.",
        "ceviri": "Yusuf: Affedersiniz, check-in bankosu nerede?\nGörevli: Şurada, kahve dükkanının yanında.\nYusuf: Teşekkürler. Uçuş saati kaçta?\nGörevli: Saat 15:00'te başlıyor.\nYusuf: Harika. Tuvalet nerede?\nGörevli: Güvenlik kontrolünün hemen arkasında.",
        "kaliplar": ["Excuse me", "Where is the check-in counter?", "What time is...?", "Where is the bathroom?"]
    },
    {
        "baslik": "Mağazada Alışveriş",
        "hikaye": "Yusuf: Excuse me, how much is this shirt?\nStaff: It's 50 dollars.\nYusuf: Do you have this in a different size?\nStaff: Yes, what size do you need?\nYusuf: Medium, please. Can I try it on?\nStaff: Of course. The fitting room is over there.",
        "ceviri": "Yusuf: Affedersiniz, bu gömlek ne kadar?\nGörevli: 50 dolar.\nYusuf: Farklı bedeni var mı?\nGörevli: Evet, hangi beden lazım?\nYusuf: Medium, lütfen. Deneyebilir miyim?\nGörevli: Elbette. Deneme kabini şurada.",
        "kaliplar": ["How much is this?", "Do you have this in a different size?", "Can I try it on?", "Of course"]
    },
    {
        "baslik": "İş Toplantısı",
        "hikaye": "Manager: Let's get started. Could you give me an update?\nYusuf: Yes. The project is going well, but we're running behind schedule.\nManager: What's the deadline?\nYusuf: Next Friday. I'll send you the details.\nManager: That makes sense. Let's schedule a meeting.",
        "ceviri": "Yönetici: Başlayalım. Güncel durumu aktarır mısın?\nYusuf: Evet. Proje iyi gidiyor ama programın gerisindeyiz.\nYönetici: Son tarih ne zaman?\nYusuf: Önümüzdeki Cuma. Detayları göndereceğim.\nYönetici: Mantıklı. Bir toplantı planlayalım.",
        "kaliplar": ["Let's get started", "Could you give me an update?", "What's the deadline?", "That makes sense"]
    },
    {
        "baslik": "Arkadaşla Buluşma",
        "hikaye": "Sarah: Hey! How's it going?\nYusuf: Not much, just working. How was your weekend?\nSarah: It was great! Do you want to hang out tonight?\nYusuf: I'd love to! What time?\nSarah: Let's go out at 7.\nYusuf: Sounds like a plan!",
        "ceviri": "Sarah: Hey! Nasıl gidiyor?\nYusuf: Pek bir şey yok, çalışıyorum. Hafta sonun nasıldı?\nSarah: Harikaydı! Bu akşam takılmak ister misin?\nYusuf: Çok isterim! Saat kaçta?\nSarah: 7'de çıkalım.\nYusuf: Plan gibi görünüyor!",
        "kaliplar": ["How's it going?", "Not much", "Do you want to hang out?", "I'd love to", "Sounds like a plan"]
    },
    {
        "baslik": "Otelde Check-in",
        "hikaye": "Yusuf: Hello, I have a reservation under the name Smith.\nStaff: Welcome! Yes, I see it. Two nights, correct?\nYusuf: Yes. Is breakfast included?\nStaff: Yes, breakfast is from 7 to 10.\nYusuf: Great. What time is check-out?\nStaff: Check-out is at 11 AM.",
        "ceviri": "Yusuf: Merhaba, Smith adına rezervasyonum var.\nGörevli: Hoş geldiniz! Evet, görüyorum. İki gece, doğru mu?\nYusuf: Evet. Kahvaltı dahil mi?\nGörevli: Evet, kahvaltı 7'den 10'a kadar.\nYusuf: Harika. Çıkış saati kaçta?\nGörevli: Çıkış 11:00'de.",
        "kaliplar": ["I have a reservation", "Is breakfast included?", "What time is check-out?", "Welcome!"]
    },
    {
        "baslik": "Telefon Görüşmesi",
        "hikaye": "Yusuf: Hello, may I speak to Mr. Smith?\nSecretary: Could you hold on a moment, please?\nYusuf: Of course.\nSecretary: I'm sorry, he's in a meeting. May I take a message?\nYusuf: Yes, please tell him Yusuf called.\nSecretary: I'll transfer you to his voicemail.",
        "ceviri": "Yusuf: Merhaba, Bay Smith ile görüşebilir miyim?\nSekreter: Bir dakika bekler misiniz?\nYusuf: Elbette.\nSekreter: Üzgünüm, toplantıda. Mesaj alabilir miyim?\nYusuf: Evet, lütfen Yusuf aradı deyin.\nSekreter: Sizi sesli mesaja yönlendireceğim.",
        "kaliplar": ["May I speak to...?", "Could you hold on a moment?", "May I take a message?", "I'll transfer you"]
    },
    {
        "baslik": "Sunum Yapma",
        "hikaye": "Yusuf: Good morning, everyone. Thank you for your attention.\nLet's move on to the next point. As you can see from the chart, sales increased by 10%.\nThere was a slight decrease in profit, but we need to cut costs.\nAny questions?",
        "ceviri": "Yusuf: Günaydın millet. İlginiz için teşekkürler.\nBir sonraki konuya geçelim. Grafikten görebileceğiniz gibi satışlar %10 arttı.\nKârda hafif bir düşüş oldu ama maliyetleri düşürmeliyiz.\nSoru var mı?",
        "kaliplar": ["Thank you for your attention", "Let's move on", "As you can see from the chart", "Any questions?"]
    },
    {
        "baslik": "Yardım İsteme",
        "hikaye": "Yusuf: Excuse me, could you help me?\nStranger: Of course. What's the problem?\nYusuf: I'm lost. Can you help me find the station?\nStranger: Sure. Go straight, then turn left.\nYusuf: Thank you so much!\nStranger: No problem. Have a nice day!",
        "ceviri": "Yusuf: Affedersiniz, yardım eder misiniz?\nYabancı: Elbette. Sorun nedir?\nYusuf: Kayboldum. İstasyonu bulmama yardım eder misiniz?\nYabancı: Tabii. Düz gidin, sonra sola dönün.\nYusuf: Çok teşekkürler!\nYabancı: Sorun değil. İyi günler!",
        "kaliplar": ["Could you help me?", "I'm lost", "Go straight, then turn left", "No problem", "Have a nice day"]
    },
]

# ============================================================
# BÖLÜM 5: ÇOKLU ALIŞTIRMA TİPLERİ
# ============================================================
ALISTIRMALAR = [
    {
        "tip": "boşluk_doldurma",
        "sorular": [
            ("I ___ a teacher.", "am", "To be fiili - I için"),
            ("She ___ (work) here.", "works", "He/She/It + fiil+s"),
            ("They ___ (play) football now.", "are playing", "Şimdiki zaman"),
            ("___ there any milk?", "Is", "There is/are"),
            ("I ___ (go) to school every day.", "go", "Geniş zaman"),
        ]
    },
    {
        "tip": "doğru_yanlış",
        "sorular": [
            ("'I am a doctor' cümlesi doğru mu?", "Doğru", "To be doğru kullanılmış"),
            ("'She work here' cümlesi doğru mu?", "Yanlış", "She works olmalı"),
            ("'They is happy' cümlesi doğru mu?", "Yanlış", "They are happy olmalı"),
            ("'I don't like coffee' cümlesi doğru mu?", "Doğru", "Olumsuz yapı doğru"),
            ("'Where you are from?' cümlesi doğru mu?", "Yanlış", "Where are you from? olmalı"),
        ]
    },
    {
        "tip": "eşleştirme",
        "sorular": [
            ("Hello", "Merhaba", "Selamlaşma"),
            ("Thank you", "Teşekkür ederim", "Nezaket"),
            ("Excuse me", "Affedersiniz", "Nezaket"),
            ("Good night", "İyi geceler", "Vedalaşma"),
            ("See you later", "Sonra görüşürüz", "Vedalaşma"),
        ]
    },
    {
        "tip": "çeviri",
        "sorular": [
            ("Ben bir öğretmenim.", "I am a teacher.", "To be"),
            ("Dün çalıştım.", "I worked yesterday.", "Geçmiş zaman"),
            ("Yarın geleceğim.", "I will come tomorrow.", "Gelecek zaman"),
            ("İki kitabım var.", "I have two books.", "Çoğul"),
            ("Nerede yaşıyorsun?", "Where do you live?", "Soru"),
        ]
    },
]

# ============================================================
# FONKSİYONLAR
# ============================================================
def gunun_telaffuz_dersi():
    gun = datetime.now().timetuple().tm_yday
    return TELAFFUZ_DERSLERI[gun % len(TELAFFUZ_DERSLERI)]

def gunun_kaliplari():
    gun = datetime.now().timetuple().tm_yday
    baslangic = (gun * 15) % len(KALIP_DERSLERI)
    return KALIP_DERSLERI[baslangic:baslangic + 15]

def gunun_gramer_dersi():
    gun = datetime.now().timetuple().tm_yday
    return GRAMER_DERSLERI[gun % len(GRAMER_DERSLERI)]

def gunun_alistirmasi():
    gun = datetime.now().timetuple().tm_yday
    return ALISTIRMALAR[gun % len(ALISTIRMALAR)]

def gunun_hikayesi():
    gun = datetime.now().timetuple().tm_yday
    return BAGLAM_HIKAYELERI[gun % len(BAGLAM_HIKAYELERI)]

def haftalik_ozet(state):
    """Pazar günü özel özet."""
    total = state.get("total_lessons", 0)
    streak = state.get("streak", 0)
    correct = state.get("total_correct", 0)
    wrong = state.get("total_wrong", 0)
    
    return {
        "toplam_ders": total,
        "streak": streak,
        "doğru": correct,
        "yanlış": wrong,
        "başarı_oranı": round(correct / (correct + wrong) * 100, 1) if (correct + wrong) > 0 else 0
    }

def e_posta_gonder():
    tarih = datetime.now().strftime('%d.%m.%Y %A')
    gun_no = datetime.now().weekday()  # 0=Pazartesi, 6=Pazar
    
    # State yükle/güncelle
    state = load_state()
    state = update_streak(state)
    
    telaffuz = gunun_telaffuz_dersi()
    kaliplar = gunun_kaliplari()
    gramer = gunun_gramer_dersi()
    alistirma = gunun_alistirmasi()
    hikaye = gunun_hikayesi()
    
    streak_msg = get_streak_message(state["streak"])
    
    # ====== HEADER ======
    header_html = f'''
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 25px; border-radius: 12px; text-align: center;">
        <h1 style="margin: 0; font-size: 26px;">🎓 GÜNLÜK İNGİLİZCE DERSİ</h1>
        <p style="margin: 8px 0 0 0; font-size: 14px;">{tarih}</p>
        <div style="background: rgba(255,255,255,0.15); border-radius: 20px; padding: 8px 20px; display: inline-block; margin-top: 10px;">
            <strong>{streak_msg}</strong>
        </div>
        <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 12px;">
        📊 Toplam Ders: {state["total_lessons"]} · Bu Ders: 15 dk</p>
    </div>'''
    
    # ====== TELAFFUZ ======
    telaffuz_html = f'''
    <div style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: white; padding: 20px; border-radius: 12px; margin-top: 20px;">
        <h2 style="margin: 0;">🗣️ 1. TELAFFUZ DERSİ (4 dakika)</h2>
        <h3 style="margin: 8px 0; color: #fff;">{telaffuz["baslik"]}</h3>
    </div>
    <div style="background: #fdedec; padding: 15px; border-left: 5px solid #e74c3c; margin: 10px 0;">
        <p><strong>📖 Kural:</strong> {telaffuz["kural"]}</p>
    </div>
    <div style="background: #fff9e6; padding: 15px; border-left: 5px solid #f39c12; margin: 10px 0;">
        <p><strong>📋 Detay:</strong></p>
        <p style="white-space: pre-line;">{telaffuz["detay"]}</p>
    </div>
    <div style="background: #e8f8f5; padding: 15px; border-left: 5px solid #27ae60; margin: 10px 0;">
        <p><strong>🎯 Örnekler:</strong></p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
        <tr style="background: #27ae60; color: white;">
            <th style="padding: 8px;">Kelime</th>
            <th style="padding: 8px;">Okunuş</th>
            <th style="padding: 8px;">Anlam</th>
        </tr>'''
    for kelime, okunus, anlam in telaffuz["ornekler"]:
        telaffuz_html += f'<tr style="background: white;"><td style="padding: 6px; border: 1px solid #ddd;"><strong>{kelime}</strong></td><td style="padding: 6px; border: 1px solid #ddd; color: #e74c3c;">{okunus}</td><td style="padding: 6px; border: 1px solid #ddd;">{anlam}</td></tr>'
    telaffuz_html += f'''</table>
    </div>
    <div style="background: #d4edda; padding: 15px; border-left: 5px solid #28a745; margin: 10px 0;">
        <p><strong>💡 Pratik İpucu:</strong> {telaffuz["ipucu"]}</p>
    </div>
    <div style="background: #e7f3ff; padding: 15px; border-left: 5px solid #3498db; margin: 10px 0;">
        <p><strong>🎤 SESLİ PRATİK:</strong> Yukarıdaki 8 kelimeyi 3 kez SESLİ okuyun. 
        Telefonunuzun ses kayıt uygulamasını açın, kendinizi kaydedin ve dinleyin. 
        Kendi sesinizi duymak, telaffuzunuzu düzeltmenin en hızlı yoludur.</p>
    </div>'''
    
    # ====== KALIPLAR ======
    kalip_html = '''
    <div style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: white; padding: 20px; border-radius: 12px; margin-top: 20px;">
        <h2 style="margin: 0;">📖 2. KALIP DERSİ (5 dakika)</h2>
        <p style="margin: 8px 0 0 0;">Bugünün 15 kalıbı — sesli okuyun</p>
    </div>
    <table style="width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 10px;">
    <tr style="background: #2c3e50; color: white;">
        <th style="padding: 8px;">Kategori</th>
        <th style="padding: 8px;">İngilizce</th>
        <th style="padding: 8px;">Türkçe Okunuş</th>
        <th style="padding: 8px;">Anlam</th>
        <th style="padding: 8px;">Örnek</th>
    </tr>'''
    for i, (kategori, ing, okunus, anlam, ornek) in enumerate(kaliplar):
        bg = "#f8f9fa" if i % 2 == 0 else "white"
        kalip_html += f'''<tr style="background: {bg};">
        <td style="padding: 6px; border: 1px solid #ecf0f1; font-size: 10px;">{kategori}</td>
        <td style="padding: 6px; border: 1px solid #ecf0f1;"><strong>{ing}</strong></td>
        <td style="padding: 6px; border: 1px solid #ecf0f1; color: #27ae60;">{okunus}</td>
        <td style="padding: 6px; border: 1px solid #ecf0f1;">{anlam}</td>
        <td style="padding: 6px; border: 1px solid #ecf0f1; font-style: italic;">{ornek}</td>
        </tr>'''
    kalip_html += '</table>'
    
    # ====== BAĞLAM HİKAYESİ ======
    hikaye_html = f'''
    <div style="background: linear-gradient(135deg, #f39c12 0%, #d35400 100%); color: white; padding: 20px; border-radius: 12px; margin-top: 20px;">
        <h2 style="margin: 0;">📚 3. BAĞLAM HİKAYESİ (3 dakika)</h2>
        <h3 style="margin: 8px 0; color: #fff;">{hikaye["baslik"]}</h3>
    </div>
    <div style="background: #fef5e7; padding: 15px; border-left: 5px solid #f39c12; margin: 10px 0;">
        <p><strong>📖 Hikaye (İngilizce):</strong></p>
        <p style="white-space: pre-line; font-size: 14px; line-height: 1.7;">{hikaye["hikaye"]}</p>
    </div>
    <div style="background: #e8f8f5; padding: 15px; border-left: 5px solid #27ae60; margin: 10px 0;">
        <p><strong>🇹🇷 Türkçe Çeviri:</strong></p>
        <p style="white-space: pre-line; font-size: 13px; color: #555;">{hikaye["ceviri"]}</p>
    </div>
    <div style="background: #fff9e6; padding: 15px; border-left: 5px solid #f1c40f; margin: 10px 0;">
        <p><strong>🎯 Bu Hikayedeki Kalıplar:</strong></p>
        <ul>'''
    for kal in hikaye["kaliplar"]:
        hikaye_html += f'<li>{kal}</li>'
    hikaye_html += '</ul></div>'
    
    # ====== GRAMER ======
    gramer_html = f'''
    <div style="background: linear-gradient(135deg, #27ae60 0%, #16a085 100%); color: white; padding: 20px; border-radius: 12px; margin-top: 20px;">
        <h2 style="margin: 0;">📝 4. GRAMER DERSİ (3 dakika)</h2>
        <h3 style="margin: 8px 0; color: #fff;">{gramer[0]}</h3>
    </div>
    <div style="background: #e8f8f5; padding: 15px; border-left: 5px solid #27ae60; margin: 10px 0;">
        <p><strong>📖 Açıklama:</strong> {gramer[1]}</p>
    </div>
    <div style="background: #fff9e6; padding: 15px; border-left: 5px solid #f39c12; margin: 10px 0;">
        <p><strong>📋 Kural:</strong></p>
        <p style="white-space: pre-line;">{gramer[2]}</p>
    </div>
    <div style="background: #d4edda; padding: 15px; border-left: 5px solid #28a745; margin: 10px 0;">
        <p><strong>💡 Örnek:</strong> {gramer[3]}</p>
    </div>'''
    
    # ====== ALIŞTIRMA ======
    tip_isimleri = {
        "boşluk_doldurma": "Boşluk Doldurma",
        "doğru_yanlış": "Doğru / Yanlış",
        "eşleştirme": "Eşleştirme",
        "çeviri": "Çeviri"
    }
    alistirma_html = f'''
    <div style="background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); color: white; padding: 20px; border-radius: 12px; margin-top: 20px;">
        <h2 style="margin: 0;">🎯 5. MİNİ ALIŞTIRMA (2 dakika)</h2>
        <p style="margin: 8px 0 0 0;">Tip: {tip_isimleri.get(alistirma["tip"], alistirma["tip"])}</p>
    </div>
    <div style="background: #f5eef8; padding: 15px; border-left: 5px solid #9b59b6; margin: 10px 0;">'''
    
    for i, soru in enumerate(alistirma["sorular"], 1):
        alistirma_html += f'<p style="margin: 8px 0;"><strong>{i}.</strong> {soru[0]}</p>'
    
    alistirma_html += '<hr style="margin: 15px 0;"><p><strong>✅ Cevaplar:</strong></p>'
    for i, soru in enumerate(alistirma["sorular"], 1):
        if len(soru) >= 3:
            alistirma_html += f'<p style="margin: 5px 0;"><strong>{i}.</strong> {soru[1]} <em style="color: #7f8c8d;">({soru[2]})</em></p>'
        else:
            alistirma_html += f'<p style="margin: 5px 0;"><strong>{i}.</strong> {soru[1]}</p>'
    alistirma_html += '</div>'
    
    # ====== HAFTALIK ÖZET (Pazar günü) ======
    haftalik_html = ""
    if gun_no == 6:  # Pazar
        ozet = haftalik_ozet(state)
        haftalik_html = f'''
        <div style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: white; padding: 25px; border-radius: 12px; margin-top: 20px;">
            <h2 style="margin: 0;">📅 HAFTALIK DEĞERLENDİRME</h2>
            <p style="margin: 8px 0 0 0;">Bu haftanın özeti</p>
        </div>
        <div style="background: #fdedec; padding: 20px; border-left: 5px solid #e74c3c; margin: 10px 0;">
            <table style="width: 100%; font-size: 14px;">
            <tr><td><strong>🔥 Seri:</strong></td><td>{ozet["streak"]} gün</td></tr>
            <tr><td><strong>📚 Toplam Ders:</strong></td><td>{ozet["toplam_ders"]} ders</td></tr>
            <tr><td><strong>✅ Doğru Cevap:</strong></td><td>{ozet["doğru"]}</td></tr>
            <tr><td><strong>❌ Yanlış Cevap:</strong></td><td>{ozet["yanlış"]}</td></tr>
            <tr><td><strong>🎯 Başarı Oranı:</strong></td><td>%{ozet["başarı_oranı"]}</td></tr>
            </table>
            <p style="margin-top: 15px;"><strong>🎯 Gelecek Hafta Hedefi:</strong> 
            Her gün derse devam et, telaffuz pratiğini ihmal etme, yeni kalıpları sesli tekrarla.</p>
        </div>'''
    
    # ====== ANA HTML ======
    html_body = f'''
    <html><body style="font-family: Arial, sans-serif; max-width: 1000px; margin: auto; background: #ecf0f1; padding: 15px;">
    
    {header_html}
    
    <div style="background: white; padding: 20px; margin-top: 15px; border-radius: 12px;">
    {telaffuz_html}
    </div>
    
    <div style="background: white; padding: 20px; margin-top: 15px; border-radius: 12px;">
    {kalip_html}
    </div>
    
    <div style="background: white; padding: 20px; margin-top: 15px; border-radius: 12px;">
    {hikaye_html}
    </div>
    
    <div style="background: white; padding: 20px; margin-top: 15px; border-radius: 12px;">
    {gramer_html}
    </div>
    
    <div style="background: white; padding: 20px; margin-top: 15px; border-radius: 12px;">
    {alistirma_html}
    </div>
    
    {haftalik_html}
    
    <div style="background: #34495e; color: white; padding: 20px; margin-top: 15px; border-radius: 12px; font-size: 12px;">
    <strong style="font-size: 14px;">📌 NASIL ÇALIŞMALISINIZ? (15 dakika)</strong><br><br>
    <strong>1️⃣ Telaffuz (4 dk):</strong> Dersi SESLİ okuyun. 8 kelimeyi 3 kez tekrarlayın.<br>
    <strong>2️⃣ Kalıplar (5 dk):</strong> 15 kalıbı SESLİ okuyun. Her kalıba kendi cümlenizi ekleyin.<br>
    <strong>3️⃣ Hikaye (3 dk):</strong> Hikayeyi okuyun, anlamadığınız kelimeleri işaretleyin.<br>
    <strong>4️⃣ Gramer (3 dk):</strong> Kuralı okuyun. 3 örnek cümle kurun.<br>
    <strong>5️⃣ Alıştırma (2 dk):</strong> Soruları cevaplayın, sonra cevaplara bakın.<br>
    <br>
    <strong>💡 İPUCU:</strong> Her gün aynı saatte çalışın. Kahvaltıda, işe giderken veya akşam yatmadan önce. 
    Düzenlilik, süreden daha önemli. 15 dakika × 30 gün = Akıcı konuşma!
    </div>
    </body></html>
    '''
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🎓 İngilizce Dersi #{state['total_lessons']} - {datetime.now().strftime('%d.%m.%Y')}"
    msg['From'] = MAIL_USER
    msg['To'] = MAIL_TO
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(MAIL_USER, MAIL_PASS)
            server.sendmail(MAIL_USER, MAIL_TO, msg.as_string())
        print(f"✅ E-posta gönderildi. Ders #{state['total_lessons']}, Streak: {state['streak']}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    # State'i kaydet
    save_state(state)

if __name__ == "__main__":
    print("İngilizce dersi hazırlanıyor...")
    e_posta_gonder()
