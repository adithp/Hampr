from django.urls import path


from .views import CommonLogoutView,LandingPageRenderView

app_name = 'core'


urlpatterns = [
    path('all/logout/',CommonLogoutView.as_view(),name='logout'),
    path('',LandingPageRenderView.as_view(),name='landing_page')
]
