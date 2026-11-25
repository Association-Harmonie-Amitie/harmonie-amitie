# Generate the six-language site (fr at root, zh/en/es/ru/ar in subfolders)
# Usage (from aha-website/):  python3 -I build/generate.py            -> site/
#                             python3 -I build/generate.py --preview DIR -> artifact preview
import sys, os, json, html
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
from content import LANGS, NAMES, HTML_LANG, MACHINE, T

BASE='https://harmonie-amitie.com/'
SHORT={'fr':'FR','zh':'中文','en':'EN','es':'ES','ru':'RU','ar':'عربي'}
PARTNERS=['IFAC du Pays de Montbéliard','Association Paris Pont Alexandre III',
          "Comité d'animation culturelle Paris 1",'Ordre de Malte France',
          'Association Internationale La Voix de la Compassion',
          "Association internationale d'échanges culturels"]
# subline of the 6th partner (A.I.E.C., RNA W751211126)
D6={'fr':"A.I.E.C. · partenaire stratégique · organisation des concerts 2024 et 2025",
    'zh':"A.I.E.C. · 长期战略合作伙伴 · 2024、2025 年音乐会执行方",
    'en':"A.I.E.C. · strategic partner · organiser of the 2024 and 2025 concerts",
    'es':"A.I.E.C. · socio estratégico · organización de los conciertos de 2024 y 2025",
    'ru':"A.I.E.C. · стратегический партнёр · организация концертов 2024 и 2025 годов",
    'ar':"\u2066A.I.E.C.\u2069 · شريك استراتيجي · تنظيم حفلَي 2024 و2025"}
