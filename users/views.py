from django.shortcuts import render
from users.serializers import CreateUserSerializer
from utils.response import service_response
from utils.exceptions import handle_internal_server_exception
from rest_framework.views import APIView

# Create your views here.


class CreateUserAPIView(APIView):
    """Create a new user"""

    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        """Register a new user post handler"""
        try:
            serializer: CreateUserSerializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                #    save serializer
                serializer.save()
                return service_response(
                    status="success",
                    message="Registration Successful",
                    status_code=201,
                )
            return service_response(
                status="error", message=serializer.errors, status_code=400
            )
        except Exception:
            return handle_internal_server_exception()
