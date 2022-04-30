from rest_framework import viewsets, serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Product, Offer
from .serializers import OfferSerializer, ProductListSerializer, ProductDetailSerializer
from .services import product_services


class OffersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.offered_objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> serializers.ModelSerializer:
        return self.action_serializer_class_mapping.get(self.action, super().get_serializer_class())

    action_serializer_class_mapping = {
        "create": ProductListSerializer,
        "retrieve": ProductDetailSerializer,
        "update": ProductDetailSerializer,
        "partial_update": ProductDetailSerializer,
        "destroy": ProductDetailSerializer,
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = product_services.product_registration(serializer.data["id"])
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            return Response(response.json(), status=response.status_code)
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response(response.json(), status=response.status_code)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
