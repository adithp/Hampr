from django.urls import path
from .views import AdminLoginView,AdminDashboardView,AdminUserManagement,AdminBlockUser



app_name = 'cadmin'


urlpatterns = [
    path('login/',AdminLoginView.as_view(),name='admin_login'),
    path('dashboard/',AdminDashboardView.as_view(),name='admin_dashboard'),
    path('user_management/',AdminUserManagement.as_view(),name='user_management'),
    path('user_block/<int:id>/',AdminBlockUser.as_view(),name='user_block')
]
