# -*- coding: utf-8 -*-
"""Duroosi static site generator. Run: cd ~/workspace/duroosi && python3 tools/build.py"""
import os, shutil, sys, re

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from data import SITE, GRADES, TERMS
from subjects import SUBJECTS

BASE_URL = "https://duroosi.example.com"  # <-- replace with real domain before deploy
OUT = os.path.join(os.path.dirname(__file__), "..", "out")
TOOLS = os.path.dirname(__file__)

def url_for(*parts):
    return "/" + "/".join(parts) + "/"

def grade_slug(g): return g["slug"]
def term_slug(t): return t["slug"]

def subjects_for_grade(gn):
    return [s for s in SUBJECTS if gn in s["grades"]]

# ---------- chrome ----------
def header_html(active="home"):
    links = [f'<a href="/" class="{"active" if active=="home" else ""}">الرئيسية</a>']
    for g in GRADES:
        links.append(f'<a href="{url_for(g["slug"])}" class="{"active" if active==g["slug"] else ""}">الصف {g["word"]}</a>')
    nav = "\n".join(links)
    return f"""<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="brand"><span class="brand-mark">د</span><span>{SITE["name"]}<small>{SITE["tagline"]}</small></span></a>
    <button class="nav-toggle" onclick="document.querySelector('.main-nav').classList.toggle('open')" aria-label="القائمة">☰</button>
    <nav class="main-nav">{nav}</nav>
  </div>
</header>"""

def footer_html():
    grade_links = "\n".join(f'<li><a href="{url_for(g["slug"])}">الصف {g["word"]} الابتدائي</a></li>' for g in GRADES)
    subj_links = "\n".join(f'<li><a href="{url_for(GRADES[0]["slug"], TERMS[0]["slug"], s["slug"])}">{s["name"]} — الصف الأول</a></li>' for s in subjects_for_grade(1))
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <h4>{SITE["name"]}</h4>
      <p style="font-size:.92rem">منصة تعليمية مستقلة تجمع مناهج المرحلة الابتدائية السعودية: الكتب الدراسية وأدلة الحلول وشروحات الدروس ونماذج الاختبارات، للصفوف من الأول إلى السادس الابتدائي في الفصول الدراسية الثلاثة.</p>
    </div>
    <div>
      <h4>الصفوف الدراسية</h4>
      <ul>{grade_links}</ul>
    </div>
    <div>
      <h4>مواد الصف الأول</h4>
      <ul>{subj_links}</ul>
    </div>
    <div>
      <h4>روابط سريعة</h4>
      <ul>
        <li><a href="/عن-المنصة/">عن المنصة</a></li>
        <li><a href="/اتصل-بنا/">اتصل بنا</a></li>
        <li><a href="/سياسة-الخصوصية/">سياسة الخصوصية</a></li>
        <li><a href="/إخلاء-المسؤولية/">إخلاء المسؤولية</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">جميع حقوق الكتب والمناهج محفوظة لوزارة التعليم في المملكة العربية السعودية. {SITE["name"]} منصة مستقلة لا تتبع أي جهة حكومية. © 2026 {SITE["name"]}</div>
</footer>
<script>
document.querySelectorAll('.nav-toggle').forEach(b=>b.addEventListener('click',()=>document.querySelector('.main-nav').classList.toggle('open')));
</script>"""

def breadcrumb(items):
    # items: list of (label, url|None)
    parts = []
    for label, u in items:
        parts.append(f'<a href="{u}">{label}</a>' if u else f'<span>{label}</span>')
    return '<nav class="breadcrumb container">' + '<span class="sep">←</span>'.join(parts) + '</nav>'

def base(title, desc, canonical, body, active="home", crumbs=None, extra_head=""):
    crumb_html = breadcrumb(crumbs) if crumbs else ""
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE_URL}{canonical}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{extra_head}
</head>
<body>
{header_html(active)}
{crumb_html}
{body}
{footer_html()}
</body>
</html>"""

