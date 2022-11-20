import os
from pprint import pprint
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sre_dashboard.settings')

import django
django.setup()
from django.conf import settings
from django.core.management.base import BaseCommand
from base_app.prometheus_lib import get_query_summarised_result
from base_app.models import AppMon, AppMonSLI, AppMonSLIData

def get_threshold_breach_status(threshold_value, expression, result):
    full_expression = f"{threshold_value} {expression} {result}"
    status = eval(full_expression)
    return status

class Command(BaseCommand):
    help = "Sync SLI Data"

    def handle(self, *args, **options):
        log_entry = "Collecting SLI data"
        self.stdout.write(log_entry)
        url = f"http://{settings.PROMETHEUS_API_HOST}:{settings.PROMETHEUS_API_PORT}"
        app_list = AppMon.objects.all()
        for app in app_list:
            for sli in app.slis.all():
                result = get_query_summarised_result(url=url, query=sli.query)
                sli_data = AppMonSLIData.objects.create(value=result)
                sli_data.save()
                sli.data_points.add(sli_data)
                sli.is_threshold_breached = get_threshold_breach_status(result=result, expression=sli.expression, threshold_value=sli.threshold)
                sli.save()
                log_entry = f"App: {app.name}\n\
                SLI: {sli.name}\n\
                Threshold: {sli.threshold}\n\
                Expression: {sli.expression}\n\
                Current Value: {result}\n\
                Threshold Breach: {sli.is_threshold_breached}"
                self.stdout.write(log_entry)

if __name__ == "__main__":
    pass