# Build homes.yosoycaroluna.com from the approved CarosellsNJ site.
# Usage: python3 build.py <dir-with-downloaded-originals>
import re, sys, os, hashlib, base64, io, tarfile
D = sys.argv[1]
HOST = "homes." + "yosoycaroluna" + ".com"
HUB = "https://" + "yosoycaroluna" + ".com/"
GF = "https://docs.google.com/forms/d/e/1FAIpQLSfRm0VMJ7vJcBIPCGSrK-NytacYRRy0o_SVX79Du8reZAmHdg/formResponse"

def rd(p): return open(os.path.join(D, p), encoding="utf-8").read()
def wr(p, s): open(os.path.join(D, p), "w", encoding="utf-8").write(s)
def sub(s, old, new, n=1, label=""):
    c = s.count(old)
    if c != n: raise SystemExit(f"PATCH FAILED [{label}]: expected {n}, found {c}: {old[:70]!r}")
    return s.replace(old, new)

# Strip the per-request Cloudflare script and verify originals are the approved version
h = re.sub(r'<script>\(function\(\)\{function c\(\)\{var b=a\.contentDocument.*?</script>', '', rd("index.html"), flags=re.S)
wr("index.html", h)
SUMS = {
 "index.html": "54613704aaa6762b33beab8cc9384f9130604e916d0af7aec1fe34306cd197b9",
 "_next/static/chunks/page-cPYjA9V1.js": "2e20cc7c9203a95e8ebdb0c216ffc27719a16925190ee3ef484a25753b6b3f11",
}
for p, want in SUMS.items():
    got = hashlib.sha256(open(os.path.join(D, p), "rb").read()).hexdigest()
    if got != want: raise SystemExit(f"CHECKSUM FAILED {p}: {got}")

EN_ABOUT_OLD = "Based in Sayreville and serving Central and North Jersey, including Monmouth and Ocean counties, I work in English and Spanish"
EN_ABOUT_NEW = "Based in Sayreville, serving Central Jersey and North Jersey. I work in English and Spanish"
ES_ABOUT_OLD = "Desde Sayreville, acompaño a clientes en el centro y norte de New Jersey, incluyendo los condados de Monmouth y Ocean en español e inglés, con honestidad, comunicación clara y respeto por tus metas y presupuesto."
ES_ABOUT_NEW = "Desde Sayreville, te acompaño a comprar, vender e invertir en el centro y norte de New Jersey, con honestidad y claridad. Trabajo en español e inglés, con respeto por tus metas y tu presupuesto."
EN_COV = "Based in Sayreville, serving Central Jersey and North Jersey. Honest guidance for buying, selling, and investing."
ES_COV = "Desde Sayreville, te acompaño a comprar, vender e invertir en el centro y norte de New Jersey, con honestidad y claridad."
EN_TITLE = "CarosellsNJ | Your home. Your investment. Your agent."
ES_TITLE = "CarosellsNJ | Tu hogar. Tu inversión. Tu agente."
EN_DESC = "Based in Sayreville, serving Central Jersey and North Jersey. Honest guidance for buying, selling, and investing with Carolina Gómez. Free homebuyer checklists, smart questions and seller guides. English & Español."
ES_DESC = "Desde Sayreville, te acompaño a comprar, vender e invertir en el centro y norte de New Jersey, con honestidad y claridad. Guías gratis para compradores y vendedores. Español e inglés."
OLD_DESC_CORE = "Buy, sell, and invest across Central and North Jersey, including Monmouth and Ocean counties with Carolina Gómez. Honest guidance, transparent communication. Free homebuyer checklists, smart questions and seller guides. English "
NEW_DESC_CORE = "Based in Sayreville, serving Central Jersey and North Jersey. Honest guidance for buying, selling, and investing with Carolina Gómez. Free homebuyer checklists, smart questions and seller guides. English "
BACK_EN = "← Back to YoSoyCaroluna.com"
BACK_ES = "← Volver a YoSoyCaroluna.com"

