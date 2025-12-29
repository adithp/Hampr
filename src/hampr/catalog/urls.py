from django.urls import path


from .views import BoxListView,box_search_suggestions,BoxDetailView

app_name = 'shop'

urlpatterns = [
    path('box_list/',BoxListView.as_view(),name='box_list'),
    path('box-search-suggestions/',box_search_suggestions,name='box_search_suggestions'),
    path('box-detail/<slug:slug>/',BoxDetailView.as_view(),name='box_detail'),
]
