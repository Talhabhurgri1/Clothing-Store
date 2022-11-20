
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# models are customer/product/order
# customer_address 


class Customer(models.Model):
    # columns 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    phonenumber = models.CharField(max_length=14)    
    first_name = models.CharField(max_length=30, null=False, blank=False, default="None") # noqa
    last_name = models.CharField(max_length=30, null=False,  blank=False, default="None") # noqa
    
    date_created = models.DateTimeField(auto_now_add=True)
    profilepic = models.ImageField(null=True, blank=True, default="user.png", upload_to="user/images") # noqa
    id_number = models.CharField(max_length=20, blank=False, null=False, default= "None") # noqa

    def __str__(self):     
        return f"{self.first_name +' ' + self.last_name}"


class Product(models.Model):
    # Categories
    categories = (
        ('shirt', 'shirt'),
        ('jeans', 'jeans'),
        ('shoes', 'shoes'),

    )
    # Size 
    size = (
        ('small', 'small'), ('medium', 'medium'), ('large', 'large')
    )
    # columns 
    product_name = models.CharField(max_length=30, blank=False)
    product_category = models.CharField(max_length=14, choices=categories, blank=False) # noqa
    product_price = models.IntegerField(blank=False)
    product_size = models.CharField(max_length=15, choices=size, blank=False, default="medium") # noqa
    product_quantity = models.IntegerField(blank=False)
    product_pic = models.ImageField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Product: {self.product_name}"
    # columns 
    
    def serialize(self):
        return {
            "product_name": self.product_name,
            "product_category": self.product_category,
            "product_price": self.product_price,
            "photo": self.product_pic.url if self.product_pic else None
        }

# Order model


class Order(models.Model):    
    # columns
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, related_name="products")
    product_quantity = models.IntegerField(default=0)
    product_price = models.IntegerField(default=0)
    # product_size = models.CharField(max_length=15,default="medium")
    status = (
        ('pending', 'pending'),
        ('out for delivery', 'out for delivery'),
        
    )
    order_status = models.CharField(max_length=20, choices=status, blank=False, default='pending') # noqa
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer.user.username} Order"
   

class Reviews(models.Model):

    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE, unique=False) # noqa
    product = models.ManyToManyField(Product)
    review_text = models.TextField()
    
    class Meta:
        db_table = "Reviews"
    
    def __str__(self):
        return f"{self.customer_name.user.username} on {self.product}" 



