from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("Слаг (URL)", unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products', 
        verbose_name="Категория"
    )
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField("Изображение", upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField("Доступен для продажи", default=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='cart', 
        verbose_name="Пользователь"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Позиция в корзине"
        verbose_name_plural = "Позиции в корзине"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('assembling', 'Собирается на складе'),
        ('delivering', 'Передан службе доставки'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='orders', 
        verbose_name="Покупатель"
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new')
    total_price = models.DecimalField("Итоговая стоимость", max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ №{self.id} ({self.user.username})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items', 
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Товар"
    )
    price = models.DecimalField("Цена при заказе", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"
