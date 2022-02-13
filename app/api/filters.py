import django_filters
from core.models import PokedexCreature


class PokedexCreatureFilter(django_filters.FilterSet):
    """Filters for pokedex creature listing"""

    name = django_filters.CharFilter(lookup_expr="icontains")
    type_1 = django_filters.CharFilter(lookup_expr="iexact")
    type_2 = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = PokedexCreature
        fields = ["name", "type_1", "type_2", "generation", "legendary"]
