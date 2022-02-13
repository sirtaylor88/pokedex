import pytest
from api.serializers import (
    PokemonSerializer,
)
from core.models import Pokemon
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_listing_pokemons(user_log, client_log, pokemon_factory):
    """Test listing Pokedex creatures."""

    # Create 3 pokemons
    pokemon_factory()
    pokemon_factory(trainer=user_log)
    pokemon_factory()

    # Unauthenticated user should be denied access
    res = APIClient().get(reverse("api:pokemon-list"))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Authenticated user should be given access
    res = client_log.get(reverse("api:pokemon-list"))
    assert res.status_code == status.HTTP_200_OK

    pokemons = Pokemon.objects.all()
    serializer = PokemonSerializer(pokemons, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert len(serializer.data) == 3
    assert serializer.data == res.data.get("results")


def test_view_pokemon_detail(user_log, client_log, pokemon_factory):
    """Test retrieving a Pokemon creature"""

    # Create 2 pokemons
    pokemon_factory()
    pokemon = pokemon_factory(trainer=user_log)

    # Unauthenticated user should be denied access
    res = APIClient().get(reverse("api:pokemon-detail", args=[pokemon.id]))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Authenticated user should be given access
    res = client_log.get(reverse("api:pokemon-detail", args=[pokemon.id]))
    assert res.status_code == status.HTTP_200_OK

    serializer = PokemonSerializer(pokemon)

    assert res.status_code == status.HTTP_200_OK
    assert serializer.data == res.data


def test_create_pokemon(
    user_log,
    client_log,
    pokedex_creature_factory,
    pokemon_factory,
):
    """Authenticated user can create a pokermon"""
    creature = pokedex_creature_factory(name="Brown Bear")
    pokemon_factory()
    pokemon_factory()

    # Create a trained pokemon
    payload = {
        "pokedex_creature": creature.id,
        "trainer": user_log.id,
        "surname": "Gozilla",
    }
    res = client_log.post(
        reverse("api:pokemon-list"),
        payload,
    )
    assert res.status_code == status.HTTP_201_CREATED

    pokemon = Pokemon.objects.get(id=res.data["id"])
    assert str(pokemon) == "Gozilla (tai)"
    assert pokemon.pokedex_creature.name == "Brown Bear"

    # Create a wild pokemon
    payload = {
        "pokedex_creature": creature.id,
    }
    res = client_log.post(
        reverse("api:pokemon-list"),
        payload,
    )
    assert res.status_code == status.HTTP_201_CREATED

    pokemon = Pokemon.objects.get(id=res.data["id"])
    assert str(pokemon) == "Brown Bear (wild)"


def test_partial_update_pokemon(client_log, pokemon_factory):
    """Authenticated user can update an existing pokemon with patch"""
    pokemon = pokemon_factory(surname="Lion")
    payload = {"surname": "Monster king"}
    res = client_log.patch(
        reverse("api:pokemon-detail", args=[pokemon.id]),
        payload,
    )
    assert res.status_code == status.HTTP_200_OK
    pokemon.refresh_from_db()
    assert pokemon.surname == payload["surname"]


def test_full_update_pokemon(
    client_log, user_log, pokedex_creature_factory, pokemon_factory
):
    """Authenticated user can update an existing pokemon with put"""
    pokemon = pokemon_factory()
    creature = pokedex_creature_factory()
    payload = {
        "surname": "Monster king",
        "trainer": user_log.id,
        "pokedex_creature": creature.id,
    }
    res = client_log.put(
        reverse("api:pokemon-detail", args=[pokemon.id]),
        payload,
    )
    assert res.status_code == status.HTTP_200_OK
    pokemon.refresh_from_db()
    assert pokemon.surname == payload["surname"]
    assert pokemon.trainer == user_log
    assert pokemon.pokedex_creature == creature


def test_delete_pokemon(client_log, pokemon_factory):
    """Authenticated user can delete an existing pokermon"""
    pokemon = pokemon_factory()

    res = client_log.delete(reverse("api:pokemon-detail", args=[pokemon.id]))
    assert res.status_code == status.HTTP_204_NO_CONTENT

    assert not Pokemon.objects.filter(id=pokemon.id).exists()


def test_give_xp_to_pokemon(client_log, pokemon_factory):
    """Authenticated user can give XP to an existing pokermon"""
    pokemon = pokemon_factory(level=1, experience=40)

    payload = {
        "amount": 150,
    }
    res = client_log.post(
        reverse("api:pokemon-give-xp", args=[pokemon.id]),
        payload,
    )
    assert res.status_code == status.HTTP_200_OK

    pokemon = Pokemon.objects.get(id=pokemon.id)
    pokemon.refresh_from_db()

    assert pokemon.level == 2
    assert pokemon.experience == 190


def test_give_xp_to_pokemon_invalid_request(client_log, pokemon_factory):
    """Authenticated user can give XP to an existing pokermon"""
    pokemon = pokemon_factory(level=1, experience=40)

    payload = {
        "amount": "Hello",
    }
    res = client_log.post(
        reverse("api:pokemon-give-xp", args=[pokemon.id]),
        payload,
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.data == {
        "amount": "invalid literal for int() with base 10: 'Hello'"
    }

    payload = {
        "attack": 100,
    }
    res = client_log.post(
        reverse("api:pokemon-give-xp", args=[pokemon.id]),
        payload,
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.data == {"reason": "Bad request"}
