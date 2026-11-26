# EWS Groep website

De volledige EWS-website in Nederlands, Engels, Turks en Bulgaars.

## Lokaal bouwen

Benodigd: Python 3 en Node.js 24 LTS.

```sh
npm ci
npm run build
npm test
npm run check:deploy
npm run preview
```

De website staat in `dist/`. Python genereert 32 pagina's vanuit `build.py`,
`inside.py`, `contact.py`, `i18n.py` en `translations.py`. Afbeeldingen,
lettertypen, CSS en JavaScript staan eveneens in `dist/` en moeten behouden blijven.

## Cloudflare Workers Builds

- Repository: `ewsserver/ewsserver-ews-groep-website-`
- Productiebranch: `main`
- Worker: `ews-groep-website`
- Hoofdmap: `/`
- Build command: `npm run build && npm test`
- Deploy command: `npm run deploy`

Verbind deze repository met de Worker in Cloudflare. Nadat die koppeling is
ingesteld, publiceert Cloudflare wijzigingen op `main` automatisch. Bewaar
toegangssleutels uitsluitend in Cloudflare; ze horen niet in deze repository.

De canonieke URL is standaard `https://ews-groep-website.server-a54.workers.dev`.
Stel de buildvariabele `SITE_URL` in op het definitieve domein zodra dat domein
aan deze Worker gekoppeld is. De build verwerkt die URL in alle canonical-
en hreflang-verwijzingen. Deze configuratie wijzigt geen DNS-records.

Het contactformulier opent een WhatsApp-concept voor EWS. De bezoeker verzendt
dat bericht zelf in WhatsApp.
