from api.views import PokedexViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register("pokedex", PokedexViewSet, basename="pokedex")

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
]
