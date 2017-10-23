# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class DataSet(models.Model):
    UNPROCESSED = 1
    IN_PROGRESS = 2
    CALCULATED = 3
    ERROR = 4
    STATUSES = (
        (UNPROCESSED, 'Unprocessed'),
        (IN_PROGRESS, 'In Progress'),
        (CALCULATED, 'Calculated'),
        (ERROR, 'Error'),
    )

    name = models.CharField(max_length=15)
    data = models.TextField()
    status = models.IntegerField(choices=STATUSES, default=1)
    datetime = models.DateTimeField(auto_now_add=True)
    result = models.TextField(blank=True, null=True)


class ErrorsLog(models.Model):
    dataset = models.ForeignKey(DataSet)
    step = models.CharField(max_length=15)
    datetime = models.DateTimeField(auto_now_add=True)
    msg = models.CharField(max_length=150)
    traceback = models.TextField()

