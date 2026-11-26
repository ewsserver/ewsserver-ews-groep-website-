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

Cloudflare Builds kiest het account via `CLOUDFLARE_ACCOUNT_ID`. Er is geen
vast account of standaard workers.dev-adres in de website ingesteld.

De openbare website-link staat in het juiste Cloudflare-account bij deze
Worker onder Settings → Domains & Routes. Gebruik het daar vermelde
workers.dev-adres; de beheerpagina op dash.cloudflare.com is geen websitelink.

Stel de buildvariabele `SITE_URL` in op die openbare URL, of op het eigen
domein zodra dat gekoppeld is. De build verwerkt die URL in alle canonical-
en hreflang-verwijzingen. Zonder `SITE_URL` worden die metagegevens weggelaten
zodat de site niet naar een onjuist account verwijst. Alle pagina's en de
taalkeuze blijven werken. Deze configuratie wijzigt geen DNS-records.

Het contactformulier opent een WhatsApp-concept voor EWS. De bezoeker verzendt
dat bericht zelf in WhatsApp.
