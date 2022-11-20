import os
from pprint import pprint
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sre_dashboard.settings')

import django
django.setup()
from django.conf import settings
from django.core.management.base import BaseCommand
from base_app.models import AppMon, AppMonSLI, AppMonSLIData

def get_threshold_breach_status(result, expression, threshold_value):
    full_expression = f"{result} {expression} {threshold_value}"
    status = eval(full_expression)
    return status

class Command(BaseCommand):
    help = "Set App status by evaluating SLI status"

    def handle(self, *args, **options):
        log_entry = "Evaluating SLIs to set app status"
        self.stdout.write(log_entry)
        app_list = AppMon.objects.all()
        for app in app_list:
            status_list = [ sli.is_threshold_breached for sli in app.slis.all() ]
            if len(status_list) == 0: # If there are no SLIs for the app
                app.status = 'green'
            else:
                if all(status_list):
                    app.status = 'red'
                elif any(status_list):
                    app.status = 'yellow'
                elif all(status_list) == False:
                    app.status = 'green'
            app.save()
            log_entry = f"App: {app.name}\nStatus: {app.status}"
            self.stdout.write(log_entry)

if __name__ == "__main__":
    pass