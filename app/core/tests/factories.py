from random import randint

import factory
from core.models import PokedexCreature
from factory.django import DjangoModelFactory
from pytest_factoryboy import register


class PokedexCreatureFactory(DjangoModelFactory):
    """Generator of PokedexCreature objects"""

    class Meta:
        model = PokedexCreature

    name = factory.Sequence(lambda n: f"Creature {n + 1}")
    ref_number = randint(1, 750)
    type_1 = "Poison"
    total = randint(100, 999)
    hp = randint(40, 200)
    attack = randint(40, 200)
    defense = randint(40, 200)
    special_attack = randint(40, 200)
    special_defence = randint(40, 200)
    speed = randint(40, 200)
    generation = randint(1, 9)
    legendary = False


register(PokedexCreatureFactory)
