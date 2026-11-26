from pathlib import Path
from html import escape
from os import environ
from urllib.parse import urlsplit
from contact import contact_body
from inside import about, detail
from i18n import language_picker, localized_url, localize_html, runtime_copy
from translations import LANGUAGES

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dist"
SITE_URL = environ.get("SITE_URL", "").strip().rstrip("/")
site_origin = urlsplit(SITE_URL)
if SITE_URL and (site_origin.scheme not in ("https", "http") or not site_origin.netloc or site_origin.path or site_origin.query or site_origin.fragment):
    raise ValueError("SITE_URL must be a complete website origin, without a path or query.")

PATHS = {
    "right": '<path d="M4 12h15m-6-6 6 6-6 6"/>',
    "up-right": '<path d="M6 18 18 6M6.5 6H18v11.5"/>',
    "shield": '<path d="M12 2.5c2.6 1.8 5.5 2.7 8.3 3.2v5.7c0 4.3-2.9 7.6-8.3 10.1-5.4-2.5-8.3-5.8-8.3-10.1V5.7c2.9-.5 5.7-1.4 8.3-3.2Z"/><path d="m8.4 11.9 2.4 2.5 4.9-5.1"/>',
    "leaf": '<path d="M20.5 3.5c-2.2 1.5-4.8 1.7-7.5 1.8-6.3.2-9.4 3.4-9.3 7.7a6.7 6.7 0 0 0 6.8 6.6c7.5 0 10.3-6.9 10-16.1Z"/><path d="M3 21c2.4-3.8 5.3-7.4 11.7-11.5"/>',
    "people": '<circle cx="9.3" cy="7.3" r="3.5"/><path d="M2.7 20v-2.3a5.6 5.6 0 0 1 5.6-5.5h2a5.6 5.6 0 0 1 5.6 5.5V20M16 4.1a3.4 3.4 0 0 1 .2 6.4M17.6 12.9a4.9 4.9 0 0 1 3.6 4.8V20"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
    "close": '<path d="m5 5 14 14m0-14L5 19"/>',
    "pin": '<path d="M19 10c0 4.7-7 11-7 11S5 14.7 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2.3"/>',
}
def icon(name, cls=""):
    return f'<svg class="icon {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{PATHS[name]}</svg>'

SERVICES = [
    dict(slug="housekeeping", title="Housekeeping", image="/media/housekeeping.webp", alt="Een housekeeper maakt een bed op in een hotelkamer", description="Verzorgde hotelkamers en vakantiewoningen, klaar voor de volgende gast."),
    dict(slug="bouwoplevering", title="Bouwoplevering", image="/media/bouw.webp", alt="Zonlicht in een ruimte die wordt klaargemaakt voor de bouwoplevering", description="Een schone overdracht van uw bouwproject, afgestemd op de opleverdatum."),
    dict(slug="kantoren", title="Kantoren", image="/media/kantoor.webp", alt="Een schoonmaker neemt een bureau af met een microvezeldoek", description="Dagelijkse en periodieke schoonmaak van werkplekken, vloeren en sanitair."),
    dict(slug="particulier", title="Particulier", image="/media/specialistisch.webp", alt="Een medewerker reinigt een roestvrijstalen kookplaat", description="Van reguliere schoonmaak tot dieptereiniging van uw woning of vakantiehuis."),
]
NAV = [("Home", "/"), ("Diensten", "/diensten/"), ("Over ons", "/over-ons/"), ("Contact", "/contact/")]
QUOTE = "/contact/?aanvraag=offerte"

