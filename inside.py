from html import escape


SERVICE_DETAILS = {
    "housekeeping": {
        "heading": "Klaar voor de volgende gast",
        "intro": "Voor hotels en vakantiewoningen stemmen we de kamerverzorging af op de wisseling van gasten. Zo weet uw team wanneer een kamer klaar is voor de volgende aankomst.",
        "work": [
            ("Kamerverzorging", "We spreken met u af hoe u de kamers of vakantiewoningen wilt laten opleveren. Uw standaard voor een gastvrije ontvangst is ons uitgangspunt."),
            ("Begeleiding op locatie", "Onze supervisors ondersteunen de housekeepers bij hun werk en houden samen met hen oog voor de afwerking."),
            ("Afstemming met uw team", "Wensen en verbeterpunten bespreekt u met onze manager. Zo kunnen we de werkwijze bijstellen als de bezetting of uw planning verandert."),
        ],
        "question": "Vertel ons om hoeveel kamers of woningen het gaat en op welke momenten u ondersteuning zoekt.",
    },
    "bouwoplevering": {
        "heading": "Schoon op het moment van overdracht",
        "intro": "Bij een bouwoplevering komt de planning nauw. We stemmen de schoonmaak af op de voortgang van het werk en het moment waarop u de sleutel overdraagt.",
        "work": [
            ("Voor de oplevering", "Samen bekijken we welke ruimtes aan de beurt zijn en hoe ze volgens afspraak moeten worden achtergelaten."),
            ("Bezemschoon opleveren", "Ons team verzorgt de afgesproken schoonmaak, van een kleine ruimte tot een groter bouwproject."),
            ("Planning op locatie", "We stemmen de volgorde van de werkzaamheden met u af. Daarmee sluit de schoonmaak aan op uw oplevermoment."),
        ],
        "question": "Geef de locatie, de omvang van het project en de gewenste opleverdatum door.",
    },
    "kantoren": {
        "heading": "Een verzorgde werkplek",
        "intro": "Ieder kantoor heeft zijn eigen ritme. We stellen met u een programma samen voor de ruimtes die uw collega’s en bezoekers dagelijks gebruiken.",
        "work": [
            ("Werkplekken en vloeren", "We verzorgen de afgesproken werkplekken en vloeren, met aandacht voor het materiaal en het gebruik van de ruimte."),
            ("Sanitaire ruimtes", "De schoonmaak van sanitaire voorzieningen krijgt een vaste plek in de werkafspraken."),
            ("Dagelijks of periodiek", "U kunt dagelijkse schoonmaak combineren met een periodieke dieptereiniging. We stemmen het tijdstip af op de bezetting van uw kantoor."),
        ],
        "question": "Geef aan om welke kantoorruimtes het gaat, hoe vaak u schoonmaak wilt en welk tijdstip het beste uitkomt.",
    },
    "particulier": {
        "heading": "Schoonmaak die bij uw woning past",
        "intro": "Of u nu hulp zoekt in uw eigen woning of in een vakantiehuis, u bepaalt welke ruimtes aandacht nodig hebben en wanneer de schoonmaak uitkomt.",
        "work": [
            ("Woning en vakantiehuis", "We bespreken welke ruimtes u wilt laten reinigen en wat voor u belangrijk is."),
            ("Reguliere schoonmaak", "Voor terugkerende werkzaamheden stemmen we de frequentie af op het gebruik van uw woning."),
            ("Dieptereiniging", "Vraagt een ruimte om een grondigere aanpak? Dan bespreken we vooraf welke onderdelen extra aandacht krijgen."),
        ],
        "question": "Vertel ons welke ruimtes u wilt laten reinigen en of u eenmalige of terugkerende hulp zoekt.",
    },
}


def _arrow(direction="right"):
    line = "M4 12h15m-6-6 6 6-6 6" if direction == "right" else "M20 12H5m6-6-6 6 6 6"
    return f'<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round"><path d="{line}"/></svg>'


