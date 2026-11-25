# Generate the six-language site (fr at root, zh/en/es/ru/ar in subfolders)
# Usage (from aha-website/):  python3 -I build/generate.py            -> site/
#                             python3 -I build/generate.py --preview DIR -> artifact preview
import sys, os, json, html
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
from content import LANGS, NAMES, HTML_LANG, MACHINE, T
import fonts as fontsmod

BASE='https://harmonie-amitie.com/'
SHORT={'fr':'FR','zh':'中文','en':'EN','es':'ES','ru':'RU','ar':'عربي'}
PARTNERS=['IFAC du Pays de Montbéliard','Association Paris Pont Alexandre III',
          "Comité d'animation culturelle Paris 1",'Ordre de Malte France',
          'Association Internationale La Voix de la Compassion',
          "Association internationale d'échanges culturels"]
# subline of the 6th partner (A.I.E.C., RNA W751211126)
D6={'fr':"A.I.E.C. · partenaire stratégique · organisation des concerts 2024 et 2025",
    'zh':"A.I.E.C. · 长期战略合作伙伴 · 2024、2025 年音乐会承办方",
    'en':"A.I.E.C. · strategic partner · organiser of the 2024 and 2025 concerts",
    'es':"A.I.E.C. · socio estratégico · organización de los conciertos de 2024 y 2025",
    'ru':"A.I.E.C. · стратегический партнёр · организация концертов 2024 и 2025 годов",
    'ar':"\u2066A.I.E.C.\u2069 · شريك استراتيجي · تنظيم حفلَي 2024 و2025"}
# past news: (datetime, label, content key)
NEWS=[('2025-05-25',{'zh':'2025 年 5 月 25 日','fr':'25 mai 2025','en':'25 May 2025','es':'25 de mayo de 2025','ru':'25 мая 2025 г.','ar':'25 مايو 2025'},'n3'),
      ('2024-11-25',{'zh':'2024 年 11 月 25 日','fr':'25 novembre 2024','en':'25 November 2024','es':'25 de noviembre de 2024','ru':'25 ноября 2024 г.','ar':'25 نوفمبر 2024'},'n4')]
# footer hint for readers who need larger text (wording confirmed by the Présidente, 2026-11-25)
ZOOM={'zh':'如需放大文字，请使用手机或浏览器的缩放功能。','fr':'Pour agrandir le texte, utilisez le zoom de votre téléphone ou de votre navigateur.',
      'en':"To enlarge the text, use your phone's or browser's zoom.",'es':'Para ampliar el texto, use el zoom de su teléfono o de su navegador.',
      'ru':'Чтобы увеличить текст, используйте масштабирование на телефоне или в браузере.','ar':'لتكبير النص، استخدموا خاصية التكبير في الهاتف أو المتصفح.'}
# cooperations under discussion (no names of individuals, no third-party logos; modest wording)
ONGOING={
 'fr':[("En préparation","Collecte d'hiver 2026 : des donateurs en Chine offrent 500 paires de chaussettes et 24 plaids-capes au Fleuron Saint-Jean, péniche d'accueil de l'Ordre de Malte France pour les personnes sans abri, à Paris. L'A.H.A. organise l'acheminement.")],
 'zh':[("筹备中","2026 年冬季物资募集：来自中国的热心捐赠者向法国马耳他骑士团在巴黎的接待驳船“圣让之花号”（Fleuron Saint-Jean）捐赠 500 双袜子和 24 件披肩毯，为当地的无家可归者送去温暖。和谊协会负责此次物资的运输组织工作。")],
 'en':[("In preparation","Winter collection 2026: donors in China are offering 500 pairs of socks and 24 blanket-capes to the Fleuron Saint-Jean, the Ordre de Malte France's shelter barge for homeless people in Paris. A.H.A. is arranging the shipment.")],
 'es':[("En preparación","Colecta de invierno 2026: donantes en China ofrecen 500 pares de calcetines y 24 mantas-capa al Fleuron Saint-Jean, la barcaza de acogida de la Orden de Malta Francia para personas sin hogar en París. La A.H.A. organiza el envío.")],
 'ru':[("В подготовке","Зимний сбор 2026 года: дарители из Китая передают 500 пар носков и 24 пледа-накидки на Fleuron Saint-Jean — баржу-приют Мальтийского ордена Франции для бездомных в Париже. A.H.A. организует доставку.")],
 'ar':[("قيد التحضير","حملة الشتاء 2026: متبرعون في الصين يقدّمون 500 زوج من الجوارب و24 غطاءً على شكل عباءة إلى ⁦Fleuron Saint-Jean⁩، مركب الإيواء التابع لمنظمة مالطا في فرنسا للأشخاص بلا مأوى في باريس. وتتولى الجمعية تنظيم الشحن.")],
}
FIGS=['2023','2','40','2','6']
# alt text for the Saint-Louis-en-l'Ile concert photo (card "music")
C2_ALT={'fr':"Le public d'un concert à l'église Saint-Louis-en-l'Île, à Paris",
        'zh':'巴黎圣路易岛教堂音乐会现场的观众',
        'en':"The audience at a concert in the church of Saint-Louis-en-l'Île, Paris",
        'es':"El público de un concierto en la iglesia de Saint-Louis-en-l'Île, en París",
        'ru':"Зрители концерта в церкви Сен-Луи-ан-л'Иль в Париже",
        'ar':"جمهور حفل موسيقي في كنيسة سان لوي أن ليل في باريس"}
