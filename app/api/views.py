from api.filters import PokedexCreatureFilter
from api.serializers import (
    PokedexCreatureDetailSerializer,
    PokedexCreatureSerializer,
)
from core.models import PokedexCreature
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet


class PokedexViewSet(ReadOnlyModelViewSet):
    """Display all Pokedex Creatures"""

    queryset = PokedexCreature.objects.all()
    serializer_class = PokedexCreatureSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PokedexCreatureFilter

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "retrieve":
            return PokedexCreatureDetailSerializer

        return self.serializer_class
