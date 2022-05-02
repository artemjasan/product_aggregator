from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import OffersViewSet, ProductsViewSet

router = SimpleRouter()

router.register(r"products", ProductsViewSet, basename="product")
router.register(r"offers", OffersViewSet, basename="offer")

urlpatterns = [path("", include(router.urls))]
