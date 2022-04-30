from django.urls import include, path

from product_app.urls import urlpatterns as products_urlpatterns

urlpatterns = [
    path("", include(products_urlpatterns)),
]
