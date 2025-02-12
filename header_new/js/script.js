// Анимация бургер-меню
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('active');
    
    // Блокировка прокрутки фона
    document.body.style.overflow = menu.classList.contains('active') ? 'hidden' : '';
}

// Закрытие меню при клике вне области
document.addEventListener('click', (e) => {
    const menu = document.getElementById('mobile-menu');
    const burger = document.querySelector('.burger-menu');
    
    if (!menu.contains(e.target) && !burger.contains(e.target)) {
        menu.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Обработка подкатегорий
document.querySelectorAll('.has-submenu > a').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const parent = item.parentElement;
        parent.classList.toggle('active');
    });
});

// Сохранение выбранного города
function saveRegion(value) {
    console.log('Выбран город с ID:', value);
    // Здесь можно добавить логику для сохранения выбора
}