# coding=utf8
"""
mysql multi database routes
"""


class MysqlRouterBase(object):
    """
    MysqlRouterBase
    """
    DB_NAME = None
    APP_NAME = None
    
    def db_for_read(self, model, **hints):
        """
        Point all read operations to the specific database.
        @param model:
        @param hints:
        @return:
        """
        if model._meta.app_label in self.APP_NAME:
            return self.DB_NAME
        return None
    
    def db_for_write(self, model, **hints):
        """
        Point all write operations to the specific database.
        @param model:
        @param hints:
        @return:
        """
        if model._meta.app_label in self.APP_NAME:
            return self.DB_NAME
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation between apps that use the same database.
        @param obj1:
        @param obj2:
        @param hints:
        @return:
        """
        if obj1._meta.app_label in self.APP_NAME or obj2._meta.app_label in self.APP_NAME:
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        @param db:
        @param app_label:
        @param model_name:
        @param hints:
        @return:
        """
        master_app_label = {'contenttypes', 'sessions', 'management', 'auth', 'admin', 'analyse'}
        
        if db != self.DB_NAME:
            return False
        
        if app_label == self.APP_NAME:
            return True
        
        if app_label in master_app_label and self.APP_NAME == 'db_master':
            return True
        
        return None
