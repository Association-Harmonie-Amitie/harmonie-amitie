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
          'Association Internationale La Voix de la Compassion']
# past news: (datetime, label, content key)
NEWS=[('2025-05-25','25.05.2025','n3'),('2024-11-25','25.11.2024','n4')]
# cooperations under discussion (no names of individuals, no third-party logos; modest wording)
ONGOING={
 'fr':[("En cours","Échanges avec la Commission nationale française pour l'UNESCO ; une rencontre est envisagée à partir de décembre."),
       ("En préparation","Collecte d'hiver 2026 : des dons en nature proposés par des donateurs en Chine (chaussettes, plaids), acceptés par l'Ordre de Malte France pour ses maraudes."),
       ("En discussion","Échanges avec un établissement bancaire sur un accompagnement dédié aux adhérents, notamment aux étudiants.")],
 'zh':[("进行中","与法国联合国教科文组织全国委员会保持沟通，拟于 12 月起安排会面。"),
       ("筹备中","2026 年冬季募集：中国捐赠者拟捐赠袜子和毛毯，马耳他骑士团法国分会已同意接收，用于冬季街头探访救助。"),
       ("洽谈中","与一家银行机构商谈为会员、特别是学生会员提供专门服务。")],
 'en':[("Ongoing","Exchanges with the French National Commission for UNESCO; a meeting is envisaged from December."),
       ("In preparation","Winter collection 2026: donations in kind offered by donors in China (socks, blankets), accepted by the Ordre de Malte France for its street outreach."),
       ("Under discussion","Talks with a banking institution about dedicated support for members, especially students.")],
 'es':[("En curso","Intercambios con la Comisión Nacional Francesa para la UNESCO; se prevé un encuentro a partir de diciembre."),
       ("En preparación","Colecta de invierno 2026: donaciones en especie ofrecidas por donantes en China (calcetines, mantas), aceptadas por la Orden de Malta Francia para sus rondas solidarias."),
       ("En conversación","Conversaciones con una entidad bancaria sobre un acompañamiento dedicado a los socios, en particular a los estudiantes.")],
 'ru':[("В процессе","Ведётся диалог с Национальной комиссией Франции по делам ЮНЕСКО; встреча предполагается начиная с декабря."),
       ("В подготовке","Зимний сбор 2026 года: вещи от дарителей из Китая (носки, пледы) приняты Мальтийским орденом Франции для помощи людям на улице."),
       ("Обсуждается","Переговоры с банковским учреждением о специальном сопровождении для членов ассоциации, прежде всего студентов.")],
 'ar':[("جارٍ","تبادل مع اللجنة الوطنية الفرنسية لليونسكو، ويُرتقب لقاء ابتداءً من ديسمبر."),
       ("قيد التحضير","حملة الشتاء 2026: تبرعات عينية يقدّمها متبرعون في الصين (جوارب وأغطية)، قبلتها منظمة فرسان مالطا في فرنسا لجولاتها الميدانية."),
       ("قيد النقاش","محادثات مع مؤسسة مصرفية حول مرافقة مخصّصة للأعضاء، ولا سيما الطلاب.")],
}
FIGS=['2023','2','40','2','5']
# alt text for the Saint-Louis-en-l'Ile concert photo (card "music")
C2_ALT={'fr':"Le public d'un concert à l'église Saint-Louis-en-l'Île, à Paris",
        'zh':'巴黎圣路易岛教堂音乐会现场的观众',
        'en':"The audience at a concert in the church of Saint-Louis-en-l'Île, Paris",
        'es':"El público de un concierto en la iglesia de Saint-Louis-en-l'Île, en París",
        'ru':"Зрители концерта в церкви Сен-Луи-ан-л'Иль в Париже",
        'ar':"جمهور حفل موسيقي في كنيسة سان لوي أن ليل في باريس"}
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
    else:
        logo=('<span class="wordmark" lang="fr" dir="ltr"><b>A.H.A</b>'
              '<span>Association Harmonie d\'Amitié</span></span>')
        fth='<bdi lang="fr">Association Harmonie d\'Amitié (A.H.A.)</bdi>'
        mark3=HEART
    up='' if l=='fr' else '../'
    rtl=(l=='ar')
    fonts=FONTS+(FONTS_AR if rtl else '')+'&display=swap'
    ltr=lambda s:'<bdi class="ltr">%s</bdi>'%s if rtl else s
    alts=''.join('<link rel="alternate" hreflang="%s" href="%s">\n'%(HTML_LANG[x] if x!='zh' else 'zh-Hans',url(x)) for x in LANGS)
    alts+='<link rel="alternate" hreflang="x-default" href="%s">\n'%BASE
    ld={"@context":"https://schema.org","@type":"NGO","name":"Association Harmonie d'Amitié",
        "alternateName":["A.H.A.","和谊协会"],"url":BASE,"email":"ahaparis@outlook.com","foundingDate":"2023",
        "address":{"@type":"PostalAddress","streetAddress":"27 rue Saint-Jacques","postalCode":"75005","addressLocality":"Paris","addressCountry":"FR"}}
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
    parts=''.join(f'<li><bdi lang="fr">{html.escape(PARTNERS[i])}</bdi><small>{t["d%d"%(i+1)]}</small></li>' for i in range(5))
    legal=f'<a href="{up}mentions-legales.html">{t["legal"]}</a>'
    body=f'''{mt}<div class="util"><div class="in">
  <a href="#contact">{t['u_news']}</a>
  <a href="#engager">{t['u_join']}</a>
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
</div></section>

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
      <div class="pic"><img src="{up}img/iut-2026.jpg" alt="{a('c1_alt')}" loading="lazy"></div>
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
  <div><h3>{t['b1_h']}</h3><p>{t['b1_p']}</p><a class="btn btn-red" href="#contact">{t['b1_b']}</a></div>
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
