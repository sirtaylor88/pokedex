from api.views import PokedexViewSet, PokemonViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register("pokedex", PokedexViewSet, basename="pokedex")
router.register("pokemon", PokemonViewSet, basename="pokemon")

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
]
