// Сохраняем выбранный регион в cookie
function saveRegion(regionId) {
    document.cookie = `SelectRegion=${regionId}; path=/; max-age=3600`; // cookie на 1 час
    window.location.reload(); // Перезагрузка страницы
}

// Устанавливаем текущее значение select из cookie
document.addEventListener('DOMContentLoaded', () => {
    let regionId = getCookie('SelectRegion');
    if (!regionId) {
        regionId = 1; // Если cookie нет, устанавливаем по умолчанию regionId = 1
    }

    const regionSelector = document.getElementById('region-selector');
    if (regionId && regionSelector) {
        regionSelector.value = regionId;
    }

    // Если на странице есть корзина, можем автоматически подгрузить адреса
    if (document.getElementById('address-selector') && regionId) {
        loadAddresses(regionId);
    }
});

// Получаем значение cookie по имени
function getCookie(name) {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))
        ?.split('=')[1];
}

// Функция для подгрузки адресов
function loadAddresses(regionId) {
    fetch(`/get_addresses/${regionId}/`)
        .then(response => response.json())
        .then(data => {
            const addressSelector = document.getElementById("address-selector");
            addressSelector.innerHTML = '<option value="">Выберите адрес</option>'; // Очищаем старые значения

            data.forEach(address => {
                const option = document.createElement("option");
                option.value = address.id;
                option.textContent = address.name;
                addressSelector.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error loading addresses:', error);
        });
}