def faq_html(faqs):
    items = "\n".join(
        f'<details><summary>{q}</summary><div class="faq-body"><p>{a}</p></div></details>'
        for q, a in faqs)
    return f'<div class="faq">{items}</div>'

def write_page(rel_path, html):
    full = os.path.join(OUT, rel_path, "index.html") if not rel_path.endswith(".xml") and not rel_path.endswith(".txt") else os.path.join(OUT, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)

# ---------- homepage ----------
def homepage():
    grade_cards = "\n".join(
        f'''<a href="{url_for(g["slug"])}" class="grade-card">
          <div class="grade-num">{g["n"]}</div>
          <h3>الصف {g["word"]} الابتدائي</h3>
          <p>{g["focus"]}</p>
        </a>''' for g in GRADES)
    body = f"""
<section class="hero">
  <div class="container hero-inner">
    <h1>مناهج المرحلة الابتدائية السعودية — كل الصفوف والفصول</h1>
    <p>دروسي يجمع لك الكتب الدراسية الرسمية وأدلة الحلول وشروحات الدروس ونماذج الاختبارات للصفوف من الأول إلى السادس الابتدائي، في الفصول الدراسية الثلاثة — في مكان واحد.</p>
    <div class="hero-tags">
      <a href="{url_for(GRADES[0]['slug'])}">الصف الأول</a>
      <a href="{url_for(GRADES[3]['slug'])}">الصف الرابع</a>
      <a href="{url_for(GRADES[5]['slug'])}">الصف السادس</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="section-title">اختر الصف الدراسي</h2>
    <p class="section-sub">ستجد لكل صف المواد الدراسية مقسمة على الفصول الثلاثة: الكتاب المدرسي، دليل الحلول، شروحات الدروس، ونماذج الاختبارات.</p>
    <div class="grade-grid">{grade_cards}</div>
  </div>
</section>

<section class="section" style="background:#fff">
  <div class="container">
    <h2 class="section-title">ماذا يقدم موقع دروسي؟</h2>
    <p class="section-sub">كل ما يحتاجه طالب المرحلة الابتدائية وولي أمره ومعلمه، منظماً حسب الصف والفصل والمادة.</p>
    <div class="subject-grid">
      <div class="subject-card"><div class="subject-icon">📚</div><h3>الكتب الدراسية</h3><p>دليل الوصول إلى الكتب الرسمية المعتمدة من وزارة التعليم لكل صف وفصل، مع شرح طريقة التحميل من البوابات الرسمية.</p></div>
      <div class="subject-card"><div class="subject-icon">✅</div><h3>أدلة الحلول</h3><p>حلول نموذجية منظمة لتمارين الكتب المدرسية تساعد الطالب على التحقق من إجاباته وفهم خطوات الحل.</p></div>
      <div class="subject-card"><div class="subject-icon">💡</div><h3>شروحات الدروس</h3><p>شرح مبسط لكل درس بأمثلة إضافية، يبني الفهم قبل الحفظ ويناسب مختلف مستويات الطلاب.</p></div>
      <div class="subject-card"><div class="subject-icon">📝</div><h3>نماذج الاختبارات</h3><p>نماذج اختبارات تجريبية تحاكي أسلوب الأسئلة الرسمية لتدريب الطالب على الاختبار الحقيقي بثقة.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="article">
      <h2>لماذا يثق أولياء الأمور بموقع دروسي؟</h2>
      <p class="lead">لأننا نركز على شيء واحد ونفعله بإتقان: تنظيم المنهج السعودي للمرحلة الابتدائية بشكل واضح وسهل الوصول.</p>
      <p>يعتمد نظام التعليم في المملكة العربية السعودية على <strong>ثلاثة فصول دراسية</strong> في العام الواحد، ويتوزع محتوى كل مادة على هذه الفصول. كثير من أولياء الأمور يجدون صعوبة في متابعة الكتب والحلول والاختبارات لكل فصل على حدة — وهنا يأتي دور دروسي: نرتب لك كل شيء حسب <strong>الصف الدراسي</strong> ثم <strong>الفصل الدراسي</strong> ثم <strong>المادة</strong>، فتصل إلى ما تريد بضغطات قليلة.</p>
      <p>نلتزم في دروسي بمحتوى <strong>أصلي ومكتوب بعناية</strong>: الشروحات والأدلة من إعداد فريقنا، أما الكتب الدراسية نفسها فحقوقها محفوظة بالكامل لوزارة التعليم، وندلك على الطرق الرسمية للحصول عليها دون أن ندعي ملكيتها.</p>
      <h2>كيف تستخدم الموقع؟</h2>
      <ol>
        <li><strong>اختر الصف الدراسي</strong> لطفلك من البطاقات أعلاه (من الأول إلى السادس الابتدائي).</li>
        <li><strong>اختر الفصل الدراسي</strong> الحالي: الأول أو الثاني أو الثالث.</li>
        <li><strong>اختر المادة</strong> وستجد صفحة متكاملة: معلومات الكتاب وطريقة تحميله رسمياً، ودليل الحلول، وشروحات الدروس، ونماذج الاختبارات، ونصائح المذاكرة.</li>
      </ol>
      <div class="info-box"><p><strong>نصيحة للآباء:</strong> أفضل وقت لبدء متابعة المنهج هو الأسبوع الأول من كل فصل. راجع صفحة المادة الخاصة بطفلك لتتعرف على المهارات المطلوبة وخطة المذاكرة المقترحة.</p></div>
      <h2>أسئلة شائعة</h2>
      {faq_html([
        ("هل موقع دروسي مجاني؟", "نعم، جميع صفحات الموقع ومحتواه مجاني بالكامل ولا يتطلب تسجيلاً أو اشتراكاً."),
        ("هل الكتب الدراسية متوفرة للتحميل من الموقع؟", "الكتب الدراسية حقوقها لوزارة التعليم، لذلك ندلك في كل صفحة مادة على الطريقة الرسمية للحصول على الكتاب من البوابات التعليمية المعتمدة (مثل بوابة عين)، مع شرح الخطوات بالتفصيل."),
        ("ما الفرق بين دليل الحلول وشرح الدروس؟", "دليل الحلول يقدم إجابات نموذجية لتمارين الكتاب، بينما شرح الدروس يشرح المفهوم نفسه بأمثلة إضافية. ننصح بالبدء بالشرح للفهم ثم استخدام الحلول للتحقق."),
        ("هل المحتوى محدث حسب أحدث المناهج؟", "نعم، نراجع المحتوى دورياً لمواكبة أي تحديثات تصدرها وزارة التعليم على المناهج الدراسية."),
        ("هل الموقع تابع لوزارة التعليم؟", "لا، دروسي منصة مستقلة تماماً ولا تتبع أي جهة حكومية ولا تمثلها."),
      ])}
    </div>
  </div>
</section>"""
    return base(
        "دروسي | مناهج المرحلة الابتدائية السعودية — كتب وحلول وشروحات",
        SITE["desc"],
        "/", body, active="home",
        extra_head='<meta property="og:title" content="دروسي | مناهج المرحلة الابتدائية السعودية">')

