from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tasks.controller.views import TaskViewSet


router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")

urlpatterns = [
    path("", include(router.urls)),
]
