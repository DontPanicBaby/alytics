# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import DataSet, ErrorsLog
from .forms import DataSetAdminForm
from .admin_actions import calculate


class ErrorsLogInline(admin.StackedInline):
    model = ErrorsLog
    readonly_fields = ('step', 'datetime', 'msg', 'traceback')


class DataSetAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'status')
    fields = ('name', 'data', 'status', 'datetime', 'result')
    readonly_fields = ('status', 'result', 'datetime')

    inlines = [ErrorsLogInline]
    actions = (calculate,)

    form = DataSetAdminForm


admin.site.register(DataSet, DataSetAdmin)


