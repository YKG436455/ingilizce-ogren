# -*- coding: utf-8 -*-
"""
Günlük İngilizce Öğrenme Bülteni
Aralıklı tekrar (1-3-7-14-30) + 15 kalıp + telaffuz + gramer + alıştırma
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ============================================================
# AYARLAR
# ============================================================
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")
MAIL_TO = os.environ.get("MAIL_TO")

# ============================================================
# KALIP HAVUZU (75 kalıp, 5 haftalık)
# ============================================================
KALIPLAR = [
    # Hafta 1: İş yerinde toplantı ve takip
    ("Let's get started.", "/lets ɡet ˈstɑːrtɪd/", "LETS get STAR-tıd", "Başlayalım.", "Let's get started with the agenda."),
    ("Could you give me an update?", "/kʊd juː ɡɪv miː æn ˈʌpdeɪt/", "kud yu giv mi ın AP-deyt", "Bana güncel durumu aktarır mısınız?", "Could you give me an update on the project?"),
    ("I'd like to follow up on...", "/aɪd laɪk tə ˈfɑːloʊ ʌp ɑːn/", "ayd layk tı FA-lou ap an", "...konusunu takip etmek istiyorum.", "I'd like to follow up on our last meeting."),
    ("Let me check and get back to you.", "/let miː tʃek ænd ɡet bæk tə juː/", "let mi ÇEK end get BEK tı yu", "Kontrol edip size döneyim.", "Let me check and get back to you tomorrow."),
    ("We're running behind schedule.", "/wɪr ˈrʌnɪŋ bɪˈhaɪnd ˈskedʒuːl/", "wir RA-ning bi-HAYND SKE-cul", "Programın gerisindeyiz.", "We're running behind schedule this week."),
    ("That makes sense.", "/ðæt meɪks sens/", "dhet MEYKS SENS", "Mantıklı / anlıyorum.", "That makes sense to me."),
    ("I see your point, but...", "/aɪ siː jʊr pɔɪnt bʌt/", "ay sii yur POYNT bat", "Ne dediğini anlıyorum ama...", "I see your point, but the cost is high."),
    ("Let's schedule a meeting.", "/lets ˈskedʒuːl ə ˈmiːtɪŋ/", "lets SKE-cul ı Mİİ-ting", "Bir toplantı planlayalım.", "Let's schedule a meeting for Monday."),
    ("What's the deadline?", "/wʌts ðə ˈdedlaɪn/", "wats dhı DED-layn", "Son tarih ne zaman?", "What's the deadline for this report?"),
    ("I'll send you the details.", "/aɪl send juː ðə ˈdiːteɪlz/", "ayl SEND yu dhı Dİİ-teylz", "Detayları size göndereceğim.", "I'll send you the details by email."),
    ("Sorry to keep you waiting.", "/ˈsɑːri tə kiːp juː ˈweɪtɪŋ/", "SA-ri tı KİİP yu WEY-ting", "Beklettiğim için özür dilerim.", "Sorry to keep you waiting."),
    ("How was your weekend?", "/haʊ wʌz jʊr ˈwiːkend/", "hau waz yur Wİİ-kend", "Hafta sonun nasıldı?", "Hi Sara, how was your weekend?"),
    ("I'm looking forward to it.", "/aɪm ˈlʊkɪŋ ˈfɔːrwərd tə ɪt/", "aym LU-king FOR-wırd tu it", "Dört gözle bekliyorum.", "I'm looking forward to the trip."),
    ("It depends on...", "/ɪt dɪˈpendz ɑːn/", "it di-PENDZ an", "...'e bağlı.", "It depends on the budget."),
    ("Do you mind if I...?", "/duː juː maɪnd ɪf aɪ/", "du yu MAYND if ay", "...sakıncası var mı?", "Do you mind if I open the window?"),
    # Hafta 2: İş e-postası ve telefon
    ("I'm writing to inquire about...", "/aɪm ˈraɪtɪŋ tə ɪnˈkwaɪr əˈbaʊt/", "aym RAY-ting tı in-KVAYR ı-BAUT", "...hakkında bilgi almak için yazıyorum.", "I'm writing to inquire about the position."),
    ("Please find attached...", "/pliːz faɪnd əˈtætʃt/", "pliiz FAYND ı-TEÇT", "Ekte bulabilirsiniz...", "Please find attached the report."),
    ("I look forward to hearing from you.", "/aɪ lʊk ˈfɔːrwərd tə ˈhɪrɪŋ frəm juː/", "ay luk FOR-wırd tı HİR-ing frım yu", "Sizden haber almayı bekliyorum.", "I look forward to hearing from you soon."),
    ("Could you please confirm...?", "/kʊd juː pliːz kənˈfɜːrm/", "kud yu pliiz kın-FIRM", "...onaylayabilir misiniz?", "Could you please confirm the meeting time?"),
    ("I apologize for the delay.", "/aɪ əˈpɑːlədʒaɪz fɔːr ðə dɪˈleɪ/", "ay ı-PO-lı-cayz for dhı di-LEY", "Gecikme için özür dilerim.", "I apologize for the delay in my response."),
    ("Thank you for your prompt reply.", "/θæŋk juː fɔːr jʊr prɑːmpt rɪˈplaɪ/", "thenk yu for yur PROMPT ri-PLAY", "Hızlı yanıtınız için teşekkürler.", "Thank you for your prompt reply."),
    ("I would appreciate it if...", "/aɪ wʊd əˈpriːʃieɪt ɪt ɪf/", "ay wud ı-PRİİ-şi-eyt it if", "...yaparsanız memnun olurum.", "I would appreciate it if you could send it today."),
    ("Please let me know if you have any questions.", "/pliːz let miː noʊ ɪf juː hæv ˈeni ˈkwestʃənz/", "pliiz let mi nou if yu hev ENi KYES-çınz", "Sorunuz olursa lütfen bana bildirin.", "Please let me know if you have any questions."),
    ("I'm calling regarding...", "/aɪm ˈkɔːlɪŋ rɪˈɡɑːrdɪŋ/", "aym KO-ling ri-GAR-ding", "...hakkında arıyorum.", "I'm calling regarding your order."),
    ("Could you hold on a moment, please?", "/kʊd juː hoʊld ɑːn ə ˈmoʊmənt pliːz/", "kud yu hould an ı MOU-mınt pliiz", "Bir dakika bekleyebilir misiniz?", "Could you hold on a moment, please?"),
    ("I'll transfer you to the right department.", "/aɪl trænsˈfɜːr juː tə ðə raɪt dɪˈpɑːrtmənt/", "ayl trans-FIR yu tı dhı RAYT di-PART-mınt", "Sizi doğru departmana yönlendireceğim.", "I'll transfer you to the right department."),
    ("May I take a message?", "/meɪ aɪ teɪk ə ˈmesɪdʒ/", "mey ay TEYK ı MES-ıc", "Mesaj alabilir miyim?", "May I take a message?"),
    ("I'm afraid I can't make it.", "/aɪm əˈfreɪd aɪ kænt meɪk ɪt/", "aym ı-FREYD ay kent MEYK it", "Maalesef gelemeyeceğim.", "I'm afraid I can't make it to the meeting."),
    ("Let's touch base next week.", "/lets tʌtʃ beɪs nekst wiːk/", "lets TAÇ BEYS nekst viik", "Gelecek hafta görüşelim.", "Let's touch base next week."),
    ("I'm on the same page.", "/aɪm ɑːn ðə seɪm peɪdʒ/", "aym an dhı SEYM PEYC", "Aynı fikirdeyim.", "I'm on the same page with you."),
    ("Could you elaborate on that?", "/kʊd juː ɪˈlæbəreɪt ɑːn ðæt/", "kud yu i-LA-bı-reyt an dhet", "Bunu biraz açar mısınız?", "Could you elaborate on that point?"),
    # Hafta 3: Seyahat ve günlük hayat
    ("Where is the check-in counter?", "/wer ɪz ðə ˈtʃekɪn ˈkaʊntər/", "ver iz dhı ÇEK-in KAUN-tır", "Check-in bankosu nerede?", "Excuse me, where is the check-in counter?"),
    ("I'd like to book a room.", "/aɪd laɪk tə bʊk ə ruːm/", "ayd layk tı BUK ı RUUM", "Bir oda ayırtmak istiyorum.", "I'd like to book a room for two nights."),
    ("What time is check-out?", "/wʌt taɪm ɪz ˈtʃekaʊt/", "vat taym iz ÇEK-aut", "Çıkış saati kaçta?", "What time is check-out?"),
    ("Is breakfast included?", "/ɪz ˈbrekfəst ɪnˈkluːdɪd/", "iz BREK-fıst in-KLUU-dıd", "Kahvaltı dahil mi?", "Is breakfast included in the price?"),
    ("Could you recommend a good restaurant?", "/kʊd juː ˌrekəˈmend ə ɡʊd ˈrestərɑːnt/", "kud yu re-kı-MEND ı gud RES-tı-rant", "İyi bir restoran önerebilir misiniz?", "Could you recommend a good restaurant nearby?"),
    ("How do I get to the city center?", "/haʊ duː aɪ ɡet tə ðə ˈsɪti ˈsentər/", "hau du ay get tı dhı Sİ-ti SEN-tır", "Şehir merkezine nasıl giderim?", "How do I get to the city center?"),
    ("I'm lost. Can you help me?", "/aɪm lɔːst kæn juː help miː/", "aym lost ken yu HELP mi", "Kayboldum. Yardım eder misiniz?", "I'm lost. Can you help me?"),
    ("How much does it cost?", "/haʊ mʌtʃ dʌz ɪt kɔːst/", "hau MAÇ daz it KOST", "Ne kadar?", "How much does it cost to go there?"),
    ("Can I pay by card?", "/kæn aɪ peɪ baɪ kɑːrd/", "ken ay PEY bay KARD", "Kartla ödeyebilir miyim?", "Can I pay by card?"),
    ("I'd like to return this, please.", "/aɪd laɪk tə rɪˈtɜːrn ðɪs pliːz/", "ayd layk tı ri-TIRN dhis pliiz", "Bunu iade etmek istiyorum.", "I'd like to return this, please."),
    ("Do you have this in a different size?", "/duː juː hæv ðɪs ɪn ə ˈdɪfrənt saɪz/", "du yu hev dhis in ı DİF-rınt SAYZ", "Bunun farklı bedeni var mı?", "Do you have this in a different size?"),
    ("I'm just looking, thanks.", "/aɪm dʒʌst ˈlʊkɪŋ θæŋks/", "aym cast LU-king THENKS", "Sadece bakıyorum, teşekkürler.", "I'm just looking, thanks."),
    ("Could you wrap it for me?", "/kʊd juː ræp ɪt fɔːr miː/", "kud yu REP it for mi", "Benim için paketler misiniz?", "Could you wrap it for me, please?"),
    ("What's the weather like today?", "/wʌts ðə ˈweðər laɪk təˈdeɪ/", "vats dhı VE-dhır layk tu-DEY", "Bugün hava nasıl?", "What's the weather like today?"),
    ("I have a reservation under the name...", "/aɪ hæv ə ˌrezərˈveɪʃn ˈʌndər ðə neɪm/", "ay hev ı re-zır-VEY-şın AN-dır dhı NEYM", "...adına rezervasyonum var.", "I have a reservation under the name Smith."),
    # Hafta 4: Restoran, alışveriş, sosyal
    ("A table for two, please.", "/ə ˈteɪbl fɔːr tuː pliːz/", "ı TEY-bıl for TU pliiz", "İki kişilik masa, lütfen.", "A table for two, please."),
    ("Could I see the menu?", "/kʊd aɪ siː ðə ˈmenjuː/", "kud ay sii dhı MEN-yu", "Menüyü görebilir miyim?", "Could I see the menu, please?"),
    ("What do you recommend?", "/wʌt duː juː ˌrekəˈmend/", "vat du yu re-kı-MEND", "Ne tavsiye edersiniz?", "What do you recommend as a starter?"),
    ("I'll have the same.", "/aɪl hæv ðə seɪm/", "ayl hev dhı SEYM", "Aynısını alayım.", "I'll have the same as him."),
    ("Could we get the bill, please?", "/kʊd wiː ɡet ðə bɪl pliːz/", "kud vi get dhı BİL pliiz", "Hesabı alabilir miyiz?", "Could we get the bill, please?"),
    ("Is service included?", "/ɪz ˈsɜːrvɪs ɪnˈkluːdɪd/", "iz SIR-vis in-KLUU-dıd", "Servis dahil mi?", "Is service included in the bill?"),
    ("I'm allergic to nuts.", "/aɪm əˈlɜːrdʒɪk tə nʌts/", "aym ı-LIR-cik tı NATS", "Kuruyemişe alerjim var.", "I'm allergic to nuts."),
    ("Could I have some water, please?", "/kʊd aɪ hæv sʌm ˈwɔːtər pliːz/", "kud ay hev sam VO-tır pliiz", "Biraz su alabilir miyim?", "Could I have some water, please?"),
    ("This is delicious!", "/ðɪs ɪz dɪˈlɪʃəs/", "dhis iz di-Lİ-şıs", "Bu çok lezzetli!", "This is delicious! Thank you."),
    ("I'm full, thank you.", "/aɪm fʊl θæŋk juː/", "aym FUL THENK yu", "Doydum, teşekkürler.", "I'm full, thank you."),
    ("Would you like to join us?", "/wʊd juː laɪk tə dʒɔɪn ʌs/", "vud yu layk tı COYN as", "Bize katılmak ister misiniz?", "Would you like to join us for dinner?"),
    ("That sounds great!", "/ðæt saʊndz ɡreɪt/", "dhet SAUNDZ GREYT", "Kulağa harika geliyor!", "That sounds great! I'd love to."),
    ("I'm sorry, I can't make it.", "/aɪm ˈsɑːri aɪ kænt meɪk ɪt/", "aym SA-ri ay kent MEYK it", "Üzgünüm, gelemem.", "I'm sorry, I can't make it this time."),
    ("Maybe next time.", "/ˈmeɪbi nekst taɪm/", "MEY-bi nekst TAYM", "Belki bir dahaki sefere.", "Maybe next time."),
    ("It was nice meeting you.", "/ɪt wʌz naɪs ˈmiːtɪŋ juː/", "it vaz NAYS Mİİ-ting yu", "Tanıştığımıza memnun oldum.", "It was nice meeting you."),
    # Hafta 5: Sunum, rakamlar, müzakere
    ("Let's move on to the next point.", "/lets muːv ɑːn tə ðə nekst pɔɪnt/", "lets MUUV an tı dhı NEKST POYNT", "Bir sonraki konuya geçelim.", "Let's move on to the next point."),
    ("As you can see from the chart...", "/æz juː kæn siː frəm ðə tʃɑːrt/", "ez yu ken Sİİ frım dhı ÇART", "Grafikten de görebileceğiniz gibi...", "As you can see from the chart, sales are up."),
    ("Sales increased by 10%.", "/seɪlz ɪnˈkriːst baɪ ten pərˈsent/", "seylz in-KRİİST bay ten pır-SENT", "Satışlar %10 arttı.", "Sales increased by 10% last quarter."),
    ("There was a slight decrease.", "/ðer wʌz ə slaɪt dɪˈkriːs/", "dher vaz ı SLAY T di-KRİİS", "Hafif bir düşüş oldu.", "There was a slight decrease in profit."),
    ("We need to cut costs.", "/wiː niːd tə kʌt kɔːsts/", "vi niid tı KAT KOSTS", "Maliyetleri düşürmeliyiz.", "We need to cut costs to stay competitive."),
    ("Let's find a middle ground.", "/lets faɪnd ə ˈmɪdl ɡraʊnd/", "lets FAYND ı Mİ-dıl GRAUND", "Orta bir yol bulalım.", "Let's find a middle ground on the price."),
    ("That's not acceptable.", "/ðæts nɑːt əkˈseptəbl/", "dhets nat ık-SEP-tı-bıl", "Bu kabul edilemez.", "That's not acceptable for us."),
    ("We can offer a discount.", "/wiː kæn ˈɔːfər ə ˈdɪskaʊnt/", "vi ken O-fır ı DİS-kaunt", "İndirim yapabiliriz.", "We can offer a 5% discount."),
    ("Let's agree on the terms.", "/lets əˈɡriː ɑːn ðə tɜːrmz/", "lets ı-GRİİ an dhı TIRMZ", "Şartlar üzerinde anlaşalım.", "Let's agree on the terms before signing."),
    ("I'll get back to you with a decision.", "/aɪl ɡet bæk tə juː wɪð ə dɪˈsɪʒn/", "ayl get BEK tı yu vidh ı di-SİJ-ın", "Kararla size döneceğim.", "I'll get back to you with a decision by Friday."),
    ("In my opinion...", "/ɪn maɪ əˈpɪnjən/", "in may ı-PİN-yın", "Bence...", "In my opinion, we should wait."),
    ("I agree with you.", "/aɪ əˈɡriː wɪð juː/", "ay ı-GRİİ vidh yu", "Sana katılıyorum.", "I agree with you on this point."),
    ("I'm not sure about that.", "/aɪm nɑːt ʃʊr əˈbaʊt ðæt/", "aym nat ŞUR ı-BAUT dhet", "Bundan emin değilim.", "I'm not sure about that."),
    ("Could you clarify that?", "/kʊd juː ˈklærəfaɪ ðæt/", "kud yu KLE-rı-fay dhet", "Bunu netleştirir misiniz?", "Could you clarify that point?"),
    ("Let's summarize the key points.", "/lets ˈsʌməraɪz ðə kiː pɔɪnts/", "lets SA-mı-rayz dhı Kİİ POYNTS", "Ana noktaları özetleyelim.", "Let's summarize the key points of the meeting."),
]

# ============================================================
# TELAFFUZ NOTLARI (8 zor ses)
# ============================================================
TELAFFUZ_NOTLARI = [
    ("th (sert)", "think, three, thank", "Dil ucunu üst ve alt dişler arasına koyun, hava üfleyin. Ses teli titremez.", "s veya t demeyin: 'sink', 'tink' değil."),
    ("th (yumuşak)", "this, that, the", "Aynı dil konumu, ama ses teli titrer.", "d veya z demeyin: 'dis', 'zat' değil."),
    ("w", "water, we, what", "Dudaklar yuvarlak, dişler dudağa değmez.", "v demeyin: 'vater' değil."),
    ("v", "very, voice, love", "Üst dişler alt dudağa değer.", "w ile karıştırmayın."),
    ("r", "red, right, around", "Dil ucu damağa değmez, hafif geriye kıvrılır.", "Türkçe r gibi yuvarlamayın."),
    ("ng", "sing, long, meeting", "Dilin arkası damağa değer; sonda ayrı bir 'g' duyulmaz.", "sin-g diye ayırmayın."),
    ("schwa /ə/", "about, teacher, banana", "Vurgusuz hecelerde çok kısa, gevşek 'ı' ile 'e' arası ses.", "Her harfi tam sesle okumayın: a-bavt değil."),
    ("Kısa ve uzun ünlüler", "ship / sheep, bit / beat", "Kısa ünlü daha kısa ve gevşek, uzun ünlü daha uzun ve gergin.", "İkisini de aynı okumayın."),
]

# ============================================================
# GRAMER KONULARI (8 haftalık plan)
# ============================================================
GRAMER_KONULARI = [
    ("Geniş ve şimdiki zaman", "I usually work from home, but today I'm working at the office.", "Sıklık zarfları: always, usually, often, sometimes, never."),
    ("Geçmiş zaman ve present perfect", "I met him in 2020. I've worked here for three years.", "have/has + V3 (past participle)."),
    ("Gelecek: will, going to", "I'll call you later. We're meeting at 3.", "will: ani karar, going to: planlanmış."),
    ("Modal fiiller", "You should send the report today.", "should: tavsiye, must: zorunluluk, could: rica, might: olasılık."),
    ("Karşılaştırma ve miktar", "This option is cheaper than that one.", "much/many, a few/a little, -er/-est."),
    ("Koşul cümleleri (if)", "If we reduce prices, sales will increase.", "1. tip: if + geniş zaman, will + fiil."),
    ("Edilgen yapı (passive)", "The report was sent yesterday.", "be + V3. Özne bilinmiyorsa veya önemli değilse."),
    ("İlgi cümleleri ve bağlaçlar", "The team that handled the project did well.", "who/which/that, although, however."),
]

# ============================================================
# GÜNLÜK ALIŞTIRMALAR (mini test)
# ============================================================
ALISTIRMALAR = [
    ("Kontrol edip size döneyim", "Let me check and get back to you.", "follow", "Let me ___ up on our last meeting."),
    ("Bana güncel durumu aktarır mısınız?", "Could you give me an update?", "following", "I'd like to follow up ___ our last meeting."),
    ("Bir toplantı planlayalım", "Let's schedule a meeting.", "schedule", "Let's ___ a meeting for Monday."),
    ("Detayları size göndereceğim", "I'll send you the details.", "send", "I'll ___ you the details by email."),
    ("Son tarih ne zaman?", "What's the deadline?", "deadline", "What's the ___ for this report?"),
    ("Dört gözle bekliyorum", "I'm looking forward to it.", "looking", "I'm ___ forward to the trip."),
    ("...'e bağlı", "It depends on...", "depends", "It ___ on the budget."),
    ("...sakıncası var mı?", "Do you mind if I...?", "mind", "Do you ___ if I open the window?"),
]

# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================
def gunun_kaliplari():
    """Her gün 15 kalıp seçer."""
    gun_sayisi = datetime.now().timetuple().tm_yday
    baslangic = (gun_sayisi * 15) % len(KALIPLAR)
    return KALIPLAR[baslangic:baslangic + 15]

def gunun_telaffuz():
    gun_sayisi = datetime.now().timetuple().tm_yday
    return TELAFFUZ_NOTLARI[gun_sayisi % len(TELAFFUZ_NOTLARI)]

def gunun_gramer():
    gun_sayisi = datetime.now().timetuple().tm_yday
    return GRAMER_KONULARI[gun_sayisi % len(GRAMER_KONULARI)]

def gunun_alistirma():
    gun_sayisi = datetime.now().timetuple().tm_yday
    return ALISTIRMALAR[gun_sayisi % len(ALISTIRMALAR)]

def tekrar_kaliplari():
    """Aralıklı tekrar için önceki günlerden kalıplar."""
    gun_sayisi = datetime.now().timetuple().tm_yday
    tekrar_gunleri = [1, 3, 7, 14, 30]
    tekrarlar = []
    for gun in tekrar_gunleri:
        if gun_sayisi - gun > 0:
            baslangic = ((gun_sayisi - gun) * 15) % len(KALIPLAR)
            tekrarlar.extend(KALIPLAR[baslangic:baslangic + 2])
    return tekrarlar[:10]

# ============================================================
# E-POSTA GÖNDER
# ============================================================
def e_posta_gonder():
    tarih = datetime.now().strftime('%d.%m.%Y %A')
    kaliplar = gunun_kaliplari()
    telaffuz = gunun_telaffuz()
    gramer = gunun_gramer()
    alistirma = gunun_alistirma()
    tekrarlar = tekrar_kaliplari()
    
    # Kalıp tablosu
    kalip_html = '<h3 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px;">📖 Günün 15 Kalıbı</h3>'
    kalip_html += '<table style="border-collapse: collapse; width: 100%; font-size: 12px;">'
    kalip_html += '<tr style="background-color: #34495e; color: white;"><th style="padding: 6px;">Kalıp</th><th style="padding: 6px;">IPA</th><th style="padding: 6px;">Türkçe Okunuş</th><th style="padding: 6px;">Anlam</th><th style="padding: 6px;">Örnek</th></tr>'
    for i, (ing, ipa, okunus, anlam, ornek) in enumerate(kaliplar):
        bg = "#f8f9fa" if i % 2 == 0 else "white"
        kalip_html += f'<tr style="background-color: {bg};"><td style="padding: 5px; border: 1px solid #ecf0f1;"><strong>{ing}</strong></td><td style="padding: 5px; border: 1px solid #ecf0f1; color: #e67e22; font-size: 11px;">{ipa}</td><td style="padding: 5px; border: 1px solid #ecf0f1; color: #27ae60;">{okunus}</td><td style="padding: 5px; border: 1px solid #ecf0f1;">{anlam}</td><td style="padding: 5px; border: 1px solid #ecf0f1; font-style: italic;">{ornek}</td></tr>'
    kalip_html += '</table>'
    
    # Tekrar
    tekrar_html = '<h3 style="color: #2c3e50; border-bottom: 2px solid #e67e22; padding-bottom: 5px;">🔄 Tekrar (1-3-7-14-30 kuralı)</h3>'
    if tekrarlar:
        tekrar_html += '<ul>'
        for ing, ipa, okunus, anlam, ornek in tekrarlar:
            tekrar_html += f'<li style="padding: 3px; background: #fdf2e9; margin: 2px 0; border-radius: 4px;"><strong>{ing}</strong> → {anlam}</li>'
        tekrar_html += '</ul>'
    else:
        tekrar_html += '<p><em>Bugün tekrar edilecek kalıp yok.</em></p>'
    
    # Telaffuz
    telaffuz_html = f'<h3 style="color: #2c3e50; border-bottom: 2px solid #e74c3c; padding-bottom: 5px;">🗣️ Telaffuz: {telaffuz[0]}</h3>'
    telaffuz_html += f'<p style="background: #fdedec; padding: 10px; border-left: 4px solid #e74c3c; border-radius: 4px;"><strong>Örnek:</strong> {telaffuz[1]}<br><strong>Nasıl:</strong> {telaffuz[2]}<br><strong>Hata:</strong> {telaffuz[3]}</p>'
    
    # Gramer
    gramer_html = f'<h3 style="color: #2c3e50; border-bottom: 2px solid #27ae60; padding-bottom: 5px;">📝 Gramer: {gramer[0]}</h3>'
    gramer_html += f'<p style="background: #e8f8f5; padding: 10px; border-left: 4px solid #27ae60; border-radius: 4px;"><strong>Örnek:</strong> {gramer[1]}<br><strong>Kural:</strong> {gramer[2]}</p>'
    
    # Alıştırma
    alistirma_html = f'<h3 style="color: #2c3e50; border-bottom: 2px solid #9b59b6; padding-bottom: 5px;">🎯 Mini Alıştırma</h3>'
    alistirma_html += f'<p style="background: #f5eef8; padding: 10px; border-left: 4px solid #9b59b6; border-radius: 4px;"><strong>1.</strong> "{alistirma[0]}" cümlesini İngilizce söyle.<br><strong>2.</strong> Boşluğu doldur: {alistirma[3]}<br><strong>3.</strong> Kendi cümleni kur ve sesli söyle.</p>'
    
    html_body = f'''
    <html><body style="font-family: Arial, sans-serif; max-width: 950px; margin: auto; background-color: #ecf0f1; padding: 20px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 12px;">
        <h1 style="margin: 0;">📚 Günlük İngilizce Bülteni</h1>
        <p style="margin: 8px 0 0 0;">{tarih}</p>
        <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 12px;">15 kalıp · 1 telaffuz · 1 gramer · 1 alıştırma · 10 tekrar</p>
    </div>
    <div style="background: white; padding: 20px; margin-top: 15px; border-radius: 12px;">
    {kalip_html}
    </div>
    <div style="background: white; padding: 20px; margin-top: 15px; border-radius: 12px;">
    {tekrar_html}
    {telaffuz_html}
    {gramer_html}
    {alistirma_html}
    </div>
    <div style="background: #34495e; color: white; padding: 12px; margin-top: 15px; border-radius: 12px; font-size: 11px; text-align: center;">
    Bu bülten otomatik oluşturulmuştur. Aralıklı tekrar: 1-3-7-14-30 gün.<br>
    Her gün 15 dakika: 4 dk yeni + 4 dk tekrar + 4 dk konuşma + 3 dk gramer.
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
