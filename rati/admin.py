from django.contrib import admin
from .models import Rent,Category,Contact,Product
# Register your models here.
admin.site.register([Rent,Category,Contact,Product])