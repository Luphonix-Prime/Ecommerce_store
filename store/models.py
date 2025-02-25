from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)



    def _str_(self):

        return self.name



class Product(models.Model):

    name = models.CharField(max_length=200)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    price = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField()

    image = models.ImageField(upload_to='products/')



    def _str_(self):

        return str(self.name)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    objects = models.Manager()  # Ensure default manager is available

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # Ensure default manager is available

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.user.username