def header(active, route, language):
    links = "".join(f'<a href="{url}"' + (' aria-current="page"' if name == active else '') + f'>{name}</a>' for name,url in NAV)
    return f'''<a class="skip" href="#inhoud">Ga naar inhoud</a>
<header class="site-head"><div class="wrap topbar">
<a class="brand" href="/" aria-label="EWS Groep, home"><img src="/media/logo.png" alt="EWS Groep" width="411" height="145"></a>
<nav id="main-nav" class="main-nav" aria-label="Hoofdnavigatie">{links}<a class="nav-quote" href="{QUOTE}">Offerte aanvragen</a></nav>
<div class="top-actions"><a class="button head-quote" href="{QUOTE}">Offerte aanvragen {icon("up-right")}</a>
{language_picker(route, language)}
<button class="mobile-nav" aria-controls="main-nav" aria-expanded="false" aria-label="Menu openen">{icon('menu','hamburger')}{icon('close','cross')}</button></div>
</div></header>'''

def footer():
    return f'''<footer class="site-foot"><div class="wrap foot-grid"><div class="foot-brand"><a href="/" aria-label="EWS Groep, home"><img src="/media/logo-voet.png" alt="EWS Groep" width="411" height="145" loading="lazy"></a><p>Housekeeping voor hotels en vakantiewoningen.</p></div>
<div><h2>Ontdek EWS</h2>{''.join(f'<a href="{url}">{name}</a>' for name,url in NAV)}</div>
<div><h2>Diensten</h2>{''.join(f'<a href="/diensten/{s["slug"]}/">{s["title"]}</a>' for s in SERVICES)}</div>
<div><h2>Contact</h2><a href="tel:+31638997384">06 38 99 73 84</a><a href="mailto:info@ewsgroep.nl">info@ewsgroep.nl</a><address>Industrieweg 14<br>3846 BD Harderwijk</address></div></div>
<div class="wrap foot-end"><span>© 2026 EWS Groep B.V.</span><div><a href="https://www.ewsgroep.nl/privacy-policy">Privacyverklaring</a><a href="https://www.ewsgroep.nl/accessibility-statement">Algemene voorwaarden</a></div></div></footer>'''

def card(s):
    return f'''<a class="service-card" href="/diensten/{s["slug"]}/"><div class="card-photo"><img src="{s["image"]}" alt="{escape(s["alt"])}" loading="lazy" width="640" height="390"></div>
<div class="card-content"><div class="card-title"><h3>{s["title"]}</h3><span>{icon("up-right")}</span></div><p>{s["description"]}</p></div></a>'''

def offer_band():
    return f'''<section class="offer-band"><div class="wrap offer-inner"><div><h2>Wat mogen we voor u schoonmaken?</h2><p>Vertel ons over uw locatie en ontvang een voorstel op maat.</p></div><a class="button button-light" href="{QUOTE}">Vraag een offerte aan {icon("right")}</a></div></section>'''

def home():
    proof=[("shield","Vakbekwame medewerkers"),("leaf","Duurzame werkwijze"),("people","Persoonlijk contact")]
    logos=[("benedict","Benedict"),("basecamp","Basecamp Eco-resorts"),("morgan-mees","Morgan & Mees Amsterdam"),("bmc","BMC Schoonmaak B.V.")]
    return f'''<section class="hero" aria-labelledby="hero-title">
<img class="hero-image" src="/media/housekeeping.webp" alt="Een housekeeper maakt het bed op voor de volgende gast." fetchpriority="high" width="1560" height="945">
<div class="hero-shade"></div><div class="wrap hero-wrap">
<div class="hero-copy">
<h1 id="hero-title" lang="en">Employees<br><em>with skills</em></h1>
<p>Onze housekeepers maken hotelkamers en vakantiewoningen klaar voor de volgende gast. We stemmen de kamerwissels af op uw aankomsttijden.</p>
<div class="hero-actions"><a class="button button-teal" href="/diensten/housekeeping/">Bekijk housekeeping {icon("right")}</a><a class="button button-glass" href="/diensten/">Alle diensten</a></div></div>
</div></section>
<section class="proof" aria-label="Onze werkwijze"><div class="wrap proof-grid">{''.join(f'<div>{icon(i)}<span>{t}</span></div>' for i,t in proof)}</div></section>
<section class="wrap services-home"><div class="section-head"><div><h2>Onze diensten<span>.</span></h2><p>Schoonmaak die past bij uw locatie.</p></div><a class="text-link" href="/diensten/">Alle diensten {icon("right")}</a></div><div class="card-grid">{''.join(card(s) for s in SERVICES)}</div></section>
<section class="about-home"><div class="wrap about-grid"><div class="about-picture"><img alt="Een medewerker reinigt het bedieningspaneel van een lift" loading="lazy" src="/media/home.webp" width="900" height="650"></div>
<div><h2>Een team met oog<br>voor detail<span>.</span></h2><p>In de housekeeping leerden we hoeveel een verzorgde ruimte betekent voor een gast. Diezelfde aandacht geven we aan elke werkplek, woning en bouwoplevering.</p><a class="button button-dark" href="/over-ons/">Maak kennis met EWS {icon("right")}</a></div></div></section>
<section class="wrap partners"><h2>Onze partners</h2><div class="logos">{''.join(f'<img src="/media/partner-{n}.webp" alt="{alt}" loading="lazy" width="120" height="120">' for n,alt in logos)}</div></section>
{offer_band()}'''

