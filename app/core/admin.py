from core.models import PokedexCreature, Pokemon
from django.contrib import admin


class PokedexCreatureAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in PokedexCreature._meta.fields
        if field.name != "id"
    ]
    ordering = ("name",)
    search_fields = ("name",)
    list_per_page = 50


class PokemonAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Pokemon._meta.fields if field.name != "id"
    ]
    ordering = ("surname",)
    search_fields = ("surname", "trainer__username")
    list_per_page = 50

    autocomplete_fields = ("pokedex_creature", "trainer")


admin.site.register(PokedexCreature, PokedexCreatureAdmin)
admin.site.register(Pokemon, PokemonAdmin)
