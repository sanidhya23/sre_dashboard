from django.contrib import admin
from base_app.models import IssuePriority, IssueLabels,\
                            Issues, IssueSLA,\
                            AppMon, AppMonSLI, AppMonSLIData

admin.site.register(IssuePriority)
admin.site.register(IssueLabels)
admin.site.register(Issues)
admin.site.register(IssueSLA)
admin.site.register(AppMon)
admin.site.register(AppMonSLI)
admin.site.register(AppMonSLIData)
