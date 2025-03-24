class MultiDBRouter:
    def db_for_read(self, model, **hints):
        """Route read operations"""
        if model._meta.app_label == 'auth':  # Users stay in SQLite
            return 'default'
        return 'mongodb'  # Everything else goes to MongoDB

    def db_for_write(self, model, **hints):
        """Route write operations"""
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations only within the same DB"""
        if obj1._state.db == obj2._state.db:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Allow migrations only in the correct DB"""
        if app_label == 'auth':
            return db == 'default'
        return db == 'mongodb'
