import os
from pprint import pprint
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sre_dashboard.settings')

import django
django.setup()
from django.conf import settings
from django.core.management.base import BaseCommand
from base_app.jira_lib import get_project_issues
from base_app.models import IssuePriority, IssueLabels, Issues


class Command(BaseCommand):
    help = "Sync Jira Issues"

    def handle(self, *args, **options):
        log_entry = "Synching Jira issues"
        self.stdout.write(log_entry)
        # Collect issues from Jira API
        issues = get_project_issues(host=settings.JIRA_HOST, project=settings.JIRA_PROJECT, 
                email=settings.JIRA_EMAIL, api_token=settings.JIRA_API_TOKEN)
        
        for issue_dict in issues:
            issue_priority, created = IssuePriority.objects.get_or_create(name=issue_dict['fields']['priority']['name'])
            issue_priority.save()

            label_list = []
            for label in issue_dict['fields']['labels']:
                issue_label, created = IssueLabels.objects.get_or_create(name=label)
                issue_label.save()
                label_list.append(issue_label)

            issue, created = Issues.objects.get_or_create(key=issue_dict['key'])
            issue.priority = issue_priority
            issue.labels.set(label_list)

            issue.project_name = issue_dict['fields']['project']['name']
            issue.project_key = issue_dict['fields']['project']['key']
            issue.created = issue_dict['fields']['created']
            issue.updated = issue_dict['fields']['updated']
            issue.status_name = issue_dict['fields']['status']['name']
            issue.summary = issue_dict['fields']['summary']

            issue.creator_display_name = issue_dict['fields']['creator']['displayName']
            # issue.creator_email_address = issue_dict['fields']['creator']['emailAddress']

            if issue_dict['fields']['assignee']:
                issue.assignee_display_name = issue_dict['fields']['assignee']['displayName']
                # issue.assignee_email_address = issue_dict['fields']['assignee']['emailAddress']
            
            issue.save()
            if created:
                log_entry = f"Issue:{issue.key} created!"
            else:
                log_entry = f"Issue:{issue.key} updated!"
            self.stdout.write(log_entry)
            

if __name__ == "__main__":
    pass