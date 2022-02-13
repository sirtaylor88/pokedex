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
    assert serializer.data == res.data["results"]


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


def test_filter_pokedex_creatures_by_name(pokedex_creature_factory):
    """Test filtering Pokedex creatures based on their name"""

    creature_1 = pokedex_creature_factory(name="Pikachu")
    creature_2 = pokedex_creature_factory(name="Goldduck")
    creature_3 = pokedex_creature_factory(name="Goldeen")

    client = APIClient()
    res = client.get(
        reverse("api:pokedex-list"),
        {"name": "gold"},
    )

    assert res.status_code == status.HTTP_200_OK

    serializer_1 = PokedexCreatureSerializer(creature_1)
    serializer_2 = PokedexCreatureSerializer(creature_2)
    serializer_3 = PokedexCreatureSerializer(creature_3)

    assert serializer_1.data not in res.data["results"]
    assert serializer_2.data in res.data["results"]
    assert serializer_3.data in res.data["results"]


def test_filter_pokedex_creatures_by_type_one(pokedex_creature_factory):
    """Test filtering Pokedex creatures based on their type 1"""
    creature_1 = pokedex_creature_factory(type_1="Poison")
    creature_2 = pokedex_creature_factory(type_1="Flying")
    creature_3 = pokedex_creature_factory(type_1="Dragon")

    client = APIClient()
    res = client.get(
        reverse("api:pokedex-list"),
        {"type_1": "Dragon"},
    )
    assert res.status_code == status.HTTP_200_OK

    serializer_1 = PokedexCreatureSerializer(creature_1)
    serializer_2 = PokedexCreatureSerializer(creature_2)
    serializer_3 = PokedexCreatureSerializer(creature_3)

    assert serializer_1.data not in res.data["results"]
    assert serializer_2.data not in res.data["results"]
    assert serializer_3.data in res.data["results"]


def test_filter_pokedex_creatures_by_type_two(pokedex_creature_factory):
    """Test filtering Pokedex creatures based on their type 2"""
    creature_1 = pokedex_creature_factory(type_2="Poison")
    creature_2 = pokedex_creature_factory(type_2="Flying")
    creature_3 = pokedex_creature_factory(type_2=None)

    client = APIClient()
    res = client.get(
        reverse("api:pokedex-list"),
        {"type_2": "Flying"},
    )
    assert res.status_code == status.HTTP_200_OK

    serializer_1 = PokedexCreatureSerializer(creature_1)
    serializer_2 = PokedexCreatureSerializer(creature_2)
    serializer_3 = PokedexCreatureSerializer(creature_3)

    assert serializer_1.data not in res.data["results"]
    assert serializer_2.data in res.data["results"]
    assert serializer_3.data not in res.data["results"]


def test_filter_pokedex_creatures_by_generation(pokedex_creature_factory):
    """Test filtering Pokedex creatures based on their generation"""
    creature_1 = pokedex_creature_factory(generation=5)
    creature_2 = pokedex_creature_factory(generation=4)
    creature_3 = pokedex_creature_factory(generation=5)

    client = APIClient()
    res = client.get(
        reverse("api:pokedex-list"),
        {"generation": 5},
    )
    assert res.status_code == status.HTTP_200_OK

    serializer_1 = PokedexCreatureSerializer(creature_1)
    serializer_2 = PokedexCreatureSerializer(creature_2)
    serializer_3 = PokedexCreatureSerializer(creature_3)

    assert serializer_1.data in res.data["results"]
    assert serializer_2.data not in res.data["results"]
    assert serializer_3.data in res.data["results"]


def test_filter_pokedex_creatures_by_legendary(pokedex_creature_factory):
    """Test filtering Pokedex creatures based on their legendary status"""
    creature_1 = pokedex_creature_factory(legendary=False)
    creature_2 = pokedex_creature_factory(legendary=True)
    creature_3 = pokedex_creature_factory(legendary=False)

    client = APIClient()
    res = client.get(
        reverse("api:pokedex-list"),
        {"legendary": True},
    )
    assert res.status_code == status.HTTP_200_OK

    serializer_1 = PokedexCreatureSerializer(creature_1)
    serializer_2 = PokedexCreatureSerializer(creature_2)
    serializer_3 = PokedexCreatureSerializer(creature_3)

    assert serializer_1.data not in res.data["results"]
    assert serializer_2.data in res.data["results"]
    assert serializer_3.data not in res.data["results"]
