"""Build complete, directly linkable HTML pages for every supported language."""

import json
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit, urlunsplit

from translations import LANGUAGES, translate

ROUTES = (
    "/", "/diensten/", "/over-ons/", "/contact/",
    "/diensten/housekeeping/", "/diensten/bouwoplevering/",
    "/diensten/kantoren/", "/diensten/particulier/",
)


def localized_url(url, language):
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or parts.path not in ROUTES:
        return url
    path = parts.path if language == "nl" else f"/{language}{parts.path}"
    return urlunsplit(("", "", path, parts.query, parts.fragment))


def language_picker(route, language):
    links = "".join(
        f'<a href="{localized_url(route, code)}" data-language="{code}" '
        f'lang="{code}" hreflang="{code}"'
        + (' aria-current="true"' if code == language else '')
        + f'>{label}<span aria-hidden="true">{code.upper()}</span></a>'
        for code, label in LANGUAGES.items()
    )
    return f'''<details class="language-picker">
<summary aria-label="Taal kiezen"><svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg><span>{language.upper()}</span><svg class="language-chevron" aria-hidden="true" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="m4 6 4 4 4-4"/></svg></summary>
<nav class="language-options" aria-label="Taal">{links}</nav></details>'''


def runtime_copy(language):
    sources = {
        "menuOpen": "Menu openen", "menuClose": "Menu sluiten",
        "quoteTitle": "Offerte aanvragen",
        "quoteLead": "Vertel ons welke ruimtes u wilt laten schoonmaken, waar uw locatie is en hoe vaak u schoonmaak nodig heeft.",
        "quoteFormTitle": "Uw offerteaanvraag",
        "nameRequired": "Vul uw naam in.", "messageRequired": "Schrijf een bericht.",
        "quoteSubject": "Ik ontvang graag een offerte.", "questionSubject": "Ik heb een vraag.",
        "greeting": "Beste EWS Groep,", "name": "Naam", "company": "Bedrijf", "service": "Dienst",
    }
    return json.dumps({key: translate(value, language) for key, value in sources.items()}, ensure_ascii=False).replace("<", "\\u003c")


class LocalizedHTML(HTMLParser):
    def __init__(self, language):
        super().__init__(convert_charrefs=True)
        self.language = language
        self.output = []
        self.raw = False

    def handle_decl(self, decl):
        self.output.append(f"<!{decl}>")

    def handle_comment(self, comment):
        self.output.append(f"<!--{comment}-->")

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        translated = []
        for key, value in attrs:
            if tag == "html" and key == "lang":
                value = self.language
            elif value and key in ("alt", "aria-label", "placeholder", "title"):
                value = translate(value, self.language)
            elif tag == "meta" and values.get("name") == "description" and key == "content":
                value = translate(value, self.language)
            elif key == "href" and value and "data-language" not in values:
                value = localized_url(value, self.language)
            translated.append(key if value is None else f'{key}="{escape(value, quote=True)}"')
        attributes = " " + " ".join(translated) if translated else ""
        self.output.append(f"<{tag}{attributes}>")
        if tag in ("script", "style"):
            self.raw = True

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.output[-1] = self.output[-1][:-1] + "/>"

    def handle_endtag(self, tag):
        self.output.append(f"</{tag}>")
        if tag in ("script", "style"):
            self.raw = False

    def handle_data(self, data):
        if self.raw or not data.strip():
            self.output.append(data)
            return
        content = data.strip()
        before = data[:len(data) - len(data.lstrip())]
        after = data[len(data.rstrip()):]
        self.output.append(before + escape(translate(content, self.language), quote=False) + after)


def localize_html(html, language):
    parser = LocalizedHTML(language)
    parser.feed(html)
    parser.close()
    return "".join(parser.output)
