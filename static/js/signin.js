
if (errorMessages.length > 0) {
    const emailInput = document.getElementById('email-input');
    const passwordInput = document.getElementById('password-input');
    emailInput.classList.add('highlight');
    passwordInput.classList.add('highlight');
    // Remove highlight after 1 second
    setTimeout(() => {
        emailInput.classList.remove('highlight');
        passwordInput.classList.remove('highlight');
    }, 1000);
        alert(errorMessages.join('\n'));
}
function toggleTheme() {
    const body = document.body; body.dataset.theme = body.dataset.theme === 'dark' ? '' : 'dark';
    const lightLogo = document.querySelector('.light-logo'), darkLogo = document.querySelector('.dark-logo');
    if (body.dataset.theme === 'dark') { 
        lightLogo.style.display = 'none'; 
        darkLogo.style.display = 'block';
    } else { 
        lightLogo.style.display = 'block'; 
        darkLogo.style.display = 'none'; 
    }
}