def services():
    return f'''<div class="wrap overview"><nav class="crumb" aria-label="Kruimelpad"><a href="/">Home</a><span>/</span>Diensten</nav>
<div class="overview-title"><h1>Onze diensten<span>.</span></h1><p>Van de eerste hotelgast tot de laatste bouwdag. Kies uw type locatie en ontdek welke schoonmaak daarbij past.</p></div>
<div class="card-grid overview-grid">{''.join(card(s) for s in SERVICES)}</div></div>{offer_band()}'''

def page(route, title, desc, active, content, stylesheet=""):
    extra = f'<link rel="stylesheet" href="/{stylesheet}">' if stylesheet else ''
    for language in LANGUAGES:
        dest = OUT / localized_url(route, language).strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        alternates = canonical = ''
        if SITE_URL:
            alternates = ''.join(f'<link rel="alternate" hreflang="{code}" href="{SITE_URL}{localized_url(route, code)}">' for code in LANGUAGES)
            alternates += f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}{route}">'
            canonical = f'<link rel="canonical" href="{SITE_URL}{localized_url(route, language)}">'
        source = f'''<!doctype html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | EWS Groep</title>
<meta name="description" content="{escape(desc)}"><meta name="theme-color" content="#0097b2"><link rel="icon" href="/media/favicon.png">
{canonical}{alternates}
<link rel="preload" href="/media/sora.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/site.css">{extra}<script src="/site.js" defer></script>
<script id="site-copy" type="application/json">{runtime_copy(language)}</script>
</head><body>{header(active, route, language)}<main id="inhoud">{content}</main>{footer()}</body></html>'''
        dest.write_text(localize_html(source, language), encoding='utf-8')

if __name__ == "__main__":
    page("/", "Housekeeping voor hotels en vakantiewoningen", "Housekeeping voor hotels en vakantiewoningen. EWS Groep verzorgt uw kamers volgens de planning van vertrekkende en aankomende gasten.", "Home", home())
    page("/diensten/", "Onze diensten", "Bekijk de vier schoonmaakdiensten van EWS Groep voor hotels, bouwprojecten, kantoren en woningen.", "Diensten", services())
    page("/over-ons/", "Over ons", "Maak kennis met de mensen en de werkwijze achter de housekeeping en schoonmaakdiensten van EWS Groep.", "Over ons", about("/media/home.webp"), "inside.css")
    page("/contact/", "Contact", "Neem contact op met EWS Groep in Harderwijk of vraag een offerte aan voor schoonmaak.", "Contact", contact_body().replace('<link rel="stylesheet" href="/contact.css">',''), "contact.css")
    for service in SERVICES:
        page("/diensten/" + service["slug"] + "/", service["title"], service["description"], "Diensten", detail(service), "inside.css")
