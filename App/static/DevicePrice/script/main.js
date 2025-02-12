const images = document.querySelectorAll('.slider .slider-line img');
const sliderLine = document.querySelector('.slider .slider-line');
let count = 0;
let width;

// Инициализация слайдера
function init() {
    console.log('resize');
    width = document.querySelector('.slider').offsetWidth;
    sliderLine.style.width = width * images.length + 'px';
    images.forEach(item => {
        item.style.width = width + 'px';
        item.style.height = 'auto';
    });
    rollSlider();
}

init();
window.addEventListener('resize', init);

// Обработчики для кнопок
document.querySelector('.slider-next').addEventListener('click', function () {
    moveNext();
    resetAutoScroll(); // Сбрасываем автопрокрутку при ручном взаимодействии
});

document.querySelector('.slider-prev').addEventListener('click', function () {
    movePrev();
    resetAutoScroll(); // Сбрасываем автопрокрутку при ручном взаимодействии
});

// Прокрутка вперед
function moveNext() {
    count++;
    if (count >= images.length) {
        count = 0;
    }
    rollSlider();
}

// Прокрутка назад
function movePrev() {
    count--;
    if (count < 0) {
        count = images.length - 1;
    }
    rollSlider();
}

// Обновление положения слайдера
function rollSlider() {
    sliderLine.style.transform = 'translate(-' + count * width + 'px)';
}

// Автопрокрутка
let autoScroll = setInterval(moveNext, 3000); // Прокрутка каждые 3 секунды

// Сброс автопрокрутки при взаимодействии
function resetAutoScroll() {
    clearInterval(autoScroll);
    autoScroll = setInterval(moveNext, 3000);
}
window.addEventListener('load', () => {
    // Находим все секции с слайдерами
    const sliders = document.querySelectorAll('.products-section');

    sliders.forEach((slider) => {
        const sliderLine = slider.querySelector('.products-line'); // Лента с элементами
        const prevButton = slider.querySelector('.products-prev'); // Кнопка "назад"
        const nextButton = slider.querySelector('.products-next'); // Кнопка "вперед"
        const productCards = slider.querySelectorAll('.product-card'); // Все карточки

        let cardWidth = productCards[0]?.offsetWidth + 7 || 0; // Ширина карточки + gap (проверяем на случай отсутствия)
        let visibleCards = Math.floor(sliderLine.offsetWidth / cardWidth); // Сколько карточек видно
        let currentIndex = 0; // Текущий индекс видимой карточки

        const updateSlider = () => {
            const offset = currentIndex * cardWidth; // Вычисляем смещение
            sliderLine.style.transform = `translateX(-${offset}px)`;

            // Проверяем, можем ли двигаться дальше
            prevButton.disabled = currentIndex === 0; // Блокируем, если в начале
            nextButton.disabled = currentIndex >= productCards.length - visibleCards; // Блокируем, если в конце
        };

        const initializeSlider = () => {
            // Пересчитываем размеры карточек и видимые элементы
            cardWidth = productCards[0]?.offsetWidth + 7 || 0;
            visibleCards = Math.floor(sliderLine.offsetWidth / cardWidth);

            // Обновляем текущий индекс, если он выходит за пределы
            if (currentIndex > productCards.length - visibleCards) {
                currentIndex = Math.max(0, productCards.length - visibleCards);
            }

            updateSlider();
        };

        nextButton.addEventListener('click', () => {
            if (currentIndex < productCards.length - visibleCards) {
                currentIndex++; // Увеличиваем индекс
                updateSlider(); // Обновляем слайдер
            }
        });

        prevButton.addEventListener('click', () => {
            if (currentIndex > 0) {
                currentIndex--; // Уменьшаем индекс
                updateSlider(); // Обновляем слайдер
            }
        });

        // Адаптивность: пересчитываем видимые карточки при изменении размеров окна
        window.addEventListener('resize', initializeSlider);

        // Инициализация с задержкой
        setTimeout(initializeSlider, 50);
    });
});


