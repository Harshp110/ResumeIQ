from django.contrib import admin
from django.urls import path
from App import views_dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views_dashboard.dashboard_home, name="home"),
    path("dashboard/", views_dashboard.comprehensive_analysis, name="dashboard"),
]
