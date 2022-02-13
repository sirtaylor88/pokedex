from django.db import models
from django.conf import settings


class PokedexCreature(models.Model):
    """PokedexCreature object"""

    name = models.CharField(max_length=100, unique=True)
    # many creature can have same ref_number
    ref_number = models.PositiveSmallIntegerField()
    type_1 = models.CharField(max_length=20)
    type_2 = models.CharField(max_length=20, blank=True, null=True)
    total = models.PositiveSmallIntegerField()
    hp = models.PositiveSmallIntegerField()
    attack = models.PositiveSmallIntegerField()
    defense = models.PositiveSmallIntegerField()
    special_attack = models.PositiveSmallIntegerField()
    special_defence = models.PositiveSmallIntegerField()
    speed = models.PositiveSmallIntegerField()
    generation = models.PositiveSmallIntegerField()
    legendary = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """Return object name"""
        return self.name


class Pokemon(models.Model):
    """Pokemon object"""

    pokedex_creature = models.ForeignKey(
        "PokedexCreature",
        on_delete=models.CASCADE,
    )

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    surname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    level = models.PositiveSmallIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)

    def clean(self):
        if not self.surname:
            self.surname = self.pokedex_creature.name
        return super().clean()

    def __str__(self):
        return "{} ({})".format(
            self.surname, self.trainer.username if self.trainer else "wild"
        )
