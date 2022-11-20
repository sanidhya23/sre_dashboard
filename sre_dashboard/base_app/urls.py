from django.urls import path
from base_app import views

app_name = 'base_app'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('issue-dashboard', views.IssueDashboardView.as_view(), name='issue-dashboard'),
    path('issue-sla-report', views.IssueSLAReportView.as_view(), name='issue-sla-report'),
    path('issue-sla-update', views.IssueSLAUpdateView.as_view(), name='issue-sla-update'),
    path('app-mon-list', views.AllAppMonStatus.as_view(), name='app-mon-list'),
    path('<str:app_id>/app-detail/', views.AppMonDetailView.as_view(), name='app-detail'),
    path('app-mon-add/', views.AppMonAddView.as_view(), name='app-mon-add'),
    path('app-mon-update/<str:pk>', views.AppMonUpdateView.as_view(), name='app-mon-update'),
    path('sli-add/', views.SLIAddView.as_view(), name='sli-add'),
]
