from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

### ✅ MongoDB Atlas (Products, Categories, Orders, Cart)
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        app_label = 'store'
        db_table = 'category'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.using('mongodb').filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(using='mongodb', *args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        app_label = 'store'
        db_table = 'product'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.using('mongodb').filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(using='mongodb', *args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        app_label = 'store'
        db_table = 'cart'

    def save(self, *args, **kwargs):
        super().save(using='mongodb', *args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'store'
        db_table = 'order'

    def save(self, *args, **kwargs):
        super().save(using='mongodb', *args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


### ✅ SQLite (User Authentication)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    class Meta:
        app_label = 'auth'
        db_table = 'profile'

    def __str__(self):
        return self.user.username


class NavbarLink(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    class Meta:
        app_label = 'store'
        db_table = 'navbar_link'

    def __str__(self):
        return self.name
