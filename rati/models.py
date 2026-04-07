from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Rent(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="rent_images")
    desc=models.TextField()
    price=models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    isdelete=models.BooleanField(default=True)
    location = models.CharField(max_length=200,null=True)
    categories = models.ManyToManyField(Category)
    phone=models.PositiveBigIntegerField(null=True)

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user=models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to="profile_images")
    bio=models.TextField()
    dob=models.DateField(null=True)

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.PositiveBigIntegerField()
    message=models.TextField()

    def __str__(self):
        return self.name