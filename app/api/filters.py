import django_filters
from core.models import PokedexCreature


class PokedexCreatureFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    TYPE_1_CHOICES = [
        (choice, choice)
        for choice in PokedexCreature.objects.all()
        .order_by("type_1")
        .values_list("type_1", flat=True)
        .distinct()
    ]
    TYPE_2_CHOICES = [
        (choice, choice)
        for choice in PokedexCreature.objects.filter(type_2__isnull=False)
        .exclude(type_2="")
        .order_by("type_2")
        .values_list("type_2", flat=True)
        .distinct()
    ]

    type_1 = django_filters.ChoiceFilter(choices=TYPE_1_CHOICES)
    type_2 = django_filters.ChoiceFilter(choices=TYPE_2_CHOICES)

    class Meta:
        model = PokedexCreature
        fields = ["name", "type_1", "type_2", "generation", "legendary"]
