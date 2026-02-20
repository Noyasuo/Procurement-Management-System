from django.contrib import admin
from django.utils.html import mark_safe
from django.contrib.auth.admin import UserAdmin


from .models import Account, Category, Product, Order, OrderRefund, Payment

class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'mobile_number', 'contact_number', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'user_type')
    list_filter = ('user_type', 'is_active', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile_number', 'contact_number')}),
        ('Account Type', {'fields': ('user_type', 'position')}),
        ('Additional Info', {'fields': ('id_number', 'address', 'business_permit')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
        ('Account Type', {'fields': ('user_type', 'position')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'mobile_number', 'contact_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

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
    list_display = ('id', 'user', 'quantity', 'status_display', 'final_status', 'request_date', 'get_products')
    
    def get_products(self, obj):
        return ", ".join([product.title for product in obj.product.all()]) 
    get_products.short_description = 'Products'
    
    def status_display(self, obj):
        """Display status in a user-friendly way"""
        if obj.status == 'reviewed':
            return 'Awaiting Municipal Approval'
        elif obj.status == 'pending':
            return 'Pending Procurement Review'
        elif obj.status == 'approved':
            return 'Approved'
        elif obj.status == 'rejected':
            return 'Rejected'
        else:
            return obj.get_status_display()
    status_display.short_description = 'Procurement Status'

    list_filter = ('status', 'request_date')
    search_fields = ('user__username', 'product__title')
    ordering = ('-request_date',)
    
    def get_queryset(self, request):
        """Filter queryset based on user role"""
        qs = super().get_queryset(request)
        
        # Municipal Admin only sees orders with status='reviewed' (awaiting their approval)
        if hasattr(request, 'user') and request.user.user_type == 'municipal_admin':
            qs = qs.filter(status='reviewed')
        
        return qs
    
    def approve_order(self, request, queryset):
        """Action to approve an order"""
        updated = queryset.update(final_status='approved')
        self.message_user(request, f'{updated} order(s) approved successfully.')
    approve_order.short_description = "Approve selected orders"
    
    def decline_order(self, request, queryset):
        """Action to decline an order"""
        updated = queryset.update(final_status='rejected')
        self.message_user(request, f'{updated} order(s) declined successfully.')
    decline_order.short_description = "Decline selected orders"
    
    def get_actions(self, request):
        """Show approve/decline actions only for Municipal Admin viewing reviewed orders"""
        actions = super().get_actions(request)
        
        # Only Municipal Admin sees the approve/decline actions
        if hasattr(request, 'user') and request.user.user_type == 'municipal_admin':
            actions['approve_order'] = self.approve_order
            actions['decline_order'] = self.decline_order
        
        return actions

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
