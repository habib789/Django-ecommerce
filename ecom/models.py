from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='ecom/photos')
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self):
        self.slug = slugify(self.title)
        super(Product, self).save()

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='pending')
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        # return f"{self.quantity} of {self.products.title}"
        return self.user.username

    def total_price(self):
        return self.products.price * self.quantity

    # def final_price(self):
    #     return self.total_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_products = models.ManyToManyField(Cart, related_name='cart')
    order_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(blank=True, null=True)
    order_address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for product in self.cart_products.all():
            total += product.total_price()
        return total

    class Meta:
        ordering = ['-order_date']


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=60)
    contact_no = models.CharField(max_length=14)
    street_address = models.CharField(max_length=200)
    country = models.CharField(max_length=20)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
