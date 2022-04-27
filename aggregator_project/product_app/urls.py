from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import OffersViewSet, ProductsViewSet

router = DefaultRouter()

router.register(r'products', ProductsViewSet, basename='product')
router.register(r'offers', OffersViewSet, basename='offer')

urlpatterns = [
    path("", include(router.urls))
]
