from django.contrib import admin
from django.urls import path, include
from django.conf import settings               
from django.conf.urls.static import static
from store.views import (
    CategoryListCreateAPI,
    CategoryDetailAPI,
    ProductListCreateAPI, 
    ProductDetailAPI,
    CartAPI,
    CartItemDetailAPI,
    OrderListCreateAPI,
    OrderDetailAPI,
    RegisterAPI
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from store.serializers import MyTokenObtainPairSerializer
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterAPI.as_view(), name='auth-register'),
    path('api/auth/login/', MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/categories/', CategoryListCreateAPI.as_view(), name='categories-list-create'),
    path('api/categories/<int:pk>/', CategoryDetailAPI.as_view(), name='categories-detail'),
    path('api/products/', ProductListCreateAPI.as_view(), name='products-list-create'),
    path('api/products/<int:pk>/', ProductDetailAPI.as_view(), name='product-detail'),
    path('api/cart/', CartAPI.as_view(), name='cart-list-create'),
    path('api/cart/<int:pk>/', CartItemDetailAPI.as_view(), name='cart-item-detail'),
    path('api/orders/', OrderListCreateAPI.as_view(), name='orders-list-create'),
    path('api/orders/<int:pk>/', OrderDetailAPI.as_view(), name='order-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)