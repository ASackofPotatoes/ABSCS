from django.apps import apps

class MissionDatabaseRouter:
    """
    Directs models to specific databases and controls which migrations apply where.
    """

    def db_for_read(self, model, **hints):
        """Choose the correct database for reading."""
        return self.get_current_mission_db()

    def db_for_write(self, model, **hints):
        """Choose the correct database for writing."""
        return self.get_current_mission_db()

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Decide whether migrations for a model should apply to a given database."""
        mission_dbs = ["Ex-Alta 2", "Ex-Alta 3"]  # List of mission databases
        if model_name is None:
            return True #In the case that this migration isn't for a specific model, return True

        model = apps.get_model(app_label, model_name)
        if model:
            model_type = getattr(model, "model_type", None)
            if model_type == "mission_config":
                return db in mission_dbs 
            if model_type == "config":
                return db == "default"
        return True  # Default behavior


    def get_current_mission_db(self):
        """Determine which mission database is currently active."""
        from django.core.cache import cache
        return cache.get("current_mission", "default")  # Default fallback
