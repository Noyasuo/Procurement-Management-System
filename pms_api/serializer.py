from rest_framework import serializers
from core.models import Account, Product, OrderRefund, Order, Payment, Category
from rest_framework.response import Response


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('username', 'email', 'password')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)  

    class Meta:
        model = Product
        fields = ['id', 'user', 'title', 'description', 'stock', 'category', 'image', 'barcode', 'created_at']

    def create(self, validated_data):
        category_data = validated_data.pop('category', None)
        
        # Create product and associate with the category
        product = Product.objects.create(category=category_data, **validated_data)
        return product

class AccountDetailsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = AccountDetailsSerializer()
    product = ProductSerializer(many=True)  

    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'quantity', 'request_date', 'status', 'approval_date', 'comments', 
                  'last_update_by', 'invoice_number', 'total', 'final_status']

class OrderRefundSerializer(serializers.ModelSerializer):
    user = AccountDetailsSerializer(required=False)
    order = OrderSerializer(required=False)

    class Meta:
        model = OrderRefund
        fields = ['id', 'user', 'order', 'reason', 'refund_amount', 'status', 'request_date', 'approval_date', 'comments']

    def update(self, instance, validated_data):
        # Only update fields if they are provided in the validated_data
        user = validated_data.get('user', instance.user)
        order = validated_data.get('order', instance.order)
        refund_amount = validated_data.get('refund_amount', instance.refund_amount)
        status = validated_data.get('status', instance.status)

        instance.user = user
        instance.order = order
        instance.refund_amount = refund_amount
        instance.status = status
        instance.save()
        return instance

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'order',
            'amount',
            'payment_method',
            'status',
            'transaction_id',
            'payment_date',
            'comments'
        ]
        read_only_fields = ['id', 'payment_date']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.CharField

    class Meta:
        model = Account
        fields = ['email']
