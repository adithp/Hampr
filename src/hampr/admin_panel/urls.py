from django.urls import path
from .views import AdminLoginView,AdminDashboardView,AdminUserManagement,AdminBlockUser,AdminProductsMainPage,AdminBoxProductsMainPage,AdminBoxProductsAddItem,AdminBoxTypeItemAdd,AdminBoxCategoryItemAdd,AdminBoxTypeManage,AdminBoxCategoryManage,AdminBoxProductsAddItemSecond



app_name = 'cadmin'


urlpatterns = [
    path('login/',AdminLoginView.as_view(),name='admin_login'),
    path('dashboard/',AdminDashboardView.as_view(),name='admin_dashboard'),
    path('user_management/',AdminUserManagement.as_view(),name='user_management'),
    path('user_block/<int:id>/',AdminBlockUser.as_view(),name='user_block'),
    path('products_manage/',AdminProductsMainPage.as_view(),name='products_manage'),
    path('box_manage/',AdminBoxProductsMainPage.as_view(),name='box_manage'),
    
    path('box_type_manage/',AdminBoxTypeManage.as_view(),name='box_type_manage'),
    path('box_type_add/',AdminBoxTypeItemAdd.as_view(),name='box_type_add'),
    
    path('box_category_manage/',AdminBoxCategoryManage.as_view(),name='box_category_manage'),
    path('box_category_add/',AdminBoxCategoryItemAdd.as_view(),name='box_category_add'),
    
    path('add_box_first/',AdminBoxProductsAddItem.as_view(),name='add_box_first_phase'),
    path('add_box_second/',AdminBoxProductsAddItemSecond.as_view(),name='add_box_second'),
    
]
