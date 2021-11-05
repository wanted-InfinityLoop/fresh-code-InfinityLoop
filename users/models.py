from django.db import models

from .managers import CustomModelManager


class Role(models.Model):
    class Type(models.IntegerChoices):
        ADMIN    = 1
        CUSTOMER = 2

    name = models.CharField(max_length=16)

    objects = CustomModelManager()

    class Meta:
        db_table = "roles"


class User(models.Model):
    name     = models.CharField(max_length=32, null=True)
    email    = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128, null=True)
    role     = models.ForeignKey(Role, on_delete=models.PROTECT, db_index=True)
    
    objects = CustomModelManager()

    class Meta:
        db_table = "users"
