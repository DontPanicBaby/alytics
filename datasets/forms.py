# -*- encoding: utf-8 -*-
from __future__ import absolute_import

import json
from django import forms
from django.core.exceptions import ValidationError

from .models import DataSet


class DataSetAdminForm(forms.ModelForm):
    class Meta:
        model = DataSet
        fields = []

    def clean_data(self):
        try:
            json.loads(self.cleaned_data['data'])
        except ValueError:
            raise ValidationError("Invalid JSON")
        return self.cleaned_data['data']
