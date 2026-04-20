from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class User(models.Model):
    user=models.ForeignKey(Login, on_delete=models.CASCADE)
    username = models.CharField(max_length=30,null=True)
    name=models.CharField(max_length=50,null=True)
    address = models.TextField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    image = models.ImageField(upload_to='User',null=True)

class Farmer(models.Model):
    user=models.ForeignKey(Login, on_delete=models.CASCADE)
    username = models.CharField(max_length=30,null=True)
    name=models.CharField(max_length=50,null=True)
    address = models.TextField(max_length=50,null=True)
    phone = models.IntegerField(null=True) 
    email = models.EmailField(null=True)
    image = models.ImageField(upload_to='Farmer',null=True)

class Delivery(models.Model):
    user=models.ForeignKey(Login, on_delete=models.CASCADE)
    username = models.CharField(max_length=30,null=True)
    name=models.CharField(max_length=50,null=True)
    address = models.TextField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    image = models.ImageField(upload_to='Delivery',null=True)

class Product(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', null=True)
    status = models.CharField(max_length=50, default='pending')

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.product.price * self.quantity

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(Cart)
    payment_method = models.CharField(max_length=50)  # 'Card' or 'Home Delivery'
    card_holder = models.CharField(max_length=100, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    expiry_date = models.CharField(max_length=5, null=True, blank=True)
    cvv = models.CharField(max_length=4, null=True, blank=True)
    total_amount = models.FloatField()
    status = models.CharField(max_length=20, default='Pending')  # 'Paid' once done
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_status = models.CharField(max_length=50, default='In Progress')  # New Field
    payment_verification = models.CharField(max_length=50, default='Not Verified')  # New Field
    delivery_name = models.CharField(max_length=100, null=True, blank=True)
    delivery_phone = models.CharField(max_length=15, null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    delivery_pin = models.CharField(max_length=10, null=True, blank=True)



class CheckoutItem(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Supply(models.Model):
    CATEGORY_CHOICES = (
        ('Seed', 'Seed'),
        ('Fertilizer', 'Fertilizer'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.FloatField() 
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='supplies/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FavoriteSupply(models.Model):
    user = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class SupplyOrder(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.FloatField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default='Pending')  # e.g., Pending, Delivered

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.supply.price
        super().save(*args, **kwargs)

class SupplyCheckout(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    card_holder = models.CharField(max_length=100, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    expiry_date = models.CharField(max_length=5, null=True, blank=True)  # MM/YY
    cvv = models.CharField(max_length=4, null=True, blank=True)
    total_amount = models.FloatField()
    status = models.CharField(max_length=30, default='Pending')  # Paid / Home Delivery
    ordered_at = models.DateTimeField(auto_now_add=True)
    assigned_delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_status = models.CharField(max_length=50, default='In Progress')  # New Field
    payment_verification = models.CharField(max_length=50, default='Not Verified')  # New Field
    delivery_name = models.CharField(max_length=100, null=True, blank=True)
    delivery_phone = models.CharField(max_length=15, null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    delivery_pin = models.CharField(max_length=10, null=True, blank=True)


class SupplyCheckoutItem(models.Model):
    checkout = models.ForeignKey(SupplyCheckout, on_delete=models.CASCADE)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class SupplyReview(models.Model):
    checkout = models.ForeignKey(SupplyCheckout, on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    rating = models.IntegerField()  # e.g., 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
