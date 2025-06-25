from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.user.controller.views import TokenObtainPairView, UserViewSet


router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    # Additional paths
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenObtainPairView.as_view(), name="token_refresh"),
]