# ---------------- page component (JS) ----------------
P = "_next/static/chunks/page-cPYjA9V1.js"
j = rd(P)
def k(en, es): return "k(`" + en + "`,`" + es + "`)"
R = [
 # language: ?lang=es support, html lang, title, description, keep address in sync
 ("(0,l.useEffect)(()=>{document.documentElement.lang=e?`es`:`en`},[e])",
  "(0,l.useEffect)(()=>{new URLSearchParams(location.search).get(`lang`)===`es`&&t(!0)},[]),(0,l.useEffect)(()=>{document.documentElement.lang=e?`es`:`en`;document.title=e?`" + ES_TITLE + "`:`" + EN_TITLE + "`;let q1=document.querySelector(`meta[name=description]`);q1&&q1.setAttribute(`content`,e?`" + ES_DESC + "`:`" + EN_DESC + "`);let q2=new URL(location.href);e?q2.searchParams.set(`lang`,`es`):q2.searchParams.delete(`lang`);history.replaceState(history.state,``,q2)},[e])", "lang"),
 # lead capture: Google Forms + static PDF on this domain
 ("let t=await fetch(`/api/leads`,{method:`POST`,headers:{\"Content-Type\":`application/json`},body:JSON.stringify({...n,resource:o,language:e?`es`:`en`,marketing:n.marketing===`on`})}),r=await t.json();if(!t.ok)throw Error(r.error);D(r.url)",
  "if(n.website)throw Error(`spam`);await fetch(`" + GF + "`,{method:`POST`,mode:`no-cors`,body:new URLSearchParams({emailAddress:n.email,\"entry.476372974\":n.name,\"entry.1998817934\":n.phone||``,\"entry.707611092\":n.town,\"entry.1055198748\":n.interest,\"entry.2075080002\":n.timeline,\"entry.1614501267\":o,\"entry.1673376902\":e?`es`:`en`,\"entry.937219708\":n.marketing===`on`?`yes`:`no`,\"entry.1966070625\":location.href})});D(`/guides/CarosellsNJ-`+o+`-`+(e?`es`:`en`)+`.pdf`)", "submit"),
 ("f(e instanceof Error?e.message:`Please try again.`)",
  "f(" + k("We couldn’t save your request. Please check your connection and try again.", "No pudimos guardar tu solicitud. Revisa tu conexión e inténtalo de nuevo.") + ")", "error"),
 # translations of fixed labels
 ("children:`REAL ESTATE WITH CAROLINA GÓMEZ`", "children:" + k("REAL ESTATE WITH CAROLINA GÓMEZ", "BIENES RAÍCES CON CAROLINA GÓMEZ"), "logo"),
 ("\"aria-label\":`Switch language`", "\"aria-label\":" + k("Switch language", "Cambiar idioma"), "aria lang"),
 ("\"aria-label\":`Toggle navigation`", "\"aria-label\":" + k("Toggle navigation", "Abrir o cerrar el menú"), "aria menu"),
 ("alt:`Carolina Gómez, your New Jersey real estate agent`", "alt:" + k("Carolina Gómez, your New Jersey real estate agent", "Carolina Gómez, tu agente inmobiliaria en New Jersey"), "alt hero"),
 ("(0,T.jsx)(`small`,{children:`YOUR NEW JERSEY AGENT`})", "(0,T.jsx)(`small`,{children:" + k("YOUR NEW JERSEY AGENT", "TU AGENTE EN NEW JERSEY") + "})", "portrait label"),
 ("` NEW JERSEY REAL ESTATE · ENGLISH + ESPAÑOL`", k(" NEW JERSEY REAL ESTATE · ENGLISH + ESPAÑOL", " BIENES RAÍCES EN NEW JERSEY · ESPAÑOL + ENGLISH"), "eyebrow hero"),
 ("children:[`Central Jersey `,(0,T.jsx)(`b`,{children:`✦`}),` North Jersey `,(0,T.jsx)(`b`,{children:`✦`}),` Monmouth `,(0,T.jsx)(`b`,{children:`✦`}),` Ocean`]",
  "children:e?[`Centro y norte de New Jersey`]:[`Central Jersey `,(0,T.jsx)(`b`,{children:`✦`}),` North Jersey`]", "townbar"),
 ("children:`A LITTLE CLARITY GOES A LONG WAY`", "children:" + k("A LITTLE CLARITY GOES A LONG WAY", "UN POCO DE CLARIDAD HACE LA DIFERENCIA"), "clarity"),
 ("alt:`Traditional detached home with a front porch and lawn`", "alt:" + k("Traditional detached home with a front porch and lawn", "Casa tradicional independiente con porche delantero y jardín"), "alt home1"),
 ("alt:`Spacious traditional home with shingle siding and a wraparound porch`", "alt:" + k("Spacious traditional home with shingle siding and a wraparound porch", "Casa tradicional amplia con revestimiento de tejas y porche envolvente"), "alt home2"),
 ("children:`THE NEXT-MOVE TOOLKIT`", "children:" + k("THE NEXT-MOVE TOOLKIT", "TU KIT PARA EL PRÓXIMO PASO"), "toolkit"),
 ("children:[`FREE PDF · `,e?`ESPAÑOL`:`ENGLISH`]", "children:[" + k("FREE PDF · ", "PDF GRATIS · ") + ",e?`ESPAÑOL`:`ENGLISH`]", "free pdf"),
 ("children:[t.n,` / THE NEXT-MOVE SERIES`]", "children:[t.n," + k(" / THE NEXT-MOVE SERIES", " / SERIE PRÓXIMO PASO") + "]", "series"),
 ("alt:`Carolina Gómez in a royal blue blouse, welcoming clients in New Jersey`", "alt:" + k("Carolina Gómez in a royal blue blouse, welcoming clients in New Jersey", "Carolina Gómez con blusa azul rey, dando la bienvenida en su oficina de New Jersey"), "alt about"),
 ("children:`MEET YOUR PERSON IN REAL ESTATE`", "children:" + k("MEET YOUR PERSON IN REAL ESTATE", "TU PERSONA DE CONFIANZA EN BIENES RAÍCES"), "meet"),
 ("children:`REAL QUESTIONS. CLEARER NEXT STEPS.`", "children:" + k("REAL QUESTIONS. CLEARER NEXT STEPS.", "PREGUNTAS REALES. PASOS MÁS CLAROS."), "faq eyebrow"),
 ("(0,T.jsx)(`span`,{children:`EMAIL`})", "(0,T.jsx)(`span`,{children:" + k("EMAIL", "CORREO") + "})", "email label"),
 ("`Carolina Gómez · New Jersey Real Estate Salesperson`", k("Carolina Gómez · New Jersey Real Estate Salesperson", "Carolina Gómez · Agente de bienes raíces (Real Estate Salesperson) en New Jersey"), "footer title"),
 ("`English + Español · @CarosellsNJ`", k("English + Español · @CarosellsNJ", "Español + English · @CarosellsNJ"), "footer langs"),
 ("`Central & North Jersey · Monmouth & Ocean`", k("Central Jersey & North Jersey", "Centro y norte de New Jersey"), "footer coverage"),
 ("children:`Cell: 347-784-7305`", "children:" + k("Cell: 347-784-7305", "Celular: 347-784-7305"), "footer cell"),
 ("children:`Office: 973-922-9578`", "children:" + k("Office: 973-922-9578", "Oficina: 973-922-9578"), "footer office"),
 ("(0,T.jsxs)(`div`,{children:[(0,T.jsx)(`button`,{onClick:()=>j(`privacy`),children:k(`Privacy`,`Privacidad`)}),(0,T.jsx)(`span`,{children:`Equal Housing Opportunity`})",
  "(0,T.jsxs)(`div`,{children:[(0,T.jsx)(`a`,{href:e?`" + HUB + "`:`" + HUB + "en.html`,children:" + k(BACK_EN, BACK_ES) + "}),(0,T.jsx)(`button`,{onClick:()=>j(`privacy`),children:k(`Privacy`,`Privacidad`)}),(0,T.jsx)(`span`,{children:" + k("Equal Housing Opportunity", "Igualdad de oportunidades en la vivienda") + "})", "footer back+eho"),
 ("\"aria-label\":`Close`", "\"aria-label\":" + k("Close", "Cerrar"), "aria close"),
 ("children:`YOUR INFORMATION`", "children:" + k("YOUR INFORMATION", "TUS DATOS"), "privacy eyebrow"),
 ("children:`A SMALL STEP. A SMARTER MOVE.`", "children:" + k("A SMALL STEP. A SMARTER MOVE.", "UN PEQUEÑO PASO. UNA DECISIÓN MÁS INTELIGENTE."), "form eyebrow"),
 ("children:[`Email *`,", "children:[" + k("Email *", "Correo electrónico *") + ",", "email field"),
 ("(0,T.jsx)(`option`,{children:`0–3 months / meses`})", "(0,T.jsx)(`option`,{value:`0-3 months`,children:" + k("0–3 months", "0–3 meses") + "})", "t1"),
 ("(0,T.jsx)(`option`,{children:`3–6 months / meses`})", "(0,T.jsx)(`option`,{value:`3-6 months`,children:" + k("3–6 months", "3–6 meses") + "})", "t2"),
 ("(0,T.jsx)(`option`,{children:`6–12 months / meses`})", "(0,T.jsx)(`option`,{value:`6-12 months`,children:" + k("6–12 months", "6–12 meses") + "})", "t3"),
 # coverage text
 (EN_ABOUT_OLD, EN_ABOUT_NEW, "about en"),
 (ES_ABOUT_OLD, ES_ABOUT_NEW, "about es"),
 ("k(`Serving Central & North Jersey, including Monmouth & Ocean counties.`,`A tu servicio en el centro y norte de New Jersey, incluyendo Monmouth y Ocean.`)", k(EN_COV, ES_COV), "coverage intro"),
 # privacy: where requests are stored now
 ("Requests are stored in the site’s database.", "Requests are stored in Carolina’s private Google Forms account.", "privacy en"),
 ("Las solicitudes se guardan en la base de datos de la página.", "Las solicitudes se guardan en la cuenta privada de Google Forms de Carolina.", "privacy es"),
]
for item in R:
    old, new, label = item
    j = sub(j, old, new, 1, label)
