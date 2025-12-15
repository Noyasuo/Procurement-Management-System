from django.urls import path, include

from .views import AccountRegistrationView, AccountLoginView, ProductDetailView, ProductListCreateView, \
    OrderRefundListCreateView, OrderDetailView, OrderRefundDetailView, OrderListCreateView, ObtainAuthTokenView, \
    PaymentDetailView, PaymentListCreateView, AccountDetailsView, AccountListView, CategoryListCreateView, CategoryDetailView, ForgotPasswordView

urlpatterns = [
    # auth
    path('get-token/', ObtainAuthTokenView.as_view(), name='api_get_token'),
    path('register/', AccountRegistrationView.as_view(), name='api_register'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),

    # product
    path('products/', ProductListCreateView.as_view(), name='product_list_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    # order
    path('orders/', OrderListCreateView.as_view(), name='order_list_create'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/refund/', OrderRefundListCreateView.as_view(), name='order_refund_list_create'),
    path('orders/<int:pk>/refund/', OrderRefundDetailView.as_view(), name='order_refund_detail'),

    # payment
    path('payments/', PaymentListCreateView.as_view(), name='payment_list_create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),

    # account
    path('accounts/<int:pk>/', AccountDetailsView.as_view(), name='account_details'),
    path('accounts/', AccountListView.as_view(), name='account_list'),

    # category
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_details'),
    path('category/', CategoryListCreateView.as_view(), name='category_list'),
]
