from core.models import PokedexCreature
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


admin.site.register(PokedexCreature, PokedexCreatureAdmin)
