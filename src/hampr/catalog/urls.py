from django.urls import path


from .views import BoxListView,box_search_suggestions,BoxDetailView,ProductListView,product_search_suggestions,ProductDetailView,DecorationListView,decoartion_search_suggestions,DecorationDetailView

app_name = 'shop'

urlpatterns = [
    path('box_list/',BoxListView.as_view(),name='box_list'),
    path('box-search-suggestions/',box_search_suggestions,name='box_search_suggestions'),
    path('box-detail/<slug:slug>/',BoxDetailView.as_view(),name='box_detail'),
    path('product-list/',ProductListView.as_view(),name='product_list'),
    path('product-search-suggestions/',product_search_suggestions),
    path('product-detail/<slug:slug>/',ProductDetailView.as_view(),name='product_detail'),
    path('decoartion-list/',DecorationListView.as_view(),name='decoation_list'),
    path('decoartion-search-suggestions/',decoartion_search_suggestions,),
    path('decoration-detail/<slug:slug>/',DecorationDetailView.as_view(),name='decoartion_detail')
]
