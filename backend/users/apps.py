# backend/users/apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # ⭐ เพิ่มส่วนนี้
    def ready(self):
        import users.signals