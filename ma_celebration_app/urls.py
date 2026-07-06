from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('celebrations/', views.celebrations_list, name='celebrations_list'),
    path('celebration/<int:celebration_id>/', views.celebration_detail, name='celebration_detail'),
    path('celebration/<int:celebration_id>/delete/', views.celebration_delete, name='celebration_delete'),
    path('accounts/', include('django.contrib.auth.urls')),
]
