import pytest
from api.serializers import (
    PokedexCreatureDetailSerializer,
    PokedexCreatureSerializer,
)
from core.models import PokedexCreature
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_listing_pokedex_creatures(pokedex_creature_factory):
    """Test listing Pokedex creatures."""

    # Create 2 creatures
    pokedex_creature_factory()
    pokedex_creature_factory()

    client = APIClient()
    res = client.get(reverse("api:pokedex-list"))
    creatures = PokedexCreature.objects.all()
    serializer = PokedexCreatureSerializer(creatures, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert len(serializer.data) == 2
    assert serializer.data == res.data.get("results")


def test_view_pokedex_creature_detail(pokedex_creature_factory):
    """Test retrieving a Pokedex creature"""

    # Create 3 creatures
    pokedex_creature_factory()
    pokedex_creature_factory()
    creature = pokedex_creature_factory()

    client = APIClient()
    res = client.get(reverse("api:pokedex-detail", args=[creature.id]))
    serializer = PokedexCreatureDetailSerializer(creature)

    assert res.status_code == status.HTTP_200_OK
    assert serializer.data == res.data
