from django.urls import include, path

from .product_app.urls import urlpatterns

urlpatterns = [
    path("", include(urlpatterns)),
]