# past news: (datetime, label, content key)
NEWS=[('2025-05-25','25.05.2025','n3'),('2024-11-25','25.11.2024','n4')]
# cooperations under discussion (no names of individuals, no third-party logos; modest wording)
ONGOING={
 'fr':[("En préparation","Collecte d'hiver 2026 : des donateurs en Chine offrent 500 paires de chaussettes et 24 plaids-capes au Fleuron Saint-Jean, péniche d'accueil de l'Ordre de Malte France pour les personnes sans abri, à Paris. L'A.H.A. organise l'acheminement.")],
 'zh':[("筹备中","2026 年冬季募集：中国爱心人士捐赠 500 双袜子和 24 件披肩毯，送往马耳他骑士团法国分会在巴黎的 Fleuron Saint-Jean 收容船，帮助无家可归的人。和谊协会负责组织运送。")],
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
 'zh':dict(h="免费入会",p="加入协会完全免费。欢迎加入，按自己的节奏关注并参与我们的行动。",b="立即登记",
      n="您的信息仅用于会员管理，绝不对外提供。",
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
def join_href(l):
    j=JOIN[l]; return 'mailto:%s?subject=%s&body=%s'%(JOIN_TO,quote(j['subj']),quote(j['body']))
HEART='<svg class="ico" viewBox="0 0 24 24" width="64" height="64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 20.5s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 7.5 2.7c0 5.6-7.5 10.2-7.5 10.2z"/></svg>'

CSS=open(os.path.join(HERE,'style.css'),encoding='utf-8').read()
FONTS=('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700'
       '&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=Noto+Serif+SC:wght@600;700')
FONTS_AR='&family=Noto+Naskh+Arabic:wght@500;600&family=Noto+Sans+Arabic:wght@400;600'

def url(l): return BASE if l=='fr' else BASE+l+'/'
CLEAN=True  # site: clean folder URLs (/, /zh/); preview: explicit index.html
def rel(frm,to):
    """relative link from page of lang frm to page of lang to"""
    up='' if frm=='fr' else '../'
    if CLEAN: return (up or './') if to=='fr' else up+to+'/'
    return up+('index.html' if to=='fr' else to+'/index.html')

def page(l, preview=False):
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
    fonts=FONTS+(FONTS_AR if rtl else '')+'&display=swap'
    ltr=lambda s:'<bdi class="ltr">%s</bdi>'%s if rtl else s
    alts=''.join('<link rel="alternate" hreflang="%s" href="%s">\n'%(HTML_LANG[x] if x!='zh' else 'zh-Hans',url(x)) for x in LANGS)
    alts+='<link rel="alternate" hreflang="x-default" href="%s">\n'%BASE
    # structured data for search engines and AI agents (SK0): association, strategic partner, concerts
    AHA_ID=BASE+'#aha'; AIEC_ID=BASE+'#aiec'; FEST_ID=BASE+'#festival-diversite'
    venue={"@type":"Place","name":"Église Saint-Louis-en-l'Île","address":{"@type":"PostalAddress","streetAddress":"19 rue Saint-Louis-en-l'Île","postalCode":"75004","addressLocality":"Paris","addressCountry":"FR"}}
    ld={"@context":"https://schema.org","@graph":[
        {"@type":"NGO","@id":AHA_ID,"name":"Association Harmonie d'Amitié","alternateName":["A.H.A.","和谊协会"],
         "url":BASE,"email":"ahaparis@outlook.com","foundingDate":"2023","identifier":"RNA W751272194",
         "description":"Association loi 1901 à but non lucratif : éducation, culture, solidarité. Passerelle d'intérêt général ; ne gère pas de flux financiers.",
         "knowsLanguage":["fr","zh","en","es","ru","ar"],
         "address":{"@type":"PostalAddress","streetAddress":"27 rue Saint-Jacques","postalCode":"75005","addressLocality":"Paris","addressCountry":"FR"}},
        {"@type":"NGO","@id":AIEC_ID,"name":"Association internationale d'échanges culturels","alternateName":"A.I.E.C.",
         "description":"Partenaire stratégique de long terme de l'A.H.A. ; met en œuvre les projets."},
        {"@type":"MusicEvent","name":"Concert à l'église Saint-Louis-en-l'Île (Festival de la diversité culturelle 2024)","startDate":"2024-05-24T20:00","location":venue,
         "organizer":{"@id":AIEC_ID},"funder":{"@id":AHA_ID},"superEvent":{"@id":FEST_ID}},
        {"@type":"MusicEvent","name":"Concert de l'Orchestre à cordes de Paris (Festival de la diversité culturelle 2025)","startDate":"2025-05-25T19:30","location":venue,
         "performer":{"@type":"MusicGroup","name":"Orchestre à cordes de Paris"},
         "organizer":{"@id":AIEC_ID},"funder":{"@id":AHA_ID},"superEvent":{"@id":FEST_ID}},
        {"@type":"Festival","@id":FEST_ID,"name":"Festival de la diversité culturelle",
         "organizer":{"@type":"Organization","name":"Comité d'animation culturelle Paris 1","url":"https://www.animationculturelle-paris1.com/"},
         "sponsor":{"@type":"Organization","name":"Commission nationale française pour l'UNESCO"}}]}
    headx=f'''<title>{t['title']}</title>
<meta name="description" content="{a('desc')}">
<meta property="og:type" content="website">
<meta property="og:title" content="{a('title')}">
<meta property="og:description" content="{a('desc')}">
<meta property="og:image" content="{BASE}img/concert-2025.jpg">
<meta property="og:url" content="{url(l)}">
<meta property="og:locale" content="{ {'fr':'fr_FR','zh':'zh_CN','en':'en_GB','es':'es_ES','ru':'ru_RU','ar':'ar_AR'}[l] }">
<link rel="canonical" href="{url(l)}">
{alts}<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{fonts}"></noscript>
<style>
*,*::before,*::after{{box-sizing:border-box}}body{{margin:0}}img{{max-width:100%}}html{{scroll-behavior:smooth}}@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
{CSS}
</style>'''
    sw=''.join('<a href="%s" hreflang="%s" lang="%s" title="%s"%s>%s</a>'%(
        rel(l,x),HTML_LANG[x],HTML_LANG[x],html.escape(NAMES[x]),' aria-current="page"' if x==l else '',SHORT[x]) for x in LANGS)
    mt=f'<div class="mtnote" role="note"><div class="in">{t["mtnote"]} <a href="{rel(l,"fr")}" hreflang="fr" lang="fr">Version française</a></div></div>\n' if l in MACHINE and t['mtnote'] else ''
    figs=''.join(f'<div class="fig"><b>{FIGS[i]}</b><span>{t["f%d"%(i+1)]}</span></div>' for i in range(5))
    news=''.join(f'<article class="item ongoing"><span class="status">{html.escape(st)}</span><p>{html.escape(tx)}</p></article>' for st,tx in ONGOING[l])
    news+=''.join(f'<article class="item"><time datetime="{d}">{ltr(s)}</time><p>{t[k]}</p></article>' for d,s,k in NEWS)
    t['d6']=html.escape(D6[l],quote=False)
    parts=''.join(f'<li><bdi lang="fr">{html.escape(PARTNERS[i])}</bdi><small>{t["d%d"%(i+1)]}</small></li>' for i in range(6))
    legal=f'<a href="{up}mentions-legales.html">{t["legal"]}</a>'
    body=f'''{mt}<div class="util"><div class="in">
  <a href="#contact">{t['u_news']}</a>
  <a href="#adherer">{t['u_join']}</a>
  <nav class="langs" aria-label="{a('langs_label')}">{sw}</nav>
  <a class="btn btn-red" href="#engager">{t['u_support']}</a>
</div></div>

<header class="main"><div class="in">
  <a class="logo" href="#top" id="top">
    {logo}
  </a>
  <nav class="menu" aria-label="Menu"><ul>
    <li><a href="#association">{t['m_assoc']}</a></li>
    <li><a href="#actions">{t['m_actions']}</a></li>
    <li><a href="#gouvernance">{t['m_gov']}</a></li>
    <li><a href="#actualites">{t['m_news']}</a></li>
    <li><a href="#partenaires">{t['m_part']}</a></li>
    <li><a href="#contact">{t['m_contact']}</a></li>
  </ul></nav>
</div></header>

<main>
<div class="hero">
  <img src="{up}img/concert-2025.jpg" alt="{a('hero_alt')}">
  <div class="in">
    <h1>{t['h1']}</h1>
    <p>{t['hero_p']}</p>
    <div class="ctas">
      <a class="btn btn-red" href="#actions">{t['cta1']}</a>
      <a class="btn btn-line" href="#association">{t['cta2']}</a>
    </div>
  </div>
  <span class="credit">{t['credit']}</span>
</div>

<section class="mission" id="association"><div class="in grid">
  <div>
    <p class="kicker">{t['mis_k']}</p>
    <h2>{t['mis_h']}</h2>
    <p class="sub">{t['mis_sub']}</p>
  </div>
  <blockquote>
    <p>{t['mis_q']}</p>
    <p class="last">{t['mis_last']}</p>
  </blockquote>
</div>
<div class="in"><div class="join" id="adherer">
  <div class="join-txt">
    <h3>{html.escape(JOIN[l]['h'])}</h3>
    <p>{html.escape(JOIN[l]['p'])}</p>
    <small>{html.escape(JOIN[l]['n'])}</small>
  </div>
  <a class="btn btn-red" href="{html.escape(join_href(l),quote=True)}">{html.escape(JOIN[l]['b'])}</a>
</div></div></section>

<section aria-labelledby="h-figs"><div class="in">
  <p class="kicker" id="h-figs">{t['fig_k']}</p>
  <div class="figs">{figs}</div>
  <p class="asof">{t['asof']}</p>
</div></section>

<section id="actions" style="padding-top:0"><div class="in">
  <p class="kicker">{t['act_k']}</p>
  <h2>{t['act_h']}</h2>
  <p class="sub">{t['act_sub']}</p>
  <div class="cards">
    <article class="card">
      <div class="pic">{mark1}</div>
      <div class="body"><span class="tag">{t['c1_tag']}</span><h3>{t['c1_h']}</h3><p>{t['c1_p']}</p></div>
    </article>
    <article class="card">
      <div class="pic"><img src="{up}img/concert-saint-louis.jpg" alt="{html.escape(C2_ALT[l],quote=True)}" loading="lazy"></div>
      <div class="body"><span class="tag">{t['c2_tag']}</span><h3>{t['c2_h']}</h3><p>{t['c2_p']}</p></div>
    </article>
    <article class="card">
      <div class="pic red">{mark3}</div>
      <div class="body"><span class="tag">{t['c3_tag']}</span><h3>{t['c3_h']}</h3><p>{t['c3_p']}</p></div>
    </article>
  </div>
</div></section>

<section class="mission" id="gouvernance"><div class="in">
  <p class="kicker">{t['gov_k']}</p>
  <h2>{t['gov_h']}</h2>
  <p class="sub">{t['gov_sub']}</p>
  <div class="people">
    <div class="person"><h3>{t['p1_n']}</h3><p class="role">{t['p1_r']}</p><p>{t['p1_p']}</p></div>
    <div class="person"><h3>{t['p2_n']}</h3><p class="role">{t['p2_r']}</p><p>{t['p2_p']}</p></div>
  </div>
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

<section class="band" id="engager"><div class="in grid">
  <div><h3>{t['b1_h']}</h3><p>{t['b1_p']}</p><a class="btn btn-line" href="#contact">{t['b1_b']}</a></div>
  <div><h3>{t['b2_h']}</h3><p>{t['b2_p']}</p><a class="btn btn-line" href="#contact">{t['b2_b']}</a></div>
  <div><h3>{t['b3_h']}</h3><p>{t['b3_p']}</p><a class="btn btn-line" href="#contact">{t['b3_b']}</a></div>
</div></section>

<section id="contact"><div class="in">
  <p class="kicker">{t['ct_k']}</p>
  <h2>{t['ct_h']}</h2>
  <dl class="contact" style="margin-top:1.5rem">
    <div><dt>{t['ct_seat']}</dt><dd dir="ltr" lang="fr">27 rue Saint-Jacques<br>75005 Paris, France</dd></div>
    <div><dt>{t['ct_mail']}</dt><dd dir="ltr"><a href="mailto:ahaparis@outlook.com">ahaparis@outlook.com</a></dd></div>
    <div><dt>{t['ct_cn']}</dt><dd dir="ltr"><a href="mailto:aha.chine@qq.com">aha.chine@qq.com</a></dd></div>
  </dl>
</div></section>
</main>

<footer><div class="in">
  <div>
    <h4>{fth}</h4>
    <p>{t['ft_p']}</p>
  </div>
  <div>
    <h4>{t['tr_h']}</h4>
    <p>{t['tr_p']}</p>
    <p>{t['pub']} {legal}</p>
  </div>
</div></footer>'''
    attrs=f'lang="{HTML_LANG[l]}"'+(' dir="rtl"' if rtl else '')
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
    out=preview or ROOT
    for l in LANGS:
        p=os.path.join(out,'index.html') if l=='fr' else os.path.join(out,l,'index.html')
        os.makedirs(os.path.dirname(p),exist_ok=True)
        open(p,'w',encoding='utf-8').write(page(l,preview=bool(preview)))
        print('wrote',p)
    if not preview:
        sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        alts=''.join(f'    <xhtml:link rel="alternate" hreflang="{HTML_LANG[x]}" href="{url(x)}"/>\n' for x in LANGS)+f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>\n'
        for l in LANGS: sm+=f'  <url>\n    <loc>{url(l)}</loc>\n{alts}  </url>\n'
        sm+=f'  <url><loc>{BASE}mentions-legales.html</loc></url>\n</urlset>\n'
        open(os.path.join(out,'sitemap.xml'),'w',encoding='utf-8').write(sm); print('wrote sitemap')

if __name__=='__main__': main()