for bad in ["Monmouth", "Ocean`", "/api/"]:
    if bad in j: raise SystemExit("LEFTOVER in JS: " + bad)
wr(P, j)

# ---------------- server-rendered HTML (English) ----------------
H = [
 ("<div>Central Jersey <b>✦</b> North Jersey <b>✦</b> Monmouth <b>✦</b> Ocean</div>", "<div>Central Jersey <b>✦</b> North Jersey</div>", 1),
 (EN_ABOUT_OLD, EN_ABOUT_NEW, 1),
 ("Serving Central &amp; North Jersey, including Monmouth &amp; Ocean counties.", EN_COV, 1),
 ("Central &amp; North Jersey · Monmouth &amp; Ocean", "Central Jersey &amp; North Jersey", 1),
 ("<div><button>Privacy</button>", "<div><a href=\"" + HUB + "en.html\">" + BACK_EN + "</a><button>Privacy</button>", 1),
 (OLD_DESC_CORE, NEW_DESC_CORE, 2),
 ("<meta charSet=\"utf-8\"/>", "<meta charSet=\"utf-8\"/><link rel=\"canonical\" href=\"https://" + HOST + "/\"/><link rel=\"alternate\" hreflang=\"en\" href=\"https://" + HOST + "/\"/><link rel=\"alternate\" hreflang=\"es\" href=\"https://" + HOST + "/?lang=es\"/><link rel=\"alternate\" hreflang=\"x-default\" href=\"https://" + HOST + "/\"/><meta property=\"og:type\" content=\"website\"/><meta property=\"og:site_name\" content=\"CarosellsNJ\"/><meta property=\"og:title\" content=\"" + EN_TITLE + "\"/><meta property=\"og:description\" content=\"" + EN_DESC.replace("&", "&amp;") + "\"/><meta property=\"og:url\" content=\"https://" + HOST + "/\"/><meta property=\"og:image\" content=\"https://" + HOST + "/images/carolina-welcome-office.png\"/>", 1),
]
for old, new, n in H:
    h = sub(h, old, new, n, "html")
