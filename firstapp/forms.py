# -*- coding: utf-8 -*-

from django import forms
from.models import Category, Good


class Errors:
    name = {"required": "Укажите название товара",
            "min_length": "Название должно быть длиннее 4х букв",
            "max_length": "Длинна названия ограничена 20 символами"}
    description = {"max_length": "Длинна описания ограничена 100 символами"}
    price = {"min_value": "Минимальное значение цены - 0,1 руб.",
             "required": "Это поле является обязательным",
             "invalid": "Допускаются только цифры"}

    @staticmethod
    def get_error_list(fieldname):
        return getattr(Errors, fieldname)


class GoodFormCustomFields(forms.ModelForm):
    class Meta:
        model = Good
        exclude = []

    name = forms.CharField(label="Название",
                           help_text="Должно быть уникальным",
                           error_messages=Errors.get_error_list("name"))
    description = forms.CharField(label="Описание",
                                  widget=forms.Textarea,
                                  error_messages=Errors.get_error_list("description"))
    price = forms.DecimalField(label="Цена",
                               required=True,
                               widget=forms.NumberInput(attrs={'type': 'number', 'step': 0.5}),
                               error_messages=Errors.get_error_list("price"))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      label="Категория",
                                      empty_label=None)
    in_stock = forms.BooleanField(initial=True,
                                  label="Есть в наличии")


class GoodFormMetaEditing(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['name', "description", ]
        labels = {"name": "Название",
                  "description": "Описание", }
        help_texts = {"name": "Должно быть уникальным"}
        error_messages = {"name": {"required": "Укажите название товара",
                                   "min_length": "Название должно быть длиннее 4х букв",
                                   "max_length": "Длинна названия ограничена 20 символами"},
                          }
