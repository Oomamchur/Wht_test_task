from django.urls import path, include
from rest_framework import routers

from management.views import TeamViewSet, HumanViewSet

router = routers.DefaultRouter()
router.register("teams", TeamViewSet)
router.register("humans", HumanViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "management"
