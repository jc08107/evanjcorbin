
// Modal behavior
const modal = document.getElementById('newsletter-modal');
const openBtns = document.querySelectorAll('[data-open-newsletter]');
const closeBtns = document.querySelectorAll('[data-close-newsletter]');
const openModal = () => modal?.classList.remove('hidden');

openBtns.forEach(btn => btn.addEventListener('click', openModal));
closeBtns.forEach(btn => btn.addEventListener('click', () => modal?.classList.add('hidden')));

// Close on ESC
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') modal?.classList.add('hidden'); });

// Open modal once per session on home page
const HOMEPAGE_PATHS = ['/', '/index', '/index/'];
const sessionKey = 'newsletterModalShown';
const isHomePage = HOMEPAGE_PATHS.includes(window.location.pathname.toLowerCase());
if (isHomePage && !sessionStorage.getItem(sessionKey)) {
  window.addEventListener('load', () => {
    sessionStorage.setItem(sessionKey, '1');
    // Slight delay for smoother load
    setTimeout(openModal, 500);
  });
}

// Subscribe handler
const form = document.getElementById('newsletter-form');
if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
      email: form.email.value,
      first_name: form.first_name.value,
      last_name: form.last_name.value,
    };
    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    btn.textContent = 'Submitting...';
    try {
      const res = await fetch('/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      const json = await res.json();
      const msg = document.getElementById('subscribe-msg');
      msg.textContent = json.message || 'Subscribed!';
      msg.classList.remove('hidden');
      form.reset();
    } catch (err) {
      const msg = document.getElementById('subscribe-msg');
      msg.textContent = 'There was an error. Please try again.';
      msg.classList.remove('hidden');
    } finally {
      btn.disabled = false;
      btn.textContent = 'Join the newsletter';
    }
  });
}
