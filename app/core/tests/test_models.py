import pytest

pytestmark = pytest.mark.django_db


def test_creature_str(pokedex_creature_factory):
    """Test creature string"""
    creature = pokedex_creature_factory(name="Crocodile")
    assert str(creature) == "Crocodile"
