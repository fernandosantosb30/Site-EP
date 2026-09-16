// The content is visible immediately; no loader or network request gates rendering.
document.documentElement.classList.add('js');
const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('.main-nav');
function closeMenu(returnFocus = false) {
    mainNav?.classList.remove('open');
    menuToggle?.setAttribute('aria-expanded', 'false');
    menuToggle?.setAttribute('aria-label', 'Abrir menu');
    if (returnFocus) menuToggle?.focus();
}
menuToggle?.addEventListener('click', () => {
    const open = mainNav.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
});
mainNav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => closeMenu()));
document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && mainNav?.classList.contains('open')) closeMenu(true);
});
document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
});
window.matchMedia('(max-width: 800px)').addEventListener('change', () => closeMenu());
document.querySelectorAll('[data-interest]').forEach(link => {
    link.addEventListener('click', () => {
        const select = document.querySelector('#interesse');
        if (select) select.value = link.dataset.interest;
    });
});
document.querySelectorAll('form[data-whatsapp]').forEach(form => {
    form.addEventListener('submit', event => {
        event.preventDefault();
        // Normalize before validating, so whitespace-only messages cannot be sent.
        form.querySelectorAll('input, textarea').forEach(field => { field.value = field.value.trim(); });
        if (!form.reportValidity()) return;
        const data = new FormData(form);
        const career = form.dataset.whatsapp === 'career';
        const lines = [career ? 'Candidatura — Trabalhe Conosco' : 'Olá! Gostaria de conversar com a EP.',
            `Nome: ${data.get('nome')}`, `WhatsApp: ${data.get(career ? 'telefone' : 'whatsapp')}`,
            `E-mail: ${data.get('email')}`];
        if (data.get('interesse')) lines.push(`Interesse: ${data.get('interesse')}`);
        lines.push('', data.get('mensagem'));
        window.location.assign(`https://wa.me/5555999628003?text=${encodeURIComponent(lines.join('\n'))}`);
    });
});
