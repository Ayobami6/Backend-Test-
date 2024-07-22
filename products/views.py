from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Q
from products.models import Product
from products.serializers import ProductSerializer
from utils.response import service_response
from utils.exceptions import handle_internal_server_exception
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    """Product REST Viewset"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        """List all products"""
        try:
            # TODO: Implement search for products
            search_query = request.query_params.get("search", None)
            category = request.query_params.get("category", None)
            if search_query:
                products = Product.objects.filter(
                    Q(name__icontains=search_query)
                    | Q(description__icontains=search_query)
                )
            # TODO: Filter by category
            elif category:
                products = Product.objects.filter(category=int(category))
            else:
                products = Product.objects.all()
            # TODO: Implement pagination

            paginator = Paginator(products, 30)
            page = request.query_params.get("page", 1)
            try:
                products_page = paginator.page(page)
            except PageNotAnInteger:
                products_page = paginator.page(1)
            except EmptyPage:
                products_page = paginator.page(paginator.num_pages)

            total_pages = paginator.num_pages
            serialized_products = self.get_serializer(products_page, many=True)
            data = {
                "products": serialized_products.data,
                "total_pages": total_pages,
                "current_page": int(page),
            }
            return service_response(
                status="success", data=data, message="Fetch Successful", status_code=200
            )
        except Exception:
            return handle_internal_server_exception()