def _breadcrumb(name, service=False):
    middle = '<a href="/diensten/">Diensten</a><i aria-hidden="true">/</i>' if service else ""
    return f'<nav aria-label="Kruimelpad" class="in-breadcrumb"><a href="/">Home</a><i aria-hidden="true">/</i>{middle}<span aria-current="page">{escape(name)}</span></nav>'


def _button(url, label):
    return f'<a class="in-button" href="{escape(url, quote=True)}">{escape(label)}{_arrow()}</a>'


def _rows(items):
    return "".join(f'<div class="in-row"><h3>{escape(title)}</h3><p>{escape(copy)}</p></div>' for title, copy in items)


def detail(service):
    """Render a service detail page inside the shared site chrome."""
    slug = service["slug"]
    copy = SERVICE_DETAILS[slug]
    title = service["title"]
    cta_url = "/contact/?aanvraag=offerte&dienst=" + slug
    return f"""
<div class="in-page">
    <div class="wrap">{_breadcrumb(title, service=True)}</div>
    <section class="wrap in-split">
        <div class="in-lead">
            <h1>{escape(title)}</h1>
            <p>{escape(copy["intro"])}</p>
            {_button(cta_url, "Offerte aanvragen")}
        </div>
        <div class="in-photo">
            <img src="{escape(service['image'], quote=True)}" alt="{escape(service['alt'], quote=True)}" fetchpriority="high">
        </div>
    </section>
    <section class="in-band" aria-labelledby="in-work">
        <div class="wrap in-work">
            <div class="in-work-intro"><h2 id="in-work">{escape(copy["heading"])}</h2></div>
            <div class="in-rows">{_rows(copy["work"])}</div>
        </div>
    </section>
    <section class="wrap in-next">
        <div><h2>Uw aanvraag</h2><p>{escape(copy["question"])}</p></div>
        <div class="in-links">{_button(cta_url, "Vraag een offerte aan")}<a class="in-text-link" href="/diensten/">{_arrow("left")} Alle diensten</a></div>
    </section>
</div>"""


def about(about_image):
    """Render the company's profile inside the shared site chrome."""
    items = [
        ("Vooraf afstemmen", "We bespreken welke ruimtes aandacht nodig hebben, wat u van ons verwacht en wanneer het werk kan plaatsvinden."),
        ("Uitvoeren op locatie", "Onze medewerkers werken volgens de afgesproken planning. Bij housekeeping ondersteunen supervisors het team op locatie."),
        ("Samen bijstellen", "Verandert er iets of heeft u een opmerking over het resultaat? Dan bespreken we met u hoe we de aanpak kunnen aanpassen."),
    ]
    return f"""
<div class="in-page">
    <div class="wrap">{_breadcrumb("Over ons")}</div>
    <section class="wrap in-split">
        <div class="in-lead">
            <h1>Over EWS Groep</h1>
            <p>Housekeeping is de basis van EWS Groep. Onze medewerkers verzorgen hotelkamers en vakantiewoningen. Supervisors begeleiden het team en stemmen de werkzaamheden af met uw locatie.</p>
            {_button("/diensten/", "Bekijk onze diensten")}
        </div>
        <div class="in-photo"><img src="{escape(about_image, quote=True)}" alt="Professionele schoonmaak op locatie" fetchpriority="high"></div>
    </section>
    <section class="in-band" aria-labelledby="in-approach">
        <div class="wrap in-work">
            <div class="in-work-intro"><h2 id="in-approach">Zo werken we samen</h2><p>De aandacht die we aan een hotelkamer geven, nemen we ook mee naar kantoren, woningen en bouwopleveringen.</p></div>
            <div class="in-rows">{_rows(items)}</div>
        </div>
    </section>
    <section class="wrap in-next">
        <div><h2>Kennismaken?</h2><p>Vertel ons over uw locatie en uw wensen. We kijken samen welke schoonmaak het beste past.</p></div>
        <div class="in-links">{_button("/contact/", "Neem contact op")}</div>
    </section>
</div>"""
