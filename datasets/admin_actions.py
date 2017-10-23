# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from celery import chain
from .models import DataSet
from .tasks import (
    load_dataset, calculate_dataset, save_result
)


def calculate(modeladmin, request, queryset):
    """
    Run calculation from queryset and update datasets statuses
    """
    for ds in queryset:
        chain(
            load_dataset.s(ds.pk),
            calculate_dataset.s(ds.pk),
            save_result.s(ds.pk),
        )()
        ds.status = DataSet.IN_PROGRESS
        ds.save()


calculate.short_description = "Calculate DataSet"
