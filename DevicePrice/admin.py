from django.contrib import admin
from .models import Product, ProductImage, Region, RegionImage, Order, CustomUser, Category, OrderItem, Brand, ProductAttribute, AdressRegion


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1  # Это количество пустых строк, которые будут отображаться для ввода новых атрибутов
    fields = ['name', 'value']  # Поля для редактирования (название и значение)

# Инлайн для изображений продукта
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'description']

# Управление продуктами
class ProductManager(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category')  # Добавлена категория
    list_filter = ('category',)  # Фильтр по категориям
    search_fields = ('name', 'description')  # Поиск по имени и описанию
    inlines = [ProductAttributeInline, ProductImageInline]  # Добавлен инлайн для характеристик

# Регистрация продуктов
admin.site.register(Product, ProductManager)

# Управление категориями
class CategoryManager(admin.ModelAdmin):
    list_display = ('name', 'parent_category')  # Показ подкатегорий
    search_fields = ('name',)  # Поиск по имени
    list_filter = ('parent_category',)  # Фильтр по родительской категории

# Регистрация категорий
admin.site.register(Category, CategoryManager)

class BrandManager(admin.ModelAdmin):
    list_display = ('name', 'parent_category')  # Показ подкатегорий
    search_fields = ('name',)  # Поиск по имени
    list_filter = ('parent_category',)  # Фильтр по родительской категории

# Регистрация категорий
admin.site.register(Brand, BrandManager)

# Инлайн для изображений регионов
class RegionImageInline(admin.TabularInline):
    model = RegionImage
    extra = 1
    fields = ['image', 'description']

class AdressRegionInline(admin.TabularInline):
    model = AdressRegion
    extra = 1  # Количество пустых строк для добавления новых адресов
    fields = ('name',)  # Показать только имя адреса, можно добавить другие поля

# Управление регионами
class RegionManager(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [AdressRegionInline, RegionImageInline]

# Регистрация регионов
admin.site.register(Region, RegionManager)

# Управление заказами
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity', 'price']  # Поля для редактирования

class OrderManager(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'total_price', 'status')
    list_filter = ('status', 'created')  # Фильтры по статусу и дате создания
    search_fields = ('user__name', 'user__surname')  # Поиск по имени и фамилии пользователя
    inlines = [OrderItemInline]

# Регистрация заказов
admin.site.register(Order, OrderManager)

# Управление пользователями
class CustomUserManager(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone_number')
    search_fields = ('name', 'surname', 'phone_number')  # Поиск по имени, фамилии и номеру телефона

admin.site.register(CustomUser, CustomUserManager)

# Управление товарами в заказах (опционально)
class OrderItemManager(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order',)

admin.site.register(OrderItem, OrderItemManager)
