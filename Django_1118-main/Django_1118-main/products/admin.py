from django.contrib import admin

# Register your models here.
from .models import Product, Size  # 從.models中引用Product函數建立的模型樣式

admin.site.register(Size)
admin.site.register(Product)  # 將products放置在網站上
