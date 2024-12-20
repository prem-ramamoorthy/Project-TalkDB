function toggleTheme() {
    const body = document.body;
    const lightLogo = document.querySelector('.light-logo');
    const darkLogo = document.querySelector('.dark-logo');
    if (body.dataset.theme === 'dark') {
        body.removeAttribute('data-theme');
        lightLogo.style.display = 'block';
        darkLogo.style.display = 'none';
    } else {
        body.setAttribute('data-theme', 'dark');
        lightLogo.style.display = 'none';
        darkLogo.style.display = 'block';
    }
}