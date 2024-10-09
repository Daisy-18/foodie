from django.contrib import admin
from . models import Product, Customer, Reservation, Feedback, Cart
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'ProductId', 'price', 'food_name', 'food_category', 'sub_category', 'Image')

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'village', 'city', 'mobile', 'pincode', 'state')
    search_fields = ('name', 'village', 'city', 'mobile', 'pincode', 'state')

@admin.register(Reservation)
class ReservationModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'time', 'guests')
    search_fields = ('name', 'email', 'date', 'time', 'guests')
    list_filter = ('date', 'time', 'guests')

@admin.register(Feedback)
class FeedbackModelAdmin(admin.ModelAdmin):
    list_display=['name', 'email', 'comment']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    def products(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', link, obj.product.food_name)
