from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('celebrations/', views.celebrations_list, name='celebrations_list'),
    path('celebration/<int:celebration_id>/', views.celebration_detail, name='celebration_detail'),
    path('celebration/<int:celebration_id>/delete/', views.celebration_delete, name='celebration_delete'),
    path('reports/', views.reports, name='reports'),
    path('reports/download/', views.reports_pdf, name='reports_pdf'),
    path('reports/monthly/', views.reports_monthly_pdf, name='reports_monthly_pdf'),
    path('reports/events/', views.reports_events_pdf, name='reports_events_pdf'),
    path('reports/certificate/', views.reports_certificate_pdf, name='reports_certificate_pdf'),
    path('accounts/', include('django.contrib.auth.urls')),
]
