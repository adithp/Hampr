from django.urls import path
from .views import CreateReview,DeleteReviewModel

app_name = 'review'

urlpatterns = [
    path('create-review/',CreateReview.as_view(),name='create_review'),
    path('delete/<int:id>/',DeleteReviewModel.as_view(),name='delete_review')
]
