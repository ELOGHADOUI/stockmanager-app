from django.contrib import admin
from .models import CustomUser, Product, StockMovement

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email', 'first_name', 'last_name')
    list_filter = ('role',)
    search_fields = ('username', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'low_stock_threshold')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'movement_type', 'date', 'user')
    list_filter = ('movement_type', 'date')
    search_fields = ('product__name',)
