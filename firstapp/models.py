# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категорию"
        verbose_name_plural = "категории"


@python_2_unicode_compatible
class Good(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=11, decimal_places=2)
    in_stock = models.BooleanField(default=True, db_index=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    def get_in_stock(self):
        return "+" if self.in_stock else ""

    def __str__(self):
        return self.name if self.in_stock else "{} (нет в наличии)".format(self.name)

    class Meta:
        ordering = ["-price", "name"]
        unique_together = ("category", "name", "price")
        verbose_name = "товар"
        verbose_name_plural = "товары"
