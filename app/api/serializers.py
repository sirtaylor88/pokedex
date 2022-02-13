from core.models import PokedexCreature, Pokemon
from django.conf import settings
from rest_framework import serializers


class PokedexCreatureSerializer(serializers.ModelSerializer):
    """Serializer of PokedexCreature object"""

    class Meta:
        model = PokedexCreature
        fields = (
            "id",
            "name",
            "type_1",
            "type_2",
            "generation",
            "legendary",
        )
        read_only_fields = ("id",)


class PokedexCreatureDetailSerializer(serializers.ModelSerializer):
    """Serializer to retrieve detail of PokedexCreature object"""

    class Meta:
        model = PokedexCreature
        fields = "__all__"
        read_only_fields = ("id",)


class UserSerializer(serializers.ModelSerializer):
    """Serializer to retrieve an user"""

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ["id", "username", "email"]


class PokemonSerializer(serializers.ModelSerializer):
    """Serializer of Pokemon object"""

    pokedex_creature = PokedexCreatureDetailSerializer
    trainer = UserSerializer

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "pokedex_creature",
            "trainer",
            "surname",
            "level",
            "experience",
        )
        read_only_fields = ("id", "level", "experience")

    def validate(self, attrs):
        """Add pokemon surname if no surname is given"""
        surname = attrs.get("surname")
        pokedex_creature = attrs.get("pokedex_creature")
        if not surname:
            attrs["surname"] = pokedex_creature.name

        return super().validate(attrs)
