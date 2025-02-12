from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Product, Region, CustomUser, Category, Brand, ProductAttribute, OrderItem, Order, AdressRegion
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def index(request):
    # Получаем первые 20 товаров
    products = Product.objects.prefetch_related('images').all()[:20]

    # Получаем корзину из сессии
    cart = request.session.get('cart', [])
    favorites = request.session.get('favorites', [])
    comparison = request.session.get('comparisons', [])
    cart_count = len(cart)
    favorites_count = len(favorites)
    comparisons_count = len(comparison)

    # Получаем ID региона из cookie
    region_id = request.COOKIES.get('SelectRegion')

    # Инициализация переменных
    images = None

    try:
        # Если регион есть в cookie, пытаемся его найти
        if region_id:
            region = Region.objects.prefetch_related('images').get(id=region_id)
        else:
            # Если регион не указан, выбираем первый
            region = Region.objects.prefetch_related('images').first()

        # Получаем первое изображение региона
        if region and region.images.exists():
            images = [{'url': image.image.url, 'description': image.description or ''} for image in region.images.all()]

    except Region.DoesNotExist:
        region = None
        image = None

    return render(request, 'index.html', {
        'products': products,
        'cart_count': cart_count,
        'favorites_count': favorites_count,
        'comparisons_count': comparisons_count,
        'region': region,
        'images': images,  # Передаем одно изображение
    })


def category(request, brand_name=None, brand_filter=None):
    # Получаем все продукты
    products = Product.objects.all()

    # Фильтрация по бренду
    brand_name = request.GET.get('brand')  # Получаем параметр 'brand' из запроса
    if brand_name:
        brand_filter = Brand.objects.filter(name=brand_name).first()
        if brand_filter:
            products = products.filter(brand=brand_filter)

    # Фильтрация по категории
    category_name = request.GET.get('category')
    if category_name:
        category_filter = Category.objects.filter(name=category_name).first()
        if category_filter:
            products = products.filter(category=category_filter)

    attributes = ProductAttribute.objects.filter(product__category=category_filter).values('name').distinct()
    for attribute in attributes:
        attribute_value = request.GET.get(attribute['name'])
        if attribute_value:
            products = products.filter(attributes__name=attribute['name'], attributes__value=attribute_value)

    # Фильтрация по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Сортировка продуктов по полю, если параметр sort присутствует в запросе
    # Ваша логика сортировки (не показана в примере)

    # Получаем количество товаров в корзине, избранном и сравнении
    cart = request.session.get('cart', [])
    favorites = request.session.get('favorites', [])
    comparison = request.session.get('comparisons', [])
    cart_count = len(cart)
    favorites_count = len(favorites)
    comparisons_count = len(comparison)

    return render(request, 'category.html', {
        'products': products,
        'brand': brand_filter,
        'cart_count': cart_count,
        'attributes': attributes,
        'favorites_count': favorites_count,
        'comparisons_count': comparisons_count
    })


def add_to_cart(request, product_id):
    product_id_str = str(product_id)
    cart = request.session.get('cart', [])

    if product_id_str not in cart:
        cart.append(product_id_str)
        request.session['cart'] = cart  # Сохраняем корзину в сессии

    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart.remove(product_id_str)  # Удаляем товар из корзины
        request.session['cart'] = cart

    return redirect('cart')


def remove_all_form_cart(request):
    request.session['cart'] = []
    return  redirect('cart')


def cart(request):
    cart = request.session.get('cart', [])
    cart_count = len(cart)  # Подсчитываем количество товаров в корзине
    product_ids = [int(product_id_str) for product_id_str in cart]
    products_in_cart = Product.objects.filter(id__in=product_ids)

    total_price = sum(product.price for product in products_in_cart)

    favorites = request.session.get('favorites', [])
    comparison = request.session.get('comparisons', [])
    favorites_count = len(favorites)
    comparisons_count = len(comparison)

    # Проверяем, авторизован ли пользователь
    user_authenticated = request.user.is_authenticated
    user_data = {
        'name': request.user.name if user_authenticated else '',
        'surname': request.user.surname if user_authenticated else '',
        'email': request.user.email if user_authenticated else '',
        'phone': '',  # Здесь можете добавить логику для получения телефона пользователя, если это нужно
    }

    if request.method == 'POST':
        # Обработка отправки формы
        if user_authenticated:
            # Создаем заказ
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                status='Pending'  # Статус нового заказа
            )

            # Добавляем товары в заказ
            for product in products_in_cart:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=cart.count(str(product.id)),
                    price=product.price
                )

            # Очищаем корзину после оформления заказа
            request.session['cart'] = []

            # Перенаправляем пользователя на страницу с подтверждением или на его личный кабинет
            return redirect('dashboard')  # Замените на вашу страницу подтверждения заказа

    return render(request, 'cart.html', {
        'products': products_in_cart,
        'cart_count': cart_count,
        'total_price': total_price,
        'favorites_count': favorites_count,
        'comparisons_count': comparisons_count,
        'user_authenticated': user_authenticated,
        'user_data': user_data,
    })

