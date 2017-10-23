# -*- encoding: utf-8 -*-
from __future__ import absolute_import

import json
import logging

from celery import Task
from alytics.celery import app

from .models import DataSet, ErrorsLog

logger = logging.getLogger(__name__)


class DataSetTask(Task):
    def __init__(self):
        self.dataset_id = None

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        Handle errors and store all in database
        """
        try:
            if not self.dataset_id:
                raise ValueError('DataSet id was not set')
            ErrorsLog(
                dataset_id=self.dataset_id,
                step=self.name,
                msg=str(exc),
                traceback=str(einfo)
            ).save()
            DataSet.objects.filter(pk=self.dataset_id).update(
                status=DataSet.ERROR
            )
        except Exception:
            # Log unhandled error (issues with connection to db and etc.)
            logger.exception('Unhandled error')
        super(DataSetTask, self).on_failure(
            exc, task_id, args, kwargs, einfo
        )

    def run(self, *args, **kwargs):
        raise NotImplementedError


class LoadDataSetTask(DataSetTask):
    def run(self, dataset_id):
        """

        :param dataset_id:
        :type dataset_id: int
        :return: raw data set
        """
        self.dataset_id = dataset_id
        data = DataSet.objects.get(pk=dataset_id).data
        return data


class CalculateTask(DataSetTask):
    def run(self, data, dataset_id):
        """

        :param data: raw data
        :type data: basestring
        :param dataset_id:
        :type dataset_id: int
        :return: calculation result
        """
        self.dataset_id = dataset_id
        dataset = json.loads(data)
        result = 0
        for row in dataset:
            result += row['a'] + row['b']
        return json.dumps({'result': result})


class SaveResultTask(DataSetTask):
    def run(self, result, dataset_id):
        """

        :param result: dict
        :type result: dict
        :param dataset_id:
        :type dataset_id: int
        :return: bool
        """
        self.dataset_id = dataset_id
        DataSet.objects.filter(pk=self.dataset_id).update(
            result=result, status=DataSet.CALCULATED
        )
        return True


load_dataset = LoadDataSetTask()
calculate_dataset = CalculateTask()
save_result = SaveResultTask()

app.register_task(load_dataset)
app.register_task(calculate_dataset)
app.register_task(save_result)


