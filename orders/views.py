from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from orders.serializers import OrderSerializer
from utils.response import service_response
from utils.exceptions import handle_internal_server_exception


class PlaceOrderAPIView(APIView):
    """Place order api view"""

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        """Place order post handler"""
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return service_response(
                    status="success",
                    message="Order placed successfully",
                    status_code=201,
                )
            return service_response(
                status="error",
                message=serializer.errors,
                status_code=400,
            )
        except Exception:
            return handle_internal_server_exception()
