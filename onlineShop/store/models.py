from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return str(self.user)


class Product(models.Model):
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', null=True, blank=True)
    price = models.DecimalField('Цена', max_digits=30, decimal_places=2)
    is_digit = models.BooleanField('Цифровой', default=False, blank=False)
    image = models.ImageField('Изображение', upload_to='product_images', default='default.png', null=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order_dt = models.DateTimeField('Время заказа', auto_now_add=True)
    transaction_id = models.CharField('Id заказа', max_length=150)
    is_completed = models.BooleanField('Завершен', default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)

    @property
    def get_total_price(self):
        total = sum([order_item.get_total_price for order_item in self.orderitem_set.all()])
        return total

    @property
    def get_total_items(self):
        total = sum([order_item.quantity for order_item in self.orderitem_set.all()])
        return total

    @property
    def need_shipping(self):
        shipping = False
        for order_item in self.orderitem_set.all():
            if not order_item.product.is_digit:
                shipping = True
                break
        return shipping


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField('Количество', default=0, blank=True)
    added_dt = models.DateTimeField('Время добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return str(self.product)

    @property
    def get_total_price(self):
        return self.quantity * self.product.price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField('Адресс', max_length=150)
    city = models.CharField('Город', max_length=150)
    state = models.CharField('Область', max_length=150)
    zip_code = models.CharField('Zip', max_length=50)

    class Meta:
        verbose_name = 'Адресс доставки'
        verbose_name_plural = 'Адресса доставки'

    def __str__(self):
        return self.address