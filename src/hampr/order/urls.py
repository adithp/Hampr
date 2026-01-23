from django.urls import path

from .views import CreateOrderView,OrderSuccsessView,razorpay_verify,OrderDetail,OrderTracking

app_name = 'order'

urlpatterns = [
    path('order/',CreateOrderView.as_view(),name='order'),
    path('order_placed/<str:order_id>/',OrderSuccsessView.as_view(),name='order_succsess'),
    path("razorpay/verify/", razorpay_verify, name="razorpay_verify"),
    path('order-detail/<str:order_id>/',OrderDetail.as_view(),name='order_detail'),
    path('order-tracking/<int:pk>/',OrderTracking.as_view(),name='order_tracking')
   
]
