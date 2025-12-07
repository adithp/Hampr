from django.urls import path
from .views import AdminLoginView,AdminDashboardView,AdminUserManagement,AdminBlockUser,AdminProductsMainPage,AdminBoxProductsMainPage,AdminBoxProductsAddItem,AdminBoxTypeItemAdd,AdminBoxCategoryItemAdd,AdminBoxTypeManage,AdminBoxCategoryManage,AdminBoxProductsAddItemSecond,AdminBoxProductsAddItemThird,redirect_to_image_upload_box,productBox_adding_cancel,AdminProductAddCategory,AdminProductCategoryManage,AdminProductAdd,AdminProductSimpleVarientAdd,varient_or_not,AdminProductVarientAdd,varients_finshed,AdminProductManage,cancel_add_product



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
    path('add_box_third/',AdminBoxProductsAddItemThird.as_view(),name='add_box_third'),
    
    path('second_to_third_redirect/',redirect_to_image_upload_box,name='second_third_redirect'),
    path('box_product_adding_cancel/',productBox_adding_cancel,name='box_product_adding_cancel'),
    
    path('add_product_category/',AdminProductAddCategory.as_view(),name='add_product_category'),
    path('products_category_list/',AdminProductCategoryManage.as_view(),name='products_category_list'),
    
    path('product_add/',AdminProductAdd.as_view(),name='product_add'),
    path('varient_or_not/',varient_or_not,name='varient_or_not'),
    path('product_varients_add/',AdminProductSimpleVarientAdd.as_view(),name='product_varients_add'),
    path('products_varients_add_extra/',AdminProductVarientAdd.as_view(),name='products_varients_add_extra'),
    path('varients_finshed/',varients_finshed,name='varients_finshed'),
    path('interior_product_manage/',AdminProductManage.as_view(),name='interior_product_manage'),
    path('cancel_add_product/',cancel_add_product,name='cancel_add_product')
    
    
    
    
    
]
