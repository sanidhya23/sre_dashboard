import os
from pprint import pprint
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sre_dashboard.settings')

import django
django.setup()
from django.conf import settings
from django.core.management.base import BaseCommand
from base_app.models import IssuePriority, IssueSLA

SLA_LIST = {'High': 360, 'Highest': 60, 'Low': 1440, 'Lowest': 2880, 'Medium': 720}

class Command(BaseCommand):
    help = "Sync Jira Issues"

    def handle(self, *args, **options):
        log_entry = "Loading defualt issue SLA"

        self.stdout.write(log_entry)
        for priority, minutes in SLA_LIST.items():   
            priority_obj, created = IssuePriority.objects.get_or_create(name=priority)
            sla, created = IssueSLA.objects.get_or_create(priority=priority_obj)
            if created:
                sla.minutes = minutes
                sla.save()
                log_entry = f"SLA added for {priority}: {minutes}"
                self.stdout.write(log_entry)        
            

if __name__ == "__main__":
    pass