BOOK='<svg class="ico" viewBox="0 0 24 24" width="64" height="64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"><path d="M12 6.5C10 5 7 4.5 3.5 5v13c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5z"/><path d="M12 6.5v13"/></svg>'
# free membership card (mailto until an online form exists)
JOIN_TO='ahaparis@outlook.com'
JOIN={
 'fr':dict(h="Adhérer gratuitement",p="L'adhésion à l'association est gratuite. Rejoignez-nous pour suivre nos actions et y participer à votre rythme.",b="Je m'inscris",
      n="Vos données servent uniquement à la gestion des adhésions et ne sont jamais cédées.",
      subj="Adhésion gratuite",body="Bonjour,\n\nJe souhaite adhérer gratuitement à l'Association Harmonie d'Amitié.\n\nNom et prénom :\nPays / ville :\nTéléphone (facultatif) :\nCentres d'intérêt (jeunesse et éducation / culture et musique / solidarité) :\nBénévolat (oui / non) :\n\nJ'accepte que ces données soient utilisées par l'association pour gérer mon adhésion.\n"),
 'zh':dict(h="免费入会",p="入会完全免费。欢迎随时关注并参与我们的行动，一切随心、量力而行。",b="立即登记",
      n="您的信息仅用于会员管理，绝不对外披露。",
      subj="免费入会申请",body="您好：\n\n我希望免费加入和谊协会。\n\n姓名：\n国家 / 城市：\n电话（选填）：\n关注领域（青年与教育 / 文化与音乐 / 公益）：\n是否愿意做志愿者（是 / 否）：\n\n我同意协会使用以上信息办理会员事务。\n"),
 'en':dict(h="Join for free",p="Membership of the association is free. Join us to follow and take part in our activities at your own pace.",b="Sign up",
      n="Your data is used only to manage memberships and is never shared.",
      subj="Free membership",body="Hello,\n\nI would like to join the Association Harmonie d'Amitié (free membership).\n\nFull name:\nCountry / city:\nPhone (optional):\nInterests (youth and education / culture and music / solidarity):\nVolunteering (yes / no):\n\nI agree that the association may use this data to manage my membership.\n"),
 'es':dict(h="Hacerse socio gratis",p="La adhesión a la asociación es gratuita. Únase a nosotros para seguir nuestras acciones y participar a su ritmo.",b="Inscribirme",
      n="Sus datos solo se utilizan para gestionar las adhesiones y nunca se ceden.",
      subj="Adhesión gratuita",body="Hola:\n\nDeseo hacerme socio/a gratuitamente de la Association Harmonie d'Amitié.\n\nNombre y apellidos:\nPaís / ciudad:\nTeléfono (opcional):\nIntereses (juventud y educación / cultura y música / solidaridad):\nVoluntariado (sí / no):\n\nAcepto que la asociación utilice estos datos para gestionar mi adhesión.\n"),
 'ru':dict(h="Вступить бесплатно",p="Членство в ассоциации бесплатное. Присоединяйтесь, чтобы следить за нашими делами и участвовать в них в своём ритме.",b="Записаться",
      n="Ваши данные используются только для учёта членов и никому не передаются.",
      subj="Бесплатное членство",body="Здравствуйте!\n\nЯ хочу бесплатно вступить в Association Harmonie d'Amitié.\n\nИмя и фамилия:\nСтрана / город:\nТелефон (по желанию):\nИнтересы (молодёжь и образование / культура и музыка / солидарность):\nВолонтёрство (да / нет):\n\nЯ согласен(на), чтобы ассоциация использовала эти данные для учёта моего членства.\n"),
 'ar':dict(h="انضموا مجانًا",p="العضوية في الجمعية مجانية. انضموا إلينا لمتابعة أنشطتنا والمشاركة فيها بالإيقاع الذي يناسبكم.",b="سجّلوا الآن",
      n="تُستخدم بياناتكم لإدارة العضوية فقط ولا تُشارك مع أي جهة.",
      subj="طلب عضوية مجانية",body="مرحبًا،\n\nأرغب في الانضمام مجانًا إلى Association Harmonie d'Amitié.\n\nالاسم الكامل:\nالبلد / المدينة:\nالهاتف (اختياري):\nالاهتمامات (الشباب والتعليم / الثقافة والموسيقى / التضامن):\nالتطوع (نعم / لا):\n\nأوافق على أن تستخدم الجمعية هذه البيانات لإدارة عضويتي.\n"),
}
from urllib.parse import quote
# Microsoft Forms "membership and contact" forms (page language + English), approved by the Présidente 2026-11-25
FORM={'zh':'https://forms.cloud.microsoft/r/ZvukM4AueZ','en':'https://forms.cloud.microsoft/r/ZvukM4AueZ',
 'fr':'https://forms.cloud.microsoft/r/qjyDrVn1sA','es':'https://forms.cloud.microsoft/r/NvSwQPzXvB',
 'ru':'https://forms.cloud.microsoft/r/KjnPvXzNPx','ar':'https://forms.cloud.microsoft/r/F3Bv8YsMaA'}
