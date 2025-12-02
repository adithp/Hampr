from django.contrib import admin

from .models import BoxType,BoxCategory,BoxCategoryImage,HamperBox



admin.site.register(BoxType)

admin.site.register(BoxCategory)

admin.site.register(BoxCategoryImage)


admin.site.register(HamperBox)