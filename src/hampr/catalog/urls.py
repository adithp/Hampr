from django.urls import path


from .views import BoxListView

app_name = 'shop'

urlpatterns = [
    path('box_list/',BoxListView.as_view(),name='box_list')
]
