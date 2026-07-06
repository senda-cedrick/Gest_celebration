from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('celebrations/', views.celebrations_list, name='celebrations_list'),
    path('celebration/<int:celebration_id>/', views.celebration_detail, name='celebration_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
]
