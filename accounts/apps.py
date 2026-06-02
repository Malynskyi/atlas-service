import os

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        if os.environ.get("RUN_MAIN") == "true":
            return

        try:
            from django.contrib.auth import get_user_model

            User = get_user_model()

            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="dm",
                    email="malynskyidmytro@gmail.com",
                    password="55",
                )
        except Exception:
            pass