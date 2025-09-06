from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse   # ✅ import added
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from vajrabox_be.views import CustomTokenObtainPairView

def health_check(request):
    """Simple health check endpoint for ALB"""
    return JsonResponse({"status": "healthy", "service": "django"})

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('vajra-admin/', admin.site.urls),
    path('api/', include('vajrabox_be.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
