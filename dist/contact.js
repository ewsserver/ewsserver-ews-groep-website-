(() => {
  const form = document.getElementById('contact-form');
  if (!form) return;
  const copy = JSON.parse(document.getElementById('site-copy').textContent);

  const params = new URLSearchParams(window.location.search);
  const quote = params.get('aanvraag') === 'offerte';
  const service = form.elements.service;
  const name = form.elements.namedItem('name');
  const message = form.elements.message;
  if (quote) {
    document.getElementById('contact-title').firstChild.textContent = copy.quoteTitle;
    document.getElementById('contact-lead').textContent = copy.quoteLead;
    document.getElementById('contact-form-title').textContent = copy.quoteFormTitle;
    document.title = copy.quoteTitle + ' | EWS Groep';
  }
  const requestedService = params.get('dienst');
  if (requestedService && Array.from(service.options).some(option => option.value === requestedService)) {
    service.value = requestedService;
  }
  form.hidden = false;
  // Report required-field errors in the chosen website language, regardless
  // of the browser's own language, including empty and whitespace-only input.
  form.noValidate = true;
  for (const field of [name, message]) {
    field.addEventListener('input', () => field.setCustomValidity(''));
  }
  form.addEventListener('submit', event => {
    event.preventDefault();
    name.setCustomValidity(name.value.trim() ? '' : copy.nameRequired);
    message.setCustomValidity(message.value.trim() ? '' : copy.messageRequired);
    if (!form.reportValidity()) return;

    const company = form.elements.company.value.trim();
    const subject = quote ? copy.quoteSubject : copy.questionSubject;
    const parts = [
      copy.greeting, '', subject, '',
      copy.name + ': ' + name.value.trim(),
      ...(company ? [copy.company + ': ' + company] : []),
      ...(service.value ? [copy.service + ': ' + service.selectedOptions[0].text] : []),
      '', message.value.trim()
    ];
    const url = new URL('https://wa.me/31638997384');
    url.searchParams.set('text', parts.join('\n'));
    window.location.assign(url.href);
  });
})();