# ---------- grade hub ----------
def grade_page(g):
    terms_cards = "\n".join(
        f'''<a href="{url_for(g["slug"], t["slug"])}" class="subject-card">
          <div class="subject-icon">🗓️</div>
          <h3>{t["name"]}</h3>
          <p>{t["framing"][:110]}...</p>
          <span class="go">عرض مواد {t["short"]} ←</span>
        </a>''' for t in TERMS)
    subj_names = "، ".join(s["name"] for s in subjects_for_grade(g["n"]))
    body = f"""
<section class="section">
  <div class="container">
    <div class="article">
      <span class="badge">المرحلة الابتدائية</span>
      <h1>منهج الصف {g["word"]} الابتدائي — الفصول الدراسية الثلاثة</h1>
      <p class="lead">{g["about"]}</p>
      <div class="info-box"><p><strong>تركيز هذا الصف:</strong> {g["focus"]}.</p></div>
      <h2>مواد الصف {g["word"]} الابتدائي</h2>
      <p>يدرس طالب الصف {g["word"]} الابتدائي المواد التالية: {subj_names}. اختر الفصل الدراسي أدناه لعرض كل مادة على حدة مع كتابها ودليل حلولها وشروحاتها ونماذج اختباراتها.</p>
      <h2>اختر الفصل الدراسي</h2>
      <div class="subject-grid">{terms_cards}</div>
      <h2>نصائح لولي الأمر</h2>
      <p>{g["tips"]}</p>
      <h2>أسئلة شائعة عن الصف {g["word"]} الابتدائي</h2>
      {faq_html([
        (f'ما مواد الصف {g["word"]} الابتدائي في السعودية؟', f'مواد الصف {g["word"]} الابتدائي هي: {subj_names}.'),
        (f'كم فصلاً دراسياً في الصف {g["word"]} الابتدائي؟', 'ثلاثة فصول دراسية حسب نظام وزارة التعليم، ويتوزع محتوى كل مادة عليها. ستجد في موقعنا صفحة مستقلة لكل مادة في كل فصل.'),
        (f'أين أجد حلول كتب الصف {g["word"]} الابتدائي؟', f'اختر الفصل الدراسي ثم المادة من هذه الصفحة، وستجد دليل الحلول وشروحات الدروس ونماذج الاختبارات لكل مادة.'),
      ])}
    </div>
  </div>
</section>"""
    return base(
        f"منهج الصف {g['word']} الابتدائي | كتب وحلول وشروحات الفصول الثلاثة — دروسي",
        f"كل ما يخص الصف {g['word']} الابتدائي في السعودية: مواد {subj_names}، الكتب الدراسية وأدلة الحلول وشروحات الدروس ونماذج الاختبارات للفصول الثلاثة.",
        url_for(g["slug"]), body, active=g["slug"],
        crumbs=[("الرئيسية", "/"), (f"الصف {g['word']} الابتدائي", None)])

