from rest_framework import generics, serializers, status
from rest_framework import status as res_status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import send_mail

from pms_api.serializer import OrderRefundSerializer, OrderSerializer
from core.models import OrderRefund, Order, Product, Account

@extend_schema(tags=["Order Refund"])
class OrderRefundListCreateView(generics.ListCreateAPIView):
    queryset = OrderRefund.objects.all()
    serializer_class = OrderRefundSerializer

    def get_queryset(self):
        # Filter payments to only return those related to the current user
        return OrderRefund.objects.filter(user=self.request.user)

@extend_schema(tags=["Order Refund"])
class OrderRefundDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderRefund.objects.all()
    serializer_class = OrderRefundSerializer


@extend_schema(tags=["Order"])
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        product_name = data.get('product_name')
        quantity = data.get('quantity')
        description = data.get('description')

        # Find the product by title
        product = Product.objects.filter(title=product_name).first()
        if not product:
            return Response(
                {"error": f"Product with title '{product_name}' does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the order instance
        order = Order.objects.create(
            user=request.user,
            comments=description,
            quantity=quantity,
            last_update_by=request.user
        )
        order.product.add(product)

        # Retrieve all admin emails dynamically
        admin_emails = Account.objects.filter(is_superuser=True).values_list('email', flat=True)

        # Prepare and send the email
        subject = f"New Order Created by {request.user.username}"
        message = (
            f"A new order has been created.\n\n"
            f"Order Details:\n"
            f"- Product: {product.title}\n"
            f"- Quantity: {quantity}\n"
            f"- Comments: {description}\n"
            f"- Created By: {request.user.username}\n"
        )
        recipient_list = list(admin_emails)  # Include all admins

        send_mail(
            subject,
            message,
            "michealnoya159@gmail.com",  # Replace with your email
            recipient_list + [request.user.email],
            fail_silently=False,
        )

        # Serialize and return the created order
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Order"])
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        order = self.get_object()

        # Update status and final status
        order_status = request.data.get('status', None)  # Renamed variable
        final_status = request.data.get('final_status', None)
        last_update_by = request.user

        if order_status is not None:
            order.status = order_status

        if final_status is not None:
            order.final_status = final_status
            order.approval_date = timezone.now()

        order.last_update_by = last_update_by
        order.save()

        # Retrieve all admin emails dynamically
        admin_emails = Account.objects.filter(is_superuser=True).values_list('email', flat=True)

        # Prepare and send the email
        subject = f"Order Updated by {request.user.username}"
        message = (
            f"An order has been updated.\n\n"
            f"Order ID: {order.id}\n"
            f"Status: {order.final_status}\n"
            f"Updated By: {request.user.username}\n"
        )
        recipient_list = list(admin_emails)

        send_mail(
            subject,
            message,
            "michealnoya159@gmail.com",  # Replace with your email
            recipient_list + [request.user.email],
            fail_silently=False,
        )

        # Return the updated order instance
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
