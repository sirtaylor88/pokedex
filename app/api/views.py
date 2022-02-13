from api.filters import PokedexCreatureFilter
from api.serializers import (
    PokedexCreatureDetailSerializer,
    PokedexCreatureSerializer,
    PokemonSerializer,
)
from core.models import PokedexCreature, Pokemon
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated


class PokedexViewSet(ReadOnlyModelViewSet):
    """Display all Pokedex Creatures"""

    queryset = PokedexCreature.objects.all()
    serializer_class = PokedexCreatureSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PokedexCreatureFilter

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "retrieve":
            return PokedexCreatureDetailSerializer

        return self.serializer_class


class PokemonViewSet(ModelViewSet):
    """Manage a pokemon"""

    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = (IsAuthenticated,)
