def contact_body():
    return """
<link rel="stylesheet" href="/contact.css">
<section class="contact-page" aria-labelledby="contact-title">
  <div class="wrap">
    <nav class="contact-crumbs" aria-label="Broodkruimelpad">
      <a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">Contact</span>
    </nav>
    <div class="contact-columns">
      <div class="contact-intro">
        <h1 id="contact-title">Contact<span>.</span></h1>
        <p id="contact-lead" class="contact-lead">Een vraag over de schoonmaak van uw locatie? Bel, mail of stuur ons een bericht.</p>
        <dl class="contact-details">
          <div>
            <dt><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.4 3h-2A2.4 2.4 0 0 0 3 5.6C3.8 13.6 10.4 20.2 18.4 21a2.4 2.4 0 0 0 2.6-2.4v-2a1.5 1.5 0 0 0-1.2-1.5l-3.2-.6a1.5 1.5 0 0 0-1.3.4l-1.4 1.3a14 14 0 0 1-6.1-6.1l1.3-1.4a1.5 1.5 0 0 0 .4-1.3l-.6-3.2A1.5 1.5 0 0 0 7.4 3Z"/></svg>Telefoon</dt>
            <dd><a href="tel:+31638997384">06 38 99 73 84</a></dd>
          </div>
          <div>
            <dt><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 6 8 7 8-7"/></svg>E-mail</dt>
            <dd><a href="mailto:info@ewsgroep.nl">info@ewsgroep.nl</a></dd>
          </div>
          <div>
            <dt><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 10c0 5.1-7 11-7 11S5 15.1 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2.2"/></svg>Adres</dt>
            <dd><a href="https://www.google.com/maps/search/?api=1&amp;query=Industrieweg+14%2C+3846+BD+Harderwijk">Industrieweg 14<br>3846 BD Harderwijk</a></dd>
          </div>
        </dl>
      </div>
      <div class="contact-panel">
        <h2 id="contact-form-title">Stuur ons een bericht</h2>
        <p class="contact-note">U controleert en verstuurt uw bericht straks in WhatsApp.</p>
        <noscript><p><a class="contact-submit" href="https://wa.me/31638997384">Open WhatsApp</a></p></noscript>
        <form id="contact-form" class="contact-form" hidden>
          <div class="contact-pair">
            <label for="contact-name">Uw naam<input name="name" id="contact-name" autocomplete="name" maxlength="100" required></label>
            <label for="contact-company">Bedrijf <span>(optioneel)</span><input name="company" id="contact-company" autocomplete="organization" maxlength="140"></label>
          </div>
          <label for="contact-service">Waar gaat uw vraag over?
            <select name="service" id="contact-service">
              <option value="">Algemene vraag</option>
              <option value="housekeeping">Housekeeping</option>
              <option value="bouwoplevering">Bouwoplevering</option>
              <option value="kantoren">Kantoorschoonmaak</option>
              <option value="particulier">Particuliere schoonmaak</option>
            </select>
          </label>
          <label for="contact-message">Uw bericht<textarea name="message" id="contact-message" rows="5" maxlength="2000" required></textarea></label>
          <button type="submit" class="contact-submit">Verder in WhatsApp <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6"/></svg></button>
        </form>
      </div>
    </div>
  </div>
</section>
<script src="/contact.js" defer></script>
"""
