"""Self-host the web fonts (fonts/ next to the pages).

Why: fonts.googleapis.com is often unreachable from mainland China (WeChat readers),
and self-hosting sends no visitor IP to a third party (GDPR). Run it once, or again
when the Chinese headings change (generate.py calls zh_subset() automatically).

  python3 -I tools/fonts.py          # latin/cyrillic/arabic families -> fonts/*.css + woff2
"""
import os, re, sys, urllib.request, urllib.parse, hashlib

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
KEEP = {'latin', 'latin-ext', 'cyrillic', 'cyrillic-ext', 'arabic'}
FAMILIES = {
    'base': 'family=Source+Sans+3:wght@400;600;700&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600',
    'arabic': 'family=Noto+Naskh+Arabic:wght@500;600&family=Noto+Sans+Arabic:wght@400;600',
}
API = 'https://fonts.googleapis.com/css2?'

def _get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=30).read()

def _localize(css, out, keep=None):
    """download each woff2 into out/, rewrite urls, drop unused subsets"""
    blocks = re.findall(r'(/\* ([\w-]+) \*/\s*)?(@font-face\s*\{[^}]*\})', css)
    res = []
    for _, sub, face in blocks:
        if keep and sub and sub not in keep: continue
        def dl(m):
            u = m.group(1)
            name = hashlib.sha1(u.encode()).hexdigest()[:12] + '.woff2'
            p = os.path.join(out, name)
            if not os.path.exists(p): open(p, 'wb').write(_get(u))
            return 'url(%s)' % name
        res.append(re.sub(r'url\((https://[^)]+)\)', dl, face))
    return '\n'.join(res) + '\n'

def build(root):
    out = os.path.join(root, 'fonts'); os.makedirs(out, exist_ok=True)
    for key, fam in FAMILIES.items():
        css = _get(API + fam + '&display=swap').decode()
        open(os.path.join(out, key + '.css'), 'w').write(_localize(css, out, KEEP))
        print('wrote fonts/%s.css' % key)

def zh_subset(root, chars, name='zh'):
    """Noto Serif SC subset for exactly these characters; reuses the files when chars are unchanged.
    Returns the relative css path, or None (offline) so the caller can fall back."""
    out = os.path.join(root, 'fonts'); os.makedirs(out, exist_ok=True)
    keyf = os.path.join(out, name + '-chars.txt'); cssf = os.path.join(out, name + '.css')
    if os.path.exists(keyf) and os.path.exists(cssf) and open(keyf, encoding='utf-8').read() == chars:
        return 'fonts/%s.css' % name
    try:
        css = _get(API + 'family=Noto+Serif+SC:wght@600;700&display=swap&text=' + urllib.parse.quote(chars)).decode()
        for f in os.listdir(out):  # old subset files
            if f.startswith(name + '-') and f.endswith('.woff2'): os.remove(os.path.join(out, f))
        n = [0]
        def dl(m):
            n[0] += 1; fn = '%s-%d.woff2' % (name, n[0])
            open(os.path.join(out, fn), 'wb').write(_get(m.group(1)))
            return 'url(%s)' % fn
        open(cssf, 'w').write(re.sub(r'url\((https://[^)]+)\)', dl, css))
        open(keyf, 'w', encoding='utf-8').write(chars)
        print('wrote fonts/%s.css (%d chars)' % (name, len(chars)))
        return 'fonts/%s.css' % name
    except Exception as e:
        print('WARNING zh font subset not refreshed (%s); using Google Fonts link' % e, file=sys.stderr)
        return None

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
    if not os.path.exists(os.path.join(root, 'CNAME')): root = os.path.join(root, 'site')
    build(root)
