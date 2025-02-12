function loadAddresses(regionId) {
        const addressSelector = document.getElementById('address-selector');
        addressSelector.innerHTML = '<option value="">Загрузка...</option>';

        fetch(`/api/addresses/${regionId}/`)
            .then(response => response.json())
            .then(data => {
                addressSelector.innerHTML = '<option value="">Выберите адрес</option>';
                data.forEach(address => {
                    const option = document.createElement('option');
                    option.value = address.id;
                    option.textContent = address.name;
                    addressSelector.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Ошибка при загрузке адресов:', error);
                addressSelector.innerHTML = '<option value="">Ошибка загрузки</option>';
            });
    }