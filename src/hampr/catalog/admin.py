from django.contrib import admin

from .models import BoxType,BoxCategory,BoxCategoryImage,HamperBox,BoxSize,BoxImage,ProductCategory



admin.site.register(BoxType)

admin.site.register(BoxCategory)

admin.site.register(BoxCategoryImage)


admin.site.register(HamperBox)
admin.site.register(BoxSize)

admin.site.register(BoxImage)

admin.site.register(ProductCategory)