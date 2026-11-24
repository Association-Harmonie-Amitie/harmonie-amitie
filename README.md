# harmonie-amitie.com

和谊协会 / Association Harmonie d'Amitié 官方网站（静态网站，GitHub Pages 托管）。
Site officiel de l'Association Harmonie d'Amitié (site statique hébergé sur GitHub Pages).

## 文件 · Fichiers
- `index.html` — 首页，中法双语切换 · page d'accueil bilingue
- `mentions-legales.html` — 法律声明 · mentions légales
- `404.html`, `robots.txt`, `sitemap.xml`, `favicon.svg`, `CNAME`, `img/`

## 更新方式 · Mise à jour
在项目里告诉 Claude 要改什么，Claude 修改并推送到本仓库，GitHub Pages 自动发布。
Demander la modification à Claude dans le projet ; Claude modifie et pousse sur ce dépôt, GitHub Pages publie automatiquement.

## 域名设置（IONOS）· DNS chez IONOS
- A @ → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
- CNAME www → association-harmonie-amitie.github.io
- 不要改动 MX 邮件记录 · Ne pas toucher aux enregistrements MX

## Six langues de l'ONU / 联合国六种语言

FR (racine /), 中文 (/zh/), EN (/en/), ES (/es/), RU (/ru/), العربية (/ar/, RTL).
Textes : `tools/content.py` · Gabarit : `tools/generate.py` · Style : `tools/style.css`.
Reconstruire / 重新生成 : `python3 -I tools/generate.py` (à la racine du dépôt).
EN/ES/RU/AR : traduction assistée par IA, à relire par un locuteur natif (bandeau affiché sur ces pages). 英、西、俄、阿语为 AI 辅助翻译，需母语人士审校，页面已显示提示。
