class MultiDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth' or model._meta.model_name in ['profile', 'cart', 'navbarlink']:  # Add navbarlink here
            return 'default'
        elif model._meta.model_name in ['product', 'category', 'order']:
            return 'mongodb'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'auth' or model_name in ['profile', 'cart', 'navbarlink']:  # Add navbarlink here
            return db == 'default'
        elif model_name in ['product', 'category', 'order']:
            return db == 'mongodb'
        return None


    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'auth' or model_name in ['profile', 'cart', 'navbarlink']:
            return db == 'default'  # Ensure migration for SQLite
        elif model_name in ['product', 'category', 'order']:
            return db == 'mongodb'
        return None
