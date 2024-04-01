from django.apps import AppConfig


class CalculatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calculator"
    def ready(self):
        from .models import populate_consumers_and_discount_rules  # Import the function
        populate_consumers_and_discount_rules('path/to/consumers.xlsx')

