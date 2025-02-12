from django.db import models
from django.core.validators import RegexValidator
from django.utils.timezone import now
from django.core.validators import EmailValidator


# Модель для хранения информации о пользователях
class CustomUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[RegexValidator(regex=r'^\+7\d{10}$', message="Введите корректный российский номер телефона")]
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        null=True,
        validators=[EmailValidator(message="Введите корректный адрес электронной почты")]
    )
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        if not self.last_login:
            self.last_login = now()
        super().save(*args, **kwargs)

    @property
    def is_authenticated(self):
        return True

# Модель для категорий товаров
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories'
    )  # Подкатегории (иерархия )

    def __str__(self):
        return self.name

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtypes'
    )  # Подкатегории (иерархия)

    def __str__(self):
        return self.name




# Модель для хранения информации о товарах
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')  # Привязка к категории
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand', null=True, blank=True)

    def __str__(self):
        return self.name

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=255)  # Название характеристики (например, "Цвет", "Вес")
    value = models.CharField(max_length=255)  # Значение характеристики (например, "Черный", "1.5 кг")

    def __str__(self):
        return f"{self.name}: {self.value} for {self.product.name}"

    class Meta:
        unique_together = ('product', 'name')  # Каждое имя характеристики должно быть уникальным для одного продукта


# Модель для изображений товаров
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"


# Модель для заказов
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')  # Привязка к пользователю
    created = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Ожидание'), ('Completed', 'Завершен'), ('Cancelled', 'Отменен')],
        default='Pending'
    )

    def __str__(self):
        return f"Order {self.id} by {self.user}"


# Модель для товаров в заказе
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена на момент заказа

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"


class AdressRegion(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, null=False, blank=False)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.name

# Модель для регионов (доставка или размещение)
class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Модель для изображений регионов
class RegionImage(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='region_images/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.region.name}"
