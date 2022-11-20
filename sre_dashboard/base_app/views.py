from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Count
# from django_pandas.io import read_frame
from base_app.models import Issues, IssueSLA, IssueLabels, IssuePriority,\
                         AppMon, AppMonSLI
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go

PLOTLY_DEFAULT_CONFIG = {        
                            "displaylogo": False, 
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                            'toImageButtonOptions': {'filename': "Overall_Report"}
                        }

def get_plot_object(fig):
    return plot(
                fig,
                output_type = 'div', 
                config = PLOTLY_DEFAULT_CONFIG,
                include_plotlyjs=False
        )

class Index(TemplateView):
    """ Default Landing Page """
    template_name = 'base_app/base_app_index.html'


class IssueSLAReportView(TemplateView):
    """ All Issue Dashboard """
    template_name = 'base_app/base_app_issue_sla_report.html'

    def get_context_data(self, **kwargs):
        context = super(IssueSLAReportView, self).get_context_data(**kwargs)
        context['issue_list'] = Issues.objects.all()
        context['issue_sla_list'] = IssueSLA.objects.all()
        return context


class IssueDashboardView(TemplateView):
    """ All Issue Dashboard """
    template_name = 'base_app/base_app_issue_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(IssueDashboardView, self).get_context_data(**kwargs)
        issue_list = Issues.objects.all()

        # Label Stats
        issue_count_by_labels = IssueLabels.objects.all()\
                                .values('name')\
                                .annotate(total=Count('label_issue'))\
                                .order_by('-total')\
        
        tmp_dict = { obj['name']:obj['total'] for obj in issue_count_by_labels }
        # Plot for Issue count by Label
        data = []
        data.append(go.Bar(x=list(tmp_dict.keys()), 
                    y=list(tmp_dict.values()),
                    marker = {'color' : 'royalblue'}
                    ))
        layout = go.Layout(barmode='group', paper_bgcolor="ghostwhite")
        fig = go.Figure(data=data, layout=layout)
        fig.update_xaxes(title_text='Labels', showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(title_text='Count', showline=True, linewidth=2, linecolor='black')
        fig.update_layout(title_text="<b>Issue Count by Labels</b>")
        fig.update_layout(width=400, height=400)
        issue_count_by_label_plot_div = get_plot_object(fig)
        context['issue_count_by_label_plot_div'] = issue_count_by_label_plot_div


        
        # Priority Stats
        issue_count_by_priority = IssuePriority.objects.all()\
                                    .values('name')\
                                    .annotate(total=Count('priority_issue'))\
                                    .order_by('-total')
        tmp_dict = { obj['name']:obj['total'] for obj in issue_count_by_priority }
        # Plot for Issue count by Priority
        data = []
        data.append(go.Bar(x=list(tmp_dict.keys()), 
                    y=list(tmp_dict.values()),
                    marker = {'color' : 'royalblue'}
                    ))
        layout = go.Layout(barmode='group', paper_bgcolor="ghostwhite")
        fig = go.Figure(data=data, layout=layout)
        fig.update_xaxes(title_text='Priority', showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(title_text='Count', showline=True, linewidth=2, linecolor='black')
        fig.update_layout(title_text="<b>Issue Count by Priority</b>")
        fig.update_layout(width=400, height=400)
        issue_count_by_priority_plot_div = get_plot_object(fig)
        context['issue_count_by_priority_plot_div'] = issue_count_by_priority_plot_div

        
        # Assignee Stats
        issue_count_by_assignee = Issues.objects.all()\
                                    .values('assignee_display_name')\
                                    .annotate(total=Count('assignee_display_name'))\
                                    .order_by('-total')
        tmp_dict = { obj['assignee_display_name']:obj['total'] for obj in issue_count_by_assignee }
        # Plot for Issue count by Assignee
        data = []
        data.append(go.Bar(x=list(tmp_dict.keys()), 
                    y=list(tmp_dict.values()),
                    marker = {'color' : 'royalblue'}
                    ))
        layout = go.Layout(barmode='group', paper_bgcolor="ghostwhite")
        fig = go.Figure(data=data, layout=layout)
        fig.update_xaxes(title_text='Assignee', showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(title_text='Count', showline=True, linewidth=2, linecolor='black')
        fig.update_layout(title_text="<b>Issue Count by Assignee</b>")
        fig.update_layout(width=400, height=400)
        issue_count_by_assignee_plot_div = get_plot_object(fig)
        context['issue_count_by_assignee_plot_div'] = issue_count_by_assignee_plot_div

        # Issues by Day
        fig = go.Figure(layout=layout)
        # issues_list = Issues.objects.values('created__date').annotate(count=Count('pk')).values('created__date', 'count').order_by('created__date')
        tmp_list = issue_list.values('created__date').annotate(count=Count('pk')).values('created__date', 'count').order_by('created__date')
        tmp_dict = { obj['created__date']:obj['count'] for obj in tmp_list }
        fig.add_trace(
                        go.Scatter(
                                    x=list(tmp_dict.keys()), 
                                    y=list(tmp_dict.values()), 
                                    fillcolor='royalblue',
                                    fill='tozeroy',
                                    mode='none' # override default markers+lines
                    ))
        layout = go.Layout(barmode='group', paper_bgcolor="ghostwhite")
        fig.update_xaxes(title_text='Day', showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(title_text='Count', showline=True, linewidth=2, linecolor='black')
        fig.update_layout(title_text="<b>Issue Count by Date</b>")
        fig.update_layout(width=400, height=400)
        issue_count_by_date_plot_div = get_plot_object(fig)
        context['issue_count_by_date_plot_div'] = issue_count_by_date_plot_div

        # Issues by Month
        fig = go.Figure(layout=layout)
        tmp_list = issue_list.values('created__date__month').annotate(count=Count('pk')).values('created__date__month', 'count').order_by('created__date__month')
        tmp_dict = { obj['created__date__month']:obj['count'] for obj in tmp_list }
        fig.add_trace(
                        go.Scatter(
                                    x=list(tmp_dict.keys()), 
                                    y=list(tmp_dict.values()), 
                                    fillcolor='royalblue',
                                    fill='tozeroy',
                                    mode='none' # override default markers+lines
                    ))
        layout = go.Layout(barmode='group', paper_bgcolor="ghostwhite")
        fig.update_xaxes(title_text='Month', showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(title_text='Count', showline=True, linewidth=2, linecolor='black')
        fig.update_layout(title_text="<b>Issue Count by Month</b>")
        fig.update_layout(width=400, height=400)
        issue_count_by_month_plot_div = get_plot_object(fig)
        context['issue_count_by_month_plot_div'] = issue_count_by_month_plot_div

        # Issues by Year
        fig = go.Figure(layout=layout)
        tmp_list = issue_list.values('created__date__year').annotate(count=Count('pk')).values('created__date__year', 'count').order_by('created__date__year')
        tmp_dict = { obj['created__date__year']:obj['count'] for obj in tmp_list }
        data = []
        data.append(go.Bar(x=list(tmp_dict.keys()), 
                    y=list(tmp_dict.values()),
                    marker = {'color' : 'royalblue'}
                    ))
        layout = go.Layout(barmode='group', paper_bgcolor="ghostwhite")
        fig = go.Figure(data=data, layout=layout)
        fig.update_xaxes(title_text='Year', showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(title_text='Count', showline=True, linewidth=2, linecolor='black')
        fig.update_layout(title_text="<b>Issue Count by Year</b>")
        fig.update_layout(width=400, height=400)
        issue_count_by_year_plot_div = get_plot_object(fig)
        context['issue_count_by_year_plot_div'] = issue_count_by_year_plot_div

        # SLA Breakup
        tmp_dict = {'In SLA': 0, 'Out Of SLA': 0}
        for issue in issue_list:
            if issue.isInSLA:
               tmp_dict['In SLA'] += 1
            else:
               tmp_dict['Out Of SLA'] += 1

        labels = list(tmp_dict.keys())
        values = list(tmp_dict.values())
        data = []
        data.append(go.Pie(labels=labels, values=values))
        layout = go.Layout(barmode='group', paper_bgcolor="ghostwhite")
        fig = go.Figure(data=data, layout=layout)
        fig.update_xaxes(title_text='Priority', showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(title_text='Count', showline=True, linewidth=2, linecolor='black')
        fig.update_layout(title_text="<b>SLA Breakup</b>")
        fig.update_layout(width=400, height=400)
        issue_sla_breakup_plot_div = get_plot_object(fig)
        context['issue_sla_breakup_plot_div'] = issue_sla_breakup_plot_div

        return context



class IssueSLAUpdateView(CreateView):
    """ Form to update the Jira ticket SLAs """
    model = IssueSLA
    fields = ['priority', 'minutes']
    template_name = "base_app/base_app_sla_update_form.html"
    
    def get_success_url(self):
        return reverse_lazy('base_app:index')


############################################
# App Monitoring                           #
############################################

class AllAppMonStatus(TemplateView):
    """ All Issue Dashboard """
    template_name = 'base_app/base_app_appmon_report.html'

    def get_context_data(self, **kwargs):
        context = super(AllAppMonStatus, self).get_context_data(**kwargs)
        context['app_list'] = AppMon.objects.all()
        return context



class AppMonDetailView(TemplateView):
    """
        View to display AppData object deatils with associated CIs   
    """
    template_name = 'base_app/base_app_appmon_detail.html'
    def get_context_data(self, **kwargs):
        context = super(AppMonDetailView, self).get_context_data(**kwargs)
        app_id = self.kwargs['app_id']
        app = AppMon.objects.get(pk=app_id)
        context['app'] = app

        # SLI trend
        layout = go.Layout(barmode='group', paper_bgcolor="ghostwhite")
        fig = go.Figure(layout=layout)
        for sli in app.slis.all():
            tmp_list = sli.data_points.all().reverse()

            tmp_dict = { obj.created_at:obj.value for obj in tmp_list }
            fig.add_trace(
                            go.Scatter( 
                                        name = sli.name,
                                        x=list(tmp_dict.keys()), 
                                        y=list(tmp_dict.values()),
                                        fill='tozeroy',
                                        # mode='none' # override default markers+lines
                        ))

        fig.update_xaxes(title_text='Timeline', showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(title_text='Value', showline=True, linewidth=2, linecolor='black')
        fig.update_layout(title_text="<b>SLIs Timeline</b>")
        fig.update_layout(width=1300, height=400)
        sli_by_date_plot_div = get_plot_object(fig)
        context['sli_by_date_plot_div'] = sli_by_date_plot_div

        return context


class AppMonAddView(CreateView):
    """ Form to add App """
    model = AppMon
    fields = ['name',]
    template_name = "base_app/base_app_appmon_add.html"
    
    def get_success_url(self):
        return reverse_lazy('base_app:app-mon-list')


class AppMonUpdateView(UpdateView):
    """ Form to update App name and SLIs"""
    model = AppMon
    fields = ['name', 'slis']
    template_name = "base_app/base_app_appmon_app_update.html"
    
    def get_success_url(self):
        return reverse_lazy('base_app:app-mon-list')


class SLIAddView(CreateView):
    """ Form to add App """
    model = AppMonSLI
    fields = ['name', 'query', 'threshold', 'expression']
    template_name = "base_app/base_app_appmon_sli_add.html"
    
    def get_success_url(self):
        return reverse_lazy('base_app:app-mon-list')
