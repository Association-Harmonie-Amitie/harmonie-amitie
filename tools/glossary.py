"""Write docs/用语表-glossaire.md: every approved public text of the site, six languages side by side.

The site texts (tools/content.py and the small tables in tools/generate.py) are the single source;
this file is regenerated from them, so the glossary never drifts from what is online.
Any change to these texts follows SK13: propose exact words, wait for the Présidente's choice.

  python3 -I tools/glossary.py
"""
import os, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from content import LANGS, T
import generate as G

ORDER = ['fr', 'zh', 'en', 'es', 'ru', 'ar']
NAMES = {'fr': 'Français', 'zh': '中文', 'en': 'English', 'es': 'Español', 'ru': 'Русский', 'ar': 'العربية'}
GROUPS = [
    ('核心用语 · Formules clés', 'Devise, titres et cartes : à reprendre mot pour mot ailleurs (affiches, réseaux, courriels).',
     ['mis_last', 'h1', 'mis_h', 'act_h', 'c1_tag', 'c1_h', 'c2_tag', 'c2_h', 'c3_tag', 'c3_h', 'gov_h', 'news_h', 'par_h', 'ct_h', 'fr_h']),
    ('按钮与导航 · Boutons et menu', 'Libellés courts ; garder la même longueur relative dans les six langues (symétrie, SK3).',
     ['u_news', 'u_join', 'u_support', 'm_assoc', 'm_actions', 'm_gov', 'm_news', 'm_part', 'm_contact', 'cta1', 'cta2',
      'b1_h', 'b1_b', 'b2_h', 'b2_b', 'b3_h', 'b3_b', 'more', 'home', 'langs_label', 'm_btn']),
    ('页眉页脚与说明 · En-tête, pied de page, mentions', '', ['title', 'desc', 'mtnote', 'ct_k', 'ct_seat', 'ct_mail', 'ct_cn', 'ft_p', 'tr_h', 'tr_p', 'pub', 'pub_gc', 'legal']),
    ('段落 · Paragraphes', 'Textes longs ; faits identiques dans toutes les langues, style propre à chaque langue (SK12).',
     ['hero_p', 'mis_sub', 'mis_q', 'act_sub', 'c1_p', 'c1_s', 'c2_p', 'c2_s', 'c3_p', 'c3_s', 'gov_sub', 'fr_p',
      'b1_p', 'b2_p', 'b3_p', 'n1', 'n2', 'n3', 'n4', 'd1', 'd2', 'd3', 'd4', 'd5', 'f1', 'f2', 'f3', 'f4', 'f5', 'asof', 'mis_k', 'fig_k', 'act_k', 'gov_k', 'news_k', 'par_k']),
    ('人物与头衔 · Personnes et titres', 'Titres uniquement (SK7) ; noms publics confirmés par la Présidente.',
     ['p1_n', 'p1_r', 'p1_p', 'p2_n', 'p2_r', 'p2_p', 'p3_n', 'p3_r', 'p3_p']),
    ('图片说明 · Textes alternatifs des images', '', ['hero_alt', 'c1_alt', 'credit']),
]

def cell(s): return str(s).replace('|', '\\|').replace('\n', ' ')

def block(title, note, rows):
    out = [f'## {title}', '']
    if note: out += [f'_{note}_', '']
    for key, vals in rows:
        out.append(f'### `{key}`')
        out += [f'- **{NAMES[l]}** — {cell(vals.get(l, "—"))}' for l in ORDER]
        out.append('')
    return out

def main():
    lines = ['# 网站已核准用语表 · Glossaire des formulations approuvées', '',
             f'_自动生成 · Généré automatiquement le {datetime.date.today().isoformat()} depuis tools/content.py et tools/generate.py (`python3 -I tools/glossary.py`)._', '',
             '- 中文：本表即网站现行文字，六语并列。改任何一条前，先按 SK13 列出具体替代词，经主席选择后才改 content.py，再重新生成本表。',
             '- Français : ce tableau est le texte en ligne, six langues côte à côte. Avant toute modification : proposer les mots exacts (SK13), attendre le choix de la Présidente, modifier content.py, puis régénérer ce tableau.', '']
    seen = set()
    for title, note, keys in GROUPS:
        rows = [(k, {l: T[l].get(k, '') for l in ORDER}) for k in keys if k in T['fr']]
        seen.update(keys); lines += block(title, note, rows)
    rest = [k for k in T['fr'] if k not in seen]
    if rest: lines += block('其他 · Autres', '', [(k, {l: T[l].get(k, '') for l in ORDER}) for k in rest])
    # small tables kept in generate.py
    extra = [('JOIN.h', {l: G.JOIN[l]['h'] for l in ORDER}), ('JOIN.p', {l: G.JOIN[l]['p'] for l in ORDER}),
             ('JOIN.b', {l: G.JOIN[l]['b'] for l in ORDER}), ('JOIN.n (隐私说明 · note données)', {l: G.JOIN[l]['n'] for l in ORDER}),
             ('SUB (订阅小框 · fenêtre abonnement)', {l: ' … '.join(G.SUB[l]) for l in ORDER}),
             ('JCOPY (邮件/复制按钮 · e-mail, bouton copier)', {l: ' / '.join(G.JCOPY[l]) for l in ORDER}),
             ('ZOOM (放大提示 · aide zoom)', {l: G.ZOOM[l] for l in ORDER}),
             ('C2_ALT', {l: G.C2_ALT[l] for l in ORDER}), ('D6 (A.I.E.C.)', {l: G.D6[l] for l in ORDER}),
             ('ONGOING (筹备中 · en préparation)', {l: ' — '.join(' : '.join(x) for x in G.ONGOING[l]) for l in ORDER})]
    lines += block('入会、订阅与其他 · Adhésion, abonnement, divers', 'Libellés définis dans tools/generate.py.', extra)
    lines += ['## 表单 · Formulaires', '', 'Microsoft Forms (compte ahaparis@outlook.com) : textes complets dans /mnt/project-files/aha-website/forms/.', '']
    lines += [f'- {NAMES[l]} : {G.FORM[l]}' for l in ORDER] + ['']
    os.makedirs(os.path.join(os.path.dirname(HERE), 'docs'), exist_ok=True)
    p = os.path.join(os.path.dirname(HERE), 'docs', '用语表-glossaire.md')
    open(p, 'w', encoding='utf-8').write('\n'.join(lines))
    print('wrote', p)

if __name__ == '__main__': main()
