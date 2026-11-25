# 发布前自检清单 · Autocontrôle avant publication

每次网站改动，发布前按本清单逐项完成；全部通过才推送上线。改动尽量合并成一批，一次发布，附变更清单。
À chaque modification du site, suivre cette liste avant publication ; ne publier que si tout passe. Regrouper les modifications en un seul lot, publié une fois, avec la liste des changements.

## 1. 文字 · Textes

- [ ] 任何文字改动都已按 SK13 先列出具体替代词，并有主席的明确选择（在线程里可查）。
      Toute modification de texte a été proposée mot pour mot (SK13) et choisie explicitement par la Présidente.
- [ ] 六种语言事实一致，各语言按本文化习惯表达（SK12），只改被审阅的语言。
      Faits identiques dans les six langues, style propre à chaque langue (SK12) ; seule la langue relue est modifiée.
- [ ] 没有个人姓名、电话、私人邮箱（荣誉主席姓名已获同意）；没有 UNESCO、CNFU、马耳他十字等标志；不提可抵税链接；不把商业与公益相连（SK2、SK7）。
      Pas de nom, téléphone ou e-mail privé (sauf noms des présidents d'honneur, autorisés) ; aucun logo UNESCO, CNFU, croix de Malte ; aucun lien de défiscalisation ; jamais de lien commerce / solidarité (SK2, SK7).
- [ ] 改完后运行 `python3 -I tools/glossary.py`，更新用语表。
      Après modification : `python3 -I tools/glossary.py` pour régénérer le glossaire.

## 2. 自动检查 · Contrôles automatiques

```
python3 -I tools/generate.py               # 生成六语页面 · génère les pages
python3 -m http.server 8765 &              # 本地预览 · aperçu local
node tools/selfcheck.js                    # 必须显示 OK · doit afficher « OK »
```

`tools/selfcheck.js` 逐页检查（18 页 × 电脑 1280 / 手机 390 / 小屏 320，手机用微信浏览器标识）：
Le script vérifie chaque page (18 pages × 1280 / 390 / 320 px, mobile avec l'identifiant du navigateur WeChat) :

| 检查 · Contrôle | 为什么 · Pourquoi |
|---|---|
| 页面能打开，站内链接和锚点都有效 · pages en 200, liens et ancres internes valides | 不出现死链 · aucun lien mort |
| 任何宽度都没有横向滚动 · aucun défilement horizontal | 微信截图里出现过的问题 · défaut déjà vu dans WeChat |
| 文字放大到 125%、150%、200% 不溢出 · texte agrandi 125/150/200 % sans débordement | 长辈读者常开大字 · lecteurs âgés en grande police |
| 中文标题字体子集包含每一个标题字，没有缺字 · police chinoise : aucun caractère manquant | “相”“和”字曾用错字体 · « 相 » et « 和 » sont déjà sortis dans une autre police |
| 字体由本站提供，不请求 Google 等第三方（统计 GoatCounter 除外） · polices auto-hébergées, aucun appel tiers sauf GoatCounter | 中国大陆可正常显示；访客 IP 不外传（GDPR） · lisible depuis la Chine ; RGPD |
| 图片都能加载并有替代文字 · images chargées, avec texte alternatif | 无障碍 · accessibilité |
| 没有脚本错误 · aucune erreur JavaScript | |
| 手机菜单能打开；“订阅通讯”小框能打开和关闭；每页只链接本语言的一份表单 · menu mobile, fenêtre « abonnement » ouverture/fermeture, un seul formulaire par page (celui de la langue) | 按钮全部可用 · tous les boutons fonctionnent |

## 3. 人工检查 · Contrôles manuels

- [ ] 看截图：电脑版和手机版，中文与阿拉伯文（从右到左）各一页，版式对称、不拥挤（SK3）。
      Captures : ordinateur et mobile, au moins la page chinoise et la page arabe (droite à gauche) ; mise en page symétrique.
- [ ] 中文页手机截图检查标题断行：不在词语中间断开（如“热爱”）。
      Capture mobile chinoise : les titres ne se coupent jamais au milieu d'un mot.
- [ ] 上线后用微信打开 harmonie-amitie.com/zh/ 实测一次（由主席或顾问完成）。
      Après mise en ligne : test réel dans WeChat (par la Présidente ou le conseiller).

## 4. 发布 · Publication

- [ ] CHANGELOG.md 加一条中法双语记录。 · Une entrée bilingue dans CHANGELOG.md.
- [ ] 推送后确认部署成功：`gh run list -L1`。 · Vérifier le déploiement.
- [ ] 在线程里报告：变更清单、预览或截图、需要主席做的事。 · Rapport dans le fil : liste des changements, captures, actions attendues.

## 5. 每月例行 · Routine mensuelle

- [ ] 发布一条动态（每月一条即可，文字先经主席确认）。 · Une actualité par mois (texte validé par la Présidente).
- [ ] 五份表单各提交一次测试，确认邮件通知收到；导出回复（Excel）存档，再删除测试回复。
      Tester les cinq formulaires (une réponse chacun), vérifier la notification, exporter les réponses (Excel), supprimer les réponses de test.
- [ ] 看 GoatCounter 访问统计（语言、页面、手机占比），据此决定版面调整。首次：2026-12-09，用于决定首页 D、E、F 三项。
      Consulter GoatCounter (langues, pages, part mobile). Première revue : 2026-12-09, pour trancher D, E, F de la page d'accueil.
- [ ] 运行 `node tools/selfcheck.js` 一次，确认外部链接（表单）仍可打开。 · Lancer le script une fois et ouvrir les liens externes.

## 6. 中文标题字体 · Police des titres chinois

中文标题字体（Noto Serif SC）只包含页面实际用到的字。改中文标题后，`generate.py` 会自动重新下载子集（需联网）；若离线，会临时改用 Google 链接并给出警告，联网后再生成一次即可。
La police des titres chinois ne contient que les caractères utilisés. Après une modification, `generate.py` télécharge automatiquement le nouveau sous-ensemble ; hors ligne, il revient au lien Google avec un avertissement : relancer une fois connecté.
