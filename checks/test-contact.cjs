// Run without a browser or network requests. Captures the WhatsApp draft URL.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const script = fs.readFileSync(path.join(root, 'dist/contact.js'), 'utf8');
let runs = 0;
for (const language of ['nl', 'en', 'tr', 'bg']) {
  const html = fs.readFileSync(path.join(root, 'dist', language === 'nl' ? '' : language, 'contact/index.html'), 'utf8');
  const rawCopy = html.match(/<script id="site-copy" type="application\/json">(.*?)<\/script>/s)[1];
  const copy = JSON.parse(rawCopy);
  const options = [...html.matchAll(/<option value="(.*?)">(.*?)<\/option>/g)].map(m => ({ value: m[1], text: m[2] }));
  for (const quote of [false, true]) {
    for (const requestedService of ['housekeeping', 'kantoren', 'unknown']) {
      let destination;
      const field = () => ({ value: '', error: '', handlers: {}, setCustomValidity(value) { this.error = value; }, addEventListener(name, fn) { this.handlers[name] = fn; } });
      const name = field(), message = field(), company = field();
      const service = { value: '', options, get selectedOptions() { return options.filter(o => o.value === this.value); } };
      const elements = { name, message, company, service, namedItem(key) { return this[key]; } };
      const form = { elements, hidden: true, events: {}, addEventListener(name, fn) { this.events[name] = fn; }, reportValidity() { return !name.error && !message.error; } };
      const nodes = { 'site-copy': { textContent: rawCopy }, 'contact-form': form, 'contact-title': { firstChild: {} }, 'contact-lead': {}, 'contact-form-title': {} };
      const document = { getElementById(id) { return nodes[id]; } };
      const window = { location: { search: `?dienst=${requestedService}${quote ? '&aanvraag=offerte' : ''}`, assign(url) { destination = url; } } };
      vm.runInNewContext(script, { document, window, URL, URLSearchParams });
      assert.equal(form.hidden, false);
      assert.equal(form.noValidate, true);
      assert.equal(service.value, requestedService === 'unknown' ? '' : requestedService);
      if (quote) {
        assert.equal(nodes['contact-title'].firstChild.textContent, copy.quoteTitle);
        assert.equal(document.title, copy.quoteTitle + ' | EWS Groep');
      }
      name.value = '  ';
      form.events.submit({ preventDefault() {} });
      assert.equal(destination, undefined);
      assert.equal(name.error, copy.nameRequired);
      assert.equal(message.error, copy.messageRequired);
      name.value = 'Çağrı & Мария'; name.handlers.input();
      assert.equal(name.error, '');
      company.value = 'EWS test';
      message.value = 'Testbericht\nТест & kontrol';
      form.events.submit({ preventDefault() {} });
      const url = new URL(destination);
      assert.equal(url.origin + url.pathname, 'https://wa.me/31638997384');
      const draft = url.searchParams.get('text');
      assert.ok(draft.startsWith(copy.greeting));
      assert.ok(draft.includes(quote ? copy.quoteSubject : copy.questionSubject));
      assert.ok(draft.includes(copy.name + ': Çağrı & Мария'));
      assert.ok(draft.includes(copy.company + ': EWS test'));
      assert.ok(draft.endsWith(message.value));
      if (requestedService !== 'unknown') assert.ok(draft.includes(copy.service + ': ' + service.selectedOptions[0].text));
      runs++;
    }
  }
}
console.log(`${runs} localized enquiry, validation and WhatsApp draft cases passed.`);
