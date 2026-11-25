// Pre-publication self-check (docs/自检清单-autocontrole.md). Run from the repo root:
//   python3 -m http.server 8765 &   then   node tools/selfcheck.js [http://localhost:8765]
// Exit code 0 = all checks pass. Prints only problems, then a one-line summary.
const {chromium, devices} = require('playwright');
const BASE = (process.argv[2] || 'http://localhost:8765').replace(/\/$/, '');
const LANGS = ['', 'zh/', 'en/', 'es/', 'ru/', 'ar/'];
const PAGES = ['', 'actions.html', 'gouvernance.html'];
const WECHAT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.47(0x18002f2c) NetType/WIFI Language/zh_CN';
const ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'gc.zgo.at', 'harmonie-amitie.goatcounter.com'];
let fails = 0, checks = 0;
const bad = (...m) => { fails++; console.log('FAIL', ...m); };

(async () => {
  const b = await chromium.launch();
  for (const l of LANGS) for (const f of PAGES) {
    const path = '/' + l + f, name = (l || 'fr/') + (f || 'index');
    // 1. desktop + phone: HTTP status, horizontal overflow, broken internal links, console errors, third-party requests
    for (const vp of [{width: 1280, height: 900}, {width: 390, height: 844}, {width: 320, height: 640}]) {
      const ctx = await b.newContext({viewport: vp, userAgent: vp.width < 400 ? WECHAT : undefined});
      const p = await ctx.newPage(); const errs = [], hosts = new Set();
      p.on('pageerror', e => errs.push(e.message));
      p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errs.push(m.text()); });
      // a failed local file is an error; the statistics counter may be blocked by the network (not a site problem)
      p.on('requestfailed', q => { const h = new URL(q.url()).hostname; if (h === 'localhost' || h === '127.0.0.1' || h === new URL(BASE).hostname) errs.push('failed ' + q.url()); });
      p.on('request', r => hosts.add(new URL(r.url()).hostname));
      const r = await p.goto(BASE + path, {waitUntil: 'networkidle'}); checks++;
      if (!r || r.status() !== 200) bad(name, vp.width, 'HTTP', r && r.status());
      const [sw, iw] = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]); checks++;
      if (sw > iw) bad(name, vp.width, 'horizontal overflow', sw, '>', iw);
      if (vp.width === 1280) {
        const broken = await p.evaluate(async () => { const out = [];
          for (const a of document.querySelectorAll('a[href]')) { const h = a.getAttribute('href');
            if (/^(mailto|tel|http)/.test(h)) continue; const u = new URL(h, location.href);
            if (u.hash && u.pathname === location.pathname) { if (u.hash.length > 1 && !document.getElementById(u.hash.slice(1))) out.push(h); }
            else { const r = await fetch(u.pathname); if (!r.ok) out.push(h); } } return out; }); checks++;
        if (broken.length) bad(name, 'broken links', broken.join(' '));
        // every image loaded and has alt text
        const imgs = await p.evaluate(() => [...document.images].map(i => ({s: i.currentSrc, ok: i.complete && i.naturalWidth > 0 || i.loading === 'lazy', alt: i.hasAttribute('alt')}))); checks++;
        imgs.filter(i => !i.ok || !i.alt).forEach(i => bad(name, 'image', i.s, i.ok ? 'no alt' : 'not loaded'));
        // fonts: self-hosted files actually load, and (zh) every heading-serif character is in the subset
        const fontInfo = await p.evaluate(async () => { await document.fonts.ready;
          const fam = [...document.fonts].filter(x => x.status === 'loaded').map(x => x.family.replace(/"/g, ''));
          const missing = new Set();
          const zh = [...document.fonts].filter(x => /Noto Serif SC/.test(x.family));
          if (zh.length) { const txt = [...document.querySelectorAll('h1,h2,h3,h4,b,blockquote,.seal,.mark,.motto')]
              .filter(e => /Noto Serif SC/.test(getComputedStyle(e).fontFamily)).map(e => e.textContent).join('');
            const link = document.querySelector('link[href*="fonts/zh-"]');
            const chars = link ? await fetch(link.href.replace(/\.css$/, '-chars.txt')).then(r => r.ok ? r.text() : '') : '';
            for (const c of txt) if (c.codePointAt(0) > 0x2e7f && !chars.includes(c)) missing.add(c); }
          return {fam: [...new Set(fam)], missing: [...missing].join('')}; }); checks++;
        if (!fontInfo.fam.some(x => /Source Sans 3|Noto Sans Arabic/.test(x))) bad(name, 'body font not loaded', fontInfo.fam.join(','));
        if (fontInfo.missing) bad(name, 'characters missing from Chinese font subset:', fontInfo.missing);
      }
      checks++; if (errs.length) bad(name, vp.width, 'JS errors', errs.join(' | '));
      const foreign = [...hosts].filter(h => !ALLOWED_HOSTS.includes(h)); checks++;
      if (foreign.length) bad(name, vp.width, 'third-party requests (privacy / China access):', foreign.join(' '));
      await ctx.close();
    }
    // 2. enlarged text (accessibility, WeChat "large font"): 125%, 150%, 200% at phone width
    for (const s of [1.25, 1.5, 2]) {
      const p = await b.newPage({viewport: {width: 390, height: 844}});
      await p.goto(BASE + path); await p.addStyleTag({content: `html{font-size:${s * 100}%!important}`});
      await p.waitForTimeout(150);
      const o = await p.evaluate(() => { const iw = innerWidth; const out = [];
        for (const e of document.querySelectorAll('body *')) { const r = e.getBoundingClientRect();
          if (r.width && (r.right > iw + 1 || r.left < -1) && getComputedStyle(e).position !== 'fixed' && !e.closest('.subbox,nav.menu:not(.open)')) out.push(e.tagName + '.' + e.className); }
        return [document.documentElement.scrollWidth > iw, out.slice(0, 4)]; }); checks++;
      if (o[0] || o[1].length) bad(name, 'text x' + s, 'overflow', o[1].join(' '));
      await p.close();
    }
  }
  // 3. buttons: newsletter box opens and closes, menu opens, join buttons go to the right form
  for (const l of LANGS) {
    const p = await b.newPage({viewport: {width: 390, height: 844}, userAgent: WECHAT});
    await p.goto(BASE + '/' + l);
    await p.click('.menu-btn'); checks++;
    if (!(await p.evaluate(() => document.querySelector('nav.menu').classList.contains('open')))) bad(l || 'fr/', 'menu does not open');
    await p.click('.menu-btn');
    await p.click('.util .sub-open'); checks++;
    if (!(await p.isVisible('#sub .subin'))) bad(l || 'fr/', 'newsletter box does not open');
    await p.click('#sub .sub-x'); checks++;
    if (await p.isVisible('#sub .subin')) bad(l || 'fr/', 'newsletter box does not close');
    const forms = await p.evaluate(() => [...new Set([...document.querySelectorAll('a[href*="forms.cloud.microsoft"]')].map(a => a.href))]); checks++;
    if (forms.length !== 1) bad(l || 'fr/', 'expected one form link per page, got', forms.join(' '));
    await p.close();
  }
  await b.close();
  console.log(fails ? `${fails} problem(s) in ${checks} checks` : `OK: ${checks} checks passed`);
  process.exit(fails ? 1 : 0);
})();