FT=' target="_blank" rel="noopener"'
def join_href(l):
    return FORM[l]
# labels for the copy fallback (wording confirmed by the Présidente, 2026-11-25)
# newsletter box texts (zh/fr approved by the Présidente 2026-11-25, option B; other languages translated on the same facts)
SUB={'zh':('订阅动态：请发邮件至','，标题写“订阅”即可，可随时退订。','或填写在线登记表','关闭'),
 'fr':('Recevoir nos nouvelles : écrivez à'," avec l'objet « Abonnement ». Désinscription à tout moment.",'ou remplir le formulaire en ligne','Fermer'),
 'en':('Receive our news: write to',' with the subject “Subscribe”. You can unsubscribe at any time.','or fill in the online form','Close'),
 'es':('Reciba nuestras noticias: escriba a',' con el asunto «Suscripción». Puede darse de baja en cualquier momento.','o rellene el formulario en línea','Cerrar'),
 'ru':('Получать наши новости: напишите на адрес',' с темой «Подписка». Отписаться можно в любой момент.','или заполните онлайн-форму','Закрыть'),
 'ar':('لتلقّي أخبارنا: راسلونا على',' مع كتابة «اشتراك» في عنوان الرسالة. يمكن إلغاء الاشتراك في أي وقت.','أو املؤوا الاستمارة الإلكترونية','إغلاق')}
JCOPY={'zh':('或发邮件至','复制邮箱','已复制','查看申请模板','复制模板'),
 'fr':('Ou écrivez-nous à',"Copier l'adresse",'Copié','Voir le modèle de demande','Copier le modèle'),
 'en':('Or write to us at','Copy address','Copied','See the application template','Copy template'),
 'es':('O escríbanos a','Copiar la dirección','Copiado','Ver el modelo de solicitud','Copiar el modelo'),
 'ru':('Или напишите нам по адресу','Скопировать адрес','Скопировано','Показать образец заявки','Скопировать образец'),
 'ar':('أو راسلونا على','نسخ العنوان','تم النسخ','عرض نموذج الطلب','نسخ النموذج')}
# Jardin de l'amitié / 友谊花园: friends and partner companies, ONLY with signed consent form on file.
# entry: dict(name='...', line={'fr':'...','zh':'...'}, url='https://...' or None)  (≤40 words, no personal contact data)
FRIENDS=[]
# cookieless audience measurement: set to the GoatCounter site code once the association has created its account (e.g. 'harmonie-amitie'); '' = off
GOATCOUNTER='harmonie-amitie'
HEART='<svg class="ico" viewBox="0 0 24 24" width="64" height="64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 20.5s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 7.5 2.7c0 5.6-7.5 10.2-7.5 10.2z"/></svg>'

CSS=open(os.path.join(HERE,'style.css'),encoding='utf-8').read()
FONTS=('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700'
       '&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600')
# Chinese serif (headings, seal) only on the Chinese page, subset to the characters actually used (SK0: light pages)
ZH_SERIF='https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@600;700&display=swap&text='
FONTS_AR='&family=Noto+Naskh+Arabic:wght@500;600&family=Noto+Sans+Arabic:wght@400;600'

PAGES=['home','actions','gouvernance']
def fname(pg): return '' if pg=='home' else pg+'.html'
def url(l,pg='home'): return (BASE if l=='fr' else BASE+l+'/')+fname(pg)
CLEAN=True  # site: clean folder URLs (/, /zh/); preview: explicit index.html
def rel(frm,to,pg='home'):
    """relative link from page pg of lang frm to the same page pg of lang to"""
    up='' if frm=='fr' else '../'
    f=fname(pg) or ('' if CLEAN else 'index.html')
    if to=='fr': return up+f if (up+f) else './'
    return up+to+'/'+f

