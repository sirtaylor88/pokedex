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
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


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

    @action(methods=["POST"], detail=True, url_path="give_xp")
    def give_xp(self, request, pk=None):
        """Give experience points to a pokemon"""
        pokemon = self.get_object()
        amount = request.POST.get("amount", None)
        if amount:
            try:
                pokemon.receive_xp(int(amount))
                pokemon.refresh_from_db()
                serializer = PokemonSerializer(pokemon)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError as err:
                return Response(
                    {"amount": str(err)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"reason": "Bad request"}, status=status.HTTP_400_BAD_REQUEST
            )
