# دروسي (Duroosi) — KSA Primary Curriculum Site

Static HTML site (Arabic RTL) covering the Saudi primary curriculum (grades 1–6, 3 terms):
- 173 pages: homepage, 6 grade hubs, 18 term pages, 144 subject pages, legal pages
- Sitemap: `out/sitemap.xml`, `out/robots.txt`

## Regenerate
```bash
cd ~/workspace/duroosi && python3 tools/build.py
```
Edit content in `tools/data.py` (grades/terms) and `tools/subjects.py` (subject profiles),
design in `tools/assets/style.css`, then rebuild. Output goes to `out/`.

## Deploy
Upload the contents of `out/` to any static host (GitHub Pages, Netlify, cPanel).
Before going live, replace `BASE_URL = "https://duroosi.example.com"` in `tools/build.py`
with the real domain and rebuild (updates canonicals + sitemap).

## Notes
- Design is original (emerald/amber theme), not a copy of any existing site.
- Book copyrights belong to the Saudi Ministry of Education; the site links to official
  sources (e.g. ien.edu.sa) and carries a disclaimer in the footer.
