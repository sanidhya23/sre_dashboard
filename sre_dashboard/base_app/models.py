from django.db import models
from django.utils import timezone

class IssuePriority(models.Model):
    name = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "issue_priority"
        ordering = ['name']


class IssueLabels(models.Model):
    name = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "issue_labels"        
        ordering = ['name']


class Issues(models.Model):
    key = models.CharField(max_length=128, primary_key=True)
    project_name = models.CharField(max_length=128, null=True, blank=True)
    project_key = models.CharField(max_length=128, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    priority = models.ForeignKey('IssuePriority', related_name='priority_issue', null=True, on_delete=models.SET_NULL)
    labels = models.ManyToManyField('IssueLabels', related_name='label_issue')
    assignee_display_name = models.CharField(max_length=256, null=True, blank=True)
    # assignee_email_address = models.EmailField(max_length=254, null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    status_name = models.CharField(max_length=64, null=True, blank=True)
    description = models.CharField(max_length=4068, null=True, blank=True)
    summary = models.CharField(max_length=1024, null=True, blank=True)
    creator_display_name = models.CharField(max_length=256, null=True, blank=True)
    # creator_email_address = models.EmailField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.key

    class Meta:
        db_table = "issues"
        ordering = ['-created']

    @property
    def workMinutes(self):
        "Minutes ticket from ticket opened and last updated"
        if self.status_name == 'Done':  # If ticket is closed take the last updated time
            time_delta = self.updated - self.created
        else:            # If ticket is under work the take the time difference from now
            time_delta = timezone.now() - self.created
        return int(time_delta.seconds/60)

    @property
    def isInSLA(self):
        "Is ticket under SLA"
        sla_metric = IssueSLA.objects.get(priority=self.priority)
        return sla_metric.minutes > self.workMinutes
        

class IssueSLA(models.Model):
    # priority = models.ForeignKey('IssuePriority', related_name='priority_sla', null=True, on_delete=models.SET_NULL)
    priority = models.OneToOneField('IssuePriority', related_name='priority_sla', on_delete=models.CASCADE)
    minutes = models.PositiveIntegerField(default=1440)            # Minutes

    def __str__(self):
        return f"{self.priority.name}: {self.minutes}"

    class Meta:
        db_table = "issue_sla"
        ordering = ['minutes']


APP_STATUS_CHOICES = (
        ('yellow', 'YELLOW'),
        ('green', 'GREEN'),
        ('red', 'RED'),
    )


class AppMon(models.Model):
    name = models.CharField(max_length=64)
    status = models.CharField(max_length=8, default='green', choices=APP_STATUS_CHOICES)
    slis = models.ManyToManyField('AppMonSLI', blank=True, related_name='sli_app')

    class Meta:
        db_table = "app_mon"
        ordering = ['name']

    def __str__(self):
        return self.name


SLI_EXPRESSION_CHOICES = (
        ('<', '<'),
        ('>', '>'),
        ('=', '='),
        ('!=', '!='),
        ('<=', '<='),
        ('>=', '>='),
    )

class AppMonSLI(models.Model):
    name = models.CharField(max_length=128)
    query = models.CharField(max_length=1024)
    threshold = models.FloatField(default=0.0)
    expression = models.CharField(max_length=8, default='<', choices=SLI_EXPRESSION_CHOICES)
    data_points = models.ManyToManyField('AppMonSLIData', blank=True, related_name='sli')
    is_threshold_breached = models.BooleanField(default=False)

    class Meta:
        db_table = "mon_sli"
        ordering = ['name']

    def __str__(self):
        return self.name


class AppMonSLIData(models.Model):
    value = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sli_data"
        ordering = ['-created_at']   # Reverse ordering for time series

    def __str__(self):
        return str(self.created_at.timestamp())