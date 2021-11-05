from django.db import models

from core.models import TimeStamp


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "categories"


class Badge(models.Model):
    name = models.CharField(max_length=16)

    class Meta:
        db_table = "badges"


class Tag(models.Model):
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=32)

    class Meta:
        db_table = "tags"


class Menu(TimeStamp):
    name        = models.CharField(max_length=32)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=128)
    badge       = models.ForeignKey(Badge, on_delete=models.PROTECT, null=True)
    is_sold     = models.BooleanField(default=False)
    tag         = models.ForeignKey(Tag, on_delete=models.PROTECT)

    class Meta:
        db_table = "menus"

    def __str__(self):
        return f"{self.name}"


class Size(models.Model):
    name = models.CharField(max_length=16)
    size = models.CharField(max_length=16)

    class Meta:
        db_table = "sizes"


class Item(TimeStamp):
    menu    = models.ForeignKey(Menu, on_delete=models.CASCADE)
    size    = models.ForeignKey(Size, on_delete=models.PROTECT)
    price   = models.PositiveIntegerField()
    is_sold = models.BooleanField(default=False)

    class Meta:
        db_table = "items"
