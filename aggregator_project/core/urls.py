from django.contrib import admin
from django.urls import path, include

api_v1_patterns = [
    path('', include('v1.product_app.urls')),
    path('users/', include('dj_rest_auth.urls')),
    path('users/registration/', include('dj_rest_auth.registration.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_v1_patterns))
]