def get_addresses(request, region_id):
    # Получаем все адреса для выбранного региона
    addresses = AdressRegion.objects.filter(region_id=region_id)

    # Формируем ответ с данными адресов
    address_data = [
        {'id': address.id, 'name': address.name} for address in addresses
    ]

    return JsonResponse(address_data, safe=False)


def register(request):
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Проверяем, чтобы все поля были заполнены
        if not all([name, surname, phone_number, email, password, password_confirm]):
            return HttpResponse("Пожалуйста, заполните все поля", status=400)

        # Проверка и исправление номера телефона
        if phone_number.startswith('8'):
            phone_number = '+7' + phone_number[1:]  # Заменяем 8 на +7
        elif not phone_number.startswith('+7'):
            phone_number = '+7' + phone_number  # Добавляем +7, если нет

        # Проверяем, чтобы пароли совпадали
        if password != password_confirm:
            return HttpResponse("Пароли не совпадают", status=400)

        if CustomUser.objects.filter(email=email).exists():
            return HttpResponse("Пользователь с таким email уже существует", status=400)

        # Проверяем, существует ли уже пользователь с таким номером телефона
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return HttpResponse("Пользователь с таким номером телефона уже существует", status=400)

        # Проверяем пароль с использованием валидаторов
        try:
            validate_password(password)  # Применяем стандартные проверки пароля Django
        except ValidationError as e:
            return HttpResponse(f"Пароль не соответствует требованиям: {'; '.join(e.messages)}", status=400)

        # Хешируем пароль
        hashed_password = make_password(password)

        # Создаем нового пользователя и сохраняем в базе данных
        user = CustomUser(
            name=name,
            surname=surname,
            phone_number=phone_number,
            email=email,
            password=hashed_password,
        )
        user.save()

        # Аутентификация и вход пользователя
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Перенаправляем на страницу dashboard после успешной регистрации

    cart = request.session.get('cart', [])
    favorites = request.session.get('favorites', [])
    comparison = request.session.get('comparisons', [])
    cart_count = len(cart)
    favorites_count = len(favorites)
    comparisons_count = len(comparison)

    return render(request, 'register.html', {
        'cart_count': cart_count,
        'favorites_count': favorites_count,
        'comparisons_count':comparisons_count
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        # Проверяем и корректируем номер телефона
        if phone_number.startswith('8'):
            phone_number = '+7' + phone_number[1:]  # Заменяем 8 на +7
        elif not phone_number.startswith('+7'):
            phone_number = '+7' + phone_number  # Добавляем +7, если нет

        # Аутентификация пользователя через кастомный бэкенд
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # После входа перенаправляем на dashboard
        else:
            return HttpResponse("Неверный логин или пароль", status=400)



    return render(request, 'login.html')


@login_required
def dashboard(request):
    user = request.user
    orders = Order.objects.filter(user=user).prefetch_related('items__product')

    cart = request.session.get('cart', [])
    favorites = request.session.get('favorites', [])
    comparison = request.session.get('comparisons', [])
    cart_count = len(cart)
    favorites_count = len(favorites)
    comparisons_count = len(comparison)

    return render(request, 'dashboard.html', {'user': user, 'orders': orders, 'favorites_count': favorites_count, 'comparisons_count': comparisons_count, 'cart_count': cart_count})


def logout_view(request):
    logout(request)
    return redirect('login')


def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    attributes = product.attributes.all()
    images = product.images.all()

    context = {
        'product': product,
        'attributes': attributes,
        'images': images,
    }
    return render(request, 'product.html', context)


def comparison(request):
    comparison = request.session.get('comparisons', [])
    comparison_count = len(comparison)  # Подсчитываем количество товаров в корзине
    product_ids = [int(product_id_str) for product_id_str in comparison]
    products_in_comparison = Product.objects.filter(id__in=product_ids)

    total_price = sum(product.price for product in products_in_comparison)

    # Получаем товары из корзины
    products_in_comparison = Product.objects.filter(id__in=product_ids)

    favorites = request.session.get('favorites', [])
    cart = request.session.get('cart', [])
    favorites_count = len(favorites)
    cart_count = len(cart)

    return render(request, 'cart.html', {'products': products_in_comparison, 'comparison_count': comparison_count, 'total_price': total_price, 'favorites_count': favorites_count, 'cart_count': cart_count})


def add_to_favorite(request, product_id):
    product_id_str = str(product_id)
    favorite = request.session.get('favorite', [])

    if product_id_str not in favorite:
        favorite.append(product_id_str)
        request.session['favorite'] = favorite

    return redirect('favorite')


def remove_from_favorite(request, product_id):
    favorite = request.session.get('favorite', [])
    product_id_str = str(product_id)

    if product_id_str in favorite:
        favorite.remove(product_id_str)  # Удаляем товар из корзины
        request.session['favorite'] = favorite

    return redirect('favorite')


def favorite(request):

    favorite = request.session.get('favorite', [])
    favorites_count = len(favorite)  # Подсчитываем количество товаров в корзине
    product_ids = [int(product_id_str) for product_id_str in favorite]

    products_in_cart = Product.objects.filter(id__in=product_ids)

    cart = request.session.get('cart', [])
    comparison = request.session.get('comparisons', [])
    cart_count = len(cart)
    comparisons_count = len(comparison)

    return render(request, 'favorite.html', {
        'products': products_in_cart,
        'favorites_count': favorites_count,
        'cart_count': cart_count,
        'comparisons_count': comparisons_count
    })

def add_to_comparisons(request, product_id):
    product_id_str = str(product_id)
    comparison = request.session.get('comparison', [])

    if product_id_str not in comparison:
        comparison.append(product_id_str)
        request.session['comparison'] = comparison  # Сохраняем корзину в сессии

    return redirect('comparison')

def remove_from_comparisons(request, product_id):
    comparison = request.session.get('comparison', [])
    product_id_str = str(product_id)

    if product_id_str in comparison:
        comparison.remove(product_id_str)  # Удаляем товар из корзины
        request.session['comparison'] = comparison

    return redirect('comparison')

def comparisons(request):

    comparison = request.session.get('comparison', [])
    comparison_count = len(comparison)  # Подсчитываем количество товаров в корзине
    product_ids = [int(product_id_str) for product_id_str in comparison]

    products_in_cart = Product.objects.filter(id__in=product_ids)

    cart = request.session.get('cart', [])
    favorites = request.session.get('favorites', [])
    cart_count = len(cart)
    favorites_count = len(favorites)

    return render(request, 'comparisons.html', {
        'products': products_in_cart,
        'comparison_count': comparison_count,
        'cart_count': cart_count,
        'favorites_count': favorites_count
    })
def search_view(request):
    query = request.GET.get('query', '')
    if query:
        # Получаем продукты, которые соответствуют запросу
        products = Product.objects.prefetch_related('images').filter(name__icontains=query)[:10]

        # Формируем результаты
        results = []
        for product in products:
            # Получаем список URL изображений для текущего продукта
            images = [
                {'url': image.image.url, 'description': image.description or ''}
                for image in product.images.all()
            ]
            # Добавляем продукт в список результатов
            results.append({
                'id': str(product.id),  # Преобразуем UUID в строку
                'name': product.name,
                'images': images  # Список изображений
            })
    else:
        results = []

    return JsonResponse(results, safe=False)

def about(request):
    return render(request, 'about.html')

def buy_in_credit(request):
    return render(request, 'buy-in-credit.html')

def clients(request):
    return render(request, 'clients.html')

def contacs(request):
    return render(request, 'contacs.html')

def delivery(request):
    return render(request, 'delivery.html')

def favorites(request):
    return render(request, 'favorite.html')

def garantiya(request):
    return render(request, 'garantiya.html')

def garantiya_nizkih_cen(request):
    return render(request, 'garantiya-nizkih-cen.html')

def payment(request):
    return render(request, 'payment.html')

def samovizov(request):
    return render(request, 'samovizov.html')

def about(request):
    return render(request, 'about.html')
def search_products(request):
    try:
        query = request.GET.get('query', '').strip().lower()

        if not query or len(query) < 0:
            return JsonResponse({'error': 'Введите хотя бы 3 символа.'}, status=400)

        products = Product.objects.filter(name__icontains=query)

        if not products.exists():
            return JsonResponse([], safe=False)

        results = []
        for product in products:
            # Получаем все изображения для текущего продукта
            images = product.images.all()  # Используем related_name 'images'

            # Если изображения есть, выбираем первое
            image_url = images[0].image.url if images else None

            results.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image': image_url  # Передаем ссылку на изображение
            })

        return JsonResponse(results, safe=False)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': 'Произошла ошибка на сервере.'}, status=500)
def update_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']
        new_quantity = data['quantity']

        # Находим товар в базе данных
        product = Product.objects.get(id=product_id)
        product.quantity = new_quantity
        product.save()

        # Пересчитываем общую стоимость корзины
        total_price = sum(item.quantity * item.price for item in сart.objects.all())

        return JsonResponse({
            'newQuantity': new_quantity,
            'totalPrice': total_price,
        })