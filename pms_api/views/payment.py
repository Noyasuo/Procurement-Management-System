from rest_framework import generics
from drf_spectacular.utils import extend_schema

from core.models import Payment
from pms_api.serializer import PaymentSerializer

@extend_schema(tags=["Payment"])
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        # Filter payments to only return those related to the current user
        return Payment.objects.filter(user=self.request.user)

@extend_schema(tags=["Payment"])
class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer