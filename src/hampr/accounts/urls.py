from django.urls import path



from .views import succses,UserSignupView,Otp_Verify_View,Otp_Resend,CustomLoginView,ResetPasswordLinkSend,ResetPassword

app_name = 'accounts'

urlpatterns = [
    path('register/',UserSignupView.as_view(),name='signup'),
    path('suc',succses,name='suc'),
    path('otp_verify/',Otp_Verify_View.as_view(),name='otp_verify'),
    path('otp_resend/',Otp_Resend.as_view(),name='otp_resend'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('reset_link/',ResetPasswordLinkSend.as_view(),name='reset_link'),
    path('reset_password/<uuid:id>/',ResetPassword.as_view(),name='reset_password'),
]
