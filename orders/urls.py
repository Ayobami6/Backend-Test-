from django.urls import path
from .views import PlaceOrderAPIView

urlpatterns = [path("orders/place", PlaceOrderAPIView.as_view(), name="place-order")]
