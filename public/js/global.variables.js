function isDarkMode() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
}

function setAttributeHtml(key, value) {
    const elements = document.getElementsByTagName('html');
    for (let i = 0; i < elements.length; i++) {
        elements[i].setAttribute(key, value)
    }
}


function checkDefaultTheme() {
    
    const theme = window.localStorage.getItem('theme');

    if(theme === null) {
        if (isDarkMode()) {
            setAttributeHtml('data-bs-theme', 'dark')
        } else {
            setAttributeHtml('data-bs-theme', 'light')
        }
    } else {
        setAttributeHtml('data-bs-theme', theme)
    }
}

function toggleTheme(el) {

    let theme = window.localStorage.getItem('theme');

    if(theme === null) {
        isDarkMode() ? theme = 'dark' :  theme = 'light'
    } else {
        (theme === 'dark') ? theme = 'light' : theme = 'dark'
    }
    
    window.localStorage.setItem('theme', theme)
    setAttributeHtml('data-bs-theme', theme)
    theme === 'dark' ? el.textContent = 'Tema Obscuro' : el.textContent = 'Tema Claro'
}

checkDefaultTheme();