from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import Product, Offer
from .serializers import OfferSerializer, ProductSerializer
from .services import product_services, token_services


class OffersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if not token_services.token_existence_verification():
            token = token_services.load_access_token_from_offers_microservice()
            token_services.store_access_token(token)

        response = product_services.product_registration(serializer.data["id"])
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            return Response(response.json(), status=response.status_code)
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response(response.json(), status=response.status_code)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


