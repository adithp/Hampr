from django.urls import path


from .views import Select_Box_View,Replace_Box_View,UpdateCartView


app_name = 'cart'

urlpatterns = [
    path('add-box/<uuid:id>/',Select_Box_View.as_view(),name='add_box'),
    path('replace-box/<uuid:id>/',Replace_Box_View.as_view(),name='replace_box'),
    path('update-cart/',UpdateCartView.as_view(),name='update_cart')
    
]