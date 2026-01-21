from django.urls import path
from .views import CreateReview

app_name = 'review'

urlpatterns = [
    path('create-review/',CreateReview.as_view(),name='create_review')
]
