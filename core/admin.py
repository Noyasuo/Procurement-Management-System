from django.contrib import admin
from django.utils.html import mark_safe
from django.contrib.auth.admin import UserAdmin


from .models import Account, Category, Product, Order, OrderRefund, Payment

class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'mobile_number', 'contact_number', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'user_type')
    list_filter = ('user_type', 'is_active', 'is_staff')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_available', 'stock', 'category', 'image_tag', 'barcode', 'created_at')
    list_filter = ('category',)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return 'No image'
    
    image_tag.short_description = 'Image'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'quantity', 'status', 'final_status', 'request_date', 'get_products')
    
    def get_products(self, obj):
        return ", ".join([product.title for product in obj.product.all()]) 
    get_products.short_description = 'Products'  

    list_filter = ('status', 'request_date')
    search_fields = ('user__username', 'product__title')
    ordering = ('-request_date',)

class OrderRefundAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'refund_amount', 'status', 'request_date', 'approval_date')
    list_filter = ('status', 'request_date')
    search_fields = ('user__username', 'order__product__title')
    ordering = ('-request_date',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order', 'amount', 'payment_method', 'status', 'payment_date']
    search_fields = ['user__username', 'order__id', 'transaction_id']
    list_filter = ['status', 'payment_method', 'payment_date']

# Register the models with the custom admin interface
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderRefund, OrderRefundAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Payment, PaymentAdmin)