# ---------- term page ----------
def term_page(g, t):
    subs = subjects_for_grade(g["n"])
    cards = "\n".join(
        f'''<a href="{url_for(g["slug"], t["slug"], s["slug"])}" class="subject-card">
          <div class="subject-icon">{s["icon"]}</div>
          <h3>{s["name"]}</h3>
          <p>{s["tagline"]}</p>
          <span class="go">عرض صفحة المادة ←</span>
        </a>''' for s in subs)
    body = f"""
<section class="section">
  <div class="container">
    <div class="article">
      <span class="badge">{t["name"]}</span>
      <h1>مواد الصف {g["word"]} الابتدائي — {t["name"]}</h1>
      <p class="lead">{t["framing"]}</p>
      <div class="info-box"><p><strong>خطة مقترحة لهذا الفصل:</strong> {t["plan"]}</p></div>
      <h2>مواد {t["short"]} للصف {g["word"]} الابتدائي</h2>
      <p>اختر المادة لعرض صفحتها المتكاملة: معلومات الكتاب وطريقة الحصول عليه رسمياً، دليل الحلول، شروحات الدروس، نماذج الاختبارات، ونصائح المذاكرة.</p>
      <div class="subject-grid">{cards}</div>
      <h2>أسئلة شائعة</h2>
      {faq_html([
        (f'ما مواد {t["short"]} للصف {g["word"]} الابتدائي؟', f'مواد {t["short"]} هي: {"، ".join(s["name"] for s in subs)}.'),
        ("كيف أحمّل الكتب الدراسية الرسمية؟", "الكتب حقوقها لوزارة التعليم. في صفحة كل مادة ستجد شرحاً مفصلاً لخطوات الحصول على الكتاب من البوابات الرسمية المعتمدة مثل بوابة عين."),
        ("متى تبدأ اختبارات نهاية الفصل؟", "تُعلن وزارة التعليم التقويم الدراسي كل عام بالمواعيد الدقيقة. ننصح ببدء المراجعة قبل الاختبارات بأسبوعين على الأقل باستخدام نماذج الاختبارات في صفحات المواد."),
      ])}
    </div>
  </div>
</section>"""
    return base(
        f"مواد الصف {g['word']} الابتدائي {t['short']} | دروسي",
        f"جميع مواد الصف {g['word']} الابتدائي {t['short']} في السعودية: {', '.join(s['name'] for s in subs)} — الكتب وأدلة الحلول والشروحات ونماذج الاختبارات.",
        url_for(g["slug"], t["slug"]), body, active=g["slug"],
        crumbs=[("الرئيسية", "/"), (f"الصف {g['word']} الابتدائي", url_for(g["slug"])), (t["short"], None)])

