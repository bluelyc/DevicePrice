// Открытие модального окна
function openModal() {
    document.getElementById('modal').classList.add('show');
}

// Закрытие модального окна
function closeModal() {
    document.getElementById('modal').classList.remove('show');
}


function toggleMenu() {
    const menu = document.getElementById("mobileMenu");
    menu.classList.toggle("active"); // Переключаем класс active
}
function openSearchModal() {
    const modal = document.getElementById('searchModal');
    modal.style.display = 'block';
    document.getElementById('search-input').focus();
}

function closeSearchModal() {
    // Закрываем модальное окно
    document.getElementById('searchModal').style.display = 'none';

    // Очищаем поле ввода
    document.getElementById('search-input').value = '';

    // Очищаем результаты поиска
    document.getElementById('search-results').innerHTML = '';
}

// Функция для выполнения поиска
// Получаем элементы
const searchInput = document.getElementById('search-input');
const resultsContainer = document.getElementById('search-results');

// Таймер для контроля задержки между запросами
let debounceTimer;

searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim();

    // Очищаем предыдущий таймер
    clearTimeout(debounceTimer);

    if (query.length > 0) {
        // Устанавливаем таймер с задержкой 300 мс перед выполнением запроса
        debounceTimer = setTimeout(() => {
            performSearch(query);
        }, 300);
    }
});

// Функция для выполнения поиска
function performSearch(query) {
    fetch(`/search/?query=${encodeURIComponent(query)}`)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP! Статус: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.error) {
                resultsContainer.innerHTML = `<p>${data.error}</p>`;
            } else {
                displaySearchResults(data);
            }
        })
        .catch((error) => {
            console.error('Ошибка поиска:', error);
            resultsContainer.innerHTML = '<p>Произошла ошибка. Попробуйте позже.</p>';
        });
}

// Функция для отображения результатов поиска
function displaySearchResults(data) {
    const resultsContainer = document.getElementById('search-results');
    resultsContainer.innerHTML = ''; // Очистить предыдущие результаты

    if (data.length === 0) {
        resultsContainer.innerHTML = '<p>Ничего не найдено.</p>';
        return;
    }

    data.forEach((product) => {
        const productElement = document.createElement('div');
        productElement.classList.add('search-result-item');

        // Формируем HTML для изображения
        const imageHTML = product.image
            ? `<img src="${product.image}" alt="${product.name}" class="search-result-image">`
            : '';

        productElement.innerHTML = `
            <div class="search-result-images">
                ${imageHTML}
            </div>
            <div class="search-result-info">
                <h4>${product.name}</h4>
            </div>
        `;

        // Добавляем обработчик редиректа
        productElement.addEventListener('click', () => {
            window.location.href = `/product/${product.id}`; // Переход на страницу товара
        });

        resultsContainer.appendChild(productElement);
    });
}




