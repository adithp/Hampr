from django.urls import path 

from .views import ReturnPage

app_name = 'return'

urlpatterns = [
    path('create_return/<int:id>',ReturnPage.as_view(),name='create_return'),
]
