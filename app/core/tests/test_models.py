import pytest

pytestmark = pytest.mark.django_db


def test_creature_str(pokedex_creature_factory) -> None:
    """Test pokedex creature string"""

    creature = pokedex_creature_factory(name="Crocodile")
    assert str(creature) == "Crocodile"


def test_pokemon_str(
    pokedex_creature_factory, pokemon_factory, user_log
) -> None:
    """Test pokemon string"""

    creature_1 = pokedex_creature_factory(name="Buffalo")
    pokemon_1 = pokemon_factory(pokedex_creature=creature_1)
    assert str(pokemon_1) == "Buffalo (wild)"

    creature_2 = pokedex_creature_factory(name="Eagle")
    pokemon_2 = pokemon_factory(pokedex_creature=creature_2, trainer=user_log)
    assert str(pokemon_2) == "Eagle (tai)"

    pokemon_3 = pokemon_factory(
        pokedex_creature=creature_1, surname="Reaper", trainer=user_log
    )
    assert str(pokemon_3) == "Reaper (tai)"
