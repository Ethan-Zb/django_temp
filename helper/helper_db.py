# coding=utf8
"""
分库分表 helper
"""
import binascii
import ctypes
import sys
from collections import defaultdict
from django.db import models
from django.db.models import IntegerField, CharField


def gen_multi_uid_mod_model(cls):
    """
    user_id 取模, 10 or 100 or 2的N次方
    自动分表,自动在cls所在的module里面生成cls.sharding_number个model
    :param cls:
    :return:
    """
    module = sys.modules[cls.__module__]
    
    for idx in range(cls.sharding_number):
        cls_obj = cls.gen_cls(idx)
        setattr(module, cls_obj.__name__, cls_obj)
    
    return cls


class ObjectDict(dict):
    """
        支持字典的点号读取属性
    """
    
    def __getattr__(self, item):
        return self.get(item)
    
    def __setattr__(self, key, value):
        self[key] = value


def model_to_dict_by_inner(instance, fields=None, exclude=None):
    """
    Return a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, return only the
    named.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.
    """
    from itertools import chain
    
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    return data


class CustomBaseModel(models.Model):
    class Meta:
        # 抽象类,不会在数据库里面生成实际的表结构
        abstract = True
        db_table = ''
        verbose_name = ''
    
    def __str__(self):
        return u', '.join([u'%s: %s' % (name, getattr(self, name)) for name in [f.name for f in self._meta.fields]])
    
    @classmethod
    def get_cursor(cls):
        """
        获得当前model所使用的连接游标
        :return:
        """
        from django.db import connections
        cursor = connections[cls._meta.app_label].cursor()  # 多个数据库connections指定
        return cursor
    
    @classmethod
    def get_all_fields(cls, *args, **kwargs):
        """
        返回model里面定义的所有字段名称
        :param args:
        :param kwargs:
        :return:
        """
        return [f.name for f in cls._meta.fields]
    
    @classmethod
    def model_to_dict_obj(cls, model):
        """
        model对象转字典对象,支持字典的点号读取字段
        :param model:
        :return:
        """
        return ObjectDict(**model_to_dict_by_inner(model))
    
    @classmethod
    def get_fields_dict(cls):
        """
        获取model所定义的字段以name作为key的字典
        :return:
        """
        return {field.name: field for field in cls._meta.fields}
    
    @classmethod
    def convert_fields_type(cls, cache_values):
        """
        转换redis存储的类型为python类型
        :param cache_values:
        :return:
        """
        py_values = ObjectDict()
        fields_name_dict = cls.get_fields_dict()
        for key, value in cache_values.items():
            py_values[key] = fields_name_dict[key].to_python(value)
        
        return py_values
    
    @classmethod
    def get_record(cls, exclude_or: dict = None, exclude_and: dict = None, **kwargs):
        query_set = cls.objects.filter(**kwargs)
        
        if exclude_or:
            query_set = query_set.exclude(**exclude_or)
        
        if exclude_and:
            for _k, _v in exclude_and.items():
                query_set = query_set.exclude(**{_k: _v})
        
        return query_set
    
    @classmethod
    def get_record_for_update(cls, exclude_or: dict = None, exclude_and: dict = None, skip_locked=True, **kwargs):
        query_set = cls.objects.select_for_update(skip_locked=skip_locked).filter(**kwargs)
        
        if exclude_or:
            query_set = query_set.exclude(**exclude_or)
        
        if exclude_and:
            for _k, _v in exclude_and.items():
                query_set = query_set.exclude(**{_k: _v})
        
        return query_set
    
    @classmethod
    def get_page_record(cls, exclude_dict=None, page_num=0, page_size=1000,
                        order_by_list=None, **kwargs):
        query = cls.get_record(exclude_and=exclude_dict, **kwargs)
        
        if order_by_list:
            if "id" not in order_by_list and "-id" not in order_by_list and "id" in cls.get_all_fields():
                order_by_list.append("id")
            
            query = query.order_by(*order_by_list)
        
        query_result = query[page_num * page_size: page_num * page_size + page_size]
        
        return query.count(), query_result


