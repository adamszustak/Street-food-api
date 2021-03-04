"""
Called from the project root's urls.py URLConf thus:
path("api/", include("conf.api", namespace="api")),
"""

from rest_framework import routers

from trucks import views as truck_views

app_name = "v1"

router = routers.DefaultRouter()
router.register(r"trucks", truck_views.TruckViewSet)
urlpatterns = router.urls