def page(l, preview=False, pg='home'):
    t={k:html.escape(v,quote=False) for k,v in T[l].items()}
    if l!='zh': t['title']=html.escape("Association Harmonie d'Amitié (A.H.A.)",quote=False)
    a=lambda k: html.escape(t[k] if k=='title' else T[l][k],quote=True)
    zh=(l=='zh')
    # Chinese seal only on the Chinese page; elsewhere the French wordmark (as on concert programmes)
    if zh:
        logo=('<span class="seal" aria-hidden="true">和谊</span>\n    <span><b>和谊协会</b>'
              '<span><bdi lang="fr">Association Harmonie d\'Amitié · A.H.A.</bdi> · 巴黎</span></span>')
        fth='和谊协会 · <bdi lang="fr">Association Harmonie d\'Amitié</bdi>'
        mark3='<span class="mark" aria-hidden="true">暖</span>'
        mark1='<span class="mark" aria-hidden="true">学</span>'
    else:
        logo=('<span class="seal latin" aria-hidden="true">AHA</span>\n    <span lang="fr" dir="ltr"><b>Association Harmonie d\'Amitié</b>'
              '<span>A.H.A. · Paris</span></span>')
        fth='<bdi lang="fr">Association Harmonie d\'Amitié (A.H.A.)</bdi>'
        mark3=HEART
        mark1=BOOK
    up='' if l=='fr' else '../'
    rtl=(l=='ar')
    SEP={'fr':'\u00a0: ','zh':'：'}.get(l,': ')
    fonts=FONTS+(FONTS_AR if rtl else '')+'&display=swap'
    if preview or not CLEAN:  # artifact preview has no fonts/ folder: keep the Google link there
        fontlinks=(f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                   f'<link rel="stylesheet" href="{fonts}" media="print" onload="this.media=\'all\'">\n')
    else:  # self-hosted (tools/fonts.py): reachable from China/WeChat, no visitor IP sent to Google (GDPR)
        fontlinks=f'<link rel="stylesheet" href="{up}fonts/base.css">\n'+(f'<link rel="stylesheet" href="{up}fonts/arabic.css">\n' if rtl else '')
    ltr=lambda s:'<bdi class="ltr">%s</bdi>'%s if rtl else s
    alts=''.join('<link rel="alternate" hreflang="%s" href="%s">\n'%(HTML_LANG[x] if x!='zh' else 'zh-Hans',url(x,pg)) for x in LANGS)
    alts+='<link rel="alternate" hreflang="x-default" href="%s">\n'%url('fr',pg)
    HOME='./' if CLEAN else 'index.html'
    H=lambda a: '#'+a if pg=='home' else HOME+'#'+a
    # structured data for search engines and AI agents (SK0): association, strategic partner, concerts
    AHA_ID=BASE+'#aha'; AIEC_ID=BASE+'#aiec'; FEST_ID=BASE+'#festival-diversite'
    venue={"@type":"Place","name":"Église Saint-Louis-en-l'Île","address":{"@type":"PostalAddress","streetAddress":"19 rue Saint-Louis-en-l'Île","postalCode":"75004","addressLocality":"Paris","addressCountry":"FR"}}
    ld={"@context":"https://schema.org","@graph":[
        {"@type":"NGO","@id":AHA_ID,"name":"Association Harmonie d'Amitié","alternateName":["A.H.A.","和谊协会"],
         "url":BASE,"email":"ahaparis@outlook.com","foundingDate":"2023","identifier":"RNA W751272194",
         "description":"Association loi 1901 à but non lucratif : éducation, culture, solidarité. Passerelle d'intérêt général ; ne gère pas de flux financiers.",
         "knowsLanguage":["fr","zh","en","es","ru","ar"],
         "address":{"@type":"PostalAddress","streetAddress":"27 rue Saint-Jacques","postalCode":"75005","addressLocality":"Paris","addressCountry":"FR"}},
        {"@type":"NGO","name":"Association Internationale La Voix de la Compassion","alternateName":"法国国际妙音同善会",
         "description":"Association fondée par la Présidente d'honneur de l'A.H.A. ; initiatrice des dons d'hiver 2024, avec l'aide de l'A.H.A."},
        {"@type":"NGO","@id":AIEC_ID,"name":"Association internationale d'échanges culturels","alternateName":"A.I.E.C.",
         "description":"Partenaire stratégique de long terme de l'A.H.A. ; met en œuvre les projets."},
        {"@type":"MusicEvent","name":"Concert à l'église Saint-Louis-en-l'Île (Festival de la diversité culturelle 2024)","startDate":"2024-05-24T20:00","location":venue,
         "organizer":{"@id":AIEC_ID},"funder":{"@id":AHA_ID},"superEvent":{"@id":FEST_ID}},
        {"@type":"MusicEvent","name":"Concert de l'Orchestre à cordes de Paris (Festival de la diversité culturelle 2025)","startDate":"2025-05-25T19:30","location":venue,
         "performer":{"@type":"MusicGroup","name":"Orchestre à cordes de Paris"},
         "organizer":{"@id":AIEC_ID},"funder":{"@id":AHA_ID},"superEvent":{"@id":FEST_ID}},
        {"@type":"Festival","@id":FEST_ID,"name":"Festival de la diversité culturelle","startDate":"2025-05-17","endDate":"2025-05-27","description":"15e édition (2025)",
         "organizer":{"@type":"Organization","name":"Comité d'animation culturelle Paris 1","url":"https://www.animationculturelle-paris1.com/"},
         "sponsor":{"@type":"Organization","name":"Commission nationale française pour l'UNESCO"}}]}
    if pg!='home':
        t['title']=html.escape({'actions':T[l]['m_actions'],'gouvernance':T[l]['m_gov']}[pg],quote=False)+' · '+t['title']
    gctag=(f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>\n' if GOATCOUNTER and not preview else '')
    if GOATCOUNTER: t['pub']=html.escape(T[l]['pub_gc'],quote=False)
    ldtag=gctag+(f'<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>\n' if pg=='home' else '')
    headx=f'''<title>{t['title']}</title>
<meta name="description" content="{a('desc')}">
<meta property="og:type" content="website">
<meta property="og:title" content="{a('title')}">
<meta property="og:description" content="{a('desc')}">
<meta property="og:image" content="{BASE}img/concert-2025.jpg">
<meta property="og:url" content="{url(l,pg)}">
<meta property="og:locale" content="{ {'fr':'fr_FR','zh':'zh_CN','en':'en_GB','es':'es_ES','ru':'ru_RU','ar':'ar_AR'}[l] }">
<link rel="canonical" href="{url(l,pg)}">
{alts}<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
{ldtag}{fontlinks}{'%%ZHFONT%%' if zh else ''}
<script>document.documentElement.classList.add('js')</script>
<style>
*,*::before,*::after{{box-sizing:border-box}}body{{margin:0}}img{{max-width:100%}}html{{scroll-behavior:smooth}}@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
{CSS}
</style>'''
    sw=''.join('<a href="%s" hreflang="%s" lang="%s" title="%s"%s>%s</a>'%(
        rel(l,x,pg),HTML_LANG[x],HTML_LANG[x],html.escape(NAMES[x]),' aria-current="page"' if x==l else '',SHORT[x]) for x in LANGS)
    mt=f'<div class="mtnote" role="note"><div class="in">{t["mtnote"]} <a href="{rel(l,"fr",pg)}" hreflang="fr" lang="fr">Version française</a></div></div>\n' if l in MACHINE and t['mtnote'] else ''
    figs=''.join(f'<div class="fig"><b>{FIGS[i]}</b><span>{t["f%d"%(i+1)]}</span></div>' for i in range(5))
    news=''.join(f'<article class="item ongoing"><span class="status">{html.escape(st)}</span><p>{html.escape(tx)}</p></article>' for st,tx in ONGOING[l])
    news+=''.join(f'<article class="item"><time datetime="{d}">{s[l]}</time><p>{t[k]}</p></article>' for d,s,k in NEWS)
    t['d6']=html.escape(D6[l],quote=False)
    parts=''.join(f'<li><bdi lang="fr">{html.escape(PARTNERS[i])}</bdi><small>{t["d%d"%(i+1)]}</small></li>' for i in range(6))
    legal=f'<a href="{up}mentions-legales.html">{t["legal"]}</a>'
    cur=lambda x: ' aria-current="page"' if pg==x else ''
    cards_full=f'''<div class="cards">
    <article class="card">
      <div class="pic">{mark1}</div>
      <div class="body"><span class="tag">{t['c1_tag']}</span><h3>{t['c1_h']}</h3><p>{t['c1_p']}</p></div>
    </article>
    <article class="card">
      <div class="pic"><picture><source srcset="{up}img/concert-saint-louis.webp" type="image/webp"><img src="{up}img/concert-saint-louis.jpg" alt="{html.escape(C2_ALT[l],quote=True)}" width="960" height="600" loading="lazy" decoding="async"></picture></div>
      <div class="body"><span class="tag">{t['c2_tag']}</span><h3>{t['c2_h']}</h3><p>{t['c2_p']}</p></div>
    </article>
    <article class="card">
      <div class="pic red">{mark3}</div>
      <div class="body"><span class="tag">{t['c3_tag']}</span><h3>{t['c3_h']}</h3><p>{t['c3_p']}</p></div>
    </article>
  </div>'''
    more=f'<a class="more" href="actions.html">{t["more"]} <span aria-hidden="true">{"←" if rtl else "→"}</span></a>'
    cards_short=f'''<div class="cards short">
    <article class="card">
      <div class="pic">{mark1}</div>
      <div class="body"><span class="tag">{t['c1_tag']}</span><h3>{t['c1_h']}</h3><p>{t['c1_s']}</p>{more}</div>
    </article>
    <article class="card">
      <div class="pic"><picture><source srcset="{up}img/concert-saint-louis.webp" type="image/webp"><img src="{up}img/concert-saint-louis.jpg" alt="{html.escape(C2_ALT[l],quote=True)}" width="960" height="600" loading="lazy" decoding="async"></picture></div>
      <div class="body"><span class="tag">{t['c2_tag']}</span><h3>{t['c2_h']}</h3><p>{t['c2_s']}</p>{more}</div>
    </article>
    <article class="card">
      <div class="pic red">{mark3}</div>
      <div class="body"><span class="tag">{t['c3_tag']}</span><h3>{t['c3_h']}</h3><p>{t['c3_s']}</p>{more}</div>
    </article>
  </div>'''
    def _fr(e):
        nm=html.escape(e['name']); ln=html.escape(e['line'].get(l,e['line']['fr']))
        nm=f'<a href="{html.escape(e["url"],quote=True)}" rel="noopener">{nm}</a>' if e.get('url') else nm
        return f'<li><bdi lang="fr">{nm}</bdi><small>{ln}</small></li>'
    friends=''.join(_fr(e) for e in FRIENDS)
    friends_sec=(f'''<section id="jardin-amitie"><div class="in">
  <h2>{t['fr_h']}</h2>
  <p class="sub">{t['fr_p']}</p>
  <ul class="partners" style="margin-top:1.5rem">{friends}</ul>
</div></section>''' if FRIENDS else '')
    MAINS={'home':f'''<section class="mission" id="association"><div class="in grid">
  <div>
    <p class="kicker">{t['mis_k']}</p>
    <h2>{t['mis_h']}</h2>
    <p class="sub">{t['mis_sub']}</p>
  </div>
  <p class="motto">{t['mis_last']}</p>
</div></section>

<section id="actions"><div class="in">
  <p class="kicker">{t['act_k']}</p>
  <h2>{t['act_h']}</h2>
  {cards_short}
</div></section>

<section id="actualites"><div class="in">
  <p class="kicker">{t['news_k']}</p>
  <h2>{t['news_h']}</h2>
  <div class="news" style="margin-top:1.5rem">{news}</div>
</div></section>

<section class="mission" id="partenaires"><div class="in">
  <p class="kicker">{t['par_k']}</p>
  <h2>{t['par_h']}</h2>
  <ul class="partners" style="margin-top:1.5rem">{parts}</ul>
</div></section>

{friends_sec}

<section class="band" id="engager"><div class="in"><div class="grid g4">
  <div id="adherer"><h3>{html.escape(JOIN[l]['h'])}</h3><p>{html.escape(JOIN[l]['p'])}</p><a class="btn btn-red" href="{html.escape(join_href(l),quote=True)}"{FT}>{html.escape(JOIN[l]['b'])}</a></div>
  <div><h3>{t['b1_h']}</h3><p>{t['b1_p']}</p><a class="btn btn-line" href="{FORM[l]}"{FT}>{t['b1_b']}</a></div>
  <div><h3>{t['b2_h']}</h3><p>{t['b2_p']}</p><a class="btn btn-line" href="{FORM[l]}"{FT}>{t['b2_b']}</a></div>
  <div><h3>{t['b3_h']}</h3><p>{t['b3_p']}</p><a class="btn btn-line" href="{FORM[l]}"{FT}>{t['b3_b']}</a></div>
</div>
<div class="jrow"><small>{html.escape(JOIN[l]['n'])}</small>
  <p class="jalt">{JCOPY[l][0]} <bdi class="jmail">{JOIN_TO}</bdi> <button type="button" class="copy" data-copy="{JOIN_TO}" data-done="{JCOPY[l][2]}">{JCOPY[l][1]}</button></p>
  <details class="jtpl"><summary>{JCOPY[l][3]}</summary><pre id="jtpl-{l}">{html.escape(JOIN[l]['body'])}</pre><button type="button" class="copy" data-copy-from="jtpl-{l}" data-done="{JCOPY[l][2]}">{JCOPY[l][4]}</button></details></div>
</div></section>

''',
 'actions':f'''<section id="actions"><div class="in">
  <p class="kicker">{t['act_k']}</p>
  <h1 class="h2">{t['act_h']}</h1>
  <p class="sub">{t['act_sub']}</p>
  {cards_full}
</div></section>
<section aria-labelledby="h-figs"><div class="in">
  <p class="kicker" id="h-figs">{t['fig_k']}</p>
  <div class="figs">{figs}</div>
  <p class="asof">{t['asof']}</p>
</div></section>''',
 'gouvernance':f'''<section class="mission" id="gouvernance"><div class="in">
  <p class="kicker">{t['gov_k']}</p>
  <h1 class="h2">{t['gov_h']}</h1>
  <p class="sub">{t['gov_sub']}</p>
  <blockquote class="values"><p>{t['mis_q']}</p><p class="last">{t['mis_last']}</p></blockquote>
  <div class="people">
    <div class="person"><h3>{t['p1_n']}</h3><p class="role">{t['p1_r']}</p><p>{t['p1_p']}</p></div>
    <div class="person"><h3>{t['p2_n']}</h3><p class="role">{t['p2_r']}</p><p>{t['p2_p']}</p></div>
    <div class="person"><h3>{t['p3_n']}</h3><p class="role">{t['p3_r']}</p><p>{t['p3_p']}</p></div>
  </div>
</div></section>''' }
    MAIN=MAINS[pg]
    if pg!='home':  # sub-pages have no h2 sections: card titles are the second level (heading order, a11y)
        MAIN=MAIN.replace('<h3','<h2').replace('</h3>','</h2>')
    HERO=f'''<div class="hero">
  <picture><source srcset="{up}img/concert-2025.webp" type="image/webp"><img src="{up}img/concert-2025.jpg" alt="{a('hero_alt')}" width="1079" height="553" fetchpriority="high"></picture>
  <div class="in">
    <h1>{t['h1']}</h1>
    <p>{t['hero_p']}</p>
    <div class="ctas">
      <a class="btn btn-red" href="actions.html">{t['cta1']}</a>
      <a class="btn btn-line" href="#association">{t['cta2']}</a>
    </div>
  </div>
  <span class="credit">{t['credit']}</span>
</div>

''' if pg=='home' else ''
    body=f'''<header class="site">
{mt}<div class="util"><div class="in">
  <a href="#sub" class="sub-open" aria-haspopup="dialog">{t['u_news']}</a>
  <a href="{H('adherer')}">{t['u_join']}</a>
  <nav class="langs" aria-label="{a('langs_label')}">{sw}</nav>
  <a class="btn btn-red" href="{FORM[l]}"{FT}>{t['u_support']}</a>
</div></div>

<div class="main"><div class="in">
  <a class="logo" href="{HOME if pg!='home' else '#top'}" id="top">
    {logo}
  </a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu-list" aria-label="{a('m_btn')}"></button>
  <nav class="menu" aria-label="Menu"><ul id="menu-list">
    <li><a href="{H('association')}">{t['m_assoc']}</a></li>
    <li><a href="actions.html"{cur('actions')}>{t['m_actions']}</a></li>
    <li><a href="gouvernance.html"{cur('gouvernance')}>{t['m_gov']}</a></li>
    <li><a href="{H('actualites')}">{t['m_news']}</a></li>
    <li><a href="{H('partenaires')}">{t['m_part']}</a></li>
    <li><a href="{H('contact')}">{t['m_contact']}</a></li>
    <li class="m-only"><a href="{FORM[l]}"{FT}>{t['u_support']}</a></li>
  </ul></nav>
</div></div>
</header>

<main>
{HERO}{MAIN}
</main>

<footer><div class="in">
  <div>
    <h2>{fth}</h2>
    <p>{t['ft_p']}</p>
  </div>
  <div id="contact">
    <h2>{t['ct_k']}</h2>
    <p>{t['ct_mail']}{SEP}<bdi><a href="mailto:ahaparis@outlook.com">ahaparis@outlook.com</a></bdi></p>
    <p>{t['ct_cn']}{SEP}<bdi><a href="mailto:aha.chine@qq.com">aha.chine@qq.com</a></bdi></p>
  </div>
  <div>
    <h2>{t['tr_h']}</h2>
    <p>{t['tr_p']}</p>
    <p>{t['pub']} {legal}</p>
    <p>{html.escape(ZOOM[l])}</p>
  </div>
</div></footer>
<div id="sub" class="subbox" role="dialog" aria-modal="true" aria-label="{t['u_news']}"><div class="subin">
  <a href="#" class="sub-x" aria-label="{SUB[l][3]}">×</a>
  <p>{SUB[l][0]} <bdi class="jmail">{JOIN_TO}</bdi>{SUB[l][1]}</p>
  <p><button type="button" class="copy" data-copy="{JOIN_TO}" data-done="{JCOPY[l][2]}">{JCOPY[l][1]}</button></p>
  <p><a href="{FORM[l]}"{FT}>{SUB[l][2]} →</a></p>
</div></div>
<script>(function(){{var d=document.getElementById('sub');if(!d)return;function sh(o){{d.classList.toggle('open',o);if(!o&&location.hash==='#sub')history.replaceState(null,'',location.pathname+location.search)}}document.querySelectorAll('.sub-open').forEach(function(a){{a.addEventListener('click',function(e){{e.preventDefault();sh(true)}})}});d.querySelector('.sub-x').addEventListener('click',function(e){{e.preventDefault();sh(false)}});d.addEventListener('click',function(e){{if(e.target===d)sh(false)}});document.addEventListener('keydown',function(e){{if(e.key==='Escape')sh(false)}})}})();</script>
<script>(function(){{function cp(t){{if(navigator.clipboard&&window.isSecureContext)return navigator.clipboard.writeText(t).catch(function(){{return fb(t)}});return Promise.resolve(fb(t))}}function fb(t){{var a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();a.setSelectionRange(0,t.length);try{{document.execCommand('copy')}}catch(e){{}}document.body.removeChild(a)}}
document.querySelectorAll('button.copy').forEach(function(b){{b.addEventListener('click',function(){{var t=b.dataset.copy||document.getElementById(b.dataset.copyFrom).textContent,o=b.textContent;cp(t).then(function(){{b.textContent=b.dataset.done;setTimeout(function(){{b.textContent=o}},2000)}})}})}})}})();</script>
<script>(function(){{var b=document.querySelector('.menu-btn'),m=document.querySelector('nav.menu');if(!b||!m)return;b.addEventListener('click',function(){{var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o)}});m.addEventListener('click',function(e){{if(e.target.closest('a')){{m.classList.remove('open');b.setAttribute('aria-expanded','false')}}}})}})();</script>'''
    attrs=f'lang="{HTML_LANG[l]}"'+(' dir="rtl"' if rtl else '')
    if zh:
        import re, urllib.parse
        # break Chinese headings only between phrases (after ，、·：；), never inside a word like 热爱
        def _ph(m):
            inner=m.group(3)
            if '<' in inner or len(inner)<6: return m.group(0)
            segs=[x for x in re.split(r'(?<=[，、·：；])\s*',inner) if x]
            if len(segs)<2: return m.group(0)
            return m.group(1)+''.join('<span class="ph">%s</span>'%x for x in segs)+m.group(4)
        body=re.sub(r'(<(h[1-3])\b[^>]*>)([^<]*)(</\2>)',_ph,body)
        parts=re.findall(r'<(h[1-4]|b|blockquote)\b[^>]*>(.*?)</\1>',body,re.S)
        parts+=re.findall(r'class="(?:seal|mark)[^"]*"[^>]*>([^<]*)<',body)
        # every element drawn in the heading serif must be in the subset, or missing glyphs fall back to another font
        parts+=re.findall(r'class="motto"[^>]*>(.*?)</',body,re.S)
        txt=''.join(x[1] if isinstance(x,tuple) else x for x in parts)
        chars=''.join(sorted({c for c in txt if ord(c)>0x2e7f}))
        zl=ZH_SERIF+urllib.parse.quote(chars)
        local=None if (preview or not CLEAN) else fontsmod.zh_subset(SITE_ROOT,chars,'zh-'+pg)
        zlink=f'<link rel="stylesheet" href="../{local}">' if local else f'<link rel="stylesheet" href="{zl}" media="print" onload="this.media=\'all\'">'
        headx=headx.replace('%%ZHFONT%%','\n'+zlink)
    if preview and l=='fr':
        # artifact main page: no document skeleton, it is added at publish time
        return headx+'\n'+f'<div {attrs}>\n'+body+'\n</div>\n'
    return f'<!doctype html>\n<html {attrs}>\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{headx}\n</head>\n<body>\n{body}\n</body>\n</html>\n'

def main():
    preview=None
    global CLEAN
    if '--preview' in sys.argv: preview=sys.argv[sys.argv.index('--preview')+1]; CLEAN=False
    ROOT=os.path.dirname(HERE)  # repo root (tools/ next to the pages); aha-website/ layout writes to site/
    if not os.path.exists(os.path.join(ROOT,'CNAME')): ROOT=os.path.join(ROOT,'site')
    global SITE_ROOT; SITE_ROOT=ROOT
    out=preview or ROOT
    for l in LANGS:
      for pg in PAGES:
        f=fname(pg) or 'index.html'
        p=os.path.join(out,f) if l=='fr' else os.path.join(out,l,f)
        os.makedirs(os.path.dirname(p),exist_ok=True)
        open(p,'w',encoding='utf-8').write(page(l,preview=bool(preview) and pg=='home',pg=pg))
        print('wrote',p)
    if not preview:
        sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        for pg in PAGES:
          alts=''.join(f'    <xhtml:link rel="alternate" hreflang="{HTML_LANG[x]}" href="{url(x,pg)}"/>\n' for x in LANGS)+f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url("fr",pg)}"/>\n'
          for l in LANGS: sm+=f'  <url>\n    <loc>{url(l,pg)}</loc>\n{alts}  </url>\n'
        sm+=f'  <url><loc>{BASE}mentions-legales.html</loc></url>\n</urlset>\n'
        open(os.path.join(out,'sitemap.xml'),'w',encoding='utf-8').write(sm); print('wrote sitemap')

if __name__=='__main__': main()