class MultiTableModel(CustomBaseModel):
    class Meta:
        # 抽象类,不会在数据库里面生成实际的表结构
        abstract = True
        db_table = ''
        verbose_name = ''
    
    # 默认的分表数量
    sharding_number = 10
    # 分表字段名
    sharding_filed_name = None
    #
    piece_dict = defaultdict()
    
    @classmethod
    def gen_cls(cls, idx):
        """
        根据idx取模生成应的model类
        :param idx:
        :return:
        """
        piece = cls.mod_table_index(idx)
        cls_name = cls.gen_cls_name(piece)
        
        if "{}{}".format(cls_name, piece) in cls.piece_dict:
            return cls.piece_dict["{}{}".format(cls_name, piece)]
        
        class MetaNew(cls.Meta):
            abstract = False
            db_table = '%s_%s' % (cls.Meta.db_table, piece)
            verbose_name = verbose_name_plural = u"%s(%s)" % (cls.Meta.verbose_name, cls_name)
        
        attrs = {
            '__module__': cls.__module__,
            'Meta': MetaNew,
        }
        cls.piece_dict["{}{}".format(cls_name, piece)] = type(cls_name, (cls,), attrs)
        return cls.piece_dict["{}{}".format(cls_name, piece)]
    
    @classmethod
    def gen_char_cls(cls, idx):
        """
        取字符串model
        :param idx:
        :return:
        """
        
        piece = cls.mod_table_index(idx)
        cls_name = cls.gen_cls_name(piece)
        
        class MetaNew(cls.Meta):
            abstract = False
            db_table = '%s_%s' % (cls.Meta.db_table, piece)
            verbose_name = verbose_name_plural = u"%s(%s)" % (cls.Meta.verbose_name, cls_name)
        
        attrs = {
            '__module__': cls.__module__,
            'Meta': MetaNew,
        }
        
        return type(cls_name, (cls,), attrs)
    
    @classmethod
    def route_func(cls, key_value):
        """
        根据指定分表字段的类型,对字段值转换为整数再取模计算出分表索引值
        :param key_value:
        :return:
        """
        field = cls._meta.get_field(cls.sharding_filed_name)
        
        if isinstance(field, IntegerField):
            int_value = int(key_value)
        
        elif isinstance(field, CharField):
            int_value = cls.uint_crc32(key_value)
        
        else:
            raise Exception('invalid field to split table, name: %s, value: %s', cls.sharding_filed_name, key_value)
        
        return cls.mod_table_index(int_value)
    
    @classmethod
    def get_objects(cls, key_value):
        """
        获得对应idx的model的objects对象
        操作多表model的任何数据,都必须使用该函数
        :param key_value:
        :return:
        """
        idx = cls.route_func(key_value)
        model = cls.gen_cls(idx)
        return getattr(model, 'objects')
    
    @classmethod
    def get_objects_by_idx(cls, idx):
        """
        只根据idx就拿到对应类的objects
        :param idx:
        :return:
        """
        model = cls.gen_cls(idx)
        return getattr(model, 'objects')
    
    @classmethod
    def filter(cls, key_value, *args, **kwargs):
        """
        封装objects.filter,自动查找对应的表
        :param key_value: 分表字段的值
        :param kwargs:
        :return:
        """
        assert key_value is not None
        
        kwargs.update({
            cls.sharding_filed_name: key_value,
        })
        
        return cls.get_objects(key_value).filter(*args, **kwargs)
    
    @classmethod
    def filter_with_table_index(cls, index, *args, **kwargs):
        """
        根据分表的id去查表
        @param index:
        @param args:
        @param kwargs:
        @return:
        """
        
        return cls.get_objects(index).filter(*args, **kwargs)
    
    @classmethod
    def filter_without_route(cls, *args, **kwargs):
        """
        封装objects.filter,自动查找对应的表
        :param kwargs:
        :return:
        """
        all_models = list()
        for tb_idx in range(cls.sharding_number):
            model_s = cls.get_objects(tb_idx).filter(*args, **kwargs)
            for model in model_s:
                all_models.append(model)
        return all_models
    
    @classmethod
    def filter_with_route_list(cls, route_list, *args, **kwargs):
        """
        封装objects.filter,自动查找对应的表
        :param route_list:
        :param kwargs:
        :return:
        """
        piece_dict = defaultdict(set)
        
        for route in route_list:
            piece_dict[cls.mod_table_index(route)].add(route)
        
        all_models = list()
        route_params = cls.sharding_filed_name + '__in'
        
        for tb_idx, routes in piece_dict.items():
            kwargs[route_params] = routes
            model_s = cls.get_objects(tb_idx).filter(*args, **kwargs)
            
            for model in model_s:
                all_models.append(model)
        
        return all_models
    
    @classmethod
    def filter_x(cls, key_value, *args, **kwargs):
        """
        封装objects.filter,自动查找对应的表
        :param key_value: 分表字段的值, 不用查询,只用来查找对应的表
        :param kwargs:
        :return:
        """
        assert key_value is not None
        
        return cls.get_objects(key_value).filter(*args, **kwargs)
    
    @classmethod
    def gen_cls_name(cls, idx):
        """
        生成类名后缀
        :param idx:
        :return:
        """
        return cls.__name__ + str(idx)
    
    @classmethod
    def gen_table_name(cls, idx):
        """
        生产多表中某个表的表名
        :param idx:
        :return:
        """
        return cls._meta.db_table + str(int(idx) % cls.sharding_number)
    
    @classmethod
    def mod_table_index(cls, idx):
        """
        用整数取模表个数分表
        :param idx:
        :return:
        """
        piece = int(idx) % cls.sharding_number
        return "0{}".format(piece) if piece < 10 else piece
    
    @classmethod
    def uint_crc32(cls, s):
        """
        把一个字符串经过CRC32哈希后,再转换为unsigned int
        :param s:
        :return:
        """
        # int 转成str
        if isinstance(s, int):
            s = str(s)
        
        return ctypes.c_uint32(binascii.crc32(s.encode())).value
    
    @classmethod
    def mod_table_index_crc32(cls, s):
        """
        先转整数再取模
        :param s:
        :return:
        """
        return cls.mod_table_index(cls.uint_crc32(s))
    
    @classmethod
    def get_model_by_crc32(cls, s):
        """
        用传入参数哈希后转换为无符号整数再取模找到对应的表
        :param s: 字符串
        :return:
        """
        return cls.gen_cls(cls.mod_table_index_crc32(s))
    
    @classmethod
    def get_all_fields(cls, idx):
        """
        返回model里面定义的所有字段名称
        :param idx:
        :return:
        """
        cls_obj = cls.gen_cls(idx)
        return [f.name for f in cls_obj._meta.fields]
    
    @classmethod
    def get_fields_dict(cls):
        """
        获取model所定义的字段以name作为key的字典
        :return:
        """
        return {field.name: field for field in cls._meta.fields}

    @classmethod
    def gen_table_by_user_id(cls, idx):
        """
        生成表名
        @param idx: idx
        @return:
        """
        idx = cls.route_func(idx)
        if not idx:
            raise Exception("gen_table_by_user_id no idx")
        return "{}_{}".format(cls.Meta.db_table, idx)
    
    @classmethod
    def create(cls, key_value, **kwargs):
        """
        create时会查找对应的表
        :param key_value: 分表的字段
        :param kwargs:
        :return:
        """
        assert key_value is not None
        
        kwargs.update({
            cls.sharding_filed_name: key_value,
        })
        
        return cls.get_objects(key_value).create(**kwargs)
    
    @classmethod
    def filter_update(cls, key_value, filter_kwargs=None, update_kwargs=None, filter_key=True):
        """
        方便更新缓存
        :param key_value: 分表的字段
        :param filter_kwargs:
        :param update_kwargs:
        :param filter_key: 是否把分表字段也加入到查询参数里面,默认加入查询
        :return:
        """
        assert key_value is not None
        
        if filter_kwargs is None:
            filter_kwargs = dict()
        
        if update_kwargs is None:
            update_kwargs = dict()
        
        if filter_key:
            filter_kwargs.update({
                cls.sharding_filed_name: key_value,
            })
        
        return cls.get_objects(key_value).filter(**filter_kwargs).update(**update_kwargs)
    
    @classmethod
    def update_or_create(cls, key_value, filter_kwargs, update_kwargs):
        """
        更新或者创建对象,如果查询的数据已经存在,就更新
        :param key_value:
        :param filter_kwargs:
        :param update_kwargs:
        :return:
        """
        idx = cls.route_func(key_value)
        model = cls.gen_cls(idx)
        
        fields = dict()
        filter_kwargs.update({
            cls.sharding_filed_name: key_value,
        })
        fields.update(filter_kwargs)
        fields.update(update_kwargs)

        try:
            obj = model.objects.get(**filter_kwargs)
            for key, value in update_kwargs.items():
                setattr(obj, key, value)
            obj.save()
        except model.DoesNotExist:
            obj = model(**fields)
            obj.save()
        
        return True