if "Monmouth" in h or "Ocean" in h: raise SystemExit("LEFTOVER in HTML")
wr("index.html", h)

# ---------------- PDFs, robots, sitemap, CNAME ----------------
os.makedirs(os.path.join(D, "guides"), exist_ok=True)
tar = tarfile.open(fileobj=io.BytesIO(base64.b64decode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "guides.b64")).read())), mode="r:gz")
for m in tar.getmembers():
    if m.isfile() and re.fullmatch(r"CarosellsNJ-(buyer|questions|seller)-(en|es)\.pdf", m.name):
        open(os.path.join(D, "guides", m.name), "wb").write(tar.extractfile(m).read())
wr("robots.txt", "User-agent: *\nAllow: /\nSitemap: https://" + HOST + "/sitemap.xml\n")
wr("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
   + ''.join(f'  <url><loc>https://{HOST}/{q}</loc><xhtml:link rel="alternate" hreflang="en" href="https://{HOST}/"/><xhtml:link rel="alternate" hreflang="es" href="https://{HOST}/?lang=es"/></url>\n' for q in ["", "?lang=es"]).replace("&", "&amp;")
   + '</urlset>\n')
wr("CNAME", HOST + "\n")
open(os.path.join(D, ".nojekyll"), "w").close()
print("BUILD OK")
