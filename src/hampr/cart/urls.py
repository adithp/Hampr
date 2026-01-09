from django.urls import path


from .views import Select_Box_View,Replace_Box_View,UpdateCartView,CartView,CartProductDelete,CartDecorationDelete,DeleteFullCart


app_name = 'cart'

urlpatterns = [
    path('add-box/<uuid:id>/',Select_Box_View.as_view(),name='add_box'),
    path('replace-box/<uuid:id>/',Replace_Box_View.as_view(),name='replace_box'),
    path('update-cart/',UpdateCartView.as_view(),name='update_cart'),
    path('cart/',CartView.as_view(),name='cart_list'),
    path('cart-product-delete/<int:pk>/',CartProductDelete.as_view(),name='cart_product_delete'),
    path('cart-decoation-delete/<int:pk>/',CartDecorationDelete.as_view(),name='cart_decortion_delete'),
    path('clear-cart/<uuid:pk>/',DeleteFullCart.as_view(),name='clear_cart')
]
