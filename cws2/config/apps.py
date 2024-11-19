from django.apps import AppConfig


class CWS2Config(AppConfig):
    name = "cws2"
    label = "cws2"
    verbose_name = "ConWorkShop 2.0"

    def ready(self):
        from pi_heif import register_heif_opener

        register_heif_opener()
