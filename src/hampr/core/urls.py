from django.urls import path


from .views import CommonLogoutView,LandingPageRenderView,after_logout

app_name = 'core'


urlpatterns = [
    path('all/logout/',CommonLogoutView.as_view(),name='logout'),
    path('',LandingPageRenderView.as_view(),name='landing_page'),
    path('after-logout/<int:user_id>/',after_logout,name='landing_page_redirect')
]
