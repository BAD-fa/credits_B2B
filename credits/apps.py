from django.apps import AppConfig


class CreditsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'credits'

    def ready(self) -> None:
        from .groups import create_supplier_group
        create_supplier_group()
        from .signals import give_per_to_supplier
        return super().ready()