# ---------- subject page ----------
def subject_page(g, t, s):
    book_full = f"{s['book']} للصف {g['word']} الابتدائي — {t['short']}"
    skills = "\n".join(f"<li>{x}</li>" for x in s["skills"])
    related = [x for x in subjects_for_grade(g["n"]) if x["slug"] != s["slug"]][:4]
    related_html = "\n".join(
        f'<a href="{url_for(g["slug"], t["slug"], x["slug"])}" class="subject-card"><div class="subject-icon">{x["icon"]}</div><h3>{x["name"]}</h3><p>{x["tagline"]}</p><span class="go">عرض ←</span></a>'
        for x in related)
    other_terms = [x for x in TERMS if x["n"] != t["n"]]
    other_terms_html = "، ".join(f'<a href="{url_for(g["slug"], x["slug"], s["slug"])}">{s["name"]} {x["short"]}</a>' for x in other_terms)
    body = f"""
<section class="section">
  <div class="container">
    <div class="article">
      <span class="badge">{s["name"]} • الصف {g["word"]} • {t["short"]}</span>
      <h1>{s["name"]} للصف {g["word"]} الابتدائي — {t["short"]}</h1>
      <p class="lead">{s["overview"]}</p>
      <p>في هذه الصفحة تجد كل ما يخص مادة {s["name"]} للصف {g["word"]} الابتدائي في {t["name"]}: معلومات {book_full} وطريقة الحصول عليه من المصادر الرسمية، ودليل الحلول، وشروحات الدروس، ونماذج الاختبارات، مع نصائح عملية للمذاكرة.</p>

      <h2>تحميل {book_full}</h2>
      <div class="dl-box">
        <h3>📥 {book_full} (الطبعة المعتمدة)</h3>
        <p>الكتب الدراسية حقوق نشرها محفوظة لوزارة التعليم في المملكة العربية السعودية. للحصول على النسخة الرسمية بصيغة PDF اتبع الخطوات التالية عبر بوابة عين التعليمية:</p>
      </div>
      <ol>
        <li>ادخل إلى <strong>بوابة عين التعليمية</strong> (ien.edu.sa) التابعة لوزارة التعليم.</li>
        <li>اختر <strong>المرحلة الابتدائية</strong> ثم <strong>الصف {g["word"]}</strong>.</li>
        <li>اختر <strong>{t["name"]}</strong> من قائمة الفصول.</li>
        <li>اختر مادة <strong>{s["name"]}</strong> ثم اضغط تحميل الكتاب بصيغة PDF.</li>
      </ol>
      <div class="warn-box"><p><strong>ملاحظة:</strong> ننصح دائماً بالاعتماد على النسخة الرسمية من البوابات المعتمدة لضمان حصولك على أحدث طبعة معتمدة من الوزارة.</p></div>

      <h2>دليل حلول {s["name"]} — {t["short"]}</h2>
      <p>دليل الحلول يساعد الطالب على <strong>التحقق من إجاباته</strong> وفهم <strong>خطوات الحل الصحيحة</strong> لتمارين {s["book"]}. القاعدة الذهبية: حاول الحل بنفسك أولاً، ثم قارن إجابتك بالحل النموذجي، وعند وجود خطأ راجع الدرس المرتبط قبل الانتقال للتمرين التالي.</p>
      <p>نعمل على إعداد حلول نموذجية مفصلة لجميع تمارين {t["short"]} — تابع هذه الصفحة للتحديثات، واستخدم في الوقت الحالي شروحات الدروس أدناه لبناء الفهم الصحيح.</p>

      <h2>ماذا يتعلم الطالب في {s["name"]}؟</h2>
      <p>يركز منهج {s["name"]} للصف {g["word"]} الابتدائي في {t["short"]} على المهارات التالية:</p>
      <ul class="check-list">{skills}</ul>

      <h2>شروحات الدروس — طريقة المذاكرة الصحيحة</h2>
      <p>{s["study"]}</p>
      <div class="info-box"><p><strong>{t["short"]} تحديداً:</strong> {t["framing"]}</p></div>

      <h2>نماذج الاختبارات والاستعداد لها</h2>
      <p>{s["exam"]}</p>
      <p>نصيحة عامة لاختبارات {t["short"]}: {t["plan"]}</p>

      <h2>أسئلة شائعة عن {s["name"]} للصف {g["word"]}</h2>
      {faq_html(s["faq"])}

      <h2>مواد أخرى للصف {g["word"]} — {t["short"]}</h2>
      <div class="subject-grid">{related_html}</div>
      <p style="margin-top:20px">تابع مادة {s["name"]} في الفصول الأخرى: {other_terms_html}.</p>
    </div>
  </div>
</section>"""
    return base(
        f"{s['name']} الصف {g['word']} الابتدائي {t['short']} | الكتاب والحلول والشروحات — دروسي",
        f"{book_full}: طريقة التحميل الرسمية، دليل الحلول، شروحات الدروس، نماذج الاختبارات ونصائح المذاكرة — كل ما يخص مادة {s['name']} للصف {g['word']} الابتدائي {t['short']}.",
        url_for(g["slug"], t["slug"], s["slug"]), body, active=g["slug"],
        crumbs=[("الرئيسية", "/"), (f"الصف {g['word']} الابتدائي", url_for(g["slug"])), (t["short"], url_for(g["slug"], t["slug"])), (s["name"], None)])

