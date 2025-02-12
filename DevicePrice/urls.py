from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Добавление в корзину
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-all-from-cart/', views.remove_all_form_cart, name='remove_all_from_cart'),
    path('cart/', views.cart, name='cart'),  # Путь для главной страницы
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('category/', views.category, name='category'),  # Путь для главной страницы
    path('product/<int:product_id>', views.product, name='product'),  # Путь для главной страницы
    path('comparisons/', views.comparisons, name='comparisons'),
    path('add-to-comparisons/<int:product_id>', views.add_to_comparisons, name='add_to_comparisons'),
    path('remove-from-comparisons/<int:product_id>', views.remove_from_comparisons, name='remove_from_comparisons'),
    path('favorite/', views.favorite, name='favorite'),
    path('add-to-favorite/<int:product_id>', views.add_to_favorite, name='add_to_favorite'),
    path('remove-from-favorite/<int:product_id>', views.remove_from_favorite, name='remove_from_favorite'),
    path('about/', views.about, name='about'),
    path('buy-in-credit/', views.buy_in_credit, name='buy_in_credit'),
    path('clients/', views.clients, name='clients'),
    path('contacs/', views.contacs, name='contacs'),
    path('delivery/', views.delivery, name='delivery'),
    path('garantiya/', views.garantiya, name='garantiya'),
    path('garantiya-nizkih-cen/', views.garantiya_nizkih_cen, name='garantiya_nizkih_cen'),
    path('samovizov/', views.samovizov, name='samovizov'),
    path('paymnet/', views.payment, name='payment'),
    path('search/', views.search_products, name='search_products'),
    path('get_addresses/<int:region_id>/', views.get_addresses, name='get_addresses'),

]
