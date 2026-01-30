from django.urls import path



from .views import not_active_error,UserSignupView,Otp_Verify_View,Otp_Resend,CustomLoginView,ResetPasswordLinkSend,ResetPassword,ProfilePageView,ProfilePictureUpdate,AddAddressView,EditAddressView,DeleteAddressView,EditProfileDetails,OrderCancel

app_name = 'accounts'

urlpatterns = [
    path('register/',UserSignupView.as_view(),name='signup'),
    path('otp_verify/',Otp_Verify_View.as_view(),name='otp_verify'),
    path('otp_resend/',Otp_Resend.as_view(),name='otp_resend'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('reset_link/',ResetPasswordLinkSend.as_view(),name='reset_link'),
    path('reset_password/<uuid:id>/',ResetPassword.as_view(),name='reset_password'),
    path('not_active_error/',not_active_error,name='not_active_error'),
    path('user-profile/',ProfilePageView.as_view(),name='user_profile'),
    path('user_profile_picture_update/',ProfilePictureUpdate.as_view(),name='profile_picture_update'),
    path('user-add-address/',AddAddressView.as_view(),name='add_address'),
    path('user-edit-address/<uuid:id>',EditAddressView.as_view(),name='address_edit'),
    path('delete-address/<uuid:pk>/',DeleteAddressView.as_view(),name='address_delete'),
    path('profile-edit/',EditProfileDetails.as_view(),name='profile_edit'),
    path('order_cancel/<int:order_id>/',OrderCancel.as_view(),name='order_cancel')
]