# ---------- legal pages ----------
def legal_page(slug, title, desc, h1, paragraphs):
    body = '<section class="section"><div class="container"><div class="article">'
    body += f"<h1>{h1}</h1>" + "".join(f"<p>{p}</p>" for p in paragraphs)
    body += "</div></div></section>"
    return base(f"{title} — دروسي", desc, f"/{slug}/", body,
                crumbs=[("الرئيسية", "/"), (title, None)])

def make_relative():
    """Rewrite root-absolute href/src to depth-relative so the site works both
    at a domain root and under a subpath (e.g. GitHub Pages /Kottby/)."""
    import glob
    for f in glob.glob(os.path.join(OUT, "**", "index.html"), recursive=True):
        reldir = os.path.dirname(os.path.relpath(f, OUT))
        d = 0 if not reldir else len(reldir.split(os.sep))
        prefix = "../" * d
        with open(f, encoding="utf-8") as fh:
            h = fh.read()
        def repl(m):
            attr, p = m.group(1), m.group(2)
            if p == "/":
                return f'{attr}="{prefix or "./"}"'
            return f'{attr}="{prefix}{p[1:]}"'
        h = re.sub(r'(href|src)="(/[^"]*)"', repl, h)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(h)

def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    # assets
    shutil.copytree(os.path.join(TOOLS, "assets"), os.path.join(OUT, "assets"))
    with open(os.path.join(OUT, "assets", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0e7c5b"/><text x="32" y="44" font-size="36" text-anchor="middle" fill="#fff" font-family="sans-serif">د</text></svg>')

    urls = []
    def add(path, html):
        write_page(path, html)
        loc = path if path else ""
        urls.append(loc)

    add("", homepage())
    for g in GRADES:
        add(g["slug"], grade_page(g))
        for t in TERMS:
            add(f"{g['slug']}/{t['slug']}", term_page(g, t))
            for s in subjects_for_grade(g["n"]):
                add(f"{g['slug']}/{t['slug']}/{s['slug']}", subject_page(g, t, s))

    add("عن-المنصة", legal_page("عن-المنصة", "عن المنصة",
        "تعرف على منصة دروسي: من نحن، وماذا نقدم لطلاب المرحلة الابتدائية السعودية وأولياء أمورهم.",
        "عن منصة دروسي",
        ["دروسي منصة تعليمية عربية مستقلة، هدفها تنظيم مناهج المرحلة الابتدائية في المملكة العربية السعودية وتقديمها بشكل واضح وسهل الوصول للطلاب وأولياء الأمور والمعلمين.",
         "نغطي الصفوف من الأول إلى السادس الابتدائي في الفصول الدراسية الثلاثة المعتمدة من وزارة التعليم، ونقدم لكل مادة: معلومات الكتاب الدراسي وطريقة الحصول عليه رسمياً، وأدلة الحلول، وشروحات الدروس، ونماذج الاختبارات.",
         "جميع الشروحات والأدلة في الموقع من إعداد فريقنا وبأسلوبنا الخاص. أما الكتب والمناهج الدراسية فحقوق نشرها محفوظة بالكامل لوزارة التعليم في المملكة العربية السعودية، ونحن لا ندعي ملكيتها ولا نتبع أي جهة حكومية ولا نمثلها."]))
    add("اتصل-بنا", legal_page("اتصل-بنا", "اتصل بنا",
        "تواصل مع فريق دروسي: اقتراحات، تصحيح معلومات، أو استفسارات حول محتوى الموقع.",
        "اتصل بنا",
        ["يسعدنا تواصلك معنا في أي وقت. يمكنك مراسلتنا عبر البريد الإلكتروني: <strong>info@duroosi.example.com</strong>.",
         "نرحب باقتراحاتكم حول مواد أو شروحات جديدة، كما نرحب بأي تصحيح لمعلومة وردت في الموقع — نراجع جميع الرسائل ونصحح الأخطاء أولاً بأول.",
         "ملاحظة: لا يمكننا تقديم الكتب الدراسية نفسها عبر البريد، لكننا ندلك دائماً على مصادرها الرسمية."]))
    add("سياسة-الخصوصية", legal_page("سياسة-الخصوصية", "سياسة الخصوصية",
        "سياسة الخصوصية لمنصة دروسي: البيانات التي نجمعها وكيفية استخدامها.",
        "سياسة الخصوصية",
        ["خصوصيتك تهمنا. موقع دروسي لا يطلب منك إنشاء حساب ولا يجمع بيانات شخصية عند تصفح المحتوى.",
         "قد نستخدم ملفات تعريف الارتباط (كوكيز) وخدمات تحليلية مثل Google Analytics لفهم كيفية استخدام الموقع وتحسينه، وقد تعرض إعلانات Google AdSense التي قد تستخدم الكوكيز لعرض إعلانات مناسبة.",
         "باستخدامك الموقع فأنت توافق على هذه السياسة. لأي استفسار حول الخصوصية راسلنا عبر صفحة اتصل بنا."]))
    add("إخلاء-المسؤولية", legal_page("إخلاء-المسؤولية", "إخلاء المسؤولية",
        "إخلاء المسؤولية: طبيعة المحتوى التعليمي في منصة دروسي وحقوق المناهج.",
        "إخلاء المسؤولية",
        ["المحتوى في موقع دروسي تعليمي واسترشادي، وقد يحتوي على أخطاء غير مقصودة رغم حرصنا على الدقة — نرجو إبلاغنا عن أي خطأ لتصحيحه.",
         "جميع الكتب والمناهج الدراسية المشار إليها في الموقع حقوق نشرها محفوظة بالكامل لوزارة التعليم في المملكة العربية السعودية.",
         "دروسي منصة مستقلة لا تتبع وزارة التعليم ولا أي جهة حكومية ولا تمثلها بأي شكل."]))

    # robots.txt
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")
    # sitemap.xml
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{BASE_URL}/{u}</loc><changefreq>monthly</changefreq></url>")
    sm.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm))

    make_relative()  # subpath-safe links (must run after all pages written)

    total = len(urls)
    print(f"Built {total} pages -> {OUT}")

if __name__ == "__main__":
    build()
