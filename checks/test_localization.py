"""Run after build.py: check all language routes and their published content."""
import json
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from i18n import ROUTES, localized_url
from translations import COPY, LANGUAGES, translate
from build import SITE_URL


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags, self.text, self.scripts = [], [], []
        self.in_script = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag == 'script':
            self.in_script = True

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False

    def handle_data(self, text):
        if text.strip():
            (self.scripts if self.in_script else self.text).append(text.strip())


class LocalizationTests(unittest.TestCase):
    def test_links_preserve_parameters_and_external_destinations(self):
        self.assertEqual(localized_url('/contact/?aanvraag=offerte&dienst=kantoren#inhoud', 'bg'), '/bg/contact/?aanvraag=offerte&dienst=kantoren#inhoud')
        for url in ('/media/logo.png', '/site.js', '#inhoud', 'https://wa.me/31638997384', 'mailto:info@ewsgroep.nl'):
            self.assertEqual(localized_url(url, 'tr'), url)

    def test_missing_copy_stops_publication(self):
        with self.assertRaises(ValueError):
            translate('Untranslated future content', 'bg')

    def test_all_32_pages(self):
        for language in LANGUAGES:
            for route in ROUTES:
                with self.subTest(language=language, route=route):
                    page_url = localized_url(route, language)
                    page = Page(ROOT / 'dist' / page_url.strip('/') / 'index.html')
                    html = next(attrs for tag, attrs in page.tags if tag == 'html')
                    self.assertEqual(html['lang'], language)
                    self.assertEqual(sum(tag == 'h1' for tag, _ in page.tags), 1)
                    self.assertTrue(any(tag == 'meta' and attrs.get('name') == 'description' and attrs.get('content') for tag, attrs in page.tags))
                    alternatives = {attrs['hreflang'] for tag, attrs in page.tags if tag == 'link' and attrs.get('rel') == 'alternate'}
                    self.assertEqual(alternatives, {*LANGUAGES, 'x-default'})
                    canonical = next(attrs['href'] for tag, attrs in page.tags if tag == 'link' and attrs.get('rel') == 'canonical')
                    self.assertEqual(canonical, SITE_URL + page_url)
                    alternate_urls = {attrs['hreflang']: attrs['href'] for tag, attrs in page.tags if tag == 'link' and attrs.get('rel') == 'alternate'}
                    self.assertEqual(alternate_urls, {**{code: SITE_URL + localized_url(route, code) for code in LANGUAGES}, 'x-default': SITE_URL + route})
                    switchers = {attrs['data-language']: attrs['href'] for tag, attrs in page.tags if 'data-language' in attrs}
                    self.assertEqual(switchers, {code: localized_url(route, code) for code in LANGUAGES})
                    copy = json.loads(page.scripts[0])
                    self.assertEqual(copy['nameRequired'], translate('Vul uw naam in.', language))
                    for tag, attrs in page.tags:
                        for key in ('href', 'src'):
                            url = attrs.get(key, '')
                            parts = urlsplit(url)
                            if not parts.path.startswith('/') or parts.netloc or parts.scheme:
                                continue
                            target = ROOT / 'dist' / parts.path.lstrip('/')
                            if parts.path.endswith('/'):
                                target /= 'index.html'
                            self.assertTrue(target.is_file(), f'{page_url}: missing {url}')
                            if tag == 'a' and 'data-language' not in attrs and language != 'nl':
                                self.assertTrue(parts.path.startswith(f'/{language}/'), f'{page_url}: language lost in {url}')
                    if language != 'nl':
                        for text in page.text:
                            if text in COPY:
                                self.assertEqual(text, translate(text, language), f'Dutch copy left in {page_url}: {text}')
                    if route == '/contact/':
                        self.assertEqual([attrs['value'] for tag, attrs in page.tags if tag == 'option'], ['', 'housekeeping', 'bouwoplevering', 'kantoren', 'particulier'])


if __name__ == '__main__':
    unittest.main()
