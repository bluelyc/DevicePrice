document.addEventListener('DOMContentLoaded', function () {
    const quantityInputs = document.querySelectorAll('.count-buttons__input');
    const totalPriceElement = document.querySelector('.total_price');

    // Функция для обновления итоговой цены
    function updateTotalPrice() {
        let total = 0;
        document.querySelectorAll('.cart_product').forEach(product => {
            const price = parseFloat(product.querySelector('.product_price p').textContent.replace('₽', '').trim());
            const quantity = parseInt(product.querySelector('.count-buttons__input').value);
            total += price * quantity;
        });
        totalPriceElement.textContent = total.toFixed(2) + ' ₽';
    }

    // Добавляем обработчики на изменение количества
    quantityInputs.forEach(input => {
        input.addEventListener('change', updateTotalPrice);
    });

    // Инициализация итоговой цены
    updateTotalPrice();
});