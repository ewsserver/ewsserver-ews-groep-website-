const menuButton = document.querySelector('.mobile-nav');
const menu = document.getElementById('main-nav');
const siteCopy = JSON.parse(document.getElementById('site-copy').textContent);
const languagePicker = document.querySelector('.language-picker');

function toggleMenu(open) {
  menu.classList.toggle('is-open', open);
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? siteCopy.menuClose : siteCopy.menuOpen);
}

menuButton.addEventListener('click', () => {
  languagePicker.open = false;
  toggleMenu(menuButton.getAttribute('aria-expanded') !== 'true');
});
languagePicker.addEventListener('toggle', () => {
  if (languagePicker.open) toggleMenu(false);
});
document.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  if (languagePicker.open) {
    languagePicker.open = false;
    languagePicker.querySelector('summary').focus();
  } else if (menuButton.getAttribute('aria-expanded') === 'true') {
    toggleMenu(false);
    menuButton.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-head')) toggleMenu(false);
  if (!languagePicker.contains(event.target)) languagePicker.open = false;
});
window.matchMedia('(min-width: 1025px)').addEventListener('change', event => {
  if (event.matches) toggleMenu(false);
});

// Keep the current page and quote/service selection when changing language.
// Ordinary links keep working when JavaScript is unavailable.
document.querySelectorAll('[data-language]').forEach(link => {
  const target = new URL(link.href);
  target.search = window.location.search;
  target.hash = window.location.hash;
  link.href = target.href;
});
