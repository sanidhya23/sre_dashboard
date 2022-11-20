from celery import shared_task
from django.core.management import call_command
from io import StringIO

@shared_task
def sync_jira_issues():
    out = StringIO()
    call_command('sync_jira_issues', stdout=out)
    return out.getvalue()

@shared_task
def collect_sli_data():
    out = StringIO()    
    call_command('collect_app_mon_sli_data', stdout=out)
    return out.getvalue()


@shared_task
def set_app_mon_status():
    out = StringIO()
    call_command('set_app_mon_status', stdout=out)
    return out.getvalue()
