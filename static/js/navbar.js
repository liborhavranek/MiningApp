document.addEventListener('DOMContentLoaded', () => {
    let navbar = document.querySelector('nav.navbar');
    let timeout;

    window.addEventListener('scroll', () => {
        // Skrytí navbaru
        navbar.classList.add('hidden');

        // Zrušení předchozího timeoutu, pokud existuje
        if (timeout) clearTimeout(timeout);

        // Nastavení timeoutu pro opětovné zobrazení navbaru po 1 sekundě
        timeout = setTimeout(() => {
            navbar.classList.remove('hidden');
        }, 1000);
    });

    // Ujistíme se, že navbar je viditelný při načtení stránky
    navbar.classList.remove('hidden');
});