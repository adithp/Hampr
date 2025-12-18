from django.urls import path
from .views import AdminLoginView,AdminDashboardView,AdminUserManagement,AdminBlockUser,AdminProductsMainPage,AdminBoxProductsMainPage,AdminBoxProductsAddItem,AdminBoxTypeItemAdd,AdminBoxCategoryItemAdd,AdminBoxTypeManage,AdminBoxCategoryManage,AdminBoxProductsAddItemSecond,AdminBoxProductsAddItemThird,redirect_to_image_upload_box,productBox_adding_cancel,AdminProductAddCategory,AdminProductCategoryManage,AdminProductAdd,AdminProductSimpleVarientAdd,varient_or_not,AdminProductVarientAdd,varients_finshed,AdminProductManage,cancel_add_product,AdminDecorationAdd,AdminDecortionManage,AdminBoxTypeDelete,AdminBoxCategoryDelete,AdminProductCategoryDelete,AdminProductVarientDelete,AdminDecorationDelete,AdminBoxDelete,AdminBoxCategoryItemEdit,AdminBoxTypeItemEdit,AdminBoxProductsEditItem,AdminMainProductDelete,AdminBoxProductsEditItemSecond,AdminBoxProductsEditItemThird,AdminProductDelete,AdminProductEditCategory,AdminProductEdit,AdminProductSimpleVarientEdit,AdminProductVarientEdit,redirect_to_add_varient,AdminDecorationEdit



app_name = 'cadmin'


urlpatterns = [
    path('login/',AdminLoginView.as_view(),name='admin_login'),
    
    path('dashboard/',AdminDashboardView.as_view(),name='admin_dashboard'),
    
    path('user_management/',AdminUserManagement.as_view(),name='user_management'),
    path('user_block/<int:id>/',AdminBlockUser.as_view(),name='user_block'),
    
    
    path('products_manage/',AdminProductsMainPage.as_view(),name='products_manage'),
    
    
    path('box_manage/',AdminBoxProductsMainPage.as_view(),name='box_manage'),
    path('box_full_delete/<pk>/',AdminMainProductDelete.as_view(),name='box_full_delete'),
    path('box_delete/<pk>/',AdminBoxDelete.as_view(),name='box_delete'),
    
    
    path('box_type_manage/',AdminBoxTypeManage.as_view(),name='box_type_manage'),
    path('box_type_add/',AdminBoxTypeItemAdd.as_view(),name='box_type_add'),
    path('box_type_delete/<pk>/',AdminBoxTypeDelete.as_view(),name='box_type_delete'),
    path('box_type_edit/<uuid:id>/',AdminBoxTypeItemEdit.as_view(),name='box_type_edit'),
    
    
    path('box_category_manage/',AdminBoxCategoryManage.as_view(),name='box_category_manage'),
    path('box_category_edit/<uuid:id>/',AdminBoxCategoryItemEdit.as_view(),name='box_category_edit'),
    path('box_category_add/',AdminBoxCategoryItemAdd.as_view(),name='box_category_add'),
    path('box_category_delete/<pk>/',AdminBoxCategoryDelete.as_view(),name='box_category_delete'),
    
    
    path('add_box_first/',AdminBoxProductsAddItem.as_view(),name='add_box_first_phase'),
    path('edit_box_first/<uuid:id>/',AdminBoxProductsEditItem.as_view(),name='edit_box_first'),
    
    path('add_box_second/',AdminBoxProductsAddItemSecond.as_view(),name='add_box_second'),
    path('edit_box_second/<uuid:id>/',AdminBoxProductsEditItemSecond.as_view(),name='edit_box_second'),

    path('add_box_third/',AdminBoxProductsAddItemThird.as_view(),name='add_box_third'),
    path('edit_box_third/<uuid:id>/',AdminBoxProductsEditItemThird.as_view(),name='edit_box_third'),
    
    path('second_to_third_redirect/',redirect_to_image_upload_box,name='second_third_redirect'),
    path('box_product_adding_cancel/',productBox_adding_cancel,name='box_product_adding_cancel'),
    
    path('add_product_category/',AdminProductAddCategory.as_view(),name='add_product_category'),
    path('edit_product_category/<slug:slug>/',AdminProductEditCategory.as_view(),name='edit_product_category'),
    path('products_category_list/',AdminProductCategoryManage.as_view(),name='products_category_list'),
    path('product_category_delete/<pk>/',AdminProductCategoryDelete.as_view(),name='product_category_delete'),
    
    path('product_add/',AdminProductAdd.as_view(),name='product_add'),
    path('product_edit/<int:id>/',AdminProductEdit.as_view(),name='product_edit'),
    path('varient_or_not/',varient_or_not,name='varient_or_not'),
    path('product_varients_add/',AdminProductSimpleVarientAdd.as_view(),name='product_varients_add'),
    
    path('product_varient_edit/<int:id>/',AdminProductSimpleVarientEdit.as_view(),name='product_varient_edit'),
    path('products_varients_edit_extra/<int:id>/',AdminProductVarientEdit.as_view(),name='products_varients_edit_extra'),
    path('products_varients_add_extra/',AdminProductVarientAdd.as_view(),name='products_varients_add_extra'),
    path('varients_finshed/',varients_finshed,name='varients_finshed'),
    path('interior_product_manage/',AdminProductManage.as_view(),name='interior_product_manage'),
    path('cancel_add_product/',cancel_add_product,name='cancel_add_product'),
    path('product_varient_delete/<pk>/',AdminProductVarientDelete.as_view(),name='product_varient_delete'),
    path('product_new_varient/<int:id>/',redirect_to_add_varient,name='product_new_varient'),
    path('product_delete/<pk>/',AdminProductDelete.as_view(),name='product_delete'),
    
    path('decoration_add/',AdminDecorationAdd.as_view(),name='decoration_add'),
    path('decoration_manage/',AdminDecortionManage.as_view(),name='decoration_manage'),
    path('decoration_delete/<pk>/',AdminDecorationDelete.as_view(),name='decoration_delete'),
    path('decoration_edit/<int:id>/',AdminDecorationEdit.as_view(),name='decoration_edit'),
    
    
    
    
    
]
