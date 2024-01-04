# coding=utf8

from django.db import models

from helper.helper_db import gen_multi_uid_mod_model, MultiTableModel


@gen_multi_uid_mod_model
class ModelDemo(MultiTableModel):
    id = models.BigAutoField(primary_key=True, verbose_name='自增ID')
    user_id = models.PositiveIntegerField(verbose_name='用户ID', db_index=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)

    class Meta:
        verbose_name = verbose_name_plural = "model_demo"
        abstract = True
        db_table = 'model_demo'
        app_label = "db_master"

    sharding_number = 100
    sharding_filed_name = 'user_id'
