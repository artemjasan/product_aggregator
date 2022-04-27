from django.contrib import admin
from django.urls import path, include

api_v1_patterns = [
    path('', include('product_app.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_v1_patterns))
]
